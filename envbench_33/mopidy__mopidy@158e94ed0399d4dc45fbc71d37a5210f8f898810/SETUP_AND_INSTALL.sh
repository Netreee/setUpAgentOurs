#!/bin/bash
# EnvBench generated install script
# Repository: mopidy/mopidy
# Revision: 158e94ed0399d4dc45fbc71d37a5210f8f898810

set -e

ls -la
cat pyproject.toml
cat README.rst
ls -la src/
pyenv versions
pyenv global 3.11.7
python --version
which python
echo $PATH
/root/.pyenv/versions/3.11.7/bin/python --version
cat tox.ini
find docs -name "*.rst" -o -name "*.md" | head -20
cat docs/installation/index.rst
cat docs/installation/debian.rst
cat docs/installation/pypi.rst
apt-get update && apt-get install -y \
    gir1.2-gst-plugins-base-1.0 \
    gir1.2-gstreamer-1.0 \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-tools \
    libcairo2-dev \
    libgirepository1.0-dev \
    python3-gst-1.0 \
    build-essential \
    python3-dev \
    python3-pip
/root/.pyenv/versions/3.11.7/bin/python --version
/root/.pyenv/versions/3.11.7/bin/python -m pip install --upgrade pip setuptools wheel
# /root/.pyenv/versions/3.11.7/bin/python -m pip install -e .[dev]
# apt-get install -y libgirepository1.0-dev gobject-introspection libgirepository-2.0-dev
dpkg -l | grep -i gobject
apt-get install -y python3-gi python3-gi-cairo
python3 --version
/usr/bin/python3 --version
apt-cache search pygobject
/root/.pyenv/versions/3.11.7/bin/python -m venv /tmp/mopidy-venv
source /tmp/mopidy-venv/bin/activate && python --version
source /tmp/mopidy-venv/bin/activate && pip install --upgrade pip setuptools wheel
source /tmp/mopidy-venv/bin/activate && pip install pykka>=4.0 requests>=2.28 setuptools>=66 tornado>=6.2
# source /tmp/mopidy-venv/bin/activate && pip install pygobject
