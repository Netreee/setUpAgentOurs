#!/bin/bash
# EnvBench generated install script
# Repository: ethereum/py-evm
# Revision: d8df507e42c885ddeca2b64bbb8f10705f075d3e

set -e

ls -la
head -100 README.md
cat DEVELOPMENT.md
cat pyproject.toml
cat setup.py
cat tox.ini
pyenv versions
python --version
pyenv global 3.12.0
python --version
which python
conda create -n py-evm python=3.12 -y
# conda activate py-evm
conda init bash
source /opt/conda/etc/profile.d/conda.sh && conda activate py-evm
python --version
cat Makefile | head -50
find . -name "requirements*.txt" -o -name "Pipfile*" -o -name "poetry.lock" -o -name "environment.yml" | head -20
grep -A 10 "Development Environment Setup" README.md
grep -r "apt-get\|apt install\|yum\|dnf\|apk\|brew" . --include="*.md" --include="*.txt" --include="*.rst" --include="*.py" 2>/dev/null | head -20
cat ./docs/guides/installation.rst
python -m pip install -U pip
python -m pip install -e ".[dev]"
python -m pip install ".[eth-extra]"
pre-commit install
python -c "import eth; print('Successfully imported eth module')"
python -c "from eth import __version__; print(f'py-evm version: {__version__}')"
python -c "from eth.vm.forks.byzantium import ByzantiumVM; print('ByzantiumVM imported successfully')"
python -m pip install ".[benchmark]"
python -m pytest tests/core/test_utils.py -xvs -k "test_to_tuple" 2>&1 | head -50
