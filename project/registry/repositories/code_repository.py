
from colorama import Fore, Style

import re

import os


class CodeRepository():

    def __init__(self, conf):

        # get conf
        self.remote = conf.remote

    def get_storage_location(self):
        """
        retrieves the git url of the configured remote (origin by default)
        handles remote formats:
        - git@github.com:username/repo-name.git
        - git@github.com:username/repo-name
        - https://github.com/username/repo-name
        """

        # list remotes
        git_remotes_cmd = f"git config --get remote.{self.remote}.url"

        remote_url = os.popen(git_remotes_cmd).read().strip()

        # check if remote is configured
        if not remote_url:
            print(Fore.RED
                  + "⚠️  Could not determine git remote url."
                  + " Please make sure it is correctly configured in"
                  + " app.yaml under `registry.code.remote`. "
                  + "If the repository does not have a remote, make sure to"
                  + " add one (on GitHub or any other repository storage"
                  + " service). "
                  + "The code needs to be backed up in order to be reliably"
                  + " deployed on production"
                  + Style.RESET_ALL)

            return "⚠️ git remote not configured"

        # parse remote
        if remote_url[:4] == "git@":

            print(f"original remote url: {remote_url}")

            # remove trailing .git in order to handle the cases
            # where it may be missing
            if remote_url[-4:] == ".git":
                remote_url = remote_url[:-4]

            # retrieve user name and repo name
            groups = re.search(r"git@github\.com:(.*)\/(.*)", remote_url)

            user_name = groups[1]
            repo_name = groups[2]

            remote_url = f"https://github.com/{user_name}/{repo_name}"

        print(f"remote url: {remote_url}")

        return remote_url

    def get_commit_hash(self):

        run_hash = self.__get_latest_commit_hash()

        print(Fore.GREEN + "\nCode run (git commit hash): "
              + Style.RESET_ALL
              + run_hash)

        return run_hash

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
        """
        retrieves latest commit hash from git
        """

        # retrieve latest commit hash
        git_latest_commit_hash_cmd = "git rev-parse master"

        commit_hash = os.popen(git_latest_commit_hash_cmd).read()

        return commit_hash.strip()
