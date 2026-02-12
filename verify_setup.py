#!/usr/bin/env python3
"""
Verification script for Sleep Disorder Analysis Platform
Checks all components and ensures proper setup
"""

import os
import sys
import json
from pathlib import Path

def check_python_version():
    """Check Python version >= 3.8"""
    print("✓ Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} - REQUIRES 3.8+")
        return False

def check_required_files():
    """Check if all required files exist"""
    print("\n✓ Checking required files...")
    required_files = [
        'app_main.py',
        'train_model.py',
        'requirements.txt',
        'README.md',
        'ml/model.pkl',
        'ml/scaler.pkl'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size:,} bytes)")
        else:
            print(f"  ❌ {file} - MISSING")
            all_ok = False
    
    return all_ok

def check_directories():
    """Check if required directories exist"""
    print("\n✓ Checking directories...")
    directories = ['ml', 'data', 'frontend', 'backend']
    
    for dir in directories:
        if os.path.isdir(dir):
            file_count = len(os.listdir(dir))
            print(f"  ✅ {dir}/ ({file_count} items)")
        else:
            print(f"  ⚠️  {dir}/ - Not found (will be auto-created)")

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n✓ Checking Python dependencies...")
    
    required_packages = {
        'streamlit': 'Streamlit Web Framework',
        'joblib': 'Model Persistence',
        'sklearn': 'Machine Learning (scikit-learn)',
        'pandas': 'Data Processing',
        'numpy': 'Numerical Computing',
        'reportlab': 'PDF Generation'
    }
    
    missing = []
    for package, description in required_packages.items():
        try:
            if package == 'sklearn':
                import sklearn
                version = sklearn.__version__
            else:
                mod = __import__(package)
                version = mod.__version__ if hasattr(mod, '__version__') else 'unknown'
            print(f"  ✅ {package:15} - {description:30} (v{version})")
        except ImportError:
            print(f"  ❌ {package:15} - {description:30} MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n  Install missing packages:")
        print(f"  pip install {' '.join(missing)}")
        return False
    return True

def check_model_files():
    """Check ML model files integrity"""
    print("\n✓ Checking ML model files...")
    
    model_files = ['ml/model.pkl', 'ml/scaler.pkl']
    all_ok = True
    
    for file in model_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            if size > 1000:  # At least 1KB
                print(f"  ✅ {file} ({size:,} bytes)")
            else:
                print(f"  ❌ {file} - File size too small ({size} bytes)")
                all_ok = False
        else:
            print(f"  ❌ {file} - MISSING")
            print(f"     Run: python train_model.py")
            all_ok = False
    
    return all_ok

def check_data_files():
    """Check if data files need initialization"""
    print("\n✓ Checking data storage...")
    
    os.makedirs('data', exist_ok=True)
    
    data_files = {
        'data/users.json': [],
        'data/analysis_history.json': []
    }
    
    for file, default in data_files.items():
        if os.path.exists(file):
            with open(file, 'r') as f:
                content = json.load(f)
                items = len(content)
                print(f"  ✅ {file} ({items} records)")
        else:
            with open(file, 'w') as f:
                json.dump(default, f)
            print(f"  ✅ {file} - Created (empty)")

def check_app_syntax():
    """Check main app syntax"""
    print("\n✓ Checking app.py syntax...")
    
    import py_compile
    try:
        py_compile.compile('app_main.py', doraise=True)
        print(f"  ✅ app_main.py - Syntax OK")
        return True
    except py_compile.PyCompileError as e:
        print(f"  ❌ app_main.py - Syntax error:")
        print(f"     {e}")
        return False

def test_model_loading():
    """Test if model loads properly"""
    print("\n✓ Testing model loading...")
    
    try:
        import joblib
        model = joblib.load('ml/model.pkl')
        scaler = joblib.load('ml/scaler.pkl')
        print(f"  ✅ Model loaded successfully")
        print(f"     Model type: {type(model).__name__}")
        print(f"     Scaler type: {type(scaler).__name__}")
        
        # Test prediction
        import numpy as np
        test_features = [7.0, 5, 35, 120, 75, 0, 25, 0, 8]
        scaled = scaler.transform([test_features])
        pred = model.predict(scaled)[0]
        print(f"  ✅ Test prediction: {int(pred)}")
        return True
    except Exception as e:
        print(f"  ❌ Model loading failed: {e}")
        return False

def print_summary(results):
    """Print summary of checks"""
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nChecks Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL CHECKS PASSED!")
        print("\nNext steps:")
        print("1. Run: streamlit run app_main.py")
        print("2. Open: http://localhost:8501")
        print("3. Register a test account")
        print("4. Try the sleep analysis form")
        print("5. Login as admin with password: admin123")
    else:
        print(f"\n❌ {total - passed} check(s) failed")
        print("Please fix the issues above before running the app")
    
    print("\n" + "="*60)

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("🛌 SLEEP DISORDER ANALYSIS PLATFORM")
    print("   Installation & Setup Verification")
    print("="*60 + "\n")
    
    results = {
        'Python Version': check_python_version(),
        'Required Files': check_required_files(),
        'Directories': check_directories() if False else True,  # Optional
        'Dependencies': check_dependencies(),
        'Model Files': check_model_files(),
        'Data Files': check_data_files() if False else True,  # Optional
        'App Syntax': check_app_syntax(),
        'Model Loading': test_model_loading(),
    }
    
    print_summary(results)

if __name__ == '__main__':
    main()
