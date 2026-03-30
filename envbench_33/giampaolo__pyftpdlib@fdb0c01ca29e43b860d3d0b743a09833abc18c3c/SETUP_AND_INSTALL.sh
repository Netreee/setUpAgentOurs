#!/bin/bash
# EnvBench generated install script
# Repository: giampaolo/pyftpdlib
# Revision: fdb0c01ca29e43b860d3d0b743a09833abc18c3c

set -e

ls -la
cat pyproject.toml
cat setup.py
find . -name "requirements*.txt" -o -name "setup.cfg" -o -name "Pipfile" -o -name "poetry.lock" -o -name "environment.yml" | head -20
head -100 README.rst
cat docs/requirements.txt
cat Makefile | head -50
cat Makefile | grep -A 20 "Install"
pyenv versions
find .github -name "*.yml" -o -name "*.yaml" | xargs cat | head -100
head -50 pyftpdlib/__init__.py
python --version
pyenv global 3.11.7
python --version
which python
find . -name "environment*.yml" -o -name "*.yaml" | head -5
cat ./docs/.readthedocs.yaml
export PATH="/root/.pyenv/versions/3.11.7/bin:$PATH" && python --version
export PATH="/root/.pyenv/versions/3.11.7/bin:$PATH" && python -m pip install --upgrade pip setuptools
export PATH="/root/.pyenv/versions/3.11.7/bin:$PATH" && python setup.py develop
export PATH="/root/.pyenv/versions/3.11.7/bin:$PATH" && python -m pip install psutil pyopenssl pytest
echo $GITHUB_ACTIONS
export PATH="/root/.pyenv/versions/3.11.7/bin:$PATH" && python -m pip install black check-manifest coverage pylint pytest-cov pytest-xdist rstcheck ruff teyit toml-sort twine
export PATH="/root/.pyenv/versions/3.11.7/bin:$PATH" && python -m pip install sphinx sphinx_rtd_theme
export PATH="/root/.pyenv/versions/3.11.7/bin:$PATH" && python -c "import pyftpdlib; print(f'pyftpdlib version: {pyftpdlib.__ver__}')"
export PATH="/root/.pyenv/versions/3.11.7/bin:$PATH" && python -c "import sys; import pyftpdlib; from pyftpdlib.handlers import FTPHandler; print('Basic imports successful')"
# export PATH="/root/.pyenv/versions/3.11.7/bin:$PATH" && python -m pytest pyftpdlib/test/test_imports.py -v
find pyftpdlib/test -name "test_*.py" | head -10
export PATH="/root/.pyenv/versions/3.11.7/bin:$PATH" && python -m pytest pyftpdlib/test/test_authorizers.py::TestDummyAuthorizer -v
# export PATH="/root/.pyenv/versions/3.11.7/bin:$PATH" && python -c "try: import pysendfile; print('pysendfile available'); except ImportError: print('pysendfile not available')"
