import streamlit as st
from joblib import load
import numpy as np
import pandas as pd

st.warning("⚠️ WorkWellAI.py is running (AI build)")



# model = load("health_risk_model.pkl")


st.title("🧬 LifeMode AI – Lifestyle Health System")

# ---------- 1. PERSONAL PROFILE ----------
st.subheader("🧍 Personal Profile")

height = st.number_input("Height (cm)", 100, 250)
weight = st.number_input("Weight (kg)", 30, 200)

biological_sex = st.selectbox("Biological sex (optional)", ["Prefer not to say", "Male", "Female"])

lifestyle = st.selectbox(
    "Working lifestyle",
    ["Desk / Office Worker", "Student / Part-time Worker", "Gamer / Streamer",
     "Restaurant / Retail Worker", "Physically Active Worker"]
)

# ---------- 2. BASIC HEALTH INPUTS ----------
st.subheader("📥 Basic Health Inputs")

age = st.number_input("Age", 1, 120)
sleep = st.number_input("Sleep (hours)", 0.0, 24.0)
water = st.number_input("Water intake (liters)", 0.0, 10.0)
protein = st.number_input("Protein intake (grams)", 0, 300)
calories = st.number_input("Calories intake (kcal)", 0, 5000)

# ---------- 3. BIOLOGICAL ENGINE ----------
def age_group(age):
    if age < 18:
        return "Adolescent", 8.5
    elif age <= 30:
        return "Young Adult", 8
    elif age <= 50:
        return "Adult", 7.5
    else:
        return "Older Adult", 7.5


def calculate_bmi(weight, height_cm):
    h = height_cm / 100
    bmi = weight / (h ** 2)

    if bmi < 18.5:
        status = "Underweight"
    elif bmi < 25:
        status = "Normal"
    elif bmi < 30:
        status = "Overweight"
    else:
        status = "Obese"

    return round(bmi, 2), status


def lifestyle_factor(lifestyle):
    if lifestyle == "Desk / Office Worker":
        return 1.2
    elif lifestyle == "Student / Part-time Worker":
        return 1.35
    elif lifestyle == "Gamer / Streamer":
        return 1.25
    elif lifestyle == "Restaurant / Retail Worker":
        return 1.55
    else:
        return 1.75


def ideal_values(age, weight, lifestyle):
    group, ideal_sleep = age_group(age)
    factor = lifestyle_factor(lifestyle)

    ideal_water = round(weight * 0.035 * factor, 2)
    ideal_protein_min = round(weight * 0.8)
    ideal_protein_max = round(weight * 1.2)
    ideal_calories = round(24 * weight * factor)

    return group, ideal_sleep, ideal_water, ideal_protein_min, ideal_protein_max, ideal_calories


# ---------- 4. ANALYSIS BUTTON ----------
if st.button("🧪 Analyze My Health"):

    group, ideal_sleep, ideal_water, p_min, p_max, ideal_calories = ideal_values(age, weight, lifestyle)
    bmi, bmi_status = calculate_bmi(weight, height)

    st.header("🧬 Biological Profile")
    st.write("Age group:", group)
    st.write("BMI:", bmi, "(", bmi_status, ")")
    
# ---------- 🤖 AI HEALTH RISK PREDICTION ----------

    lifestyle_code = ["Desk / Office Worker",
                      "Student / Part-time Worker",
                      "Gamer / Streamer",
                      "Restaurant / Retail Worker",
                      "Physically Active Worker"].index(lifestyle)

    ai_input = np.array([[age, bmi, sleep, water, protein, calories, lifestyle_code]])

    #ai_prediction = model.predict(ai_input)[0]

    risk_map = {
        0: ("🟢 Low Risk", "Your lifestyle shows good biological balance."),
        1: ("🟡 Moderate Risk", "Some health factors need improvement."),
        2: ("🟠 High Risk", "Your current lifestyle may lead to health problems."),
        3: ("🔴 Critical Risk", "Serious lifestyle health risks detected.")
    }

    ai_risk, ai_message = risk_map[ai_prediction]

    st.markdown("---")
    st.subheader("🤖 AI Health Risk Assessment")
    st.write("AI Predicted Risk Level:", ai_risk)
    st.write(ai_message)


    st.subheader("🎯 Your Ideal Health Targets")
    st.write("Ideal sleep:", ideal_sleep, "hrs")
    st.write("Ideal water:", ideal_water, "L")
    st.write("Ideal protein:", f"{p_min} – {p_max} g")
    st.write("Ideal calories:", ideal_calories, "kcal")
    
# ---------- 4.5 HEALTH SCORE & RISK ENGINE ----------

    sleep_score = min((sleep / ideal_sleep) * 100, 100)
    water_score = min((water / ideal_water) * 100, 100)
    protein_score = min((protein / p_max) * 100, 100)
    calorie_score = min((calories / ideal_calories) * 100, 100)

    # BMI score
    if bmi_status == "Normal":
        bmi_score = 100
    elif bmi_status == "Underweight" or bmi_status == "Overweight":
        bmi_score = 70
    else:
        bmi_score = 40

    # Final LifeMode score
    health_score = round(
        (sleep_score + water_score + protein_score + calorie_score + bmi_score) / 5
    )

    # Risk interpretation
    if health_score >= 85:
        risk = "🟢 Optimal"
        message = "Excellent lifestyle balance. Your biological needs are well supported."
    elif health_score >= 65:
        risk = "🟡 Needs Attention"
        message = "You are doing well, but some biological needs are not fully met."
    elif health_score >= 40:
        risk = "🟠 High Risk"
        message = "Multiple lifestyle gaps detected. Long-term health risk is rising."
    else:
        risk = "🔴 Critical"
        message = "Serious biological imbalance detected. Immediate lifestyle correction is recommended."

    st.markdown("---")
    st.subheader("🧠 LifeMode Health Score")

    st.metric("Overall Health Score", f"{health_score} / 100", risk)
    st.write(message)


    # ---------- 5. GRAPH ----------
    actual = [sleep, water, protein, calories]
    ideal = [ideal_sleep, ideal_water, p_max, ideal_calories]

    data = pd.DataFrame({
        "Category": ["Sleep (hrs)", "Water (L)", "Protein (g)", "Calories (kcal)"],
        "Your intake": actual,
        "Ideal": ideal
    })

    st.subheader("📊 Lifestyle vs Biological Needs")
    st.bar_chart(data.set_index("Category"))

    # ---------- 6. PROGRESS ----------
    st.subheader("📈 Fulfillment Levels")

    st.progress(min(float(sleep/max(ideal_sleep, 1)), 1.0))
    st.caption("Sleep fulfillment")

    st.progress(min(float(water/max(ideal_water,1)), 1.0))
    st.caption("Hydration fulfillment")

    st.progress(min(float(protein/p_max), 1.0))
    st.caption("Protein fulfillment")

    st.progress(min(float(calories/ideal_calories), 1.0))
    st.caption("Energy fulfillment")
