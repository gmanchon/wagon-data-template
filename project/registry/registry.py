
from project.registry.repositories.run_repository import RunRepository
from project.registry.repositories.model_repository import ModelRepository


class Registry():

    def __init__(self, conf):

        # get conf
        self.conf = conf
        self.experiment = self.conf.experiment_name

        # create repositories
        self.run_repository = RunRepository()
        self.model_repository = ModelRepository(conf.model)

    # def experiments(self):
    #     pass

    # def experiment(self, experiment_name):
    #     pass

    def get_experiment(self):

        # return experiment
        return self.experiment

    # def runs(self, experiment_name):
    #     pass

    # def run(self, experiment_name, id):
    #     pass

    def get_current_run(self):

        # get current run
        return self.run_repository.get_current_run()

    def new_run(self):

        # create new run
        self.run_repository.new_run()

    # def log_dataset(self, key, value):
    #     pass

    # def log_preprocessing(self, items, name):
    #     pass

    # def log_estimator(self, key, value):
    #     pass

    # def log_hyperparam(self, key, value):
    #     pass

    # def log_dict_hyperparam(self, items, name):
    #     pass

    def log_param(self, key, value):
        pass

    def log_dict_param(self, items, name):
        pass

    def log_metric(self, key, value):
        pass

    def log_model(self):

        # get current run
        run = self.run_repository.get_current_run()

        # store model
        self.model_repository.store_model(self.experiment, run)

    def list_models(self):

        # list model
        return self.model_repository.list_models()

    def get_model(self, run):

        # store model
        self.model_repository.get_model(self.experiment, run)

    def log_code(self, key, value):
        pass
