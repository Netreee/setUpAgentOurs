#!/bin/bash
# EnvBench generated install script
# Repository: guardrails-ai/guardrails
# Revision: d85ea96e123850391e2667864f148639dc335b9e

set -e

ls -la
cat pyproject.toml
head -100 README.md
grep -i "install\|setup\|requirement" README.md | head -20
cat CONTRIBUTING.md
cat Makefile
pyenv versions
python --version
cat package.json
poetry --version
# make dev
pyenv global 3.12.0
python --version
which python
/root/.pyenv/versions/3.12.0/bin/python --version
poetry env use /root/.pyenv/versions/3.12.0/bin/python
make dev
source $(poetry env info --path)/bin/activate
which python
# make test-basic
ls -la guardrails/
find guardrails -name "*version*" -type f
head -50 guardrails/__init__.py
# grep -r "__version__" guardrails/
grep -n "version" pyproject.toml
python -c "import guardrails; print('Guardrails imported successfully')"
grep -n "test-basic" Makefile -A 2
sed -n '46,52p' Makefile
find . -name "*.py" -type f -exec grep -l "__version__" {} \;
python -c "import guardrails; print(dir(guardrails))"
