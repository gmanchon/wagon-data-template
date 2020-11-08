
from project.conf.conf import ConfLoader
from project.registry.registry import Registry
from project.trainer.trainer import Trainer

from os.path import join, dirname

import pandas as pd

from colorama import Fore, Style

import os


REGISTRY_ENABLED = os.environ.get("reg")

if REGISTRY_ENABLED:

    print(Fore.GREEN + "\n✅ Registry enabled"
          + Style.RESET_ALL)

else:
    print(Fore.GREEN + "\n❌ Registry disabled"
          + Style.RESET_ALL)


class App:

    def __init__(self, params):

        # getting params
        self.params = params

        # load conf
        print(Fore.GREEN + "\nLoading configuration..."
              + Style.RESET_ALL)

        conf_path = join(dirname(__file__), "conf")
        project_conf_path = join(conf_path, "app.yaml")
        defaults_conf_path = join(conf_path, "app.defaults.yaml")
        self.conf_loader = ConfLoader(project_conf_path, defaults_conf_path)
        self.conf = self.conf_loader.conf

        print(Fore.GREEN + "\nLoaded configuration:"
              + Style.RESET_ALL
              + str(self.conf_loader))

        # load registry
        print(Fore.GREEN + "\nLoading registry..."
              + Style.RESET_ALL)

        self.registry = Registry(self.conf.registry, REGISTRY_ENABLED)

        # getting data params
        data_params = self.params.get('data', dict())
        self.nrows = data_params.get('nrows', 1_000)

        # data source
        self.data = "s3://wagon-public-datasets/taxi-fare-train.csv"

        # data storage
        project_path = os.path.dirname(os.path.dirname(__file__))
        self.data_path = os.path.join(project_path, "data", "data.csv")

        print(Fore.GREEN + "\nLoading trainer..."
              + Style.RESET_ALL)

        # instanciating trainer
        self.trainer = Trainer(params, self.registry)

    def check_registry(self, registry_enabled):

        # check if registry is enabled
        if not registry_enabled:
            return True

        print(Fore.GREEN + "\nValidating git status..."
              + Style.RESET_ALL)

        # get git status
        is_clean = self.registry.is_git_status_clean()

        if not is_clean:
            print(Fore.RED
                  + "⚠️  Cannot train the model and register the performance"
                  + " unless the git status is clean. "
                  + "The code needs to be committed in order to be deployable "
                  + " in the future. "
                  + "Please clean the git status of the repository"
                  + " (commit or stash the code)"
                  + Style.RESET_ALL)

        return is_clean

    def fetch(self):

        # fetching data
        print(Fore.GREEN + "\nFetching %s lines from %s data 🚀"
              % (self.nrows, self.data)
              + Style.RESET_ALL)

        df = pd.read_csv(self.data, nrows=self.nrows)

        # saving data locally
        df.to_csv(self.data_path)

        print(Fore.GREEN + "Data saved to %s 👍"
              % self.data_path
              + Style.RESET_ALL)

        return self

    def head(self):

        # reading local data
        df = pd.read_csv(self.data_path, nrows=self.nrows)

        print(Fore.GREEN + "\nDataset:\n"
              + Style.RESET_ALL
              + "%s" % df.head(self.nrows))

        return self

    def preprocess(self):

        print(Fore.GREEN + "\nPreprocessing model..."
              + Style.RESET_ALL)

        # running trainer
        self.trainer.preprocess()

        return self

    def train(self):

        print(Fore.GREEN + "\nTraining model..."
              + Style.RESET_ALL)

        # running trainer
        rmse = self.trainer.train()

        print(Fore.GREEN + "\nModel trained, rmse: %s 👍"
              % rmse
              + Style.RESET_ALL)

        return self


def main():

    params = dict(
        data=dict(
            nrows=10),
        trainer=dict(
            estimator='linear',
            hyperparams=dict(
                n_estimators=100,
                max_depth=10,
                n_jobs=-1),
            pipeline=dict(
                distance=dict(
                    type="haversine"),
                time=dict(
                    zone="America/New_York"))))

    app = App(params)

    if app.check_registry(REGISTRY_ENABLED):

        # app.fetch()
        app.head()
        app.preprocess()
        app.train()


if __name__ == '__main__':
    main()
