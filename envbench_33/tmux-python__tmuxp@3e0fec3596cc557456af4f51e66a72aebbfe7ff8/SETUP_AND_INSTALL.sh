#!/bin/bash
# EnvBench generated install script
# Repository: tmux-python/tmuxp
# Revision: 3e0fec3596cc557456af4f51e66a72aebbfe7ff8

set -e

ls -la
cat .python-version
cat .tool-versions
pyenv versions
head -50 README.md
grep -A 20 -B 5 "Development\|Installation\|Contributing\|Setup" README.md
grep -n "Development\|Contributing\|Setup\|Getting Started" README.md
cat Makefile
cat pyproject.toml
ls -la src/
# which tmux
find . -name "*.md" -o -name "*.txt" -o -name "*.rst" | xargs grep -l "apt-get\|apt install\|yum\|dnf\|brew\|system.*depend\|require.*tmux" 2>/dev/null | head -10
grep -i "install\|depend\|require" ./docs/quickstart.md | head -20
find . -name "CONTRIBUTING*" -o -name "DEVELOPMENT*" -o -name "HACKING*"
ls -la .github/
cat .github/contributing.md
tail -100 README.md
find docs -name "*.md" -o -name "*.rst" | xargs grep -l "development\|setup\|install.*from.*source\|contribut" 2>/dev/null
cat docs/developing.md
grep -r "tmux" docs/developing.md | head -5
cat .github/workflows/tests.yml
python --version
pyenv versions | grep 3.12
grep "python" pyproject.toml | head -5
pyenv global 3.12.0
python --version
which python
conda create -n tmuxp-env python=3.12 -y
# conda activate tmuxp-env
conda init bash
