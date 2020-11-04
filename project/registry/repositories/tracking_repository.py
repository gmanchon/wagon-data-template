
import mlflow
from mlflow.tracking import MlflowClient

from memoized_property import memoized_property

from collections.abc import Mapping

from colorama import Fore, Style


class TrackingRepository():

    def __init__(self, conf, experiment_name, code_commit_hash,
                 code_storage_location, model_storage_location):

        self.code_commit_hash = code_commit_hash
        self.experiment_name = experiment_name
        self.code_storage_location = code_storage_location
        self.model_storage_location = model_storage_location

        # get conf
        self.mlflow_uri = conf.server

        # create client
        mlflow.set_tracking_uri(self.mlflow_uri)
        self.mlflow_client = MlflowClient()

    @memoized_property
    def mlflow_experiment_id(self):
        try:
            # create experiment
            return self.mlflow_client.create_experiment(self.experiment_name)
        except BaseException:
            # retrieve existing experiment
            return self.mlflow_client.get_experiment_by_name(
                self.experiment_name).experiment_id

    def mlflow_create_run(self):

        # run only once (TODO: use memoized property ?)
        if hasattr(self, 'mlflow_run'):
            return

        print(Fore.GREEN + "\nCreating tracking run..."
              + Style.RESET_ALL)

        self.mlflow_run = self.mlflow_client.create_run(
            self.mlflow_experiment_id)

        print(Fore.GREEN + "\nTracking created at:\n"
              + Style.RESET_ALL
              + f"{self.mlflow_uri}/#"
              + f"/experiments/{self.mlflow_experiment_id}"
              + f"/runs/{self.mlflow_run.info.run_id}")

        # set run tags
        self.mlflow_set_tag("code storage", self.code_storage_location)
        self.mlflow_set_tag("code commit hash", self.code_commit_hash)
        self.mlflow_set_tag("model storage", self.model_storage_location)

    def mlflow_set_tag(self, key, value):

        # set tag
        self.mlflow_client.set_tag(
            self.mlflow_run.info.run_id, key, value)

    def mlflow_log_param(self, key, value):

        # create run
        self.mlflow_create_run()

        # log param
        self.mlflow_client.log_param(
            self.mlflow_run.info.run_id,
            key, value)

    def mlflow_log_metric(self, key, value):

        # create run
        self.mlflow_create_run()

        # log metric
        self.mlflow_client.log_metric(
            self.mlflow_run.info.run_id,
            key, value)

    def mlflow_log_dict_param(self, dict, radix):

        # create run
        self.mlflow_create_run()

        # iterate through dictionary
        key_radix = "%s__" % radix
        for key, value in dict.items():
            if isinstance(value, Mapping):
                # iterate recursively through sub dictionary
                self.mlflow_log_dict_param(value, key_radix + key)
            else:
                # other datatypes are convertd to their string representation
                self.mlflow_log_param(key_radix + key, value)
