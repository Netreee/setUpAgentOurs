#!/bin/bash
# EnvBench generated install script
# Repository: platformio/platformio-core
# Revision: 7cf8d1d6961761eab681d49eea7fbafae0889186

set -e

ls -la
find . -name "requirements*.txt" -o -name "pyproject.toml" -o -name "setup.cfg" -o -name "Pipfile" -o -name "poetry.lock" | head -20
head -50 README.rst
cat setup.py
find . -name "dependencies.py" -type f | head -5
cat platformio/dependencies.py
python --version
pyenv versions
find . -name "*.md" -o -name "*.txt" -o -name "*.rst" | xargs grep -l -i "install\|requirement\|depend" | head -10
cat CONTRIBUTING.md
cat tox.ini
cat Makefile
ls -la platformio/
grep -r "apt-get\|apt install\|yum\|dnf\|apk\|brew" . --include="*.md" --include="*.rst" --include="*.txt" --include="*.py" | head -10
grep -B5 -A5 "brew update" ./platformio/maintenance.py
ls -la platformio/assets/system/
pip install tox
grep -r "gcc\|g++\|clang\|make\|cmake\|compiler" . --include="*.py" --include="*.md" --include="*.rst" | head -10
pip install -e .
python -c "import platformio; print(f'PlatformIO version: {platformio.__version__}')"
pio --version
pip install black isort pylint pytest pytest-xdist jsondiff
find . -type f -name "*.py" -exec grep -l "subprocess\|Popen\|check_call\|run" {} \; | xargs grep -l "apt\|apt-get\|yum\|dnf\|apk\|brew\|pacman" | head -5
grep -n "apt\|apt-get\|yum\|dnf\|apk\|brew\|pacman" ./platformio/proc.py ./platformio/maintenance.py ./platformio/project/options.py ./platformio/debug/cli.py
pio system info
ls -la scripts/
head -50 scripts/install_devplatforms.py
# which gcc g++ make cmake
apt-get update && apt-get install -y cmake
python -m pytest tests/ -xvs -k "test_version" 2>&1 | head -50
