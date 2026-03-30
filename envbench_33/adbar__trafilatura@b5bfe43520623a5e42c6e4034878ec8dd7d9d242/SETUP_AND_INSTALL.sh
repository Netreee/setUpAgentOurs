#!/bin/bash
# EnvBench generated install script
# Repository: adbar/trafilatura
# Revision: b5bfe43520623a5e42c6e4034878ec8dd7d9d242

set -e

ls -la
cat setup.py
find . -name "requirements*.txt" -o -name "pyproject.toml" -o -name "setup.cfg" -o -name "Pipfile" -o -name "poetry.lock" | head -20
head -100 README.md
grep -n -i "install\|setup\|requirement" README.md | head -20
ls -la trafilatura/
pyenv versions
python --version
cat docs/requirements.txt
cat pytest.ini
head -50 HISTORY.md
pip install -e .
python -c "import trafilatura; print('Trafilatura version:', trafilatura.__version__)"
trafilatura --help
python -c "from trafilatura import fetch_url, extract; print('Basic imports successful')"
ls tests/ | head -10
apt-get update && apt-get install -y libcurl4-openssl-dev libssl-dev 2>/dev/null || true
pip install -e .[all]
# pip install -e .[gui]
python -c "
import trafilatura
from trafilatura import fetch_url, extract
import brotli
import pycurl
import zstandard
import py3langid
print('All core and optional dependencies imported successfully')
print('Trafilatura version:', trafilatura.__version__)
"
cd tests && python -m pytest cli_tests.py -v -k "test_" 2>&1 | head -50
# grep -i pytest setup.py
# grep -i pytest setup.py
# pwd && ls -la setup.py
cd .. && grep -i pytest setup.py
pip install pytest
python -m pytest tests/cli_tests.py::test_cli_help -xvs 2>&1 | head -100
python -m pytest tests/cli_tests.py --collect-only 2>&1 | head -50
python -m pytest tests/cli_tests.py::test_parser -xvs
find . -name "*.md" -o -name "*.rst" -o -name "*.txt" | xargs grep -l -i "install\|depend\|requirement" 2>/dev/null | head -10
