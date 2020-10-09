
# todo

## train

- [x] package

- [x] data: use taxifaremodel

- [x] taxifare: from existing model



- [x] makefile: env
- [x] makefile: packages

- [x] notebook: load project

- [x] app: use app + model + pipeline nested parameters

- [x] trainer: log training steps in cli

- [x] registry tracking repo: auto parse nested parameters
- [x] registry tracking repo: upload tracking to mlflow
- [ ] registry model repo: upload trained model on gcs
- [ ] registry code repo: auto commit if required and label trained code

- [ ] registry: do not store all runs ? / Bruno

- [x] train locally
- [ ] train on colab
- [ ] train on aipf

- [ ] how much lines trained locally (which features / model) in 1h
- [ ] how much lines trained colab (which features / model) in 1h
- [ ] how much lines trained on aipf (which features / model) in 1h

- [ ] pipeline debug: parse column transformer to display outcome of each step
- [ ] pipeline debug: auto parse various architectures of pipelines

- [ ] gridsearch + forward to registry

- [ ] tracking: train time

- [ ] env: make activate_env directive does not work

- [ ] test: pipeline steps outcome

- [ ] data: aggregate weather data
- [ ] data: periodical retrain

## pred

- [ ] registry tracking repo: mlflow api to retrieve metrics as csv
- [ ] registry model repo: get model from gcs
- [ ] registry code repo: get code from git label

- [ ] performance tracker: visualize in notebook perfs accross registry trainings

- [ ] back: prod pred model from registry according to selected perf

- [ ] back: run locally
- [ ] back: prod docker + gcr
- [ ] back: prod docker + gke

- [ ] back: fastapi
- [ ] back: flask

- [ ] front: separate repo for front (limit size)
- [ ] front: streamlit + heroku

## kampai

- [ ] reintegrate as much code as possible in kampai framework classes and helpers (metrics)

# usage

``` bash
python -m project.app                   # run trainer
```
