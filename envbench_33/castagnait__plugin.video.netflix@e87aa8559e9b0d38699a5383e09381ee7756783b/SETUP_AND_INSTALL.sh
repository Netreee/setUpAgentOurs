#!/bin/bash
# EnvBench generated install script
# Repository: castagnait/plugin.video.netflix
# Revision: e87aa8559e9b0d38699a5383e09381ee7756783b

set -e

ls -la
find . -name "*.toml" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "poetry.lock" -o -name "environment.yml" | head -20
head -100 README.md
cat requirements.txt
find . -type f -name "*.py" | head -20
grep -r "python" . --include="*.py" --include="*.md" --include="*.txt" --include="*.yml" --include="*.yaml" | grep -i "version\|3\." | head -10
pyenv versions
pyenv global 3.10.13
python --version
which python
find . -name "environment.yml" -o -name "*.yaml" | xargs grep -l "dependencies\|channels" 2>/dev/null || true
cat Makefile
cat tox.ini
head -50 addon.xml
pip install -r requirements.txt
find . -name "*.sh" -o -name "*.bash" -o -name "install*" -o -name "setup*" | head -10
ls -la tests/
grep -r "import" resources/lib/*.py resources/lib/*/*.py 2>/dev/null | grep -v "from resources" | head -20
cat tests/run.py
# python -c "import sys; sys.path.insert(0, '.'); from resources.lib import run_addon; print('Import successful')"
grep -r "AddonSignals" . --include="*.py" --include="*.xml" | head -10
cat tests/AddonSignals.py
grep -A5 -B5 "test-unit" Makefile
cat tests/__init__.py
grep -r "apt-get\|apt install\|yum\|dnf\|apk\|brew" . --include="*.md" --include="*.txt" --include="*.sh" 2>/dev/null | head -10
find .github/workflows -name "*.yml" -o -name "*.yaml" | xargs cat | grep -i "apt\|install\|sudo" | head -20
apt-get update && apt-get install -y libxml2-utils gettext
apt-get install -y libmysqlclient-dev default-libmysqlclient-dev 2>/dev/null || apt-get install -y default-mysql-client libmysqlclient21 2>/dev/null || true
# cd /data/project && PYTHONPATH=/data/project/tests:$PYTHONPATH python -c "import sys; sys.path.insert(0, '.'); from resources.lib import run_addon; print('Import successful')"
pwd && ls -la
