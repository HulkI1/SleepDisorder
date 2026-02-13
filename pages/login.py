import streamlit as st
from pages.utils import load_users
from werkzeug.security import check_password_hash

st.set_page_config(page_title="Login - Sleep Disorder Classification", layout="wide", initial_sidebar_state="collapsed")

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

st.title("🔐 Login to Your Account")
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="e.g., user@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        submitted = st.form_submit_button("Sign In", use_container_width=True)
    
    if submitted:
        if not email or not password:
            st.error("❌ Email and password are required!")
        else:
            users = load_users()
            if email not in users:
                st.error("❌ Email not found! Please register first.")
            else:
                user = users[email]
                if check_password_hash(user["password"], password):
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.user_name = user["name"]
                    st.success(f"✅ Welcome back, {user['name']}!")
                    st.balloons()
                    # Switch to dashboard after login
                    st.switch_page("pages/dashboard.py")
                else:
                    st.error("❌ Incorrect password!")

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Don't have an account?")
    if st.button("📝 Create New Account", use_container_width=True):
        st.switch_page("pages/register.py")

with col2:
    st.markdown("### Go Back")
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")

st.markdown("""
<div style="text-align: center; margin-top: 30px; color: #888;">
    <p>Login Form | Sleep Disorder Classification System</p>
</div>
""", unsafe_allow_html=True)
