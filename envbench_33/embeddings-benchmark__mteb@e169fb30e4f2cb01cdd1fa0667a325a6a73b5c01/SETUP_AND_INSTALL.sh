#!/bin/bash
# EnvBench generated install script
# Repository: embeddings-benchmark/mteb
# Revision: e169fb30e4f2cb01cdd1fa0667a325a6a73b5c01

set -e

ls -la
cat README.md | head -100
cat pyproject.toml
find . -name "requirements*.txt" -o -name "setup.py" -o -name "setup.cfg" -o -name "Pipfile" -o -name "Pipfile.lock" -o -name "poetry.lock" | head -20
pyenv versions
python --version
ls -la mteb/
cat CONTRIBUTING.md | head -50
cat Makefile
ls -la scripts/
grep -r "cuda\|gpu\|torch\|cudnn" . --include="*.py" --include="*.md" --include="*.txt" --include="*.toml" | head -20
pip install --upgrade pip
pip install -e ".[dev]"
# python -c "import mteb; print('MTEB version:', mteb.__version__)"
pip install ".[speedtask]"
python -c "import mteb; print('MTEB version:', mteb.__version__)"
python -c "from mteb import get_tasks; tasks = get_tasks(tasks=['Banking77Classification']); print(f'Found {len(tasks)} task(s)')"
mteb --help
mteb available_tasks --help
grep -r "codecarbon" . --include="*.py" | head -5
grep -r "apt\|apt-get\|yum\|dnf\|brew\|apk\|system\|install" . --include="*.md" --include="*.txt" --include="*.rst" | grep -i "package\|dependency\|install" | head -10
python -m pytest tests/ -xvs -k "test_" --tb=short 2>&1 | head -100
python -c "
import mteb
from sentence_transformers import SentenceTransformer

# Define the sentence-transformers model name
model_name = 'average_word_embeddings_komninos'
# or directly from huggingface:
# model_name = 'sentence-transformers/all-MiniLM-L6-v2'

model = SentenceTransformer(model_name)
tasks = mteb.get_tasks(tasks=['Banking77Classification'])
evaluation = mteb.MTEB(tasks=tasks)
print('MTEB evaluation object created successfully')
print(f'Number of tasks: {len(tasks)}')
"
python -c "import sys; print(f'Python version: {sys.version}'); import torch; print(f'PyTorch version: {torch.__version__}'); import sentence_transformers; print(f'Sentence Transformers version: {sentence_transformers.__version__}')"
python -c "
import importlib
deps = ['datasets', 'numpy', 'requests', 'scikit_learn', 'scipy', 'sentence_transformers', 'torch', 'tqdm', 'rich', 'pytrec_eval_terrier', 'pydantic', 'typing_extensions', 'eval_type_backport', 'polars']
for dep in deps:
    try:
        importlib.import_module(dep.replace('-', '_'))
        print(f'✓ {dep}')
    except ImportError as e:
        print(f'✗ {dep}: {e}')
"
python -c "
import importlib
# Try different import names
modules_to_try = [
    ('scikit_learn', 'sklearn'),
    ('pytrec_eval_terrier', 'pytrec_eval')
]
for orig_name, alt_name in modules_to_try:
    try:
        importlib.import_module(alt_name)
        print(f'✓ {orig_name} (imported as {alt_name})')
    except ImportError:
        print(f'✗ {orig_name} (tried as {alt_name})')
"
python -c "
# Test all imports with correct module names
import datasets
import numpy as np
import requests
import sklearn
import scipy
import sentence_transformers
import torch
import tqdm
import rich
import pytrec_eval
import pydantic
import typing_extensions
import eval_type_backport
import polars
print('All main dependencies imported successfully!')
print(f'numpy version: {np.__version__}')
print(f'scikit-learn version: {sklearn.__version__}')
print(f'torch version: {torch.__version__}')
"
make install 2>&1 | tail -5
cat > test_mteb_installation.py << 'EOF'
#!/usr/bin/env python
"""Test script to verify MTEB installation"""
import mteb
import sys

def test_installation():
    print("Testing MTEB installation...")
    
    # Test 1: Check version
    print(f"1. MTEB version: {mteb.__version__}")
    
    # Test 2: Get available tasks
    tasks = mteb.get_tasks(tasks=['Banking77Classification'])
    print(f"2. Retrieved {len(tasks)} task(s)")
    
    # Test 3: Check task metadata
    if tasks:
        task = tasks[0]
        print(f"3. Task name: {task.description['name']}")
        print(f"4. Task type: {task.description['type']}")
        print(f"5. Task category: {task.description['category']}")
    
    # Test 4: Import key modules
    from mteb.evaluation import MTEB
    print("6. Successfully imported MTEB evaluation module")
    
    # Test 5: Create evaluation object
    evaluation = MTEB(tasks=tasks)
    print("7. Created MTEB evaluation object")
    
    print("\n✅ All tests passed! MTEB is properly installed.")
    return True

if __name__ == "__main__":
    try:
        success = test_installation()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)
EOF
# python test_mteb_installation.py
