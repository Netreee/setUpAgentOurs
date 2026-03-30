#!/bin/bash
# EnvBench generated install script
# Repository: huggingface/datasets
# Revision: a6ccf944e42c1a84de81bf326accab9999b86c90

set -e

ls -la
head -100 README.md
cat pyproject.toml
cat setup.py
cat additional-tests-requirements.txt
cat Makefile
ls -la src/
pyenv versions
python --version
find . -name "*.md" -type f | xargs grep -l "install\|requirement\|dependency" -i | head -10
cat docs/source/installation.md
apt-get update && apt-get install -y libsndfile1 ffmpeg
pip install --upgrade pip
pip install -e .
python -c "from datasets import load_dataset; print('Datasets library imported successfully')"
# pip install -e .[tests]
python -c "import datasets; print(f'Datasets version: {datasets.__version__}')"
python -c "
from datasets import load_dataset
# Try to load a small dataset
dataset = load_dataset('squad', split='train[:1]')
print(f'Dataset loaded successfully: {dataset}')
print(f'First example: {dataset[0]}')
"
cat additional-tests-requirements.txt
pip install soundfile>=0.12.1 librosa Pillow>=9.4.0
python -c "import soundfile, librosa, PIL; print('Audio and vision dependencies installed successfully')"
# python -c "
# # Test basic functionality
# from datasets import load_dataset, list_datasets, get_dataset_config_names
# print('1. Testing list_datasets()...')
# datasets = list_datasets()
# print(f'   Found {len(datasets)} datasets')
# print('2. Testing get_dataset_config_names()...')
# configs = get_dataset_config_names('squad')
# print(f'   SQuAD configs: {configs}')
# print('3. Testing load_dataset() with different splits...')
# dataset = load_dataset('squad', split='train[:2]')
# print(f'   Loaded dataset with {len(dataset)} examples')
# print('4. Testing dataset operations...')
# dataset = dataset.map(lambda x: {'context_length': len(x['context'])})
# print(f'   Added new column: context_length')
# print('✓ All tests passed!')
# "
python -c "
from datasets import load_dataset
import sys
print('Testing datasets library...')
try:
    dataset = load_dataset('squad', split='train[:1]')
    print(f'Successfully loaded dataset: {type(dataset).__name__}')
    print(f'Dataset features: {list(dataset.features.keys())}')
    print('✓ Datasets library is working correctly!')
    sys.exit(0)
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
"
datasets-cli --help 2>&1 | head -20
python --version && pip list | grep -E "(datasets|numpy|pandas|pyarrow|huggingface)" | head -10
ls -la src/datasets/__init__.py
grep "__version__" src/datasets/__init__.py
cat > test_installation.py << 'EOF'
#!/usr/bin/env python
"""Test script to verify datasets installation."""
import sys
import datasets

def test_import():
    print("Testing imports...")
    try:
        from datasets import load_dataset, Dataset, DatasetDict
        print("✓ Core imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_version():
    print(f"\nChecking version...")
    print(f"  datasets version: {datasets.__version__}")
    return True

def test_basic_functionality():
    print("\nTesting basic functionality...")
    try:
        # Create a simple dataset
        data = {"text": ["Hello", "World"], "label": [0, 1]}
        dataset = datasets.Dataset.from_dict(data)
        print(f"✓ Created dataset with {len(dataset)} examples")
        
        # Test map operation
        dataset = dataset.map(lambda x: {"text_length": len(x["text"])})
        print(f"✓ Applied map operation")
        
        return True
    except Exception as e:
        print(f"✗ Error in basic functionality: {e}")
        return False

def main():
    print("=" * 60)
    print("Testing HuggingFace Datasets Installation")
    print("=" * 60)
    
    tests = [
        test_import,
        test_version,
        test_basic_functionality,
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed! Installation is complete.")
        sys.exit(0)
    else:
        print("✗ Some tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF
python test_installation.py
rm test_installation.py
