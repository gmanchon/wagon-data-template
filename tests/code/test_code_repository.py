
from tests.conf.test_conf import TestConf

from project.registry.repositories.code_repository import CodeRepository

import unittest


class TestCodeRepository(unittest.TestCase):

    def __init__(self, *args, **kwargs):

        # call base class init
        super().__init__(*args, **kwargs)

        # get stubs
        self.conf_loader = TestConf()._TestConf__gen_stubs()
        self.conf = self.conf_loader.conf

        # generate stubs
        self.code_repo = self.__gen_stubs()

    def __gen_stubs(self):

        # create code repo
        code_repo = CodeRepository(self.conf.registry.code)

        return code_repo
