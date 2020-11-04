
from project.registry.repositories.code_repository import CodeRepository
from project.registry.repositories.model_repository import ModelRepository
from project.registry.repositories.tracking_repository import TrackingRepository


class Registry():

    def __init__(self, conf, enabled):

        self.enabled = enabled

        # check whether registry is enabled
        if not self.enabled:
            return

        # get conf
        self.conf = conf
        self.experiment = self.conf.experiment_name

        # create code repository
        self.code_repository = CodeRepository(conf.code)

        # get code storage location
        code_storage_location = self.code_repository.get_storage_location()

        # get current run (current code commit hash)
        self.run = self.code_repository.get_commit_hash()

        # create model repository
        self.model_repository = ModelRepository(
            conf.model, self.experiment, self.run)

        # get model storage location
        model_storage_location = self.model_repository.get_storage_location()

        # create tracking repository
        self.tracking_repository = TrackingRepository(
            conf.tracking, self.experiment,
            code_storage_location, model_storage_location)

    # def experiments(self):
    # def experiment(self, experiment_name):

    def get_experiment(self):

        # return experiment
        return self.experiment

    # def runs(self, experiment_name):
    # def run(self, experiment_name, id):
    # def get_current_run(self):
    # def new_run(self):
    # def log_dataset(self, key, value):
    # def log_preprocessing(self, items, name):
    # def log_estimator(self, key, value):
    # def log_hyperparam(self, key, value):
    # def log_dict_hyperparam(self, items, name):

    def log_param(self, key, value):

        # check whether registry is enabled
        if not self.enabled:
            return

        # log param
        self.tracking_repository.mlflow_log_param(key, value)

    def log_dict_param(self, items, name):

        # check whether registry is enabled
        if not self.enabled:
            return

        # log dict param
        self.tracking_repository.mlflow_log_dict_param(items, name)

    def log_metric(self, key, value):

        # check whether registry is enabled
        if not self.enabled:
            return

        # log dict param
        self.tracking_repository.mlflow_log_metric(key, value)

    def log_model(self):

        # check whether registry is enabled
        if not self.enabled:
            return

        # store model
        self.model_repository.store_model()

    def list_models(self):

        # list model
        return self.model_repository.list_models()

    def get_model(self, run):

        # store model
        self.model_repository.get_model(run)

    def is_git_status_clean(self):

        # return git status
        return self.code_repository.is_git_status_clean()

    def get_commit_hash(self):

        # return git status
        return self.code_repository.get_commit_hash()
