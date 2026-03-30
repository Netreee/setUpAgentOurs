#!/bin/bash
# EnvBench generated install script
# Repository: kedro-org/kedro
# Revision: 9883223c9e03a58c2acc572ac65ce0d223d899ad

set -e

ls -la
head -100 README.md
cat pyproject.toml
pyenv versions
python --version
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" | head -20
cat Makefile
head -50 CONTRIBUTING.md
ls -la docs/
cat .pre-commit-config.yaml
uv --version
uv pip install --system -e .
uv pip install --system -e ".[test]"
# kedro --version
python -c "import sys; print(f'Python {sys.version}')"
python -W "default:Kedro is not yet fully compatible" -m kedro --version
# python -c "import kedro; print(f'Successfully imported kedro version {kedro.__version__}')"
python -W "ignore:Kedro is not yet fully compatible" -c "import kedro; print(f'Successfully imported kedro version {kedro.__version__}')"
pre-commit --version
find . -type f -name "*.md" -exec grep -l "apt-get\|apt install\|yum\|dnf\|apk\|brew" {} \; | head -10
grep -n "apt-get\|apt install\|yum\|dnf\|apk\|brew" ./docs/source/deployment/aws_step_functions.md ./docs/source/deployment/amazon_emr_serverless.md | head -5
ls -la tools/
cat tools/print_env.sh
python -W "ignore:Kedro is not yet fully compatible" -m kedro info 2>/dev/null || echo "Checking kedro info"
python -c "import pytest; print(f'pytest version: {pytest.__version__}')"
pyenv versions | grep 3.12
cd /data/project && python -m pytest tests/framework/cli/test_cli.py::TestKedroCli::test_kedro_cli -xvs 2>&1 | head -50
find tests -name "test_cli.py" -type f | head -5
ls -la
cd /data/project && ls -la
