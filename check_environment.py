#!/usr/bin/env python3
"""
Environment check script for the Bhagavad Gita Chatbot.
This script verifies that all required packages are installed and accessible.
"""

import sys
import importlib
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    else:
        print("✅ Python version is compatible")
        return True

def check_package(package_name, import_name=None):
    """Check if a package is installed and importable."""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {package_name}: {version}")
        return True
    except ImportError as e:
        print(f"❌ {package_name}: Not installed ({e})")
        return False

def check_pip_packages():
    """Check all required packages using pip list."""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            installed_packages = result.stdout.lower()
            return installed_packages
        else:
            print("❌ Could not check pip packages")
            return ""
    except Exception as e:
        print(f"❌ Error checking pip packages: {e}")
        return ""

def main():
    """Main environment check."""
    print("🔍 Bhagavad Gita Chatbot - Environment Check")
    print("=" * 50)
    
    # Check Python version
    python_ok = check_python_version()
    print()
    
    # Check required packages
    print("Checking required packages:")
    print("-" * 30)
    
    required_packages = [
        ("streamlit", "streamlit"),
        ("datasets", "datasets"),
        ("sentence-transformers", "sentence_transformers"),
        ("faiss-cpu", "faiss"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("scikit-learn", "sklearn"),
        ("torch", "torch"),
        ("transformers", "transformers"),
    ]
    
    optional_packages = [
        ("google-generativeai", "google.generativeai"),
        ("openai", "openai"),
    ]
    
    all_ok = True
    
    for package_name, import_name in required_packages:
        if not check_package(package_name, import_name):
            all_ok = False
    
    print("\nChecking optional packages:")
    print("-" * 30)
    
    for package_name, import_name in optional_packages:
        check_package(package_name, import_name)
    
    print("\n" + "=" * 50)
    
    if all_ok:
        print("✅ All required packages are installed!")
        print("\nNext steps:")
        print("1. Run: python quick_test.py")
        print("2. Run: streamlit run app.py")
    else:
        print("❌ Some required packages are missing!")
        print("\nTo install missing packages:")
        print("pip install -r requirements.txt")
    
    # Show Python path info
    print(f"\nPython executable: {sys.executable}")
    print(f"Python path: {sys.path[0]}")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in a virtual environment")
    else:
        print("⚠️  Not running in a virtual environment (this is OK)")

if __name__ == "__main__":
    main()
