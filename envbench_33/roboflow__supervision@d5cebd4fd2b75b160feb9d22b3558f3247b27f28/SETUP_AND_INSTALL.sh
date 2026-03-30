#!/bin/bash
# EnvBench generated install script
# Repository: roboflow/supervision
# Revision: d5cebd4fd2b75b160feb9d22b3558f3247b27f28

set -e

ls -la
head -100 README.md
cat pyproject.toml
pyenv versions
python --version
grep -i "install\|setup\|requirement" README.md | head -20
head -50 CONTRIBUTING.md
find . -name "*.md" -type f | xargs grep -l -i "install\|setup\|requirement" | head -10
ls -la docs/
find docs -name "*.md" -type f -exec grep -l "development\|install from source\|local install" {} \;
grep -i "install\|development\|source" docs/index.md | head -10
cat tox.ini
ls -la supervision/
poetry --version
poetry env info
# poetry install --no-root
# poetry install --no-dev
poetry install --help | head -30
# poetry install --without dev,docs
pyenv global 3.12.0 && python --version
which python
conda create -n supervision-env python=3.12 -y
# conda activate supervision-env && python --version
eval "$(conda shell.bash hook)" && conda activate supervision-env && python --version
pip install -e .
python -c "import supervision; print(f'Supervision version: {supervision.__version__}')"
pip install "supervision[desktop]"
pip install "supervision[assets]"
pip install pytest ruff mypy pre-commit notebook ipywidgets jupytext nbconvert
python -c "
import supervision as sv
import numpy as np

# Test basic imports
print('Testing supervision imports...')
print(f'Supervision version: {sv.__version__}')

# Test creating a simple detection
detections = sv.Detections(
    xyxy=np.array([[10, 20, 30, 40], [50, 60, 70, 80]]),
    confidence=np.array([0.9, 0.8]),
    class_id=np.array([0, 1])
)
print(f'Created detections with {len(detections)} objects')

# Test annotators
from supervision.annotators.base import BaseAnnotator
print(f'BaseAnnotator imported successfully')

print('All tests passed!')
"
