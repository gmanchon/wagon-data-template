
from google.cloud import storage

from os.path import join

from colorama import Fore, Style

import re


class ModelRepository():

    def __init__(self, conf, experiment_name, run):

        self.experiment_name = experiment_name
        self.run = run

        # get conf
        self.bucket_name = conf.bucket_name
        self.storage_path = conf.storage_path
        self.local_path = conf.local_path
        self.model_filename = conf.model_filename

        # client
        self.storage_client = storage.Client()

    def get_storage_location(self):
        """
        returns gcp model storage location
        """

        storage_location = "https://console.cloud.google.com/storage" \
            + f"/browser/{self.bucket_name}" \
            + "/registry" \
            + f"/experiments/{self.experiment_name}" \
            + f"/runs/{self.run}"

        return storage_location

    def store_model(self):
        """
        uploads model to gcp storage location
        """

        # get storage path
        storage_path = self.__get_model_storage_path()

        # build local model file path
        local_model_path = join(self.local_path, self.model_filename)

        # build storage model file path
        storage_model_path = join(storage_path, self.model_filename)

        # store model on bucket
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(storage_model_path)
        blob.upload_from_filename(local_model_path)

        # show storage location
        store_location = self.get_storage_location()

        print(Fore.GREEN + "\nModel stored at:\n"
              + Style.RESET_ALL
              + store_location)

    def list_models(self):
        """
        returns a lists of gcp uploaded model runs (code commit hashes)
        """

        # list blobs from bucket
        blobs = self.storage_client.list_blobs(self.bucket_name)

        paths = "".join([blob.name for blob in blobs])

        # extract runs from blob paths
        runs = re.findall(r"/([a-z0-9]{32})/", paths)

        return runs

    def get_model(self, run):
        """
        downloads from gcp a model defined by its run (code commit hash)
        """

        # get storage path
        storage_path = self.__get_model_storage_path(run)

        # build local model file path
        local_model_path = join(self.local_path, self.model_filename)

        # build storage model file path
        storage_model_path = join(storage_path, self.model_filename)

        # get model from bucket
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(storage_model_path)
        blob.download_to_filename(local_model_path)

    def __get_model_storage_path(self, run=None):
        """
        returns model storage path on gcp depending on its run
        (code commit hash)
        """

        # default to current run
        if run is None:
            run = self.run

        # build storage path from expirement and current run
        storage_path = self.storage_path \
            .replace(":experiment", self.experiment_name) \
            .replace(":run", self.run)

        return storage_path
