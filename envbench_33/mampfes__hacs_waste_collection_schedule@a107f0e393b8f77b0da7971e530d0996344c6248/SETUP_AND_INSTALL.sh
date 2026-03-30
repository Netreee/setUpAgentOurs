#!/bin/bash
# EnvBench generated install script
# Repository: mampfes/hacs_waste_collection_schedule
# Revision: a107f0e393b8f77b0da7971e530d0996344c6248

set -e

ls -la
cat requirements.txt
find . -name "pyproject.toml" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "poetry.lock" | head -20
head -100 README.md
grep -i "python" README.md | head -20
find . -name "manifest.json" -type f | head -5
cat ./custom_components/waste_collection_schedule/manifest.json
python --version
pyenv versions
find . -name ".python-version" -o -name ".tool-versions" -o -name "runtime.txt" | head -10
ls -la custom_components/
ls -la custom_components/waste_collection_schedule/
find custom_components/waste_collection_schedule -name "*.py" -o -name "setup*" | head -20
ls -la tests/
find .github -name "*.yml" -o -name "*.yaml" | head -10
cat .github/workflows/hassfest.yaml
find . -name "*.yml" -o -name "*.yaml" | xargs grep -l "python" 2>/dev/null | head -10
cat .pre-commit-config.yaml
pip install -r requirements.txt
python -c "
import json
with open('custom_components/waste_collection_schedule/manifest.json') as f:
    data = json.load(f)
print('Requirements from manifest.json:', data.get('requirements', []))
"
find . -name "setup.py" -o -name "setup.cfg" -o -name "pyproject.toml"
python -c "import lxml; print('lxml imported successfully')"
python -c "
import sys
packages = ['icalendar', 'recurring_ical_events', 'icalevents', 'beautifulsoup4', 'lxml', 'DateTime', 'python_dateutil', 'pytz', 'yaml', 'requests', 'urllib3', 'jinja2']
for pkg in packages:
    try:
        if pkg == 'yaml':
            import yaml
        elif pkg == 'python_dateutil':
            import dateutil
        else:
            __import__(pkg)
        print(f'✓ {pkg} imported successfully')
    except ImportError as e:
        print(f'✗ {pkg} failed to import: {e}')
"
pip show beautifulsoup4
python -c "import bs4; print('bs4 imported successfully')"
grep -r "beautifulsoup4\|bs4" custom_components/ | head -5
cd custom_components/waste_collection_schedule && python -c "import waste_collection_schedule; print('Main component imported successfully')"
find . -name "*.md" -type f | xargs grep -l -i "install\|setup\|requirement" | head -10
# ls -la doc/
find . -type d -name "*doc*" | head -10
