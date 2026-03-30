#!/bin/bash
# EnvBench generated install script
# Repository: amperser/proselint
# Revision: 94a1eea991ffc171a28115523876add890f78225

set -e

ls -la
head -100 README.md
cat pyproject.toml
pyenv versions
python --version
pyenv global 3.8.18
python --version
which python
/root/.pyenv/versions/3.8.18/bin/python --version
ls -la proselint/
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "environment.yml" | head -20
ls -la scripts/
cat CONTRIBUTING.md
head -50 app.py
poetry --version
poetry env info --path 2>/dev/null || echo "No poetry environment yet"
poetry env use /root/.pyenv/versions/3.8.18/bin/python
# poetry install
# poetry lock --no-update
poetry lock
poetry install
poetry env info --path
source $(poetry env info --path)/bin/activate
which python && python --version
# python -c "import proselint; print('proselint version:', proselint.__version__)"
python -c "import proselint; import proselint.version; print('proselint version:', proselint.version.__version__)"
proselint --help
# echo "John is very unique." > test.txt && proselint test.txt
cat worker.py
grep -r "apt-get\|apt install\|yum\|dnf\|brew" . --include="*.md" --include="*.txt" --include="*.rst" 2>/dev/null | head -10
