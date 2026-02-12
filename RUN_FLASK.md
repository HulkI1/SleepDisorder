# Flask Web Application - Quick Start Guide

## 🚀 Running the Flask Application

### Option 1: Direct Execution (Recommended for Development)

```bash
cd /workspaces/SleepDisorder
python flask_app.py
```

The server will start on **http://localhost:5000**

### Option 2: Using Gunicorn (For Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
```

## 📋 Application Structure

```
flask_app.py                          # Main Flask application (450+ lines)
├── Configuration & Setup
├── Data Management (Users, Analysis)
├── Authentication Routes
│   ├── /register              (GET, POST)   - New user registration
│   ├── /login                 (GET, POST)   - User login
│   ├── /logout                (GET)         - Logout
│   └── /login-redirect        (GET)         - Redirect handling
├── User Routes
│   ├── /dashboard             (GET)         - Main user dashboard
│   ├── /predict               (POST)        - ML prediction
│   ├── /analysis-history      (GET)         - JSON: user's analyses
│   └── /download-pdf/<id>     (GET)         - PDF report download
├── Admin Routes
│   ├── /admin-login           (GET, POST)   - Admin authentication
│   ├── /admin-dashboard       (GET)         - Admin dashboard
│   ├── /admin-reports         (GET)         - JSON: all patient reports
│   ├── /admin-reports-filtered (POST)       - JSON: filtered reports
│   ├── /admin-urgent          (GET)         - JSON: urgent cases
│   ├── /admin-stats           (GET)         - JSON: statistics
│   ├── /admin-report/<id>     (GET)         - JSON: specific report
│   └── /admin-logout          (GET)         - Admin logout
├── Error Handlers
│   ├── 404 Error Page         - Not Found
│   └── 500 Error Page         - Server Error
└── Helper Functions
    ├── load_users()           - Load user data
    ├── save_users()           - Save user data
    ├── load_analysis()        - Load analysis history
    ├── save_analysis()        - Save analysis
    ├── @login_required        - User authentication decorator
    └── @admin_required        - Admin authentication decorator

templates/                                # HTML templates
├── dashboard.html             - User dashboard with form & history
├── login.html                 - User login page
├── register.html              - User registration page
├── admin_login.html           - Admin login page
├── admin_dashboard.html       - Admin management interface
├── 404.html                   - Page not found
└── 500.html                   - Server error page
```

## 🔐 Test Credentials

### User Registration
1. Go to http://localhost:5000/register
2. Add new user:
   - Email: `test@example.com`
   - Phone: `+1234567890`
   - Password: `Test@123`

### User Login
1. Go to http://localhost:5000/login
2. Email: `test@example.com`
3. Password: `Test@123`

### Admin Portal
1. Go to http://localhost:5000/admin-login
2. Password: `admin123`

## 📊 Sleep Analysis Form Fields

When logged in, you can analyze sleep with these parameters:

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| Phone | Text | - | Patient contact |
| Age | Number | 1-100 | Patient age |
| Gender | Select | M/F | Gender |
| Occupation | Text | - | Job type |
| Stress Level | Number | 1-10 | Stress rating |
| Blood Pressure | Number | 60-200 | Systolic BP |
| Heart Rate | Number | 40-200 | Beats per minute |
| Sleep Duration | Number | 0-12 | Hours per night |
| Tea Coffee | Number | 0-10 | Daily cups |
| BMI | Number | 10-50 | Body mass index |

## 🔍 Admin Features

### All Patients Tab
- View all patient records in a table format
- Search by email
- Filter by severity: All/Critical/High/Moderate/Normal
- Download PDF reports for each patient

### URGENT Cases Tab
- See critical and high-risk cases highlighted
- Quick overview of urgent patients
- Immediate action items

### Statistics Tab
- Total patients analyzed
- Critical case count
- High-risk patients
- Moderate risk count
- Normal cases
- Unique patient count

## 📈 ML Model

**Model Used**: Random Forest Classifier
- **Training Accuracy**: 99.1%
- **Test Accuracy**: 78.5%
- **Features**: 9 sleep-related parameters
- **Classes**: 4 sleep disorders
  - 0: Normal Sleep
  - 1: Sleep Deprivation
  - 2: Insomnia
  - 3: Sleep Apnea

## 💾 Data Storage

- **Users**: `data/users.json`
- **Analysis History**: `data/analysis_history.json`
- **ML Models**: `ml/model.pkl`, `ml/scaler.pkl`

## 🛠️ Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -i :5000
kill -9 <PID>
```

### Module Not Found Errors
```bash
cd /workspaces/SleepDisorder
pip install -r requirements.txt
```

### Data Files Missing
The app creates `data/` directory automatically on first run.

### Templates Not Found
Ensure `templates/` directory exists with all .html files

## 🌐 Browser Access

Open any of these URLs in your browser:

1. **User Dashboard**: http://localhost:5000/dashboard
2. **User Login**: http://localhost:5000/login
3. **Registration**: http://localhost:5000/register
4. **Admin Portal**: http://localhost:5000/admin-login

## 📦 Dependencies

All dependencies are in `requirements.txt`:
```
Flask==3.1.2
Flask-Session==0.5.0
scikit-learn==1.8.0
joblib==1.5.3
reportlab==4.0.9
pandas==2.3.3
numpy==2.4.2
werkzeug==3.0.0  (included with Flask)
```

## 🔗 Environment

- **Python Version**: 3.8+
- **OS**: Cross-platform (Linux, macOS, Windows)
- **Web Server**: Flask Built-in Development Server
- **Production**: Use Gunicorn or similar WSGI server

## 📞 Support

For any issues:
1. Check the console output for error messages
2. Verify all data files exist in `data/` directory
3. Ensure all templates are in `templates/` directory
4. Check that ML models are in `ml/` directory
