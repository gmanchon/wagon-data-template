
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


class TimeTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, time_column, zone='America/New_York'):
        self.time_column = time_column
        self.zone = zone

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X.index = pd.to_datetime(X[self.time_column])
        X.index = X.index.tz_convert(self.zone)
        X["dow"] = X.index.weekday
        X["hour"] = X.index.hour
        X["month"] = X.index.month
        X["year"] = X.index.year
        return X[["dow", "hour", "month", "year"]].reset_index(drop=True)

    def fit(self, X, y=None):
        return self
