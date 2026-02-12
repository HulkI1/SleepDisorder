import streamlit as st
import joblib
import numpy as np
import psycopg2
import os

# Load ML model with error handling
try:
    model = joblib.load("ml/model.pkl")
    scaler = joblib.load("ml/scaler.pkl")
    model_loaded = True
except Exception as e:
    model_loaded = False
    error_msg = str(e)

st.title("🛌 Sleep Disorder Prediction App")

# Display error if model failed to load
if not model_loaded:
    st.error(f"⚠️ Model loading error: {error_msg}")
    st.info("The model files (ml/model.pkl and ml/scaler.pkl) are corrupted or missing. Please regenerate them by running your training script.")
    st.stop()


# --- Form ---
with st.form("sleep_form"):
    email = st.text_input("Email")
    age = st.number_input("Age", 1, 120)
    sleep_duration = st.number_input("Sleep Duration (hours)", 0.0, 24.0)
    stress = st.slider("Stress Level", 1, 10)
    bp = st.text_input("Blood Pressure (120/80)")
    heart_rate = st.number_input("Heart Rate", 30, 200)
    tea_coffee = st.selectbox("Tea/Coffee", ["Yes", "No"])
    bmi = st.number_input("BMI", 0.0, 60.0)
    snoring = st.selectbox("Snoring", ["Yes", "No"])
    work_hours = st.number_input("Work Hours", 0, 24)

    submit = st.form_submit_button("Predict")

# --- Helper functions ---
def parse_bp(bp):
    try:
        if "/" in bp:
            s, d = bp.split("/")
            return (float(s) + float(d)) / 2
        return float(bp)
    except:
        return 0.0

def binary(val):
    return 1 if val.lower() == "yes" else 0

# --- Prediction ---
if submit:
    features = [
        sleep_duration,
        stress,
        age,
        parse_bp(bp),
        heart_rate,
        binary(tea_coffee),
        bmi,
        binary(snoring),
        work_hours
    ]

    features_scaled = scaler.transform([features])
    prediction = model.predict(features_scaled)[0]

    st.success(f"Prediction: {prediction}")
