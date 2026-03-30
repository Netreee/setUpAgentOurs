#!/bin/bash
# EnvBench generated install script
# Repository: spec-first/connexion
# Revision: a930303faa9e10603cdd820c497303b2e52d8253

set -e

ls -la
head -50 README.md
cat pyproject.toml
pyenv versions
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "environment.yml" | head -20
cat tox.ini
cat .pre-commit-config.yaml
ls -la connexion/
find docs -name "*.md" -o -name "*.rst" -o -name "*.txt" | head -10
head -50 docs/quickstart.rst
poetry --version
# poetry install --all-extras --with tests
python --version
pyenv global 3.8.18 && python --version
which python
pip install -e .[flask,swagger-ui,uvicorn,mock]
pip install pytest pytest-asyncio pytest-cov pre-commit
pip install sphinx sphinx_copybutton sphinx_design sphinx-rtd-theme sphinxemoji
# python -c "import connexion; print(f'Connexion version: {connexion.__version__}')"
python -c "import connexion; print('Connexion imported successfully'); print(dir(connexion))"
python -c "import importlib.metadata; print(f'Connexion version: {importlib.metadata.version(\"connexion\")}')"
python -m pytest tests/test_quickstart.py -v 2>/dev/null || echo "Test file not found, checking other tests"
find tests -name "*.py" | head -10
python -m pytest tests/test_utils.py::test_camelcase -v 2>/dev/null || echo "Running any test" && python -m pytest tests/ -k "test_" --collect-only 2>/dev/null | head -20
connexion --help
ls examples/
cd examples/helloworld && python -c "
import connexion
app = connexion.AsyncApp(__name__)
print('Successfully created AsyncApp')
"
pre-commit --version
# cat .readthedocs.yaml
# ls -la .readthedocs*
