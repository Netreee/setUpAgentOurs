#!/bin/bash
# EnvBench generated install script
# Repository: posit-dev/great-tables
# Revision: c4cbd943e9376c62872c3c402e64d168264e5623

set -e

ls -la
head -100 README.md
cat pyproject.toml
pyenv versions
python --version
which python
cat Makefile
# ls -la *.py
find . -name "setup.py" -o -name "requirements*.txt" -o -name "Pipfile" -o -name "poetry.lock" | head -20
ls -la .github/
ls -la .github/workflows/
cat .github/workflows/ci-tests.yaml
ls -la great_tables/
pip install -e '.[all]'
python -c "import great_tables; print('Great Tables imported successfully')"
cd tests && python -m pytest test_gt.py -v -k "test_gt" 2>&1 | head -50
# ls -la .github/scripts/
find . -name "save_browser_table.py" -type f
find . -path "*github*" -name "*.py" -type f
find . -type d -name "scripts"
# find .github -type f
# ls -la .github/
pwd && ls -la
cd .. && pwd && ls -la
ls -la .github/
ls -la .github/scripts/
cat .github/scripts/save_browser_table.py
python -c "import selenium; print('Selenium imported successfully')"
grep -r "apt-get\|apt install\|yum\|dnf\|apk" . --include="*.md" --include="*.txt" --include="*.py" --include="*.toml" --include="*.yaml" --include="*.yml" 2>/dev/null | head -20
cat .pre-commit-config.yaml
