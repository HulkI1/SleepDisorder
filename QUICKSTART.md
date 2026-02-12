# 🚀 Quick Start Guide - Sleep Disorder Analysis Platform

Get up and running in **5 minutes**!

---

## ⚡ Quick Setup

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Train the ML Model
```bash
python train_model.py
```
**Output:** Creates `ml/model.pkl` and `ml/scaler.pkl`

### 3️⃣ Start the Application
```bash
streamlit run app_main.py
```

**That's it!** 🎉 Your app is running at: `http://localhost:8501`

---

## 🧪 Test the Application

### Test User Registration & Login

**1. Register a new user:**
- Click **📝 Register**
- Email: `test@example.com`
- Password: `test123`
- Phone: `9876543210`
- Click **✅ Create Account**

**2. Login:**
- Email: `test@example.com`
- Password: `test123`
- Click **🔐 Login**

✅ You're now in the **User Dashboard**

---

### Test Sleep Analysis

**Fill the form with sample data:**
```
Phone Number:      9876543210
Age:               35
Gender:            Male
Occupation:        Software Engineer
Stress Level:      7 (slider)
Blood Pressure:    130/85
Heart Rate:        92
Sleep Duration:    6.5
BMI:               26
Snoring:           Yes
Work Hours:        10
```

**Click 🔮 Generate Prediction**

Expected Result: One of these diagnoses:
- ✅ Normal
- ⚠️ Sleep Deprivation
- 🔴 Chronic Insomnia
- ⛔ Sleep Apnea

---

### View Analysis History

**Click 📊 Analysis History tab:**
- See your analysis in the table
- Click to expand and view details
- Metrics shown: Sleep duration, heart rate, stress, BMI, age, etc.

---

### Generate PDF Report

**Click 📄 Generate Report tab:**
- Select your analysis from dropdown
- Click **📥 Download Medical Report (PDF)**
- PDF will download with:
  - Patient information
  - Sleep data
  - Diagnosis
  - Medical disclaimer

---

### Test Admin Portal

**1. Click 🔑 Admin Login**

**2. Enter Password:** `admin123`

**3. Click 🔓 Admin Login**

**4. You're now in Admin Portal with 3 tabs:**

#### Tab 1: 👥 All Patient Analyses
- See all users' analyses
- Filter by severity
- Search by email
- View patient details
- Download patient reports

#### Tab 2: 🔴 URGENT Cases
- See HIGH & CRITICAL risk patients
- Most recent first
- Click to view patient details

#### Tab 3: 📊 Statistics
- Total analyses count
- Critical cases count
- High risk cases count
- Charts for analysis

---

## 📊 Feature Checklist

| Feature | Default State | How to Test |
|---------|---------------|------------|
| Registration | ✅ Working | Click Register, fill form |
| Login | ✅ Working | Use test@example.com / test123 |
| Sleep Form | ✅ Working | Enter data, click Predict |
| ML Prediction | ✅ Working | Check diagnosis result |
| History | ✅ Working | Click History tab |
| PDF Reports | ✅ Working | Click Generate Report tab |
| Admin Panel | ✅ Working | Use password: admin123 |
| Urgent Cases | ✅ Working | Appears in Admin portal |

---

## 🔑 Test Credentials

### User Account
```
Email:    test@example.com
Password: test123
Phone:    9876543210
```

### Admin Account
```
Password: admin123
```

---

## 📁 Data Files (Auto-Created)

After first run, these files will be created:

```
data/
├── users.json              # User credentials & info
└── analysis_history.json   # All patient analyses
```

These files store all app data. **Backup them regularly!**

---

## 🐛 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Model loading error" | Run `python train_model.py` |
| No analyses showing | Create a new analysis first |
| Admin login fails | Password is exactly `admin123` |
| PDF not downloading | Ensure `reportlab` is installed |
| Page not responding | Restart app: `streamlit run app_main.py` |

---

## 💡 Pro Tips

1. **Create multiple test accounts** to simulate different patients
2. **Try different sleep metrics** to see how predictions change
3. **Admin filter by severity** to find critical cases
4. **Download PDFs** to verify formatting
5. **Check JSON files** in `data/` to see stored data structure

---

## 📈 Next: Advanced Usage

After testing, explore:
- Modify `ADMIN_PASSWORD` in app_main.py
- Customize disorder risk thresholds
- Change feature importance weights
- Train with your own dataset

---

## ✅ What's Working

✔ Full user authentication system  
✔ Secure password hashing  
✔ Sleep analysis form with validation  
✔ ML predictions with 78.5% accuracy  
✔ Analysis history storage  
✔ PDF medical report generation  
✔ Complete admin portal  
✔ URGENT case alerts  
✔ Analytics dashboard  
✔ Session management & logout  

---

**🎉 You're ready to go!**

Start with: `streamlit run app_main.py`

Questions? Check the full README.md for detailed documentation.
