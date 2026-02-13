import streamlit as st
import pandas as pd
from pages.utils import load_analysis

st.set_page_config(page_title="Admin Dashboard - Sleep Disorder Classification", layout="wide", initial_sidebar_state="collapsed")

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
</style>""", unsafe_allow_html=True)

# Check if admin is logged in
if "admin_logged_in" not in st.session_state or not st.session_state.admin_logged_in:
    st.warning("⚠️ Admin access required!")
    if st.button("🔐 Go to Admin Login"):
        st.switch_page("pages/admin_login.py")
    st.stop()

st.title("👨‍💼 Admin Dashboard")
st.markdown("---")

# Load all analyses
analysis_history = load_analysis()

if not analysis_history:
    st.info("📭 No analyses recorded yet.")
else:
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Analyses", len(analysis_history))
    
    with col2:
        unique_users = len(set([a["email"] for a in analysis_history]))
        st.metric("Unique Users", unique_users)
    
    with col3:
        disorders = [a["diagnosis"] for a in analysis_history]
        insomnia_count = sum(1 for d in disorders if d == "Insomnia")
        st.metric("Insomnia Cases", insomnia_count)
    
    with col4:
        apnea_count = sum(1 for d in disorders if d == "Sleep Apnea")
        st.metric("Sleep Apnea Cases", apnea_count)
    
    st.markdown("---")
    
    # Display all analyses in table format
    st.markdown("### 📊 All User Analyses")
    
    # Prepare data for display
    display_data = []
    for record in analysis_history:
        display_data.append({
            "Date": record["date"],
            "Email": record["email"],
            "Age": record["age"],
            "Gender": record["gender"],
            "Sleep Duration (hrs)": record["sleep_duration"],
            "Stress Level": record["stress_level"],
            "Heart Rate (bpm)": record["heart_rate"],
            "BP (sys/dia)": f"{record['systolic_bp']}/{record['diastolic_bp']}",
            "BMI": record["bmi"],
            "Diagnosis": record["diagnosis"]
        })
    
    df = pd.DataFrame(display_data)
    
    # Sort by date (newest first)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date", ascending=False)
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    
    st.dataframe(df, use_container_width=True, height=400)
    
    st.markdown("---")
    
    # Filter by diagnosis
    st.markdown("### 🔍 Filter by Diagnosis")
    
    diagnosis_filter = st.selectbox(
        "Select Diagnosis to View",
        ["All", "None", "Insomnia", "Sleep Apnea", "Narcolepsy"]
    )
    
    if diagnosis_filter != "All":
        filtered_analyses = [a for a in analysis_history if a["diagnosis"] == diagnosis_filter]
    else:
        filtered_analyses = analysis_history
    
    if filtered_analyses:
        st.markdown(f"### {diagnosis_filter.upper()} - {len(filtered_analyses)} Records")
        
        for record in filtered_analyses[::-1]:  # Show newest first
            with st.expander(f"📅 {record['date']} - {record['email']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**Personal Info**")
                    st.write(f"Email: {record['email']}")
                    st.write(f"Age: {record['age']}")
                    st.write(f"Gender: {record['gender']}")
                    st.write(f"BMI: {record['bmi']}")
                
                with col2:
                    st.write("**Sleep & Health**")
                    st.write(f"Sleep Duration: {record['sleep_duration']} hrs")
                    st.write(f"Heart Rate: {record['heart_rate']} bpm")
                    st.write(f"BP: {record['systolic_bp']}/{record['diastolic_bp']} mmHg")
                    st.write(f"Daily Steps: {record['daily_steps']}")
                
                with col3:
                    st.write("**Lifestyle**")
                    st.write(f"Stress Level: {record['stress_level']}/10")
                    st.write(f"Caffeine: {record['caffeine_intake']} mg")
                    st.write(f"Smoking: {record['smoking']}")
                    st.write(f"Alcohol: {record['alcohol']}")
                
                st.markdown("---")
                st.markdown(f"**🩺 Diagnosis: `{record['diagnosis']}`**")
    else:
        st.info(f"No records found for {diagnosis_filter}")

st.markdown("---")

# Admin navigation
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Statistics")
    if analysis_history:
        # Average metrics
        avg_age = sum([a["age"] for a in analysis_history]) / len(analysis_history)
        avg_stress = sum([a["stress_level"] for a in analysis_history]) / len(analysis_history)
        avg_sleep = sum([a["sleep_duration"] for a in analysis_history]) / len(analysis_history)
        
        st.write(f"**Average Age:** {avg_age:.1f} years")
        st.write(f"**Average Stress Level:** {avg_stress:.1f}/10")
        st.write(f"**Average Sleep Duration:** {avg_sleep:.1f} hours")

with col2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.switch_page("app.py")
