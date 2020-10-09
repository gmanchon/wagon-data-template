
from project.trainer.transformers.distance_transformer \
    import DistanceTransformer
from project.trainer.transformers.geohash_transformer \
    import GeohashTransformer
from project.trainer.transformers.direction_transformer \
    import DirectionTransformer
from project.trainer.transformers.distance_to_center_transformer \
    import DistanceToCenterTransformer
from project.trainer.transformers.time_transformer \
    import TimeTransformer

from sklearn.preprocessing import OneHotEncoder, RobustScaler

import category_encoders as ce

from sklearn.compose import ColumnTransformer

from sklearn.linear_model import Lasso, Ridge, LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.pipeline import Pipeline, make_pipeline

from colorama import Fore, Style


class ProjectPipeline():

    def __init__(self, params):

        # getting params
        self.params = params

        # getting trainer parameters
        self.estimator = self.params.get('estimator', 'linear')
        self.hyperparams = self.params.get('hyperparams', dict())
        self.pipeline = self.params.get('pipeline', dict())

    def create_estimator(self):

        print(Fore.GREEN + "\nModel hyperparameters:\n"
              + Style.RESET_ALL
              + "%s" % self.hyperparams)

        estimator = self.estimator

        if estimator == 'linear':
            return LinearRegression(self.hyperparams)
        elif estimator == 'lasso':
            return Lasso(self.hyperparams)
        elif estimator == 'ridge':
            return Ridge(self.hyperparams)
        elif estimator == 'randomforest':
            return RandomForestRegressor(**self.hyperparams)

    def create_pipeline(self):

        # create pipeline
        distance_arguments = dict(start_lat="pickup_latitude",
                                  start_lon="pickup_longitude",
                                  end_lat="dropoff_latitude",
                                  end_lon="dropoff_longitude")

        distance_columns = list(distance_arguments.values())

        time_columns = ["pickup_datetime"]

        # getting distance params
        distance_params = self.pipeline.get('distance', dict())
        dt_params = {**distance_params, **distance_arguments}

        pipe_distance = make_pipeline(
            DistanceTransformer(**dt_params),
            RobustScaler())

        pipe_geohash = make_pipeline(
            GeohashTransformer(),
            ce.HashingEncoder())

        pipe_direction = make_pipeline(
            DirectionTransformer(),
            RobustScaler())

        pipe_distance_to_center = make_pipeline(
            DistanceToCenterTransformer(),
            RobustScaler())

        pipe_time = make_pipeline(
            TimeTransformer(time_column='pickup_datetime'),
            OneHotEncoder(handle_unknown='ignore'))

        transformers = [
            ('distance', pipe_distance, distance_columns),
            # ('geohash', pipe_geohash, distance_columns),  # bug
            ('direction', pipe_direction, distance_columns),
            ('distance_to_center', pipe_distance_to_center, distance_columns),
            ('time', pipe_time, time_columns),
        ]

        preprocessor = ColumnTransformer(transformers)

        estimator = self.create_estimator()

        steps = [('preprocessor', preprocessor),
                 ('regressor', estimator)]

        pipeline = Pipeline(steps=steps)

        return pipeline
