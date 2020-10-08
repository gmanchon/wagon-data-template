

from project.trainer.trainer import Trainer

import pandas as pd

from colorama import Fore, Style

import os


class App:

    def __init__(self):

        # data source
        self.data = "s3://wagon-public-datasets/taxi-fare-train.csv"

        # data storage
        project_path = os.path.dirname(os.path.dirname(__file__))
        self.data_path = os.path.join(project_path, "data", "data.csv")

        print(Fore.GREEN + "Loading trainer..."
              + Style.RESET_ALL)

        # instanciating trainer
        self.trainer = Trainer()

    def fetch(self, nrows):

        # fetching data
        print(Fore.GREEN + "\nFetching %s lines from %s data 🚀"
              % (nrows, self.data)
              + Style.RESET_ALL)

        df = pd.read_csv(self.data, nrows=nrows)

        # saving data locally
        df.to_csv(self.data_path)

        print(Fore.GREEN + "Data saved to %s 👍"
              % self.data_path
              + Style.RESET_ALL)

        return self

    def head(self, nrows):

        # reading local data
        df = pd.read_csv(self.data_path, nrows=nrows)

        print(Fore.GREEN + "\nDataset:\n"
              + Style.RESET_ALL
              + "%s" % df.head(nrows))

        return self

    def preprocess(self, nrows):

        print(Fore.GREEN + "\nPreprocessing model..."
              + Style.RESET_ALL)

        # running trainer
        self.trainer.preprocess(nrows)

        return self

    def train(self, nrows):

        print(Fore.GREEN + "\nTraining model..."
              + Style.RESET_ALL)

        # running trainer
        rmse = self.trainer.train(nrows)

        print(Fore.GREEN + "Model trained, rmse: %s 👍"
              % rmse
              + Style.RESET_ALL)

        return self


def main():

    n_rows = 1_000

    app = App()
    app.fetch(n_rows)
    app.head(n_rows)
    app.preprocess(n_rows)
    app.train(n_rows)


if __name__ == '__main__':
    main()
