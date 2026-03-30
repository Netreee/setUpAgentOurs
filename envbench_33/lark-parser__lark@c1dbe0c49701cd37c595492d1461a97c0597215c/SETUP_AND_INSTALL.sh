#!/bin/bash
# EnvBench generated install script
# Repository: lark-parser/lark
# Revision: c1dbe0c49701cd37c595492d1461a97c0597215c

set -e

ls -la
cat pyproject.toml
cat test-requirements.txt
head -100 README.md
grep -i -A5 -B5 "install" README.md
cat tox.ini
pyenv versions
python --version
ls -la lark/
find . -name "setup.py" -o -name "requirements*.txt" -o -name "Pipfile" -o -name "poetry.lock" -o -name "environment.yml" | head -20
cat ./docs/requirements.txt
git submodule status
cat .gitmodules
cat .pre-commit-config.yaml
git submodule sync -q && git submodule update --init
python -m pip install --upgrade pip
python -m pip install -e .[regex,nearley,atomic_cache,interegular]
python -m pip install -r test-requirements.txt
python -c "import lark; print(f'Lark version: {lark.__version__}'); print('Import successful!')"
python -c "
from lark import Lark
grammar = '''start: WORD \",\" WORD \"!\"
            %import common.WORD
            %ignore \" \"'''
parser = Lark(grammar)
result = parser.parse(\"Hello, World!\")
print(f'Parse result: {result}')
print('Test passed!')
"
python -m pip install pre-commit
python -m pip install -r docs/requirements.txt
# python -m pip install mypy==1.10 types-atomicwrites types-regex rich<=13.4.1
python -m pip install "mypy==1.10" "types-atomicwrites" "types-regex" "rich<=13.4.1"
# cd tests && python -m pytest --version
python -m pip install pytest
# cd tests && python -m pytest test_parser.py -xvs -k "test_basic" 2>&1 | head -50
ls tests/*.py | head -10
pwd && ls -la
python -m pytest test_parser.py::TestParser::test_basic -xvs 2>&1 | head -100
