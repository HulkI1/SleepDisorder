# 🛠️ Technical Documentation - Sleep Disorder Analysis Platform

Complete technical reference for developers and system administrators.

---

## 📚 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Code Structure](#-code-structure)
- [API Reference](#-api-reference)
- [Database Schema](#-database-schema)
- [Authentication Flow](#-authentication-flow)
- [ML Pipeline](#-ml-pipeline)
- [Extending the Application](#-extending-the-application)
- [Performance Optimization](#-performance-optimization)

---

## 🏗️ Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────┐
│         Frontend (Streamlit Web UI)                 │
├─────────────────────────────────────────────────────┤
│  - User Registration/Login                          │
│  - Sleep Analysis Form                              │
│  - History Dashboard                                │
│  - PDF Report Generation                            │
│  - Admin Portal                                     │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│      Application Layer (app_main.py)                │
├─────────────────────────────────────────────────────┤
│  - Session Management                               │
│  - Form Validation                                  │
│  - Authentication Logic                             │
│  - Report Generation                                │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    ┌────────┐ ┌────────┐ ┌────────┐
    │ ML     │ │ Data   │ │ PDF    │
    │ Model  │ │Storage │ │Engine  │
    │(model. │ │(JSON)  │ │(Report │
    │ pkl)   │ │        │ │Lab)    │
    └────────┘ └────────┘ └────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit | Web UI Framework |
| **Backend** | Python | Core Application Logic |
| **ML** | Scikit-Learn | Machine Learning Models |
| **Data** | JSON Files | User & Analysis Storage |
| **Reports** | ReportLab | PDF Generation |
| **Deployment** | Docker/Cloud | Production Hosting |

---

## 📁 Code Structure

### Main Application Flow

```
app_main.py
├── Configuration & Setup (Lines 1-100)
│   ├── Imports
│   ├── Page configuration
│   ├── File paths
│   └── Model loading
│
├── Utility Functions (Lines 100-300)
│   ├── Password hashing
│   ├── File I/O
│   ├── Predictions
│   └── PDF generation
│
├── Session State Management (Lines 300-320)
│   └── Session initialization
│
├── Authentication Pages (Lines 320-500)
│   ├── User login
│   ├── User registration
│   └── Admin login
│
├── User Dashboard (Lines 500-750)
│   ├── Sleep analysis form
│   ├── Analysis history
│   └── Report generation
│
├── Admin Portal (Lines 750-1000)
│   ├── Patient search
│   ├── Urgent cases
│   └── Analytics
│
└── Main Router (Lines 1000-1100)
    └── Page routing logic
```

---

## 🔌 API Reference

### Core Functions

#### Authentication Functions

```python
def hash_password(password: str) -> str
```
- **Purpose:** Hash password using SHA-256
- **Parameters:** 
  - `password` (str): Plain text password
- **Returns:** Hashed password string
- **Example:**
  ```python
  hashed = hash_password("mypassword123")
  ```

```python
def verify_password(password: str, hashed: str) -> bool
```
- **Purpose:** Verify password against hash
- **Parameters:**
  - `password` (str): Plain text password to verify
  - `hashed` (str): Stored hash
- **Returns:** True/False
- **Example:**
  ```python
  if verify_password("mypassword123", stored_hash):
      login_user()
  ```

#### Data Management Functions

```python
def load_users() -> dict
```
- **Purpose:** Load user database from JSON
- **Returns:** Dictionary of users
- **Example:**
  ```python
  users = load_users()
  if "user@example.com" in users:
      print("User exists")
  ```

```python
def save_users(users: dict)
```
- **Purpose:** Save users to JSON file
- **Parameters:**
  - `users` (dict): User database
- **Example:**
  ```python
  users['newuser@example.com'] = {
      'password': hash_password('pass'),
      'phone': '1234567890'
  }
  save_users(users)
  ```

```python
def load_analysis_history() -> list
```
- **Purpose:** Load analysis history from JSON
- **Returns:** List of analysis records
- **Example:**
  ```python
  history = load_analysis_history()
  for record in history:
      print(record['diagnosis'])
  ```

#### ML Prediction Functions

```python
def predict_disorder(features: list) -> tuple
```
- **Purpose:** Predict sleep disorder from features
- **Parameters:**
  - `features` (list): 9 feature values
    - Index 0: sleep_duration (float)
    - Index 1: stress (int 1-10)
    - Index 2: age (int)
    - Index 3: blood_pressure_avg (float)
    - Index 4: heart_rate (int)
    - Index 5: tea_coffee (0/1)
    - Index 6: bmi (float)
    - Index 7: snoring (0/1)
    - Index 8: work_hours (int)
- **Returns:** (prediction, diagnosis_text, severity)
- **Example:**
  ```python
  features = [7.0, 5, 35, 120, 75, 0, 25, 0, 8]
  pred, diag, sev = predict_disorder(features)
  # Returns: (0, "✅ No sleep disorder detected", "Low")
  ```

#### PDF Generation Function

```python
def generate_pdf_report(user_data: dict, analysis_result: dict) -> bytes
```
- **Purpose:** Generate PDF medical report
- **Parameters:**
  - `user_data` (dict): Patient information
  - `analysis_result` (dict): Analysis data
- **Returns:** PDF bytes
- **Example:**
  ```python
  pdf = generate_pdf_report(user_data, analysis)
  st.download_button("Download PDF", pdf)
  ```

---

## 💾 Data Schema

### Users JSON Structure

**File:** `data/users.json`

```json
{
  "user@example.com": {
    "password": "sha256_hash_here",
    "phone": "9876543210",
    "created_at": "2024-01-15T10:30:00"
  },
  "doctor@hospital.com": {
    "password": "sha256_hash_here",
    "phone": "9876543211",
    "created_at": "2024-01-15T11:00:00"
  }
}
```

### Analysis History JSON Structure

**File:** `data/analysis_history.json`

```json
[
  {
    "id": "user@example.com_20240115_103045",
    "email": "user@example.com",
    "phone": "9876543210",
    "age": 35,
    "gender": "Male",
    "occupation": "Engineer",
    "stress": 7,
    "bp": "130/85",
    "heart_rate": 92,
    "sleep_duration": 6.5,
    "bmi": 26.0,
    "snoring": "Yes",
    "work_hours": 10,
    "diagnosis": "⚠️ Moderate Risk: Sleep Deprivation",
    "prediction": 1,
    "severity": "Moderate",
    "timestamp": "2024-01-15T10:30:45"
  }
]
```

---

## 🔐 Authentication Flow

### User Registration Flow

```
User Registration Form
        │
        ▼
  Validate Input
  (email, password, phone)
        │
        ▼
  Check Email Not Exists
        │
        ▼
  Hash Password (SHA-256)
        │
        ▼
  Save to users.json
        │
        ▼
  Show Success Message
        │
        ▼
  Redirect to Login
```

### User Login Flow

```
Login Form
    │
    ▼
Validate Input
(email, password)
    │
    ▼
Load users.json
    │
    ▼
Find Email
    │
    ├─ NOT FOUND ──→ Error Message
    │
    ├─ FOUND
    │    │
    │    ▼
    │  Verify Password Hash
    │    │
    │    ├─ MISMATCH ──→ Error Message
    │    │
    │    ├─ MATCH
    │         │
    │         ▼
    │    Set Session State:
    │    - logged_in = True
    │    - user_email = email
    │    - user_role = "user"
    │         │
    │         ▼
    │    Load User Dashboard
```

### Admin Authentication Flow

```
Admin Login Form
      │
      ▼
Enter Admin Password
      │
      ▼
Compare with ADMIN_PASSWORD
      │
      ├─ MISMATCH ──→ Error
      │
      ├─ MATCH
           │
           ▼
      Set Session State:
      - logged_in = True
      - user_role = "admin"
           │
           ▼
      Load Admin Portal
```

---

## 🤖 ML Pipeline

### Model Training Pipeline

```
1. Feature Generation
   └─ 1000 synthetic samples
      └─ 9 features per sample

2. Target Classification
   └─ Calculate risk score:
      ├─ Sleep duration (weight: 2x)
      ├─ Stress level (weight: 1x)
      ├─ Heart rate (weight: 1.5x)
      ├─ Snoring (weight: 2x)
      ├─ BMI (weight: 0.5-1x)
      ├─ Age (weight: 0.5x)
      ├─ Blood pressure (weight: 1x)
      └─ Work hours (weight: 1x)

3. Target Mapping
   └─ risk_score → class:
      ├─ < 1.0 → 0 (Normal)
      ├─ 1.0-2.5 → 1 (Sleep Deprivation)
      ├─ 2.5-4.0 → 2 (Insomnia)
      └─ ≥ 4.0 → 3 (Sleep Apnea)

4. Feature Scaling
   └─ StandardScaler
      ├─ Fit on training data
      └─ Transform train & test

5. Model Training
   └─ RandomForestClassifier
      ├─ n_estimators: 150
      ├─ max_depth: 15
      ├─ Training accuracy: 99.1%
      └─ Test accuracy: 78.5%

6. Model Serialization
   └─ joblib.dump()
      ├─ Save model.pkl
      └─ Save scaler.pkl
```

### Prediction Pipeline

```
User Input (9 features)
        │
        ▼
Load Scaler
        │
        ▼
Scale Features
(StandardScaler.transform)
        │
        ▼
Load Model
        │
        ▼
Predict Class
(model.predict)
        │
        ▼
Map Class to Diagnosis:
0 → Normal (Low)
1 → Sleep Deprivation (Moderate)
2 → Chronic Insomnia (High)
3 → Sleep Apnea (Critical)
        │
        ▼
Return (pred, diagnosis, severity)
```

---

## 🔧 Extending the Application

### Adding New Features

#### 1. Add New Sleep Analysis Field

**Step 1:** Add to form (app_main.py, ~line 550)
```python
new_field = st.number_input("New Field Label", min_value=0, max_value=100)
```

**Step 2:** Add to features list (app_main.py, ~line 600)
```python
features = [
    sleep_duration, stress, age, bp_avg, heart_rate,
    0, bmi, snoring_binary, work_hours,
    new_field  # Add new feature
]
```

**Step 3:** Retrain model (train_model.py)
- Add feature to dataset generation
- Update feature count in prediction function
- Run: `python train_model.py`

#### 2. Add New Disorder Category

**Step 1:** Update classify_disorder function (train_model.py)
```python
def classify_disorder(row):
    risk_score = # ... calculate
    if risk_score < 1:
        return 0  # Normal
    elif risk_score < 2:
        return 1  # New Category 1
    # ... etc
```

**Step 2:** Update disorder_map (app_main.py, ~line 270)
```python
disorder_map = {
    0: ("Normal", "✅ No sleep disorder detected", "Low"),
    1: ("New Disorder", "Description", "Severity"),
    # ... etc
}
```

**Step 3:** Retrain and restart app

#### 3. Add Email Notifications

**Install:** `pip install smtplib`

**Add function (app_main.py):**
```python
import smtplib
from email.mime.text import MIMEText

def send_email_alert(recipient, subject, body):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)
```

**Usage:**
```python
send_email_alert(email, 
                 "Sleep Analysis Result",
                 f"Your diagnosis: {diagnosis}")
```

#### 4. Add Database Support

**Install:** `pip install sqlalchemy psycopg2-binary`

**Replace JSON with database:**
```python
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    email = Column(String(255), primary_key=True)
    password = Column(String(255))
    phone = Column(String(20))

class Analysis(Base):
    __tablename__ = 'analysis'
    id = Column(String(255), primary_key=True)
    email = Column(String(255))
    diagnosis = Column(String(100))
    # ... other columns

# Create engine
engine = create_engine('postgresql://user:pass@localhost/db')
Base.metadata.create_all(engine)
```

---

## ⚡ Performance Optimization

### 1. Model Caching

```python
@st.cache_resource
def load_models():
    model = joblib.load("ml/model.pkl")
    scaler = joblib.load("ml/scaler.pkl")
    return model, scaler

model, scaler = load_models()
```

### 2. Data Caching

```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_analysis_history():
    return load_analysis_history()
```

### 3. Lazy Loading

```python
# Don't load all analyses if not needed
def get_user_analyses(email):
    history = load_analysis_history()
    return [h for h in history if h['email'] == email]
```

### 4. Index Commonly Accessed Data

```python
def build_email_index(history):
    """Build index for fast email lookup"""
    index = {}
    for record in history:
        email = record['email']
        if email not in index:
            index[email] = []
        index[email].append(record)
    return index
```

---

## 🧪 Testing

### Unit Tests

```python
# tests/test_auth.py
def test_password_hashing():
    password = "test123"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)

def test_user_registration():
    users = load_users()
    initial_count = len(users)
    users['test@example.com'] = {
        'password': hash_password('pass'),
        'phone': '123'
    }
    save_users(users)
    assert len(load_users()) == initial_count + 1
```

### Integration Tests

```python
# tests/test_prediction.py
def test_ml_prediction():
    features = [7.0, 5, 35, 120, 75, 0, 25, 0, 8]
    pred, diag, sev = predict_disorder(features)
    assert pred in [0, 1, 2, 3]
    assert sev in ["Low", "Moderate", "High", "Critical"]
```

---

## 📊 Monitoring & Metrics

### Key Performance Indicators

```python
# Log important metrics
def log_prediction(email, diagnosis, severity):
    metrics = {
        'timestamp': datetime.now(),
        'email': email,
        'diagnosis': diagnosis,
        'severity': severity
    }
    # Write to metrics.log
```

### Analysis by Severity

```python
def get_severity_stats():
    history = load_analysis_history()
    stats = {}
    for record in history:
        severity = record['severity']
        stats[severity] = stats.get(severity, 0) + 1
    return stats
```

---

## 📞 Support & Debugging

### Enable Debug Mode

```python
# In app_main.py
DEBUG = os.getenv("DEBUG", "False") == "True"
if DEBUG:
    st.write("DEBUG MODE - Session State:")
    st.write(st.session_state)
```

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| ModelNotFound | ml/ files missing | Run train_model.py |
| JSONError | Corrupted data file | Delete & let app recreate |
| MemoryError | Too large dataset | Implement pagination |
| SlowPrediction | Model loading | Use @st.cache_resource |

---

**For more support, check README.md and DEPLOYMENT.md**
