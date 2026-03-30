#!/bin/bash
# EnvBench generated install script
# Repository: pypa/pip
# Revision: 67e2a5698706751161d8af3dad1dbb8e62bc8cbb

set -e

ls -la
cat README.rst
cat pyproject.toml
ls -la src/
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "Pipfile.lock" -o -name "poetry.lock" | head -20
cat tests/requirements.txt
head -100 noxfile.py
pyenv versions
python --version
pip install setuptools>=67.6.1 wheel
pip install -e .
pip --version
pip install -r tests/requirements.txt
cat .pre-commit-config.yaml
ls -la tools/
find .github/workflows -name "*.yml" -o -name "*.yaml" | head -5
head -100 .github/workflows/ci.yml
pip install nox
pip install ruff black mypy codespell pre-commit
pip install keyring==24.2.0 types-docutils==0.20.0.3 types-setuptools==68.2.0.0 types-freezegun==1.1.10 types-pyyaml==6.0.12.12
find . -name "*.md" -o -name "*.rst" -o -name "*.txt" | xargs grep -l "apt-get\|apt install\|yum\|dnf\|apk\|system" | head -10
cat docs/html/development/contributing.rst | head -100
find docs -name "*.rst" -o -name "*.md" | xargs grep -l "setup\|install\|development" | head -10
cat docs/html/development/index.rst
cat docs/html/development/getting-started.rst
python -c "import pip; print(f'pip version: {pip.__version__}')"
python -c "from pip._internal.cli.main import main; print('pip main function imported successfully')"
# which git svn bzr hg
cat tests/requirements-common_wheels.txt
nox -s lint -- -k "not test" 2>&1 | head -50
