
from project.data import get_data, clean_df
from project.pipeline import ProjectPipeline
from project.utils import compute_rmse

from sklearn.model_selection import train_test_split

import joblib


class Trainer():

    def train(self):

        # get data
        df = get_data()
        df = clean_df(df)

        # get X and y
        # TODO: not generic
        cols = ["pickup_latitude",
                "pickup_longitude",
                "dropoff_latitude",
                "dropoff_longitude"]

        y = df["fare_amount"]
        X = df[cols]

        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=0.1,
                                                            random_state=42)

        # create pipeline
        self.model = ProjectPipeline().create_pipeline()

        # train
        self.model.fit(X_train, y_train)

        # predict
        y_pred = self.model.predict(X_test)

        # perf
        rmse = compute_rmse(y_pred, y_test)

        # save model
        joblib.dump(self.model, 'model.joblib')

        return rmse
