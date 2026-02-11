import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("ml/model.pkl")
scaler = joblib.load("ml/scaler.pkl")

st.title("🛌 Sleep Disorder Prediction")

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
