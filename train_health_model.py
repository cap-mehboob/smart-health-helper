import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from joblib import dump

# -------------------------------
# 1. Generate synthetic dataset
# -------------------------------

np.random.seed(42)
samples = 1200

age = np.random.randint(16, 65, samples)
bmi = np.random.uniform(16, 35, samples)
sleep = np.random.uniform(3, 9, samples)
water = np.random.uniform(0.5, 4.5, samples)
protein = np.random.uniform(20, 160, samples)
calories = np.random.uniform(900, 3800, samples)
lifestyle = np.random.randint(0, 5, samples)

# Risk logic (biotech-inspired)
risk = []

for i in range(samples):
    score = 0
    if sleep[i] < 6: score += 1
    if water[i] < 2: score += 1
    if protein[i] < 50: score += 1
    if calories[i] < 1500 or calories[i] > 3200: score += 1
    if bmi[i] < 18.5 or bmi[i] > 30: score += 1

    if score <= 1:
        risk.append(0)   # Low
    elif score == 2:
        risk.append(1)   # Moderate
    elif score == 3:
        risk.append(2)   # High
    else:
        risk.append(3)   # Critical

data = pd.DataFrame({
    "age": age,
    "bmi": bmi,
    "sleep": sleep,
    "water": water,
    "protein": protein,
    "calories": calories,
    "lifestyle": lifestyle,
    "risk": risk
})

X = data.drop("risk", axis=1)
y = data["risk"]

# -------------------------------
# 2. Train model
# -------------------------------

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=150)
model.fit(X_train, y_train)

# -------------------------------
# 3. Save model
# -------------------------------

dump(model, "health_risk_model.pkl")

print("✅ AI health risk model trained and saved as health_risk_model.pkl")
