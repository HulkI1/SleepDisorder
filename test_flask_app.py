#!/usr/bin/env python3
"""
Flask Application Validation Script
Tests that the Flask application starts and routes work correctly
"""

import os
import sys
import json
import time
import threading
import requests
from pathlib import Path

sys.path.insert(0, '/workspaces/SleepDisorder')

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ {text}{RESET}")

def test_imports():
    """Test that all required modules can be imported"""
    print_header("Testing Module Imports")
    
    modules = {
        'Flask': 'flask',
        'Flask-Session': 'flask_session',
        'scikit-learn': 'sklearn',
        'joblib': 'joblib',
        'reportlab': 'reportlab',
        'pandas': 'pandas',
        'numpy': 'numpy'
    }
    
    all_good = True
    for name, module in modules.items():
        try:
            __import__(module)
            print_success(f"{name} is installed")
        except ImportError as e:
            print_error(f"{name} import failed: {e}")
            all_good = False
    
    return all_good

def test_data_structure():
    """Test that data directories and files exist or can be created"""
    print_header("Testing Data Structure")
    
    paths_to_check = [
        '/workspaces/SleepDisorder/data',
        '/workspaces/SleepDisorder/ml',
        '/workspaces/SleepDisorder/templates',
        '/workspaces/SleepDisorder/ml/model.pkl',
        '/workspaces/SleepDisorder/ml/scaler.pkl'
    ]
    
    all_good = True
    for path in paths_to_check:
        if os.path.exists(path):
            if os.path.isdir(path):
                print_success(f"Directory exists: {path}")
            else:
                print_success(f"File exists: {path}")
        else:
            print_warning(f"Missing: {path}")
    
    # Check templates
    templates = ['dashboard.html', 'login.html', 'register.html', 
                 'admin_login.html', 'admin_dashboard.html', '404.html', '500.html']
    
    print_info("\nTemplate files:")
    for template in templates:
        template_path = f'/workspaces/SleepDisorder/templates/{template}'
        if os.path.exists(template_path):
            print_success(f"Template: {template}")
        else:
            print_error(f"Missing template: {template}")
            all_good = False
    
    return all_good

def test_flask_app():
    """Test that Flask app can be imported and initialized"""
    print_header("Testing Flask Application")
    
    try:
        import flask_app
        print_success("Flask app imported successfully")
        
        app = flask_app.app
        print_success(f"Flask app instance created: {app.name}")
        
        # Test routes
        routes = list(app.url_map.iter_rules())
        print_success(f"Found {len(routes)} registered routes")
        
        # Check critical routes
        critical_routes = [
            '/register',
            '/login',
            '/dashboard',
            '/predict',
            '/admin-login',
            '/admin-dashboard'
        ]
        
        route_paths = [str(rule.rule) for rule in routes]
        all_good = True
        
        for route in critical_routes:
            if route in route_paths:
                print_success(f"Critical route exists: {route}")
            else:
                print_error(f"Missing critical route: {route}")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print_error(f"Flask app test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ml_models():
    """Test that ML models can be loaded"""
    print_header("Testing ML Models")
    
    try:
        import joblib
        
        model_path = '/workspaces/SleepDisorder/ml/model.pkl'
        scaler_path = '/workspaces/SleepDisorder/ml/scaler.pkl'
        
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            print_success(f"Model loaded: {type(model).__name__}")
            
            # Check model properties
            if hasattr(model, 'n_estimators'):
                print_info(f"  - Tree count: {model.n_estimators}")
            if hasattr(model, 'n_features_in_'):
                print_info(f"  - Input features: {model.n_features_in_}")
        else:
            print_error(f"Model file not found: {model_path}")
            return False
        
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            print_success(f"Scaler loaded: {type(scaler).__name__}")
        else:
            print_error(f"Scaler file not found: {scaler_path}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"ML model test failed: {e}")
        return False

def test_json_files():
    """Test that JSON data files can be opened and parsed"""
    print_header("Testing JSON Data Files")
    
    data_dir = '/workspaces/SleepDisorder/data'
    json_files = ['users.json', 'analysis_history.json']
    
    all_good = True
    for json_file in json_files:
        file_path = os.path.join(data_dir, json_file)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                print_success(f"JSON file valid: {json_file} ({len(data)} records)")
            except json.JSONDecodeError as e:
                print_error(f"JSON parsing error in {json_file}: {e}")
                all_good = False
        else:
            print_warning(f"JSON file not found (will be created on first run): {json_file}")
    
    return all_good

def start_flask_server():
    """Start Flask server in background thread and run tests"""
    print_header("Starting Flask Server")
    
    try:
        # Import app
        import flask_app
        
        # Start Flask app in background thread
        def run_flask():
            try:
                flask_app.app.run(host='0.0.0.0', port=5000, debug=False)
            except Exception as e:
                print_error(f"Flask server error: {e}")
        
        server_thread = threading.Thread(target=run_flask, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        print_info("Waiting for server to start...")
        time.sleep(3)
        
        # Test basic connectivity
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = requests.get('http://localhost:5000/login', timeout=2)
                if response.status_code == 200:
                    print_success("Server is responding to requests")
                    print_info(f"Login page loaded: {len(response.text)} bytes")
                    return True
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    print_info(f"Connection attempt {attempt + 1} failed, retrying...")
                    time.sleep(2)
                else:
                    print_error(f"Could not connect after {max_retries} attempts")
                    return False
        
        return False
        
    except Exception as e:
        print_error(f"Flask server start failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print_header("Sleep Disorder Analysis - Flask Application Validation")
    
    tests = [
        ("Module Imports", test_imports),
        ("Data Structure", test_data_structure),
        ("Flask Application", test_flask_app),
        ("ML Models", test_ml_models),
        ("JSON Data Files", test_json_files),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Summary
    print_header("Validation Summary")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, result in results.items():
        status = f"{GREEN}PASSED{RESET}" if result else f"{RED}FAILED{RESET}"
        print(f"{test_name:30} {status}")
    
    print(f"\n{BLUE}{'='*60}{RESET}")
    if passed == total:
        print(f"{GREEN}✓ All tests passed ({passed}/{total}){RESET}")
        print(f"\n{GREEN}Application is ready to run!{RESET}")
        print(f"\n{YELLOW}To start the Flask server, run:{RESET}")
        print(f"  cd /workspaces/SleepDisorder && python flask_app.py")
        print(f"\n{YELLOW}Then open your browser to:{RESET}")
        print(f"  http://localhost:5000")
        return 0
    else:
        print(f"{RED}✗ Some tests failed ({passed}/{total}){RESET}")
        print(f"\n{RED}Please fix the errors above before running the application.{RESET}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
