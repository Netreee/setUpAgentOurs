#!/bin/bash
# EnvBench generated install script
# Repository: cantools/cantools
# Revision: 2c92c60f2d1b50894ad0c5652afd331283e03402

set -e

ls -la
cat pyproject.toml
head -50 README.rst
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "poetry.lock" | head -20
cat ./docs/requirements.txt
pyenv versions
python --version
which python && python -c "import sys; print(sys.version)"
cat tox.ini
cat Makefile
ls -la src/
ls -la src/cantools/
pip --version
ls -la setup.py 2>/dev/null || echo "No setup.py found"
pip install -e .
python -c "import cantools; print('Cantools version:', cantools.__version__)"
pip install -e ".[dev]"
pip install -e ".[plot]"
which gcc && gcc --version | head -1
python -c "
import cantools
print('Cantools successfully imported')
print('Version:', cantools.__version__)
# Try to load a simple database
try:
    import os
    db = cantools.database.load_file('tests/files/dbc/motohawk.dbc')
    print('Successfully loaded test DBC file')
    print('Number of messages:', len(db.messages))
except Exception as e:
    print('Error loading DBC file:', e)
"
pip install pytest==7.4.* pytest-cov==4.1.* coverage==7.3.* parameterized==0.9.*
pip install Sphinx==6.* sphinx_rtd_theme
cd /data/project && python -m pytest tests/ -xvs -k "test_load" --tb=short 2>&1 | head -100
# ls -la tests/
pwd && ls -la
cd cantools__cantools@2c92c60f2d1b50894ad0c5652afd331283e03402 && pwd && ls -la
python -m pytest tests/test_database.py::test_load -xvs --tb=short 2>&1 | head -50
find tests/ -name "*.py" -type f | head -10
# python -c "
# import cantools
# print('Testing basic functionality...')
# # Test loading a DBC file
# db = cantools.database.load_file('tests/files/dbc/motohawk.dbc')
# print(f'Loaded DBC with {len(db.messages)} messages')
# # Test encoding/decoding
# message = db.get_message_by_name('ExampleMessage')
# data = message.encode({'Enable': 1, 'AverageRadius': 100, 'Temperature': 250})
# print(f'Encoded message: {data.hex()}')
# decoded = message.decode(data)
# print(f'Decoded values: {decoded}')
# print('All tests passed!')
# "
python -c "
import cantools
print('Testing basic functionality...')
# Test loading a DBC file
db = cantools.database.load_file('tests/files/dbc/motohawk.dbc')
print(f'Loaded DBC with {len(db.messages)} messages')
# Test encoding/decoding with valid values
message = db.get_message_by_name('ExampleMessage')
data = message.encode({'Enable': 1, 'AverageRadius': 3, 'Temperature': 250})
print(f'Encoded message: {data.hex()}')
decoded = message.decode(data)
print(f'Decoded values: {decoded}')
print('All tests passed!')
"
