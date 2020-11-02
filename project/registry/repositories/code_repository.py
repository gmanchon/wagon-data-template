
import os


class CodeRepository():

    def __init__(self, conf):

        # get conf
        self.label_prefix = conf.label_prefix

    def store_code(self):

        pass

    def list_codes(self):

        pass

    def get_code(self):

        pass

    def is_git_status_clean(self):
        """
        checks whether git status is clean
        """

        git_status_cmd = "git status"

        git_status = os.popen(git_status_cmd).read()

        return "nothing to commit, working tree clean" in git_status
