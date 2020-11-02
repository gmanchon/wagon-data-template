
from tests.conf.test_conf import TestConf

from project.registry.repositories.code_repository import CodeRepository

import os

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

    def test_git_status(self):

        # clean repo
        os.system("git stash")

        is_clean = self.code_repo.is_git_status_clean()

        self.assertTrue(is_clean)

        # modify repo
        os.system("touch delete_me.txt")

        is_clean = self.code_repo.is_git_status_clean()

        self.assertFalse(is_clean)

        # restore repo
        os.system("rm delete_me.txt")

        os.system("git stash pop")
