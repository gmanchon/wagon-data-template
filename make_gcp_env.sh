
# - - - - - - - - - - - - - - - - - - - - - - - -
# ai platform training

# Code package
export PACKAGE_NAME="project"
export PACKAGE_ENTRY_POINT="app"

# Training environment
export REGION="europe-west1"
export PYTHON_VERSION=3.7
export RUNTIME_VERSION=2.2

# Training job
export JOB_PREFIX="job"

# Training storage
export BUCKET_NAME="le-wagon-data"
export JOB_FOLDER="trainings"

# - - - - - - - - - - - - - - - - - - - - - - - -
# gcp prod prediction

# Google Cloud Platform project
export PROJECT_ID=le-wagon-data

# Google Cloud Registry
export DOCKER_IMAGE_NAME=wagon-data-tpl-image

# Google Kubernetes Engine
export CLUSTER_NAME=wagon-data-tpl-cluster
export DEPLOYMENT_NAME=ml-kube-deployment
