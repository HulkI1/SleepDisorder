"""
Model training script for Sleep Disorder Prediction
This script trains and saves the ML model and scaler for the Streamlit app.
Sleep Disorder Categories:
- 0: Normal (No sleep disorder)
- 1: Sleep Deprivation (Moderate Risk)
- 2: Chronic Insomnia (High Risk)
- 3: Obstructive Sleep Apnea (Critical Risk)
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Create ml directory if it doesn't exist
os.makedirs("ml", exist_ok=True)

# Generate sample sleep disorder dataset
# Feature order: sleep_duration, stress, age, blood_pressure_avg, heart_rate, tea_coffee, bmi, snoring, work_hours
np.random.seed(42)
n_samples = 1000

data = {
    'sleep_duration': np.random.uniform(3, 10, n_samples),
    'stress': np.random.randint(1, 11, n_samples),
    'age': np.random.randint(20, 80, n_samples),
    'blood_pressure_avg': np.random.uniform(80, 160, n_samples),
    'heart_rate': np.random.randint(50, 150, n_samples),
    'tea_coffee': np.random.randint(0, 2, n_samples),
    'bmi': np.random.uniform(18, 40, n_samples),
    'snoring': np.random.randint(0, 2, n_samples),
    'work_hours': np.random.randint(0, 16, n_samples),
}

df = pd.DataFrame(data)

# Create target variable (sleep disorder classification)
# Smart classification logic combining multiple risk factors
def classify_disorder(row):
    """
    Classify sleep disorder severity based on multiple factors
    Returns: 0 = Normal, 1 = Sleep Deprivation, 2 = Insomnia, 3 = Sleep Apnea
    """
    risk_score = 0
    
    # Sleep duration risk (critical factor)
    if row['sleep_duration'] < 4:
        risk_score += 2  # Severe sleep deprivation
    elif row['sleep_duration'] < 6:
        risk_score += 1  # Moderate sleep deprivation
    
    # Stress impact
    if row['stress'] > 8:
        risk_score += 1
    elif row['stress'] > 6:
        risk_score += 0.5
    
    # Heart rate elevation (indicates stress/sleep issues)
    if row['heart_rate'] > 110:
        risk_score += 1.5
    elif row['heart_rate'] > 90:
        risk_score += 0.5
    
    # Snoring (sleep apnea indicator)
    if row['snoring'] == 1:
        risk_score += 2
    
    # BMI (obesity link to sleep apnea)
    if row['bmi'] > 35:
        risk_score += 1
    elif row['bmi'] > 30:
        risk_score += 0.5
    
    # Age factor (older age increases risk)
    if row['age'] > 60:
        risk_score += 0.5
    
    # High blood pressure
    if row['blood_pressure_avg'] > 140:
        risk_score += 1
    
    # Long working hours
    if row['work_hours'] > 12:
        risk_score += 1
    
    # Classify based on cumulative risk score
    if risk_score < 1:
        return 0  # Normal
    elif risk_score < 2.5:
        return 1  # Sleep Deprivation
    elif risk_score < 4:
        return 2  # Chronic Insomnia
    else:
        return 3  # Obstructive Sleep Apnea

df['disorder'] = df.apply(classify_disorder, axis=1)

print(f"Dataset created with {len(df)} samples")
print(f"Disorder distribution:\n{df['disorder'].value_counts().sort_index()}")
print()

X = df.drop('disorder', axis=1)
y = df['disorder']

# Split the data (80-20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training set: {len(X_train)} samples")
print(f"Test set: {len(X_test)} samples")

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the Random Forest model
print("\nTraining Random Forest model...")
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train_scaled, y_train)

# Evaluate the model
train_score = model.score(X_train_scaled, y_train)
test_score = model.score(X_test_scaled, y_test)

print(f"\n✅ Model trained successfully!")
print(f"Training accuracy: {train_score:.3f} ({train_score*100:.1f}%)")
print(f"Testing accuracy: {test_score:.3f} ({test_score*100:.1f}%)")

# Feature importance
print(f"\nFeature Importance:")
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print(feature_importance.to_string(index=False))

# Save the model and scaler
joblib.dump(model, "ml/model.pkl", protocol=5)
joblib.dump(scaler, "ml/scaler.pkl", protocol=5)

print(f"\n✓ Model saved to ml/model.pkl")
print(f"✓ Scaler saved to ml/scaler.pkl")
print(f"\nFeature order (for predictions):")
print(list(X.columns))

# Disorder labels
print(f"\nDisorder Classification:")
print(f"0 = Normal (No sleep disorder)")
print(f"1 = Sleep Deprivation (Moderate Risk)")
print(f"2 = Chronic Insomnia (High Risk)")
print(f"3 = Obstructive Sleep Apnea (Critical Risk)")

