
default: pylint pytest

# - - - - - - - - - - - - - - - - - - - - - - - -
# Virtual env

create_env:
	pyenv virtualenv 3.8.5 taxifareproject

list_env:
	pyenv versions

activate_env:
	pyenv activate taxifareproject

# - - - - - - - - - - - - - - - - - - - - - - - -
# Packages

install_jupyter:
	pip install jupyter
	pip install jupyter_contrib_nbextensions
	pip install jupyter_nbextensions_configurator

install_requirements:
	pip install -r requirements.txt

install_project:
	pip install -e .

# - - - - - - - - - - - - - - - - - - - - - - - -
# Project

pylint:
	find . -iname "*.py" -not -path "./tests/*" | xargs pylint --output-format=colorized; true

pytest:
	# $(file) allows to `make pytest file=test/conf`
	PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes $(file)

run:
	python -m project.app $(reg)

# - - - - - - - - - - - - - - - - - - - - - - - -
# ai platform training

show_gcp_creds:
	cat ${GOOGLE_APPLICATION_CREDENTIALS}

show_aipf_env:
	@echo ""
	@echo "Code package:"
	@echo "- PACKAGE_NAME: ${PACKAGE_NAME}"
	@echo "- PACKAGE_ENTRY_POINT: ${PACKAGE_ENTRY_POINT}"
	@echo ""
	@echo "Training environment:"
	@echo "- REGION: ${REGION}"
	@echo "- PYTHON_VERSION: ${PYTHON_VERSION}"
	@echo "- RUNTIME_VERSION: ${RUNTIME_VERSION}"
	@echo ""
	@echo "Training job:"
	@echo "- JOB_PREFIX: ${JOB_PREFIX}"
	@echo ""
	@echo "Training storage:"
	@echo "- BUCKET_NAME: ${BUCKET_NAME}"
	@echo "- JOB_FOLDER: ${JOB_FOLDER}"

JOB_NAME=${JOB_PREFIX}_$(shell date +'%Y%m%d_%H%M%S')

gcp_submit_training:
	gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir "gs://${BUCKET_NAME}/${JOB_FOLDER}" \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${PACKAGE_ENTRY_POINT} \
		--region ${REGION} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--stream-logs

gcp_submit_registry:
	gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir "gs://${BUCKET_NAME}/${JOB_FOLDER}" \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${PACKAGE_ENTRY_POINT} \
		--region ${REGION} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--stream-logs \
		-- \
		--reg=True

# - - - - - - - - - - - - - - - - - - - - - - - -
# gcp prod prediction

show_prod_env:
	@echo ""
	@echo "Google Cloud Platform project:"
	@echo "- PROJECT_ID: ${PROJECT_ID}"
	@echo ""
	@echo "Google Cloud Registry:"
	@echo "- DOCKER_IMAGE_NAME: ${DOCKER_IMAGE_NAME}"
	@echo ""
	@echo "Google Kubernetes Engine:"
	@echo "- CLUSTER_NAME: ${CLUSTER_NAME}"
	@echo "- DEPLOYMENT_NAME: ${DEPLOYMENT_NAME}"

show_gcp_conf:
	gcloud auth list
	gcloud config list
	gcloud iam service-accounts list

# - - - - - - - - - - - - - - - - - - - - - - - -
# api

run_api:
	env FLASK_APP=api.flask flask run
