#!/bin/bash
# EnvBench generated install script
# Repository: getsentry/sentry-python
# Revision: ec7172e15311b88695827a76ca7fa83fba2efff4

set -e

ls -la
cat .tool-versions
cat pyproject.toml
cat setup.py
head -50 README.md
pyenv versions
cat test-requirements.txt
cat devenv-requirements.txt
cat linter-requirements.txt
head -100 tox.ini
cat Makefile
python --version
pyenv global 3.12.0
python --version
which python
ls -la sentry_sdk/
pip --version
conda create -n sentry-sdk python=3.12 -y
# conda activate sentry-sdk
eval "$(conda shell.bash hook)" && conda activate sentry-sdk
python --version
pip install -e .
pip install -r test-requirements.txt
pip install -r linter-requirements.txt
python -c "import sentry_sdk; print('Sentry SDK imported successfully')"
pip install tox
head -100 CONTRIBUTING.md
pip install -r devenv-requirements.txt
pre-commit install
# python -c "import sentry_sdk; print(f'Sentry SDK version: {sentry_sdk.__version__}')"
