
from project.trainer.transformers.distance \
    import haversine_vectorized, minkowski_distance

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin

from colorama import Fore, Style


class DistanceTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, type="euclidian", **kwargs):
        self.type = type

    def transform(self, X, y=None):

        distance_arguments = dict(start_lat="pickup_latitude",
                                  start_lon="pickup_longitude",
                                  end_lat="dropoff_latitude",
                                  end_lon="dropoff_longitude")

        print(Fore.GREEN + "\nDistance type: %s" % self.type
              + Style.RESET_ALL)

        assert isinstance(X, pd.DataFrame)
        if self.type == "haversine":
            X["distance"] = haversine_vectorized(X, **distance_arguments)
        if self.type == "euclidian":
            X["distance"] = minkowski_distance(X, p=2, **distance_arguments)
        if self.type == "manhattan":
            X["distance"] = minkowski_distance(X, p=1, **distance_arguments)
        return X[["distance"]]

    def fit(self, X, y=None):
        return self
