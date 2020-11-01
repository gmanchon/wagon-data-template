
from test.conf.test_conf import TestConf

from project.registry.registry import Registry

import unittest


class TestRegistry(unittest.TestCase):

    def __init__(self, *args, **kwargs):

        # call base class init
        super().__init__(*args, **kwargs)

        # get stubs
        self.conf_loader = TestConf()._TestConf__gen_stubs()
        self.conf = self.conf_loader.conf

        # generate stubs
        self.reg = self.__gen_stubs()

    def __gen_stubs(self):

        # create registry
        print(self.conf.registry)
        registry = Registry(self.conf.registry)

        return registry

    # def test_disable_registry(self):
    #     pass

    def test_get_current_experiment(self):

        experiment = self.reg.get_experiment()

        self.assertEqual(experiment, "[FR] [Paris] [username] my project name")

    def test_get_current_run(self):

        run = self.reg.get_current_run()

        self.assertIsInstance(run, str)

    def test_new_run(self):

        run = self.reg.get_current_run()

        self.reg.new_run()

        new_run = self.reg.get_current_run()

        self.assertNotEqual(run, new_run)

    # def test_log_params(self):

    #     self.reg.log_param("rows", 10)
    #     self.reg.log_param("model", "randomforest")

    # def test_log_dict_params(self):

    #     hyperparams = dict(
    #                 n_estimators=100,
    #                 max_depth=10,
    #                 n_jobs=-1)
    #     pipe_params = dict(
    #                 distance=dict(
    #                     type="haversine"),
    #                 time=dict(
    #                     zone="America/New_York"))

    #     self.reg.log_dict_param(hyperparams, "hyper")
    #     self.reg.log_dict_param(pipe_params, "pipe")

    # def test_log_metrics(self):

    #     self.reg.log_metric("rmse", 1.234)

    def test_log_model(self):

        self.reg.log_model()

        # run = self.reg.get_current_run()

        # self.reg.get_model(run)

        # TODO

    def test_list_models(self):

        models = self.reg.list_models()

        print(models)

        # TODO

    def test_get_model(self):

        run = "150e640602b74d81b2fab91d59187a26"

        self.reg.get_model(run)

        # TODO

    # def test_log_code(self):

    #     pass
