
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
	PYTHONDONTWRITEBYTECODE=1 pytest -v --color=yes

run:
	python -m project.app
