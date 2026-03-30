#!/bin/bash
# EnvBench generated install script
# Repository: dj-stripe/dj-stripe
# Revision: f271062a7662968385113df2482cd26a2ec69ac9

set -e

ls -la
cat pyproject.toml
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "Pipfile.lock" | head -20
find . -name "README*" -o -name "INSTALL*" -o -name "CONTRIBUTING*" | head -10
cat docs/README.md
cat docs/CONTRIBUTING.md | head -100
cat tox.ini
pyenv versions
python --version
ls -la djstripe/
cat manage.py
poetry --version
# poetry install --no-root
poetry install --no-root --no-interaction
source $(poetry env info --path)/bin/activate
which python && python --version
# python -c "import django; import stripe; print(f'Django version: {django.__version__}'); print(f'Stripe version: {stripe.__version__}')"
python -c "import django; import stripe; print(f'Django version: {django.__version__}'); print(f'Stripe version: {stripe._version.VERSION}')"
python -c "import djstripe; print('djstripe imported successfully')"
poetry install --with dev
poetry install --with docs
# python manage.py check
# poetry add psycopg2 --optional
head -50 tests/settings.py
# export DJSTRIPE_TEST_DB_VENDOR=sqlite && python manage.py check
# python -c "import stripe; print(dir(stripe))" | grep -i usage
python -c "import stripe; print([x for x in dir(stripe) if 'Usage' in x])"
# python -c "import stripe; print(stripe.__all__)"
python -c "import stripe; import inspect; print([m for m in dir(stripe) if not m.startswith('_')])"
grep -A2 -B2 "stripe" pyproject.toml
