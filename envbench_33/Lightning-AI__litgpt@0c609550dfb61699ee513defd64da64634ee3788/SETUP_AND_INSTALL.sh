#!/bin/bash
# EnvBench generated install script
# Repository: Lightning-AI/litgpt
# Revision: 0c609550dfb61699ee513defd64da64634ee3788

set -e

ls -la
cat pyproject.toml
head -100 README.md
grep -n -i "install\|quick start\|setup\|requirement" README.md | head -20
sed -n '109,140p' README.md
grep -i "python" pyproject.toml
pyenv versions
python --version
pyenv global 3.10.13
python --version
which python
/root/.pyenv/versions/3.10.13/bin/python --version
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "poetry.lock" | head -20
find . -name ".*" -type f | grep -E "(python|version|env)" | head -10
ls -la .github/
ls -la .github/workflows/
cat .github/workflows/cpu-tests.yml
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && python --version
pip install -e '.[all]'
python -c "import litgpt; print('litgpt imported successfully')"
litgpt --help
pip install '.[test]'
python -c "import litgpt; import pytest; print('litgpt and pytest imported successfully')"
find . -type f -name "*.md" -o -name "*.txt" -o -name "*.rst" | xargs grep -l -i "apt\|apt-get\|yum\|dnf\|brew\|system\|install" | head -10
grep -i "apt\|apt-get\|system" ./README.md
head -50 ./tutorials/0_to_litgpt.md
grep -r -i "cuda\|gpu\|torch" pyproject.toml README.md | head -10
# python -c "
# import torch
# import litgpt
# print(f'PyTorch version: {torch.__version__}')
# print(f'LitGPT version: {litgpt.__version__}')
# print('All imports successful!')
# "
python -c "
import pkg_resources
version = pkg_resources.get_distribution('litgpt').version
print(f'LitGPT version: {version}')
print('Installation successful!')
"
cd /data/project && python -m pytest tests/test_config.py -v -k "test_" | head -50
