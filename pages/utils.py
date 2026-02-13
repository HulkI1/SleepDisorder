import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
import joblib

USERS_FILE = "data/users.json"
ANALYSIS_FILE = "data/analysis_history.json"
ADMIN_PASSWORD = "admin123"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    os.makedirs("data", exist_ok=True)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_analysis():
    if not os.path.exists(ANALYSIS_FILE):
        try:
            os.makedirs("data", exist_ok=True)
            with open(ANALYSIS_FILE, 'w') as f:
                json.dump([], f)
        except:
            pass
        return []
    try:
        with open(ANALYSIS_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except:
        return []

def save_analysis(data):
    try:
        os.makedirs("data", exist_ok=True)
        with open(ANALYSIS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except:
        pass

def load_models():
    try:
        model = joblib.load("ml/model.pkl")
        scaler = joblib.load("ml/scaler.pkl")
        return model, scaler, True
    except:
        return None, None, False
