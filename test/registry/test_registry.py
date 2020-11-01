
from project.conf import ConfLoader
from project.registry.registry import Registry

from os.path import join, dirname

import unittest


class TestRegistry(unittest.TestCase):

    def __init__(self, *args, **kwargs):

        # call base class init
        super().__init__(*args, **kwargs)

        # generate stubs
        self.__gen_stubs()

    def __gen_stubs(self):

        # load conf from test folder defaults and project file
        project_path = dirname(dirname(__file__))
        project_conf_path = join(project_path, "conf", "config.yaml")
        defaults_conf_path = join(project_path, "conf", "config.defaults.yaml")
        self.conf = ConfLoader(project_conf_path, defaults_conf_path).conf

        # create registry
        self.reg = Registry(self.conf.registry)

    def test_disable_registry(self):
        pass
