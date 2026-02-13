import streamlit as st
from pages.utils import load_users, save_users
from werkzeug.security import generate_password_hash

st.set_page_config(page_title="Register - Sleep Disorder Classification", layout="wide", initial_sidebar_state="collapsed")

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
.stTextInput>div>div>input, .stNumberInput>div>div>input {
    background-color: #0f1623;
    color: #ffffff;
    border: 1px solid #f39c12;
    border-radius: 5px;
    padding: 10px;
}
</style>""", unsafe_allow_html=True)

st.title("📝 Register for Sleep Disorder Classification")
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    with st.form("registration_form"):
        name = st.text_input("Full Name", placeholder="e.g., John Doe")
        email = st.text_input("Email Address", placeholder="e.g., user@example.com")
        phone = st.text_input("Phone Number", placeholder="e.g., +1234567890")
        password = st.text_input("Password", type="password", placeholder="Enter a strong password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        
        submitted = st.form_submit_button("Create Account", use_container_width=True)
    
    if submitted:
        if not name or not email or not phone or not password or not confirm_password:
            st.error("❌ All fields are required!")
        elif password != confirm_password:
            st.error("❌ Passwords do not match!")
        elif len(password) < 6:
            st.error("❌ Password must be at least 6 characters long!")
        elif "@" not in email or "." not in email:
            st.error("❌ Invalid email format!")
        else:
            users = load_users()
            if email in users:
                st.error("❌ Email already registered!")
            else:
                hashed_password = generate_password_hash(password)
                users[email] = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "password": hashed_password
                }
                save_users(users)
                st.success("✅ Registration successful! Please log in.")
                st.balloons()

st.markdown("---")
st.markdown("### Already have an account?")
if st.button("🔐 Go to Login Page", use_container_width=True):
    st.switch_page("pages/login.py")

st.markdown("""
<div style="text-align: center; margin-top: 30px; color: #888;">
    <p>Registration Form | Sleep Disorder Classification System</p>
</div>
""", unsafe_allow_html=True)
