
from flask import Flask, escape, request

import pandas as pd

import joblib

app = Flask(__name__)


@app.route('/')
def hello():
    # get param from http://127.0.0.1:5000/?name=value
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/predict_fare', methods=['GET'])
def predict_fare():

    # get request arguments
    key = request.args.get('key')

    pickup_datetime = request.args.get('pickup_datetime')
    pickup_longitude = float(request.args.get('pickup_longitude'))
    pickup_latitude = float(request.args.get('pickup_latitude'))
    dropoff_longitude = float(request.args.get('dropoff_longitude'))
    dropoff_latitude = float(request.args.get('dropoff_latitude'))
    passenger_count = int(request.args.get('passenger_count'))

    # build X ⚠️ beware to the order of the parameters ⚠️
    X = pd.DataFrame(dict(
        key=[key],
        pickup_datetime=[pickup_datetime],
        pickup_longitude=[pickup_longitude],
        pickup_latitude=[pickup_latitude],
        dropoff_longitude=[dropoff_longitude],
        dropoff_latitude=[dropoff_latitude],
        passenger_count=[passenger_count]))

    # print(X_test.dtypes)

    # TODO: get model from GCP
    # pipeline = get_model_from_gcp()
    pipeline = joblib.load('model.joblib')

    # make prediction
    results = pipeline.predict(X)

    # convert response from numpy to python type
    pred = float(results[0])

    return dict(
        prediction=pred)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
