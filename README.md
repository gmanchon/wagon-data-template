
# usage

## project

run trainer

``` bash
python -m project.app                   # run trainer
make run                                # run trainer
make run reg=True                       # run trainer with registry
```

run tests

``` bash
make pytest file=tests/conf
make pytest file=tests/code
make pytest file=tests/registry
```

## api locally

``` bash
make run_api
```

## api container locally

build local image

``` bash
docker build --tag=test .
```

run local image

``` bash
docker run -p 8000:8000 test
```

connect to http://localhost:8000/

``` bash
docker ps
```

``` bash
docker stop <container id>
```

## api container on GCR

enable [Google Container Registry API](https://console.cloud.google.com/flows/enableapi?apiid=containerregistry.googleapis.com&redirect=https://cloud.google.com/container-registry/docs/quickstart
) for your project

login to gcp

``` bash
gcloud auth login
```

configure docker for gcp

``` bash
gcloud auth configure-docker
```

list your config

``` bash
gcloud config list
```

configure your project

``` bash
export PROJECT_ID=replace-with-my-gcloud-project-id
echo $PROJECT_ID
gcloud config set project $PROJECT_ID
```

define a docker image name for your project

``` bash
export DOCKER_IMAGE_NAME=replace_with_your_docker_image_name
echo $DOCKER_IMAGE_NAME
```

build image

``` bash
docker build -t eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME .
```

push image to Google Container Registry

``` bash
docker push eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME
```
