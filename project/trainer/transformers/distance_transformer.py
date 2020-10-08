
from project.trainer.transformers.distance \
    import haversine_vectorized, minkowski_distance

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


class DistanceTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, distance_type="euclidian", **kwargs):
        self.distance_type = distance_type

    def transform(self, X, y=None):

        distance_arguments = dict(start_lat="pickup_latitude",
                                  start_lon="pickup_longitude",
                                  end_lat="dropoff_latitude",
                                  end_lon="dropoff_longitude")

        assert isinstance(X, pd.DataFrame)
        if self.distance_type == "haversine":
            X["distance"] = haversine_vectorized(X, **distance_arguments)
        if self.distance_type == "euclidian":
            X["distance"] = minkowski_distance(X, p=2, **distance_arguments)
        if self.distance_type == "manhattan":
            X["distance"] = minkowski_distance(X, p=1, **distance_arguments)
        return X[["distance"]]

    def fit(self, X, y=None):
        return self
