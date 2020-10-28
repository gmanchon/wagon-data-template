
# todo

## sister projects

framework code

- [ ] kampai

code inspiration for kampai framwework, source projects

- [ ] Keurcien car accidents (pipelines)
      https://github.com/keurcien/car-accidents/blob/master/pipeline.py
      https://github.com/keurcien/car-accidents/blob/master/transformers.py
- [ ] Jean taxifaremodel (trainer)
- [ ] Bruno olist (data aggregation)

code inspiration for data eng week challenge, source projects

- [ ] own recaps for code simplicity (all code complexity is banner and goes into kampai)
      https://github.com/gmanchon/taxifare-gcp-trainer/blob/master/Taxifare/trainer.py

## train

- [x] package

- [x] data: use taxifaremodel

- [x] taxifare: from existing model

- [x] makefile: env
- [x] makefile: packages

- [x] notebook: load project

- [x] conf: test hydra vs dotenv
- [x] conf: use yaml + transform conf dictionary into object attributes

- [x] app: use app + model + pipeline nested parameters

- [ ] app: use hydra conf for nested params
- [ ] app: option for the nested parameters dict using the scikit double underscore syntax
- [ ] app: add syntax validation for the nested parameters dict (warn for erroneous param syntax)

- [x] trainer: log training steps in cli

- [x] registry tracking repo: auto parse nested parameters
- [x] registry tracking repo: upload tracking to mlflow
- [ ] registry model repo: upload trained model on gcs
- [ ] registry code repo: auto commit if required and label trained code

- [ ] registry: do not store all runs ? / Bruno

- [x] train locally
- [ ] train on colab
- [ ] train on aipf

- [ ] perf: how much lines trained locally (which features / model) in 1h
- [ ] perf: how much lines trained colab (which features / model) in 1h
- [ ] perf: how much lines trained on aipf (which features / model) in 1h

- [ ] pipeline debug: parse column transformer to display outcome of each step
- [ ] pipeline debug: auto parse various architectures of pipelines

- [ ] gridsearch + forward to registry
- [ ] gridsearch: progress bar
- [ ] gridsearch: progress bar on aipf ?

- [ ] tracking: train time

- [ ] env: make activate_env directive does not work

- [ ] test: pipeline steps outcome

- [ ] data: aggregate weather data
- [ ] data: periodical retrain

- [ ] de week challenge: version ultra réduite du template kampai sans code complexe façon code des reboots
- [ ] de week challenge: laisser les élèves implémenter le modèle RandomForestRegressor(self.hyperparams)
- [ ] de week challenge: deep l'archi du modèle c'est pas un param



> course slides: recherche mode gridsearch/dev vs mode prod
> parcours utilisateur du ds au data engineer
> => comprend pourquoi on faire un truc complexe sur la semaine 7



>>> 2 modes de fonctionnement : mode gridsearch / notebook où je search dans le notebook
>>> et le mode registry / label / prod où je labelise les trains
>>> c'est pas parce qu'on train sur aipf que c'est de la prod
- [ ] optimisation: comment on cache un csv preprocessé s'il prend plein de temps
tout en restant cohérent avec l'utilisation du pipeline en pred
- [ ] faire des pipelines avec du cache pour le geohash
c'est le pipe de la gridsearch
le pipe dédié à la gridsearch il a pas besoin de pred donc il peut utiliser
des csv intermédiaires pour pas trop refaire le preprocessing
- [ ] avoir un pipe différent pour la prod, comme ça il est cohérent



- [ ] mode gridsearch où on utilise pas la registry:
y'a juste un gros log avec tout si on fait 10k runs de qqes secondes
on va pas tout stocker dans la registry
- [ ] gridsearcher et fine tuner c'est pas la même intention
=> en mode grid search on ne stocke pas dans la registry

app sert à 1 modèle
gridsearch plus en amont, c'est du search dans le notebook pour trouver le bon axe de recherche

le preprocessing peut être preprocessé aussi dans le notebook

on joue avec le notebook à piloter l'app pour gridsearch
quand on a un train dont on est fier on le labelise dans la registry

en semaine 1 on défriche
en semaine 2 on labelise une baseline



- [ ] optimisation: gridsearch, s'assurer que le code ne refait pas de tâches inutiles
- [ ] optimisation: dask ???



// perf viz:
// scatterplot perf / training time
// scatterplot perf / size
// => tradeoff perf vs complexité ou train time

// learning curve fonction de la taille du nrows
// learning curve à l'intérieur d'un type de modèle ou d'hyper params

// communication pas automatisable (la learning curve accross trainings de la team ds)

// course : rappel la version du code doit être cohérente entre train et pred
// rajouter un point sur fonctionnement jobkib



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

- [ ] env: warning quand le bon env est pas activé

- [ ] nlp: reintegrate a nlp project

- [ ] deep: reintegrate a deep project / Zuza ?

# usage

``` bash
python -m project.app                   # run trainer
```
