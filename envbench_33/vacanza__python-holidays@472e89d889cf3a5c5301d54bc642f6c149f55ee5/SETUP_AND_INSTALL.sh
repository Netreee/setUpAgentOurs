#!/bin/bash
# EnvBench generated install script
# Repository: vacanza/python-holidays
# Revision: 472e89d889cf3a5c5301d54bc642f6c149f55ee5

set -e

ls -la
cat pyproject.toml
cat setup.py
ls -la requirements/
cat requirements/runtime.txt
cat requirements/dev.txt
cat requirements/tests.txt
cat requirements/docs.txt
head -100 README.rst
cat Makefile
pyenv versions
make setup
pip install -e .
python -c "import holidays; print('holidays version:', holidays.__version__); us_holidays = holidays.US(); print('Is 2024-12-25 a US holiday?', '2024-12-25' in us_holidays)"
python -m pytest tests/test_holidays.py -xvs -k "test_US" 2>&1 | head -50
ls -la tests/
python -m pytest tests/test_imports.py -xvs
cat .pre-commit-config.yaml
cat tox.ini
python --version
cat .readthedocs.yaml
python -c "
import holidays
import sys
print('Python version:', sys.version)
print('Holidays version:', holidays.__version__)
print('Available countries:', len(holidays.list_supported_countries()))
print('Testing a few countries:')
for country in ['US', 'CA', 'GB', 'AU', 'IN']:
    try:
        h = getattr(holidays, country)()
        print(f'  {country}: {len(h)} holidays in 2024')
    except Exception as e:
        print(f'  {country}: Error - {e}')
"
python -c "
import holidays
us = holidays.US(years=2024)
print(f'US holidays in 2024: {len(us)}')
print('Sample holidays:')
for date, name in sorted(us.items())[:5]:
    print(f'  {date}: {name}')
"
make test 2>&1 | tail -20
ls -la scripts/
which python
python -c "
import sys
try:
    import pre_commit
    import ruff
    import tox
    import pytest
    import coverage
    import sphinx
    import convertdate
    import hijridate
    import build
    import git
    from github import Github
    print('All development dependencies imported successfully!')
except ImportError as e:
    print(f'Import error: {e}')
    sys.exit(1)
"
python -c "import dateutil; print('python-dateutil version:', dateutil.__version__)"
# cat > test_holidays_demo.py << 'EOF'
# #!/usr/bin/env python
# """Demo script to show holidays package is working."""
# import holidays

# def main():
#     print("=== Holidays Package Demo ===")
#     print(f"Package version: {holidays.__version__}")
#     print(f"Python version: {holidays.__python_version__}")
    
#     # Test US holidays
#     us_holidays = holidays.US(years=2024)
#     print(f"\nUS Holidays in 2024 ({len(us_holidays)} total):")
#     for date, name in sorted(us_holidays.items()):
#         print(f"  {date}: {name}")
    
#     # Test Canada holidays
#     ca_holidays = holidays.CA(years=2024)
#     print(f"\nCanada Holidays in 2024 ({len(ca_holidays)} total):")
#     for date, name in sorted(ca_holidays.items()):
#         print(f"  {date}: {name}")
    
#     # Check if specific dates are holidays
#     test_dates = ["2024-12-25", "2024-07-04", "2024-01-01"]
#     print("\nChecking specific dates in US:")
#     for date_str in test_dates:
#         is_holiday = date_str in us_holidays
#         print(f"  {date_str}: {'HOLIDAY' if is_holiday else 'Not a holiday'}")

# if __name__ == "__main__":
#     main()
# EOF
# python test_holidays_demo.py
cat > test_holidays_demo.py << 'EOF'
#!/usr/bin/env python
"""Demo script to show holidays package is working."""
import holidays
import sys

def main():
    print("=== Holidays Package Demo ===")
    print(f"Package version: {holidays.__version__}")
    print(f"Python version: {sys.version.split()[0]}")
    
    # Test US holidays
    us_holidays = holidays.US(years=2024)
    print(f"\nUS Holidays in 2024 ({len(us_holidays)} total):")
    for date, name in sorted(us_holidays.items()):
        print(f"  {date}: {name}")
    
    # Test Canada holidays
    ca_holidays = holidays.CA(years=2024)
    print(f"\nCanada Holidays in 2024 ({len(ca_holidays)} total):")
    for date, name in sorted(ca_holidays.items()):
        print(f"  {date}: {name}")
    
    # Check if specific dates are holidays
    test_dates = ["2024-12-25", "2024-07-04", "2024-01-01"]
    print("\nChecking specific dates in US:")
    for date_str in test_dates:
        is_holiday = date_str in us_holidays
        print(f"  {date_str}: {'HOLIDAY' if is_holiday else 'Not a holiday'}")

if __name__ == "__main__":
    main()
EOF
python test_holidays_demo.py
