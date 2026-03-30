#!/bin/bash
# EnvBench generated install script
# Repository: hips/autograd
# Revision: 9c756149ec3020286b21434023064226c9174b1a

set -e

ls -la
cat pyproject.toml
head -100 README.md
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "Pipfile.lock" -o -name "poetry.lock" | head -20
cat tox.ini
pyenv versions
python --version
pyenv global 3.11.7 && python --version
which python
conda info --envs
conda list python
conda create -n autograd-env python=3.11 -y
# conda activate autograd-env && python --version
conda init bash
source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && python --version
source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && pip install numpy six future
source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && pip install -e .
source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && pip install scipy
# source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && python -c "import autograd.numpy as np; from autograd import grad; print('Autograd imported successfully')"
source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && python -c "import numpy; print('NumPy version:', numpy.__version__)"
source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && pip install "numpy<2.0" --force-reinstall
source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && python -c "import autograd.numpy as np; from autograd import grad; print('Autograd imported successfully')"
source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && python -c "
import autograd.numpy as np
from autograd import grad

def tanh(x):
    y = np.exp(-2.0 * x)
    return (1.0 - y) / (1.0 + y)

grad_tanh = grad(tanh)
result = grad_tanh(1.0)
print('Gradient at x=1.0:', result)
print('Test passed!')
"
ls tests/
source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && python -m pytest tests/test_core.py -v -k "test_grad" | head -50
source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && pip install pytest coverage
# source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && python -m pytest tests/test_core.py::test_grad -v
grep -n "def test" tests/test_core.py | head -20
source /opt/conda/etc/profile.d/conda.sh && conda activate autograd-env && python -m pytest tests/test_core.py::test_add -v
ls -la conda_recipe/
