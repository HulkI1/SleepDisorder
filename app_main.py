"""
Sleep Disorder Analysis Application - Complete MVP
Features: User Auth, Sleep Analysis, ML Prediction, Admin Portal, PDF Reports
"""

import streamlit as st
import json
import os
import hashlib
import hmac
from datetime import datetime
import joblib
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io

# ============================================================================
# CONFIGURATION & SETUP
# ============================================================================

st.set_page_config(
    page_title="Sleep Disorder Analysis",
    page_icon="🛌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File paths for data storage
USERS_FILE = "data/users.json"
ANALYSIS_FILE = "data/analysis_history.json"
ADMIN_PASSWORD = "admin123"  # Change in production - use environment variable

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Load ML model
try:
    model = joblib.load("ml/model.pkl")
    scaler = joblib.load("ml/scaler.pkl")
    model_loaded = True
except Exception as e:
    model_loaded = False
    error_msg = str(e)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed

def load_users() -> dict:
    """Load users from JSON file"""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users: dict):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_analysis_history() -> list:
    """Load analysis history from JSON file"""
    if not os.path.exists(ANALYSIS_FILE):
        return []
    try:
        with open(ANALYSIS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_analysis_history(history: list):
    """Save analysis history to JSON file"""
    with open(ANALYSIS_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def predict_disorder(features: list) -> tuple:
    """
    Predict sleep disorder from features
    Returns: (prediction_value, diagnosis_text, severity)
    """
    if not model_loaded:
        return None, "Model not loaded", "ERROR"
    
    try:
        features_scaled = scaler.transform([features])
        prediction = model.predict(features_scaled)[0]
        
        # Map predictions to disorder categories
        disorder_map = {
            0: ("Normal", "✅ No sleep disorder detected", "Low"),
            1: ("Sleep Deprivation", "⚠️ Moderate Risk: Sleep Deprivation", "Moderate"),
            2: ("Chronic Insomnia", "🔴 High Risk: Chronic Insomnia", "High"),
            3: ("Sleep Apnea", "🔴 High Risk: Possible Obstructive Sleep Apnea", "Critical")
        }
        
        if prediction in disorder_map:
            return prediction, disorder_map[prediction][1], disorder_map[prediction][2]
        return prediction, "Unknown disorder", "Unknown"
    except Exception as e:
        return None, f"Prediction error: {str(e)}", "ERROR"

def generate_pdf_report(user_data: dict, analysis_result: dict) -> bytes:
    """Generate PDF medical report"""
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=12,
        alignment=1
    )
    story.append(Paragraph("🛌 MEDICAL SLEEP ANALYSIS REPORT", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Report Info
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.grey
    )
    story.append(Paragraph(f"<b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", info_style))
    story.append(Paragraph(f"<b>Report ID:</b> {analysis_result.get('id', 'N/A')}", info_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Patient Information
    story.append(Paragraph("PATIENT INFORMATION", styles['Heading2']))
    patient_data = [
        ['Email', user_data.get('email', 'N/A')],
        ['Phone Number', user_data.get('phone', 'N/A')],
        ['Age', str(user_data.get('age', 'N/A'))],
        ['Gender', user_data.get('gender', 'N/A')],
        ['Occupation', user_data.get('occupation', 'N/A')],
    ]
    
    patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(patient_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Sleep Analysis Data
    story.append(Paragraph("SLEEP ANALYSIS DATA", styles['Heading2']))
    sleep_data = [
        ['Metric', 'Value'],
        ['Sleep Duration (hours)', str(user_data.get('sleep_duration', 'N/A'))],
        ['Stress Level (1-10)', str(user_data.get('stress', 'N/A'))],
        ['Blood Pressure', user_data.get('bp', 'N/A')],
        ['Heart Rate (bpm)', str(user_data.get('heart_rate', 'N/A'))],
        ['BMI Category', user_data.get('bmi', 'N/A')],
        ['Snoring', user_data.get('snoring', 'N/A')],
        ['Working Hours', str(user_data.get('work_hours', 'N/A'))],
    ]
    
    sleep_table = Table(sleep_data, colWidths=[2.5*inch, 3.5*inch])
    sleep_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    story.append(sleep_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Diagnosis Result
    story.append(Paragraph("DIAGNOSIS RESULT", styles['Heading2']))
    diagnosis = analysis_result.get('diagnosis', 'N/A')
    severity = analysis_result.get('severity', 'N/A')
    
    result_style = ParagraphStyle(
        'ResultStyle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#d62728'),
        spaceAfter=10
    )
    story.append(Paragraph(f"<b>{diagnosis}</b>", result_style))
    story.append(Paragraph(f"<b>Severity Level:</b> {severity}", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    # Medical Disclaimer
    story.append(Paragraph("IMPORTANT DISCLAIMER", styles['Heading3']))
    disclaimer_style = ParagraphStyle(
        'DisclaimerStyle',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        leading=10
    )
    disclaimer_text = """
    This report is generated by an automated machine learning system and should not be 
    considered a professional medical diagnosis. Please consult with a qualified healthcare 
    provider for proper medical evaluation and treatment. The information provided is for 
    informational purposes only and does not replace professional medical advice.
    """
    story.append(Paragraph(disclaimer_text, disclaimer_style))
    
    # Build PDF
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_role = None
    st.session_state.page = "login"

# ============================================================================
# AUTHENTICATION PAGES
# ============================================================================

def page_user_login():
    """User login page"""
    st.title("🛌 Sleep Disorder Analysis Platform")
    st.subheader("User Login")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("---")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        col_login, col_register = st.columns(2)
        
        with col_login:
            if st.button("🔐 Login", key="login_btn", use_container_width=True):
                if not email or not password:
                    st.error("❌ Please enter both email and password")
                else:
                    users = load_users()
                    if email in users and verify_password(password, users[email]['password']):
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.session_state.user_role = "user"
                        st.session_state.page = "dashboard"
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password")
        
        with col_register:
            if st.button("📝 Register", key="register_btn", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
    
    with col2:
        st.markdown("#### Features")
        st.markdown("""
        ✅ User Registration with Secure Login
        
        ✅ Sleep Analysis Form
        
        ✅ ML-Based Prediction System
        
        ✅ Analysis History Tracking
        
        ✅ Medical Report Generation
        
        ✅ Admin Portal for Hospitals
        """)
    
    st.markdown("---")
    
    if st.button("🔑 Admin Login", key="admin_login_btn", use_container_width=True):
        st.session_state.page = "admin_login"
        st.rerun()

def page_user_register():
    """User registration page"""
    st.title("📝 User Registration")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        phone = st.text_input("Phone Number", key="reg_phone")
        
        if st.button("✅ Create Account", use_container_width=True):
            # Validation
            if not email or not password or not confirm_password or not phone:
                st.error("❌ All fields are required")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters")
            else:
                users = load_users()
                if email in users:
                    st.error("❌ Email already registered")
                else:
                    users[email] = {
                        'password': hash_password(password),
                        'phone': phone,
                        'created_at': datetime.now().isoformat()
                    }
                    save_users(users)
                    st.success("✅ Account created successfully! Please login.")
                    st.balloons()
                    st.session_state.page = "login"
                    st.rerun()
        
        st.markdown("---")
        if st.button("← Back to Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

def page_admin_login():
    """Admin login page"""
    st.title("🔐 Admin Portal Login")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        admin_password = st.text_input("Admin Password", type="password", key="admin_pass")
        
        if st.button("🔓 Admin Login", use_container_width=True):
            if admin_password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user_role = "admin"
                st.session_state.page = "admin_portal"
                st.success("✅ Admin login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid admin password")
        
        st.markdown("---")
        if st.button("← Back to Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

# ============================================================================
# USER DASHBOARD
# ============================================================================

def page_user_dashboard():
    """User dashboard with sleep analysis form"""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.title("🛌 Sleep Analysis Dashboard")
        st.write(f"Welcome, **{st.session_state.user_email}**")
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.session_state.page = "login"
            st.success("✅ Logged out successfully!")
            st.rerun()
    
    st.markdown("---")
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📋 Sleep Analysis", "📊 Analysis History", "📄 Generate Report"])
    
    # ========== TAB 1: Sleep Analysis Form ==========
    with tab1:
        st.subheader("Enter Your Sleep Analysis Data")
        
        with st.form("sleep_analysis_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                phone = st.text_input("Phone Number*", value=load_users().get(st.session_state.user_email, {}).get('phone', ''))
                age = st.number_input("Age*", min_value=1, max_value=120, value=30)
                gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
                occupation = st.text_input("Occupation*", value="")
                stress = st.slider("Stress Level (1-10)*", 1, 10, 5)
            
            with col2:
                bp = st.text_input("Blood Pressure (e.g., 120/80)*", value="120/80")
                heart_rate = st.number_input("Heart Rate (bpm)*", min_value=30, max_value=200, value=75)
                sleep_duration = st.number_input("Sleep Duration (hours)*", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
                bmi = st.number_input("BMI*", min_value=10.0, max_value=60.0, value=24.0, step=0.1)
                snoring = st.selectbox("Do you snore?*", ["No", "Yes"])
            
            work_hours = st.slider("Working Hours per Day*", 0, 24, 8)
            
            st.markdown("---")
            submit = st.form_submit_button("🔮 Generate Prediction", use_container_width=True)
        
        if submit:
            # Validation
            if not all([phone, occupation, bp]):
                st.error("❌ Please fill all required fields (marked with *)")
            else:
                # Parse blood pressure
                try:
                    if "/" in bp:
                        s, d = bp.split("/")
                        bp_avg = (float(s) + float(d)) / 2
                    else:
                        bp_avg = float(bp)
                except:
                    st.error("❌ Invalid blood pressure format")
                    st.stop()
                
                # Prepare features for ML model
                snoring_binary = 1 if snoring == "Yes" else 0
                
                features = [
                    sleep_duration,
                    stress,
                    age,
                    bp_avg,
                    heart_rate,
                    0,  # tea_coffee placeholder
                    bmi,
                    snoring_binary,
                    work_hours
                ]
                
                # Get prediction
                pred_value, diagnosis, severity = predict_disorder(features)
                
                if pred_value is not None:
                    # Create analysis record
                    analysis_record = {
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
                        'prediction': int(pred_value),
                        'severity': severity,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # Save to history
                    history = load_analysis_history()
                    history.append(analysis_record)
                    save_analysis_history(history)
                    
                    # Display result
                    st.markdown("---")
                    st.subheader("🔮 Prediction Result")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Diagnosis", analysis_record['severity'])
                    with col2:
                        st.metric("Sleep Duration", f"{sleep_duration}h")
                    with col3:
                        st.metric("Stress Level", stress)
                    
                    # Color-coded result
                    if severity == "Low":
                        st.success(diagnosis)
                    elif severity == "Moderate":
                        st.warning(diagnosis)
                    else:
                        st.error(diagnosis)
                    
                    st.info("""
                    📌 **DISCLAIMER**: This prediction is generated by an automated ML system and should not be 
                    considered a professional medical diagnosis. Please consult with a qualified healthcare provider 
                    for proper medical evaluation and treatment.
                    """)
                    
                    st.success("✅ Analysis saved to your history!")
                else:
                    st.error(f"❌ Prediction failed: {diagnosis}")
    
    # ========== TAB 2: Analysis History ==========
    with tab2:
        st.subheader("Your Analysis History")
        
        history = load_analysis_history()
        user_history = [h for h in history if h['email'] == st.session_state.user_email]
        
        if user_history:
            # Display as table
            df = pd.DataFrame(user_history)
            df = df[['timestamp', 'diagnosis', 'severity', 'sleep_duration', 'stress', 'heart_rate']]
            df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df, use_container_width=True)
            
            # Detailed view
            st.subheader("Detailed Analysis")
            selected_idx = st.selectbox(
                "Select an analysis to view details:",
                range(len(user_history)),
                format_func=lambda i: f"{user_history[i]['timestamp']} - {user_history[i]['diagnosis']}"
            )
            
            selected = user_history[selected_idx]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Sleep Duration", f"{selected['sleep_duration']}h")
                st.metric("Heart Rate", f"{selected['heart_rate']} bpm")
            with col2:
                st.metric("Stress Level", selected['stress'])
                st.metric("BMI", selected['bmi'])
            with col3:
                st.metric("Age", selected['age'])
                st.metric("Snoring", selected['snoring'])
        else:
            st.info("📭 No analysis history yet. Start by creating your first analysis!")
    
    # ========== TAB 3: Generate Report ==========
    with tab3:
        st.subheader("Generate Medical Report (PDF)")
        
        history = load_analysis_history()
        user_history = [h for h in history if h['email'] == st.session_state.user_email]
        
        if user_history:
            selected_idx = st.selectbox(
                "Select an analysis to generate report:",
                range(len(user_history)),
                format_func=lambda i: f"{user_history[i]['timestamp']} - {user_history[i]['diagnosis']}",
                key="report_select"
            )
            
            selected = user_history[selected_idx]
            
            if st.button("📥 Download Medical Report (PDF)", use_container_width=True):
                # Generate PDF
                pdf_data = generate_pdf_report(selected, selected)
                
                st.download_button(
                    label="📄 Click to Download PDF",
                    data=pdf_data,
                    file_name=f"Sleep_Analysis_Report_{selected['id']}.pdf",
                    mime="application/pdf"
                )
                st.success("✅ PDF generated successfully!")
        else:
            st.info("📭 No analysis history. Create an analysis first to generate a report.")

# ============================================================================
# ADMIN PORTAL
# ============================================================================

def page_admin_portal():
    """Admin portal for viewing patient analyses"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("🏥 Hospital Admin Portal")
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.page = "login"
            st.success("✅ Logged out successfully!")
            st.rerun()
    
    st.markdown("---")
    
    # Load all analysis history
    history = load_analysis_history()
    
    # Tabs for admin functions
    tab1, tab2, tab3 = st.tabs(["👥 All Patient Analyses", "🔴 URGENT Cases", "📊 Statistics"])
    
    # ========== TAB 1: All Analyses ==========
    with tab1:
        st.subheader("All Patient Sleep Analyses")
        
        if history:
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                severity_filter = st.multiselect(
                    "Filter by Severity:",
                    ["Low", "Moderate", "High", "Critical"],
                    default=["Low", "Moderate", "High", "Critical"]
                )
            
            with col2:
                search_email = st.text_input("Search by Email:", "")
            
            # Filter data
            filtered_history = history
            if severity_filter:
                filtered_history = [h for h in filtered_history if h['severity'] in severity_filter]
            if search_email:
                filtered_history = [h for h in filtered_history if search_email.lower() in h['email'].lower()]
            
            # Display as table
            if filtered_history:
                df = pd.DataFrame(filtered_history)
                df = df[['timestamp', 'email', 'phone', 'diagnosis', 'severity', 'age', 'stress']]
                df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
                
                st.dataframe(df, use_container_width=True, height=400)
                
                # Detailed view
                st.subheader("View Patient Details")
                selected_idx = st.selectbox(
                    "Select a patient to view full details:",
                    range(len(filtered_history)),
                    format_func=lambda i: f"{filtered_history[i]['email']} - {filtered_history[i]['timestamp']}"
                )
                
                selected = filtered_history[selected_idx]
                
                # Patient info
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Email", selected['email'])
                with col2:
                    st.metric("Phone", selected['phone'])
                with col3:
                    st.metric("Age", selected['age'])
                with col4:
                    st.metric("Gender", selected['gender'])
                
                st.markdown("---")
                
                # Sleep data
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Sleep Duration", f"{selected['sleep_duration']}h")
                    st.metric("Stress Level", selected['stress'])
                with col2:
                    st.metric("Heart Rate", f"{selected['heart_rate']} bpm")
                    st.metric("Blood Pressure", selected['bp'])
                with col3:
                    st.metric("BMI", selected['bmi'])
                    st.metric("Snoring", selected['snoring'])
                
                st.markdown("---")
                st.subheader("Diagnosis & Severity")
                
                severity_color = {
                    "Low": "🟢",
                    "Moderate": "🟡",
                    "High": "🔴",
                    "Critical": "⛔"
                }
                
                st.info(f"{severity_color.get(selected['severity'], '❓')} {selected['diagnosis']}")
                st.info(f"**Severity Level:** {selected['severity']}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📥 Download Patient Report (PDF)", use_container_width=True):
                        pdf_data = generate_pdf_report(selected, selected)
                        st.download_button(
                            label="📄 Download",
                            data=pdf_data,
                            file_name=f"Patient_Report_{selected['id']}.pdf",
                            mime="application/pdf"
                        )
                
                with col2:
                    if st.button("📞 Call Patient", use_container_width=True, disabled=not selected['phone']):
                        st.info(f"📞 Calling: {selected['phone']}")
                
                with col3:
                    if st.button("📧 Send Email", use_container_width=True):
                        st.info(f"📧 Email would be sent to: {selected['email']}")
            else:
                st.info("No records match the selected filters.")
        else:
            st.info("📭 No analysis records in the system yet.")
    
    # ========== TAB 2: URGENT Cases ==========
    with tab2:
        st.subheader("🚨 URGENT Cases (High & Critical Risk)")
        
        urgent_cases = [h for h in history if h['severity'] in ['High', 'Critical']]
        
        if urgent_cases:
            # Sort by timestamp (most recent first)
            urgent_cases = sorted(urgent_cases, key=lambda x: x['timestamp'], reverse=True)
            
            for i, case in enumerate(urgent_cases):
                with st.container():
                    col1, col2, col3 = st.columns([2, 2, 2])
                    
                    with col1:
                        severity_emoji = "⛔" if case['severity'] == "Critical" else "🔴"
                        st.warning(f"{severity_emoji} **{case['email']}**")
                        st.text(f"Phone: {case['phone']}")
                        st.text(f"Age: {case['age']}")
                    
                    with col2:
                        st.text(f"📝 {case['diagnosis']}")
                        st.text(f"⏰ {case['timestamp']}")
                    
                    with col3:
                        if st.button("👁️ View Details", key=f"urgent_{i}"):
                            st.session_state.selected_urgent = case
                    
                    st.markdown("---")
        else:
            st.success("✅ No urgent cases at the moment!")
    
    # ========== TAB 3: Statistics ==========
    with tab3:
        st.subheader("📊 Analytics & Statistics")
        
        if history:
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Analyses", len(history))
            
            with col2:
                critical_count = len([h for h in history if h['severity'] == 'Critical'])
                st.metric("Critical Cases", critical_count)
            
            with col3:
                high_count = len([h for h in history if h['severity'] == 'High'])
                st.metric("High Risk Cases", high_count)
            
            with col4:
                unique_patients = len(set([h['email'] for h in history]))
                st.metric("Unique Patients", unique_patients)
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Severity distribution
                severity_counts = pd.Series([h['severity'] for h in history]).value_counts()
                st.bar_chart(severity_counts, use_container_width=True)
                st.caption("Cases by Severity")
            
            with col2:
                # Diagnosis distribution
                diagnosis_counts = pd.Series([h['prediction'] for h in history]).value_counts()
                st.bar_chart(diagnosis_counts, use_container_width=True)
                st.caption("Cases by Disorder Type")
        else:
            st.info("No data available for statistics.")

# ============================================================================
# MAIN ROUTER
# ============================================================================

def main():
    """Main application router"""
    if not model_loaded and st.session_state.logged_in:
        st.error(f"⚠️ Model loading error: {error_msg}")
        st.info("The model files (ml/model.pkl and ml/scaler.pkl) are missing or corrupted.")
        st.stop()
    
    # Route to appropriate page
    if not st.session_state.logged_in:
        if st.session_state.page == "register":
            page_user_register()
        elif st.session_state.page == "admin_login":
            page_admin_login()
        else:
            page_user_login()
    else:  # User is logged in
        if st.session_state.user_role == "user":
            page_user_dashboard()
        elif st.session_state.user_role == "admin":
            page_admin_portal()
        else:
            st.error("❌ Invalid role. Please login again.")

if __name__ == "__main__":
    main()
