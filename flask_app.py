"""
Sleep Disorder Analysis Platform - Flask Web Application
Modern web-based interface with HTML templates
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import datetime
import joblib
import numpy as np
from functools import wraps

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
app.secret_key = 'sleep_disorder_secret_key_2025'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600

# Initialize session management
try:
    from flask_session import Session
    Session(app)
except ImportError:
    # Fallback to built-in Flask sessions if flask_session not available
    pass

# File paths
USERS_FILE = "data/users.json"
ANALYSIS_FILE = "data/analysis_history.json"
ADMIN_PASSWORD = "admin123"

# Create data directory
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
# DATA MANAGEMENT FUNCTIONS
# ============================================================================

def load_users():
    """Load users from JSON"""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    """Save users to JSON"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_analysis():
    """Load analysis history from JSON"""
    if not os.path.exists(ANALYSIS_FILE):
        return []
    try:
        with open(ANALYSIS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_analysis(data):
    """Save analysis to JSON"""
    with open(ANALYSIS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ============================================================================
# AUTHENTICATION DECORATORS
# ============================================================================

def login_required(f):
    """Require user login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session or not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# AUTH ROUTES
# ============================================================================

@app.route('/')
def index():
    """Home page"""
    if 'user_email' in session:
        return redirect(url_for('dashboard'))
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.form
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm = data.get('confirm_password', '')
        phone = data.get('phone', '').strip()

        # Validation
        if not all([email, password, confirm, phone]):
            return render_template('register.html', error='All fields required')
        if password != confirm:
            return render_template('register.html', error='Passwords do not match')
        if len(password) < 6:
            return render_template('register.html', error='Password must be 6+ characters')

        users = load_users()
        if email in users:
            return render_template('register.html', error='Email already registered')

        # Create user
        users[email] = {
            'password': generate_password_hash(password),
            'phone': phone,
            'created_at': datetime.now().isoformat()
        }
        save_users(users)
        return redirect(url_for('login_redirect', msg='Account created! Please login.'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        users = load_users()
        if email in users and check_password_hash(users[email]['password'], password):
            session['user_email'] = email
            session['user_phone'] = users[email].get('phone', '')
            session.permanent = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@app.route('/login-redirect')
def login_redirect():
    """Redirect after registration"""
    msg = request.args.get('msg', '')
    return render_template('login.html', message=msg)

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('login'))

# ============================================================================
# USER DASHBOARD & FUNCTIONALITY
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html', email=session.get('user_email'))

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    """Make prediction"""
    if not model_loaded:
        return jsonify({'error': 'Model not available'}), 500

    try:
        data = request.form
        email = session.get('user_email')

        # Extract and validate features
        sleep_duration = float(data.get('sleep_duration', 0))
        stress = int(data.get('stress', 5))
        age = int(data.get('age', 30))
        
        # Parse blood pressure
        bp_str = data.get('bp', '120/80')
        if '/' in bp_str:
            s, d = bp_str.split('/')
            bp_avg = (float(s) + float(d)) / 2
        else:
            bp_avg = float(bp_str)
        
        heart_rate = int(data.get('heart_rate', 75))
        tea_coffee = int(data.get('tea_coffee', 0))
        
        # BMI category to number
        bmi_map = {'Normal': 22, 'Overweight': 28, 'Obese': 32}
        bmi = bmi_map.get(data.get('bmi', 'Normal'), 22)
        
        # Snoring to binary
        snoring_map = {'Never': 0, 'Sometimes': 0.5, 'Every Night': 1}
        snoring = snoring_map.get(data.get('snoring', 'Never'), 0)
        
        work_hours = int(data.get('work_hours', 8))

        # Create feature array
        features = [sleep_duration, stress, age, bp_avg, heart_rate, tea_coffee, bmi, snoring, work_hours]

        # Scale and predict
        features_scaled = scaler.transform([features])
        prediction = int(model.predict(features_scaled)[0])

        # Map prediction
        disorder_map = {
            0: ('Normal', 'No sleep disorder detected', 'green'),
            1: ('Sleep Deprivation', 'Moderate Risk: Sleep Deprivation', 'orange'),
            2: ('Chronic Insomnia', 'High Risk: Chronic Insomnia', 'red'),
            3: ('Sleep Apnea', 'Critical Risk: Possible Sleep Apnea', 'darkred')
        }

        diagnosis, full_text, severity_color = disorder_map.get(prediction, ('Unknown', 'Unknown', 'gray'))

        # Save to history
        record = {
            'id': f"{email}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'email': email,
            'phone': data.get('phone_number', ''),
            'age': age,
            'gender': data.get('gender', ''),
            'occupation': data.get('occupation', ''),
            'stress': stress,
            'bp': bp_str,
            'heart_rate': heart_rate,
            'sleep_duration': sleep_duration,
            'bmi': data.get('bmi', ''),
            'snoring': data.get('snoring', ''),
            'work_hours': work_hours,
            'diagnosis': diagnosis,
            'full_diagnosis': full_text,
            'prediction': prediction,
            'severity_color': severity_color,
            'timestamp': datetime.now().isoformat()
        }

        history = load_analysis()
        history.append(record)
        save_analysis(history)

        return jsonify({
            'success': True,
            'diagnosis': diagnosis,
            'full_text': full_text,
            'color': severity_color,
            'timestamp': record['timestamp']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/analysis-history')
@login_required
def get_history():
    """Get user's analysis history"""
    email = session.get('user_email')
    history = load_analysis()
    user_history = [h for h in history if h['email'] == email]
    return jsonify(user_history)

@app.route('/download-pdf/<record_id>')
@login_required
def download_pdf(record_id):
    """Download PDF report"""
    email = session.get('user_email')
    history = load_analysis()
    record = next((h for h in history if h['id'] == record_id and h['email'] == email), None)
    
    if not record:
        return jsonify({'error': 'Report not found'}), 404

    # Generate simple PDF
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        import io

        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Title
        title = Paragraph("SLEEP ANALYSIS MEDICAL REPORT", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.3*inch))

        # Patient Info
        story.append(Paragraph(f"<b>Patient Email:</b> {record['email']}", styles['Normal']))
        story.append(Paragraph(f"<b>Date:</b> {record['timestamp']}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

        # Data Table
        data = [
            ['Metric', 'Value'],
            ['Age', str(record['age'])],
            ['Gender', record['gender']],
            ['Sleep Duration', f"{record['sleep_duration']} hrs"],
            ['Stress Level', str(record['stress'])],
            ['Heart Rate', f"{record['heart_rate']} bpm"],
            ['Blood Pressure', record['bp']],
            ['Snoring', record['snoring']],
        ]
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))

        # Diagnosis
        story.append(Paragraph(f"<b>Diagnosis:</b> {record['full_diagnosis']}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

        # Disclaimer
        disclaimer = Paragraph(
            "<i><font size='8'>DISCLAIMER: This report is generated by an automated system. "
            "Please consult a healthcare provider for professional medical advice.</font></i>",
            styles['Normal']
        )
        story.append(disclaimer)

        doc.build(story)
        pdf_buffer.seek(0)
        
        from flask import send_file
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"Sleep_Report_{record['id']}.pdf"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# ADMIN ROUTES
# ============================================================================

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session.permanent = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid password')

    return render_template('admin_login.html')

@app.route('/admin-dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    return render_template('admin_dashboard.html')

@app.route('/admin-reports')
@admin_required
def admin_reports():
    """Get all reports for admin"""
    history = load_analysis()
    
    # Sort by timestamp, most recent first
    history = sorted(history, key=lambda x: x['timestamp'], reverse=True)
    
    return jsonify(history)

@app.route('/admin-reports-filtered')
@admin_required
def admin_reports_filtered():
    """Get filtered reports"""
    severity = request.args.get('severity', '')
    email = request.args.get('email', '')
    
    history = load_analysis()
    
    if severity and severity != 'all':
        history = [h for h in history if h['severity_color'] == convert_severity(severity)]
    
    if email:
        history = [h for h in history if email.lower() in h['email'].lower()]
    
    history = sorted(history, key=lambda x: x['timestamp'], reverse=True)
    return jsonify(history)

@app.route('/admin-urgent')
@admin_required
def admin_urgent():
    """Get urgent cases"""
    history = load_analysis()
    urgent = [h for h in history if h['severity_color'] in ['red', 'darkred']]
    urgent = sorted(urgent, key=lambda x: x['timestamp'], reverse=True)
    return jsonify(urgent)

@app.route('/admin-report/<report_id>')
@admin_required
def admin_report(report_id):
    """View specific report"""
    history = load_analysis()
    report = next((h for h in history if h['id'] == report_id), None)
    
    if not report:
        return jsonify({'error': 'Report not found'}), 404
    
    return jsonify(report)

@app.route('/admin-stats')
@admin_required
def admin_stats():
    """Get admin statistics"""
    history = load_analysis()
    
    stats = {
        'total': len(history),
        'critical': len([h for h in history if h['severity_color'] == 'darkred']),
        'high_risk': len([h for h in history if h['severity_color'] == 'red']),
        'moderate': len([h for h in history if h['severity_color'] == 'orange']),
        'normal': len([h for h in history if h['severity_color'] == 'green']),
        'unique_patients': len(set([h['email'] for h in history]))
    }
    
    return jsonify(stats)

@app.route('/admin-logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def convert_severity(color_name):
    """Convert color name to color code"""
    colors_map = {
        'critical': 'darkred',
        'high': 'red',
        'moderate': 'orange',
        'normal': 'green'
    }
    return colors_map.get(color_name, '')

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """500 error handler"""
    return render_template('500.html'), 500

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, port=5000)
