import streamlit as st
import json
import os
from datetime import datetime
import joblib
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash

# Page config
st.set_page_config(page_title="Sleep Disorder Classification", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for dark theme
st.markdown("""
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background-color: #050a14 !important; color: white !important; }
    .main { background-color: #050a14 !important; }
    .stApp { background-color: #050a14 !important; }
    .stButton>button { background-color: #f39c12; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; }
    .stButton>button:hover { background-color: #e67e22; }
    .stTextInput>div>div>input, .stPasswordInput>div>div>input, .stNumberInput>div>div>input, .selectbox { background-color: #16213e !important; color: white !important; border: 1px solid #333 !important; }
    .stSelectbox { background-color: #16213e !important; }
    .stSelectbox label { color: #ccc !important; }
    h1, h2, h3 { color: #f39c12 !important; }
    .stMarkdown { color: white !important; }
    .stSidebar { background-color: #0b1120 !important; }
</style>
""", unsafe_allow_html=True)

# File paths
USERS_FILE = "data/users.json"
ANALYSIS_FILE = "data/analysis_history.json"
ADMIN_PASSWORD = "admin123"

# Create data directory
os.makedirs("data", exist_ok=True)

# Load ML models
try:
    model = joblib.load("ml/model.pkl")
    scaler = joblib.load("ml/scaler.pkl")
    model_loaded = True
except Exception as e:
    model_loaded = False
    st.error(f"ML Model Error: {e}")

# Data management functions
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_analysis():
    if not os.path.exists(ANALYSIS_FILE):
        try:
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
        with open(ANALYSIS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except:
        pass

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.admin_logged_in = False

# Home / Login / Register page
if not st.session_state.logged_in and not st.session_state.admin_logged_in:
    st.title("CLASSIFICATION OF SLEEP DISORDERS")
    st.markdown("### AN ENSEMBLE LEARNING APPROACH FOR IMPROVED SLEEP DISORDER PREDICTION")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("#### REGISTER")
        with st.form("register_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number (10 digits)")
            password = st.text_input("Password (Min 8 chars)", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button("CREATE ACCOUNT"):
                if not all([name, email, phone, password, confirm]):
                    st.error("All fields required")
                elif password != confirm:
                    st.error("Passwords do not match")
                elif len(password) < 8:
                    st.error("Password must be 8+ characters")
                else:
                    users = load_users()
                    if email in users:
                        st.error("Email already registered")
                    else:
                        users[email] = {
                            'password': generate_password_hash(password),
                            'phone': phone,
                            'name': name,
                            'created_at': datetime.now().isoformat()
                        }
                        save_users(users)
                        st.success("Account created! Please login.")
    
    with col2:
        st.markdown("#### LOGIN")
        with st.form("login_form"):
            email = st.text_input("Email Address", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.form_submit_button("LOG IN"):
                users = load_users()
                if email in users and check_password_hash(users[email]['password'], password):
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
    
    with col3:
        st.markdown("#### ADMIN LOGIN")
        with st.form("admin_form"):
            admin_pass = st.text_input("Admin Password", type="password")
            
            if st.form_submit_button("UNLOCK"):
                if admin_pass == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.success("Admin access granted!")
                    st.rerun()
                else:
                    st.error("Invalid password")

# User Dashboard
elif st.session_state.logged_in:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"Welcome, {st.session_state.user_email}")
    with col2:
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.rerun()
    
    st.markdown("---")
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("### NEW SLEEP ANALYSIS")
        with st.form("prediction_form"):
            phone = st.text_input("Phone Number")
            age = st.number_input("Age", min_value=1, max_value=120)
            gender = st.selectbox("Gender", ["Male", "Female"])
            occupation = st.text_input("Occupation")
            stress = st.slider("Stress Level (1-10)", 1, 10, 5)
            bp = st.text_input("Blood Pressure", "120/80")
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200)
            sleep_duration = st.number_input("Sleep Duration (hrs)", min_value=0.0, max_value=24.0, step=0.1)
            tea_coffee = st.number_input("Tea/Coffee (cups)", min_value=0)
            bmi = st.selectbox("BMI Category", ["Normal", "Overweight", "Obese"])
            snoring = st.selectbox("Snoring", ["Never", "Sometimes", "Every Night"])
            work_hours = st.number_input("Working Hours/Week", min_value=0, max_value=168)
            
            if st.form_submit_button("GENERATE PREDICTION"):
                if not model_loaded:
                    st.error("ML Model not available")
                else:
                    try:
                        # Parse blood pressure
                        if '/' in bp:
                            s, d = bp.split('/')
                            bp_avg = (float(s) + float(d)) / 2
                        else:
                            bp_avg = float(bp)
                        
                        # Map values
                        bmi_map = {'Normal': 22, 'Overweight': 28, 'Obese': 32}
                        snoring_map = {'Never': 0, 'Sometimes': 0.5, 'Every Night': 1}
                        
                        features = [sleep_duration, stress, age, bp_avg, heart_rate, tea_coffee, 
                                   bmi_map[bmi], snoring_map[snoring], work_hours]
                        
                        features_scaled = scaler.transform([features])
                        prediction = int(model.predict(features_scaled)[0])
                        
                        disorder_map = {
                            0: ('Normal', 'No sleep disorder detected', '🟢'),
                            1: ('Sleep Deprivation', 'Moderate Risk: Sleep Deprivation', '🟠'),
                            2: ('Chronic Insomnia', 'High Risk: Chronic Insomnia', '🔴'),
                            3: ('Sleep Apnea', 'Critical Risk: Possible Sleep Apnea', '🔴')
                        }
                        
                        diagnosis, full_text, icon = disorder_map.get(prediction, ('Unknown', 'Unknown', '⚪'))
                        
                        # Save record
                        record = {
                            'id': f"{st.session_state.user_email}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                            'email': st.session_state.user_email,
                            'phone': phone,
                            'age': age,
                            'gender': gender,
                            'occupation': occupation,
                            'stress': stress,
                            'bp': bp,
                            'heart_rate': heart_rate,
                            'sleep_duration': sleep_duration,
                            'bmi': bmi,
                            'snoring': snoring,
                            'work_hours': work_hours,
                            'diagnosis': diagnosis,
                            'full_diagnosis': full_text,
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        history = load_analysis()
                        history.append(record)
                        save_analysis(history)
                        
                        st.success(f"{icon} {full_text}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    with col2:
        st.markdown("### ANALYSIS HISTORY")
        history = load_analysis()
        user_history = [h for h in history if h.get('email') == st.session_state.user_email]
        
        if user_history:
            for record in reversed(user_history[-5:]):
                st.write(f"📅 {record.get('timestamp', 'N/A')[:10]}")
                st.write(f"🔍 {record.get('diagnosis', 'N/A')}")
                st.divider()
        else:
            st.info("No analysis records yet.")

# Admin Dashboard
elif st.session_state.admin_logged_in:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("ADMIN DASHBOARD")
    with col2:
        if st.button("LOGOUT"):
            st.session_state.admin_logged_in = False
            st.rerun()
    
    st.markdown("---")
    st.markdown("### ALL SLEEP DISORDER REPORTS")
    
    history = load_analysis()
    
    if history:
        for record in reversed(history):
            with st.expander(f"📋 {record.get('email')} - {record.get('diagnosis')} ({record.get('timestamp', 'N/A')[:10]})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Email**: {record.get('email')}")
                    st.write(f"**Phone**: {record.get('phone')}")
                    st.write(f"**Age**: {record.get('age')}")
                    st.write(f"**Gender**: {record.get('gender')}")
                with col2:
                    st.write(f"**Occupation**: {record.get('occupation')}")
                    st.write(f"**Stress Level**: {record.get('stress')}")
                    st.write(f"**Sleep Duration**: {record.get('sleep_duration')} hrs")
                    st.write(f"**Heart Rate**: {record.get('heart_rate')} bpm")
                
                st.write(f"**Diagnosis**: {record.get('full_diagnosis')}")
                st.write(f"**Timestamp**: {record.get('timestamp')}")
    else:
        st.info("No reports found.")
