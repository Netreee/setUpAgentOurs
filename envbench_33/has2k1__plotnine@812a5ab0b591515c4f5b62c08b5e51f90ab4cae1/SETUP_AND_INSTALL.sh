#!/bin/bash
# EnvBench generated install script
# Repository: has2k1/plotnine
# Revision: 812a5ab0b591515c4f5b62c08b5e51f90ab4cae1

set -e

ls -la
head -50 README.md
cat pyproject.toml
pyenv versions
python --version
cat Makefile
ls -la requirements/
cat requirements/doc.txt
ls -la .github/
ls -la .github/workflows/
head -50 .github/workflows/testing.yml
pyenv global 3.10.13
python --version
which python
/root/.pyenv/versions/3.10.13/bin/python --version
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && python --version
# export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && pip install -e ".[all]"
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && apt-get update && apt-get install -y gfortran
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && pip install ".[extra]"
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && python -c "import plotnine; print('plotnine version:', plotnine.__version__)"
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && python -c "from plotnine import ggplot, aes, geom_point; from plotnine.data import mtcars; print('Import successful')"
cat .pre-commit-config.yaml
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && pip install ".[test]"
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && python -m pytest tests/test_ggplot.py -xvs -k "test_ggplot" 2>&1 | head -50
find tests -name "*.py" | head -20
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && python -c "import pytest; print('pytest version:', pytest.__version__)"
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && pip install -e .
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && cat > test_plotnine.py << 'EOF'
from plotnine import ggplot, aes, geom_point
from plotnine.data import mtcars

# Create a simple plot
p = ggplot(mtcars, aes('wt', 'mpg')) + geom_point()
print("Plot created successfully!")
print(f"Plot object type: {type(p)}")

# Test some imports
from plotnine import theme_bw, labs
print("Additional imports successful!")

# Check version
import plotnine
print(f"plotnine version: {plotnine.__version__}")
EOF
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && python test_plotnine.py
echo "export PATH=\"/root/.pyenv/versions/3.10.13/bin:\$PATH\"" >> ~/.bashrc
