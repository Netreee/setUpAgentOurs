#!/bin/bash
# EnvBench generated install script
# Repository: nonebot/nonebot2
# Revision: 7b724925badfe7133979c3d4d90a15054cdebabd

set -e

ls -la
cat pyproject.toml
head -100 README.md
grep -n -i "install\|setup\|quick" README.md | head -20
pyenv versions
python --version
ls -la nonebot/
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "environment.yml" | head -20
head -50 CONTRIBUTING.md
poetry --version
ls -la envs/
ls -la envs/test/
cat package.json
find .github -name "*.yml" -o -name "*.yaml" | head -10
head -50 .github/workflows/noneflow.yml
head -100 .github/workflows/ruff.yml
head -100 .github/workflows/pyright.yml
find .github/actions -type f -name "*.yml" -o -name "*.yaml" | xargs cat
# node --version && npm --version && yarn --version
npm install -g yarn
yarn --version
# poetry install --all-extras
pyenv global 3.12.0 && python --version
which python && python --version
echo $PATH
/root/.pyenv/versions/3.12.0/bin/python --version
poetry env use /root/.pyenv/versions/3.12.0/bin/python
poetry install --all-extras
source $(poetry env info --path)/bin/activate && python --version
ls -la website/
