FROM python:3.8.6-buster

COPY api /api
COPY project /project
COPY model.joblib /model.joblib
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD env FLASK_APP=api.flask flask run --host 0.0.0.0 --port $PORT
