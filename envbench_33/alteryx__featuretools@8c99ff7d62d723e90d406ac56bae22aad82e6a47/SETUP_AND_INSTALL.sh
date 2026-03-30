#!/bin/bash
# EnvBench generated install script
# Repository: alteryx/featuretools
# Revision: 8c99ff7d62d723e90d406ac56bae22aad82e6a47

set -e

ls -la
head -50 README.md
cat pyproject.toml
pyenv versions
python --version
cat Makefile
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "Pipfile.lock" | head -20
ls -la featuretools/
grep -i "install\|dependency\|requirement\|system" README.md | head -30
head -100 contributing.md
# which dot && which pandoc
apt-cache policy graphviz pandoc
apt-get update && apt-get install -y graphviz pandoc
which dot && which pandoc && dot -V && pandoc --version | head -5
make installdeps
python -c "import featuretools; print(f'Featuretools version: {featuretools.__version__}')"
python -c "import featuretools as ft; import pandas as pd; import numpy as np; print('All imports successful')"
make installdeps-dev
# python -c "import featuretools as ft; print(f'Featuretools version: {ft.__version__}'); import black; print(f'Black version: {black.__version__}'); import ruff; print(f'Ruff version: {ruff.__version__}')"
python -c "import featuretools as ft; print(f'Featuretools version: {ft.__version__}'); import black; print(f'Black version: {black.__version__}'); import ruff; print('Ruff imported successfully')"
# cd /data/project && python -c "
# import featuretools as ft
# import pandas as pd
# import numpy as np

# # Create a mock dataset
# data = pd.DataFrame({
#     'id': [1, 2, 3, 4, 5],
#     'value': [10, 20, 30, 40, 50],
#     'time': pd.date_range('2023-01-01', periods=5, freq='D')
# })

# # Create an entityset
# es = ft.EntitySet()
# es = es.add_dataframe(
#     dataframe_name='data',
#     dataframe=data,
#     index='id',
#     time_index='time'
# )

# print('EntitySet created successfully')
# print(f'Number of dataframes: {len(es.dataframes)}')
# print(f'Dataframe shape: {es[\"data\"].shape}')
# "
python -c "import woodwork as ww; print(f'Woodwork version: {ww.__version__}')"
# cd /data/project && python -c "
# import featuretools as ft
# import pandas as pd
# import numpy as np

# # Create a mock dataset
# data = pd.DataFrame({
#     'id': [1, 2, 3, 4, 5],
#     'value': [10, 20, 30, 40, 50],
#     'time': pd.date_range('2023-01-01', periods=5, freq='D')
# })

# # Initialize woodwork for the dataframe
# data.ww.init(index='id', time_index='time')

# # Create an entityset
# es = ft.EntitySet()
# es = es.add_dataframe(
#     dataframe_name='data',
#     dataframe=data
# )

# print('EntitySet created successfully')
# print(f'Number of dataframes: {len(es.dataframes)}')
# print(f'Dataframe shape: {es[\"data\"].shape}')
# "
pwd && ls -la
cd alteryx__featuretools@8c99ff7d62d723e90d406ac56bae22aad82e6a47 && python -c "
import featuretools as ft
print(f'Featuretools successfully imported. Version: {ft.__version__}')

# Try a simpler test without woodwork issues
from featuretools import list_primitives
primitives = list_primitives()
print(f'Number of available primitives: {len(primitives)}')
print('Installation successful!')
"
# cd alteryx__featuretools@8c99ff7d62d723e90d406ac56bae22aad82e6a47 && make lint 2>&1 | head -50
ls -la
python -c "
import sys
print(f'Python version: {sys.version}')

import featuretools as ft
print(f'Featuretools version: {ft.__version__}')

import pandas as pd
print(f'Pandas version: {pd.__version__}')

import numpy as np
print(f'Numpy version: {np.__version__}')

import woodwork as ww
print(f'Woodwork version: {ww.__version__}')

# Test basic functionality
from featuretools import list_primitives
primitives = list_primitives()
print(f'Number of available primitives: {len(primitives)}')

print('\\nAll core dependencies installed successfully!')
"
# python -c "
# import pytest
# print(f'Pytest version: {pytest.__version__}')

# import pytest_cov
# print('Pytest-cov imported successfully')

# import pytest_xdist
# print('Pytest-xdist imported successfully')

# print('\\nTest dependencies installed successfully!')
# "
python -c "import pkg_resources; dists = [d for d in pkg_resources.working_set if 'pytest' in d.key]; [print(f'{d.key}=={d.version}') for d in dists]"
