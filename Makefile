
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
# gcp configuration
gcp_conf:
	export PROJECT_ID=le-wagon-data
	export DOCKER_IMAGE_NAME=wagon-data-tpl-image
	export CLUSTER_NAME=wagon-data-tpl-cluster

show_gcp_conf:
	@echo "PROJECT_ID: ${PROJECT_ID}"
	@echo "DOCKER_IMAGE_NAME: ${DOCKER_IMAGE_NAME}"
	@echo "CLUSTER_NAME: ${CLUSTER_NAME}"

# - - - - - - - - - - - - - - - - - - - - - - - -
# api

run_api:
	env FLASK_APP=api.flask flask run
