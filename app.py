import streamlit as st
import json
import os

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
    a { color: #f39c12 !important; }
</style>
""", unsafe_allow_html=True)

# Create data directory
os.makedirs("data", exist_ok=True)

# Landing/Home Page
st.title("CLASSIFICATION OF SLEEP DISORDERS")
st.markdown("### AN ENSEMBLE LEARNING APPROACH FOR IMPROVED SLEEP DISORDER PREDICTION")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📝 REGISTER", use_container_width=True):
        st.switch_page("pages/register.py")

with col2:
    if st.button("🔐 LOGIN", use_container_width=True):
        st.switch_page("pages/login.py")

with col3:
    if st.button("👨‍💼 ADMIN", use_container_width=True):
        st.switch_page("pages/admin_login.py")

st.markdown("---")

st.markdown("""
## About Our Platform

Our platform utilizes a **Multi-Model Ensemble** technique to provide accurate sleep disorder predictions.

### Key Technologies:
- 🤖 **Artificial Neural Networks (ANN)** - Pattern recognition for sleep cycles
- 🌲 **Random Forest** - High-dimensional data processing  
- 📊 **Support Vector Machines (SVM)** - Advanced classification

### Sleep Disorders Detected:
1. **Normal** - No sleep disorder
2. **Sleep Deprivation** - Moderate risk
3. **Chronic Insomnia** - High risk
4. **Sleep Apnea** - Critical risk

Start by registering an account to get your personalized sleep analysis!
""")
    else:
        st.info("No reports found.")
