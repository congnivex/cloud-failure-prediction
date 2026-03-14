#!/usr/bin/env python
"""
Project verification script.
Checks that all required files are present and imports work correctly.
"""

import sys
from pathlib import Path

def main():
    """Verify project structure and dependencies."""
    
    print("=" * 70)
    print("CLOUD FAILURE PREDICTION PROJECT - VERIFICATION")
    print("=" * 70)
    
    project_root = Path(__file__).parent
    
    # Check folder structure
    print("\n📁 Checking folder structure...")
    
    required_dirs = [
        "src",
        "notebooks",
        "data",
        "data/raw",
        "data/processed",
        "experiments",
        "experiments/results",
        "experiments/figures",
        "experiments/logs",
    ]
    
    all_dirs_exist = True
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        status = "✅" if dir_path.exists() else "❌"
        print(f"  {status} {dir_name}")
        if not dir_path.exists():
            all_dirs_exist = False
    
    # Check required files
    print("\n📄 Checking required files...")
    
    required_files = [
        "run.py",
        "requirements.txt",
        "README.md",
        "QUICKSTART.md",
        "PROJECT_SUMMARY.md",
        "src/__init__.py",
        "src/utils.py",
        "src/data_loader.py",
        "src/preprocessing.py",
        "src/features.py",
        "src/context_engine.py",
        "src/models.py",
        "src/training.py",
        "src/evaluation.py",
        "notebooks/experiments.ipynb",
    ]
    
    all_files_exist = True
    for file_name in required_files:
        file_path = project_root / file_name
        status = "✅" if file_path.exists() else "❌"
        print(f"  {status} {file_name}")
        if not file_path.exists():
            all_files_exist = False
    
    # Check imports
    print("\n🐍 Checking Python imports...")
    
    sys.path.insert(0, str(project_root))
    
    imports_to_check = [
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("sklearn", "scikit-learn"),
        ("lightgbm", "lightgbm"),
        ("torch", "PyTorch"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("src.utils", "src.utils"),
        ("src.data_loader", "src.data_loader"),
        ("src.preprocessing", "src.preprocessing"),
        ("src.features", "src.features"),
        ("src.context_engine", "src.context_engine"),
        ("src.models", "src.models"),
        ("src.training", "src.training"),
        ("src.evaluation", "src.evaluation"),
    ]
    
    all_imports_work = True
    for import_path, display_name in imports_to_check:
        try:
            __import__(import_path)
            status = "✅"
        except ImportError as e:
            status = "❌"
            all_imports_work = False
        print(f"  {status} {display_name}")
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    if all_dirs_exist and all_files_exist and all_imports_work:
        print("\n✅ ALL CHECKS PASSED!")
        print("\nThe project is ready to run. To start:")
        print(f"\n  python {project_root / 'run.py'}")
        print("\nOr for interactive analysis:")
        print(f"\n  jupyter notebook {project_root / 'notebooks' / 'experiments.ipynb'}")
        return 0
    else:
        print("\n❌ SOME CHECKS FAILED")
        if not all_dirs_exist:
            print("  - Some directories are missing")
        if not all_files_exist:
            print("  - Some files are missing")
        if not all_imports_work:
            print("  - Some dependencies are not installed")
            print("\nTry: pip install -r requirements.txt")
        return 1
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
