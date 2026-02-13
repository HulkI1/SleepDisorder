import streamlit as st
from pages.utils import ADMIN_PASSWORD

st.set_page_config(page_title="Admin - Sleep Disorder Classification", layout="wide", initial_sidebar_state="collapsed")

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
.stTextInput>div>div>input {
    background-color: #0f1623;
    color: #ffffff;
    border: 1px solid #f39c12;
    border-radius: 5px;
    padding: 10px;
}
</style>""", unsafe_allow_html=True)

st.title("👨‍💼 Admin Dashboard Access")
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### Enter Admin Password")
    
    with st.form("admin_login_form"):
        admin_password = st.text_input("Admin Password", type="password", placeholder="Enter admin password")
        submitted = st.form_submit_button("Unlock Admin Panel", use_container_width=True)
    
    if submitted:
        if not admin_password:
            st.error("❌ Password is required!")
        elif admin_password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.success("✅ Admin access granted!")
            st.balloons()
            st.switch_page("pages/admin_dashboard.py")
        else:
            st.error("❌ Incorrect admin password!")

st.markdown("---")
if st.button("🏠 Back to Home", use_container_width=True):
    st.switch_page("app.py")

st.markdown("""
<div style="text-align: center; margin-top: 30px; color: #888;">
    <p>Admin Login | Sleep Disorder Classification System</p>
</div>
""", unsafe_allow_html=True)
