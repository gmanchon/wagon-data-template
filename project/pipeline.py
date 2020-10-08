
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression

from sklearn.pipeline import Pipeline


class ProjectPipeline():

    def create_pipeline(self):

        # create pipeline
        steps = [('scaler', StandardScaler()),
                 ('model', LinearRegression())]

        pipeline = Pipeline(steps=steps)

        return pipeline
