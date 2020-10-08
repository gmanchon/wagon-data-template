
from project.trainer.transformers.distance import haversine_vectorized

from sklearn.base import BaseEstimator, TransformerMixin


class DistanceToCenterTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def transform(self, X, y=None):
        nyc_center = (40.7141667, -74.0063889)
        X["nyc_lat"], X["nyc_lng"] = nyc_center[0], nyc_center[1]
        args_pickup = dict(start_lat="nyc_lat",
                           start_lon="nyc_lng",
                           end_lat="pickup_latitude",
                           end_lon="pickup_longitude")
        args_dropoff = dict(start_lat="nyc_lat",
                            start_lon="nyc_lng",
                            end_lat="dropoff_latitude",
                            end_lon="dropoff_longitude")
        X['pickup_distance_to_center'] = haversine_vectorized(X, **args_pickup)
        X['dropoff_distance_to_center'] = \
            haversine_vectorized(X, **args_dropoff)
        return X[["pickup_distance_to_center", "dropoff_distance_to_center"]]

    def fit(self, X, y=None):
        return self
