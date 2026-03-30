#!/bin/bash
# EnvBench generated install script
# Repository: lmcinnes/umap
# Revision: b45cece876513b3f95bd2dc7cb400240b1edab2a

set -e

ls -la
find . -name "requirements*.txt" -o -name "pyproject.toml" -o -name "setup.cfg" -o -name "Pipfile" -o -name "poetry.lock" | head -20
find . -type f \( -name "requirements*.txt" -o -name "pyproject.toml" -o -name "setup.cfg" -o -name "Pipfile" -o -name "poetry.lock" -o -name "environment.yml" \) 2>/dev/null
ls -la | grep -E "(txt|toml|cfg|yml|yaml|json)"
cat setup.py
head -100 README.rst
grep -i "python" setup.py
pyenv versions
python --version
pyenv global 3.12.0
python --version
which python
cat docs_requirements.txt
grep -A 20 -i "install" README.rst
pip --version
/root/.pyenv/versions/3.12.0/bin/python --version
apt-get update && apt-get install -y build-essential python3-dev 2>/dev/null | tail -20
/root/.pyenv/versions/3.12.0/bin/python -m pip install --upgrade pip
/root/.pyenv/versions/3.12.0/bin/python -m pip install -e .
/root/.pyenv/versions/3.12.0/bin/python -c "import umap; print('UMAP version:', umap.__version__); print('Import successful!')"
# /root/.pyenv/versions/3.12.0/bin/python -c "
# import umap
# import numpy as np
# print('Testing UMAP with simple data...')
# data = np.random.rand(100, 10)
# reducer = umap.UMAP()
# embedding = reducer.fit_transform(data)
# print(f'Embedding shape: {embedding.shape}')
# print('UMAP test completed successfully!')
# "
/root/.pyenv/versions/3.12.0/bin/python -c "import sklearn; print('scikit-learn version:', sklearn.__version__)"
find . -name "test*.py" -type f | head -10
grep -A 5 "install_requires" setup.py
grep -n "force_all_finite" umap/umap_.py | head -5
/root/.pyenv/versions/3.12.0/bin/python -c "import sklearn; from sklearn.utils.validation import check_array; import inspect; print('check_array signature:', inspect.signature(check_array))"
find . -name "*.txt" -o -name "*.cfg" -o -name "*.toml" -o -name "*.yml" -o -name "*.yaml" | xargs grep -l "scikit-learn\|sklearn" 2>/dev/null
cat umap_learn.egg-info/requires.txt
grep -r "force_all_finite" --include="*.py" .
# /root/.pyenv/versions/3.12.0/bin/python -m pip install 'scikit-learn<1.0' --force-reinstall
