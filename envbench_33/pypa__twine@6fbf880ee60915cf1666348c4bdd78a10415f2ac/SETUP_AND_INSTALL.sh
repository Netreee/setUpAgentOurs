#!/bin/bash
# EnvBench generated install script
# Repository: pypa/twine
# Revision: 6fbf880ee60915cf1666348c4bdd78a10415f2ac

set -e

ls -la
cat README.rst
cat pyproject.toml
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "poetry.lock" | head -20
cat ./docs/requirements.txt
cat tox.ini
pyenv versions
python --version
ls -la twine/
find . -name "*.py" -path "*/setup.py" -o -name "setup.cfg" | head -10
# ls -la | grep -i poetry
find . -name "poetry.lock" -o -name "Pipfile.lock"
pip --version
pip install setuptools>=61.2 wheel setuptools_scm[toml]>=6.0
pip install -e .
# python -c "import twine; print(f'Twine version: {twine.__version__}')"
head -50 twine/__init__.py
python -c "import importlib_metadata; metadata = importlib_metadata.metadata('twine'); print(list(metadata.keys()))"
# python -c "import twine; print(dir(twine))"
# twine --help
python -c "import importlib_metadata; metadata = importlib_metadata.metadata('twine'); print('Project-URL values:'); [print(f'  {k}: {v}') for k, v in metadata.items() if k == 'Project-URL']"
# python -c "import sys; sys.path.insert(0, '.'); exec(open('twine/__init__.py').read().replace('metadata[\"home-page\"]', 'dict(metadata.get_all(\"Project-URL\")).get(\"Homepage\")')); print(f'Version: {__version__}')"
# cd /data/project && python -m pytest --version
pip install pretend pytest pytest-socket build coverage
# pip install -r docs/requirements.txt
find . -name "requirements.txt" -type f
# pip install -r ./docs/requirements.txt
pwd && ls -la
cd pypa__twine@6fbf880ee60915cf1666348c4bdd78a10415f2ac && pwd && ls -la
pip install -r docs/requirements.txt
