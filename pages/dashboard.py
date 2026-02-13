import streamlit as st
import pandas as pd
import json
from pages.utils import load_analysis, save_analysis, load_models
from datetime import datetime

st.set_page_config(page_title="Dashboard - Sleep Disorder Classification", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body {
    background-color: #050a14;
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.stApp {
    background-color: #050a14;
}
.stButton>button {
    background-color: #f39c12;
    color: #050a14;
    font-weight: bold;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #e67e22;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(243, 156, 18, 0.3);
}
.stNumberInput>div>div>input {
    background-color: #0f1623;
    color: #ffffff;
    border: 1px solid #f39c12;
    border-radius: 5px;
    padding: 10px;
}
.metric-card {
    background-color: #0f1623;
    border: 1px solid #f39c12;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
}
</style>""", unsafe_allow_html=True)

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please log in to access the dashboard!")
    if st.button("🔐 Go to Login"):
        st.switch_page("pages/login.py")
    st.stop()

st.title(f"📊 Welcome, {st.session_state.user_name}!")
st.markdown("---")

# Load models
model, scaler, models_loaded = load_models()

if not models_loaded:
    st.error("❌ ML Models not found. Please ensure ml/model.pkl and ml/scaler.pkl exist.")
    st.stop()

# Sidebar for navigation
with st.sidebar:
    st.markdown("### Navigation")
    page_option = st.radio("Select Section", ["New Analysis", "Analysis History", "Profile"])
    
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.user_name = None
        st.switch_page("app.py")

if page_option == "New Analysis":
    st.markdown("### Sleep Disorder Analysis Form")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        sleep_duration = st.number_input("Sleep Duration (hours)", min_value=0.0, max_value=24.0, value=7.0, step=0.1)
        stress_level = st.number_input("Stress Level (0-10)", min_value=0, max_value=10, value=5)
        systolic_pressure = st.number_input("Systolic Blood Pressure (mmHg)", min_value=80, max_value=200, value=120)
    
    with col2:
        diastolic_pressure = st.number_input("Diastolic Blood Pressure (mmHg)", min_value=50, max_value=130, value=80)
        heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=70)
        daily_steps = st.number_input("Daily Steps", min_value=0, max_value=50000, value=5000)
        caffeine_intake = st.number_input("Caffeine Intake (mg/day)", min_value=0, max_value=1000, value=100)
    
    co1, co2 = st.columns(2)
    with co1:
        alcohol = st.selectbox("Alcohol Consumption", ["None", "Light", "Moderate", "Heavy"])
        smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
    
    with co2:
        snoring = st.selectbox("Snoring", ["No", "Yes"])
        bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0, step=0.1)
    
    if st.button("🔍 Analyze & Predict", use_container_width=True):
        # Prepare features for prediction
        gender_val = 1 if gender == "Male" else 0
        alcohol_val = {"None": 0, "Light": 1, "Moderate": 2, "Heavy": 3}[alcohol]
        smoking_val = {"Never": 0, "Former": 1, "Current": 2}[smoking]
        snoring_val = 1 if snoring == "Yes" else 0
        
        # Create feature array
        features = [[
            age, gender_val, sleep_duration, stress_level, 
            systolic_pressure, diastolic_pressure, heart_rate, 
            daily_steps, caffeine_intake, alcohol_val, 
            smoking_val, snoring_val, bmi
        ]]
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Map prediction to disorder name
        disorders = {
            0: "None",
            1: "Insomnia",
            2: "Sleep Apnea",
            3: "Narcolepsy"
        }
        
        disorder_name = disorders.get(int(prediction), "Unknown")
        
        # Save to analysis history
        analysis_record = {
            "email": st.session_state.user_email,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "age": age,
            "gender": gender,
            "sleep_duration": sleep_duration,
            "stress_level": stress_level,
            "systolic_bp": systolic_pressure,
            "diastolic_bp": diastolic_pressure,
            "heart_rate": heart_rate,
            "daily_steps": daily_steps,
            "caffeine_intake": caffeine_intake,
            "alcohol": alcohol,
            "smoking": smoking,
            "snoring": snoring,
            "bmi": bmi,
            "diagnosis": disorder_name
        }
        
        analysis_history = load_analysis()
        analysis_history.append(analysis_record)
        save_analysis(analysis_history)
        
        # Display results
        st.markdown("---")
        st.markdown("### 📋 Analysis Results")
        
        # Color code based on diagnosis
        if disorder_name == "None":
            color = "#27ae60"  # Green
        elif disorder_name == "Insomnia":
            color = "#e74c3c"  # Red
        elif disorder_name == "Sleep Apnea":
            color = "#e67e22"  # Orange
        else:  # Narcolepsy
            color = "#8e44ad"  # Purple
        
        st.markdown(f"""
        <div style="background-color: {color}20; border-left: 4px solid {color}; padding: 15px; border-radius: 5px;">
            <h3 style="color: {color}; margin: 0;">🩺 Diagnosis: <strong>{disorder_name}</strong></h3>
            <p style="color: #ccc; margin-top: 10px;">Analysis completed on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("✅ Analysis saved to your history!")

elif page_option == "Analysis History":
    st.markdown("### 📜 Your Analysis History")
    
    analysis_history = load_analysis()
    user_analyses = [a for a in analysis_history if a["email"] == st.session_state.user_email]
    
    if not user_analyses:
        st.info("No analyses yet. Go to 'New Analysis' to create your first analysis!")
    else:
        # Sort by date (newest first)
        user_analyses.sort(key=lambda x: x["date"], reverse=True)
        
        for i, record in enumerate(user_analyses):
            with st.expander(f"📅 {record['date']} - {record['diagnosis']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Age:** {record['age']}")
                    st.write(f"**Gender:** {record['gender']}")
                    st.write(f"**Sleep Duration:** {record['sleep_duration']} hours")
                    st.write(f"**Stress Level:** {record['stress_level']}/10")
                    st.write(f"**Heart Rate:** {record['heart_rate']} bpm")
                
                with col2:
                    st.write(f"**Blood Pressure:** {record['systolic_bp']}/{record['diastolic_bp']} mmHg")
                    st.write(f"**BMI:** {record['bmi']}")
                    st.write(f"**Snoring:** {record['snoring']}")
                    st.write(f"**Smoking:** {record['smoking']}")
                    st.write(f"**Alcohol:** {record['alcohol']}")
                
                st.write("---")
                st.write(f"**Diagnosis:** `{record['diagnosis']}`")

else:  # Profile
    st.markdown("### 👤 Your Profile")
    
    st.write(f"**Name:** {st.session_state.user_name}")
    st.write(f"**Email:** {st.session_state.user_email}")
    
    # Count analyses
    analysis_history = load_analysis()
    user_count = len([a for a in analysis_history if a["email"] == st.session_state.user_email])
    st.write(f"**Total Analyses:** {user_count}")
    
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.user_name = None
        st.switch_page("app.py")
