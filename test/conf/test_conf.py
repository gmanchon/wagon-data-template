
from project.conf import ConfLoader, ConfStruct

from os.path import join, dirname

from colorama import Fore, Style

import unittest


class TestConf(unittest.TestCase):

    def __init__(self, *args, **kwargs):

        # call base class init
        super().__init__(*args, **kwargs)

        # generate stubs
        self.__gen_stubs()

    def __gen_stubs(self):

        # load conf from test folder defaults and project file
        project_path = dirname(__file__)
        project_conf_path = join(project_path, "config.yaml")
        defaults_conf_path = join(project_path, "config.defaults.yaml")
        self.conf_loader = ConfLoader(project_conf_path, defaults_conf_path)
        self.conf = self.conf_loader.conf

    def test_conf_structure(self):

        self.assertIsInstance(self.conf_loader, ConfLoader)

        self.assertIsInstance(self.conf, ConfStruct)

    def test_conf_content(self):

        print(self.conf)

        self.assertEqual(self.conf.registry.experiment_name, "[FR] [Paris] [username] my project name")
        self.assertEqual(self.conf.registry.model.type, "gcp")
        self.assertEqual(self.conf.registry.model.bucket_name, "my-bucket-name")
        self.assertEqual(self.conf.registry.code.type, "git")
        self.assertEqual(self.conf.registry.code.label_prefix, "kmp")
        self.assertEqual(self.conf.registry.code.foo.bar.toto, True)
        self.assertEqual(self.conf.registry.tracking.type, "mlflow")
        self.assertEqual(self.conf.registry.tracking.server, "https://my.mlflow.server.url/")

    def test_conf_diff(self):

        print(self.conf_loader)

        # checking line in defaults conf only gets flagged as magenta
        conf_repr = repr(self.conf_loader).split("\n")

        defaults_line = Fore.MAGENTA \
            + "registry.model.type = 'gcp'" \
            + Style.RESET_ALL

        # checking line in project conf only gets flagged as cyan
        project_line = Fore.CYAN \
            + "registry.model.bucket_name = 'my-bucket-name'" \
            + Style.RESET_ALL

        # checking line identical in defaults and conf does not get flagged
        common_line = "registry.code.type = 'git'"

        self.assertTrue(defaults_line in conf_repr)
        self.assertTrue(project_line in conf_repr)
        self.assertTrue(common_line in conf_repr)
