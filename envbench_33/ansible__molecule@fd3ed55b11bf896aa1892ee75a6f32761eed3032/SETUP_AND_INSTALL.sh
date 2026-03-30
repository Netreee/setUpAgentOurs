#!/bin/bash
# EnvBench generated install script
# Repository: ansible/molecule
# Revision: fd3ed55b11bf896aa1892ee75a6f32761eed3032

set -e

ls -la
cat pyproject.toml
pyenv versions
pyenv global 3.10.13
python --version
which python
# conda deactivate && python --version
ls -la .config/
cat .config/requirements.in
head -50 README.md
grep -i "install\|setup\|requirement" README.md
cat tox.ini
ls -la src/
pip --version
/root/.pyenv/versions/3.10.13/bin/python --version
/root/.pyenv/versions/3.10.13/bin/python -m pip install -U pip setuptools
/root/.pyenv/versions/3.10.13/bin/python -m pip install -e .
/root/.pyenv/versions/3.10.13/bin/python -m pip install -e ".[test]"
# /root/.pyenv/versions/3.10.13/bin/python -m molecule --version
/root/.pyenv/versions/3.10.13/bin/python -c "import ansible; print(ansible.__version__)"
find /root/.pyenv/versions/3.10.13 -name "ansible-config" -type f
echo $PATH
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && which ansible-config
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && python -m molecule --version
export PATH="/root/.pyenv/versions/3.10.13/bin:$PATH" && molecule --version
cat .config/requirements-docs.txt
cat .config/requirements-testinfra.txt
find . -type f -name "*.md" -o -name "*.txt" -o -name "*.rst" | xargs grep -l "apt-get\|apt install\|yum\|dnf\|apk\|brew" 2>/dev/null | head -10
cat ./docs/installation.md
cat ./docs/ci.md
