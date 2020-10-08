
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin


class DirectionTransformer(BaseEstimator, TransformerMixin):
    def __init__(self,
                 start_lat="pickup_latitude",
                 start_lon="pickup_longitude",
                 end_lat="dropoff_latitude",
                 end_lon="dropoff_longitude"):
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.end_lat = end_lat
        self.end_lon = end_lon

    def transform(self, X, y=None):

        def calculate_direction(d_lon, d_lat):
            result = np.zeros(len(d_lon))
            length = np.sqrt(d_lon**2 + d_lat**2)
            result[d_lon > 0] = (180/np.pi) * \
                np.arcsin(d_lat[d_lon > 0]/length[d_lon > 0])
            idx = (d_lon < 0) & (d_lat > 0)
            result[idx] = 180 - (180/np.pi) * \
                np.arcsin(d_lat[idx]/length[idx])
            idx = (d_lon < 0) & (d_lat < 0)
            result[idx] = -180 - (180/np.pi) * \
                np.arcsin(d_lat[idx]/length[idx])
            return result

        X['delta_lon'] = X[self.start_lon] - X[self.end_lon]
        X['delta_lat'] = X[self.start_lat] - X[self.end_lat]
        X['direction'] = calculate_direction(X.delta_lon, X.delta_lat)

        return X[["delta_lon", "delta_lat", "direction"]]

    def fit(self, X, y=None):
        return self
