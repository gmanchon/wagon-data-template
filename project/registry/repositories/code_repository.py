
import os


class CodeRepository():

    def __init__(self, conf):

        # get conf
        self.label_prefix = conf.label_prefix

    def get_commit_hash(self):

        return self.__get_latest_commit_hash()

    def list_commit_hashes(self):

        pass

    def get_code(self, commit_hash):

        pass

    def is_git_status_clean(self):
        """
        checks whether git status is clean
        """

        # retrieve git status
        git_status_cmd = "git status"

        git_status = os.popen(git_status_cmd).read()

        return "nothing to commit, working tree clean" in git_status

    def __get_latest_commit_hash(self):

        # retrieve latest commit hash
        git_latest_commit_hash_cmd = "git rev-parse master"

        commit_hash = os.popen(git_latest_commit_hash_cmd).read()

        return commit_hash
