#!/bin/bash
# EnvBench generated install script
# Repository: tortoise/tortoise-orm
# Revision: bc18384bdb490cc14e96d27a18956fe1b122829d

set -e

ls -la
cat pyproject.toml
head -100 README.rst
pyenv versions
cat Makefile
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "Pipfile.lock" | head -20
ls -la tortoise/
poetry --version
poetry env info
# poetry install -E asyncpg -E aiomysql -E accel -E psycopg -E asyncodbc
# poetry install --no-root
python --version
pyenv global 3.12.0
python --version
which python
/root/.pyenv/versions/3.12.0/bin/python --version
poetry env use /root/.pyenv/versions/3.12.0/bin/python
poetry install --no-root
source $(poetry env info --path)/bin/activate
python --version
poetry install
python -c "import tortoise; print('Tortoise ORM imported successfully')"
python -c "from tortoise import Tortoise; print('Tortoise class imported successfully')"
python -m pytest tests/ -xvs -k "test_simple" 2>&1 | head -50
poetry install -E asyncpg -E aiomysql -E accel -E psycopg -E asyncodbc
python -c "import asyncpg; print('asyncpg imported successfully')"
python -m pytest tests/test_models.py -xvs -k "test_basic" 2>&1 | head -100
find tests -name "*.py" | head -10
python -m pytest tests/test_basic.py::test_create -xvs 2>&1 | head -100
grep -n "def test" tests/test_basic.py | head -10
