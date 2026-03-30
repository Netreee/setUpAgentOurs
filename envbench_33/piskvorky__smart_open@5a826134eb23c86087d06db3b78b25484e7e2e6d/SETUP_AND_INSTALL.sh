#!/bin/bash
# EnvBench generated install script
# Repository: piskvorky/smart_open
# Revision: 5a826134eb23c86087d06db3b78b25484e7e2e6d

set -e

ls -la
cat pyproject.toml
cat setup.py
find . -name "requirements*.txt" -o -name "setup.cfg" -o -name "Pipfile" -o -name "poetry.lock" | head -20
cat ./integration-tests/requirements.txt
head -100 README.rst
grep -n -i "install" README.rst | head -20
sed -n '113,135p' README.rst
pyenv versions
python --version
cat MANIFEST.in
ls -la smart_open/
cat smart_open/version.py
find . -name "*.cfg" -o -name "*.ini" -o -name "*.yml" -o -name "*.yaml" -o -name "tox.ini" -o -name "Makefile" | head -20
head -50 .github/workflows/python-package.yml
sed -n '40,80p' .github/workflows/python-package.yml
# python -c "
# import setup
# print('Base deps:', setup.base_deps)
# print('Test deps:', setup.tests_require)
# "
python -c "
import ast
with open('setup.py', 'r') as f:
    content = f.read()
tree = ast.parse(content)
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if hasattr(target, 'id'):
                if target.id in ['base_deps', 'aws_deps', 'gcs_deps', 'azure_deps', 'http_deps', 'ssh_deps', 'zst_deps', 'all_deps', 'tests_require']:
                    print(f'{target.id}: {ast.unparse(node.value) if hasattr(ast, \"unparse\") else ast.dump(node.value)}')
"
python -m pip install -U pip
pip install -e .
python -c "import smart_open; print('smart_open imported successfully')"
pip install -e .[test]
python -c "
import smart_open
print('smart_open version:', smart_open.__version__)
print('smart_open imported successfully with all dependencies')

# Try to import some of the optional dependencies
try:
    import boto3
    print('boto3 imported successfully')
except ImportError:
    print('boto3 import failed')

try:
    import google.cloud.storage
    print('google.cloud.storage imported successfully')
except ImportError:
    print('google.cloud.storage import failed')

try:
    import azure.storage.blob
    print('azure.storage.blob imported successfully')
except ImportError:
    print('azure.storage.blob import failed')

try:
    import paramiko
    print('paramiko imported successfully')
except ImportError:
    print('paramiko import failed')
"
python -c "
from smart_open import open
import tempfile
import os

# Test basic file operations
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write('Hello, world!\\n')
    temp_path = f.name

try:
    with open(temp_path, 'r') as f:
        content = f.read()
        print('Read from file:', repr(content))
        assert content == 'Hello, world!\\n'
        print('Basic file operations work correctly')
finally:
    os.unlink(temp_path)
"
pip install awscli
find . -type f -name "*.md" -o -name "*.rst" -o -name "*.txt" | xargs grep -l -i "apt-get\|apt install\|yum\|dnf\|apk\|system" | head -10
grep -i "apt-get\|apt install\|yum\|dnf\|apk\|system" README.rst CHANGELOG.md MIGRATING_FROM_OLDER_VERSIONS.rst help.txt | head -20
pip install flake8
python -m pytest --version
python -m pytest smart_open/tests/test_compression.py -v -k "test_compression" --tb=short
