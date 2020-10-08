
from project.data import get_data, clean_df
from project.pipeline import ProjectPipeline
from project.metrics import compute_rmse

from sklearn.model_selection import train_test_split

import joblib

from colorama import Fore, Style


class Trainer():

    def __init__(self):
        # self.X_train, self.X_test, self.y_train, self.y_test
        pass

    def __get_training_data(self, nrows):

        # get data
        df = get_data(nrows)
        df = clean_df(df)

        # get X and y
        # TODO: not generic
        cols = ["pickup_latitude",
                "pickup_longitude",
                "dropoff_latitude",
                "dropoff_longitude"]

        y = df["fare_amount"]
        X = df[cols]

        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(X, y,
                             test_size=0.1,
                             random_state=42)

    def preprocess(self, nrows):
        """
        shows input and output of each steps of the pipeline
        runs all the steps of the pipeline except for the estimator
        """

        # retrieve training data
        self.__get_training_data(nrows)

        # create pipeline
        self.pipeline = ProjectPipeline().create_pipeline()

        X_tmp = self.X_train

        print(Fore.GREEN + "\nPipeline input:\n"
              + Style.RESET_ALL
              + "%s" % X_tmp)

        # executing all steps except estimator
        for name, transformer in self.pipeline.steps[:-1]:

            # executing step
            X_tmp = transformer.fit_transform(X_tmp)

            print(Fore.GREEN + "\nPipeline step \"%s\", output:\n" % name
                  + Style.RESET_ALL
                  + "%s" % X_tmp)

    def train(self, nrows):
        """
        trains the model
        runs all the steps of the pipeline
        """

        # retrieve training data
        self.__get_training_data(nrows)

        # create pipeline
        self.pipeline = ProjectPipeline().create_pipeline()

        # train
        self.pipeline.fit(self.X_train, self.y_train)

        # predict
        y_pred = self.pipeline.predict(self.X_test)

        # perf
        rmse = compute_rmse(y_pred, self.y_test)

        # save model
        joblib.dump(self.pipeline, 'model.joblib')

        return rmse
