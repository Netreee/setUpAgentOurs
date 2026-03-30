#!/bin/bash
# EnvBench generated install script
# Repository: jazzband/pip-tools
# Revision: 53309647980e2a4981db54c0033f98c61142de0b

set -e

ls -la
cat pyproject.toml
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "Pipfile.lock" -o -name "poetry.lock" | head -20
head -100 README.md
grep -i "install\|requirement\|dependency\|test\|dev" README.md | head -30
pyenv versions
cat CONTRIBUTING.md
cat tox.ini
cat docs/requirements.txt
cat .pre-commit-config.yaml
python --version
which python && python -c "import sys; print(sys.version)"
ls -la piptools/
pip --version
pip install -e .
pip install -e .[testing,coverage]
pip install pre-commit
pip-compile --help | head -20
pip-sync --help | head -20
# python -c "import piptools; print(f'pip-tools version: {piptools.__version__}')"
python -c "import piptools; from importlib.metadata import version; print(f'pip-tools version: {version(\"pip-tools\")}')"
python -m pytest --version
find . -name "*.md" -type f | xargs grep -l -i "install\|setup\|requirement\|dependency" | head -10
ls -la .github/workflows/
head -100 .github/workflows/ci.yml
pip install black isort pyupgrade flake8 flake8-pytest-style mypy bandit
pip install click==8.0.1 pep517==0.10.0 toml==0.10.2 pip==20.3.4 build==1.0.0 pyproject_hooks==1.0.0 pytest==7.4.2
# pip install --upgrade pip>=22.2
# python -m pip install --upgrade pip
conda install -y pip
