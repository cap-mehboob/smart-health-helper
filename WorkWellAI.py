import streamlit as st
from joblib import load
import numpy as np
import pandas as pd

# -------------------------------
# Load trained AI model
# -------------------------------
model = load("health_risk_model.pkl")

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

# ---------- 2.5 OCCUPATIONAL HEALTH INPUTS ----------
st.subheader("💼 Work & Body Strain Profile")

work_hours = st.slider("Average working hours per day", 0, 16, 8)

work_type = st.selectbox(
    "Your main work posture",
    ["Mostly sitting", "Mostly standing", "Mixed (sit + stand)", "Physical / moving a lot"]
)

screen_time = st.slider("Daily screen time (hours)", 0, 16, 6)

pain_areas = st.multiselect(
    "Do you experience pain or discomfort in these areas?",
    ["Neck", "Shoulders", "Upper back", "Lower back", "Wrist/Hand", "Hips", "Knees", "Feet", "Eyestrain", "Headache"]
)

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
    
#---------BMI Calculations-------------

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
    factors = {
        "Desk / Office Worker": 1.2,
        "Student / Part-time Worker": 1.35,
        "Gamer / Streamer": 1.25,
        "Restaurant / Retail Worker": 1.55,
        "Physically Active Worker": 1.75
    }
    return factors[lifestyle]


def ideal_values(age, weight, lifestyle):
    group, ideal_sleep = age_group(age)
    factor = lifestyle_factor(lifestyle)

    ideal_water = round(weight * 0.035 * factor, 2)
    ideal_protein_min = round(weight * 0.8)
    ideal_protein_max = round(weight * 1.2)
    ideal_calories = round(24 * weight * factor)

    return group, ideal_sleep, ideal_water, ideal_protein_min, ideal_protein_max, ideal_calories


def occupational_risk(lifestyle, work_type, work_hours, screen_time, pain_areas):
    score = 0
    risks = []

    if lifestyle in ["Desk / Office Worker", "Gamer / Streamer"]:
        score += 2; risks.append("Sedentary strain risk")

    if lifestyle == "Restaurant / Retail Worker":
        score += 2; risks.append("Prolonged standing strain")

    if lifestyle == "Physically Active Worker":
        score += 2; risks.append("Joint overuse risk")

    if work_type == "Mostly sitting":
        score += 2; risks.append("Neck & spine compression")

    if work_type == "Mostly standing":
        score += 2; risks.append("Knee, hip & foot stress")

    if screen_time >= 6:
        score += 2; risks.append("Digital eye strain")

    if work_hours >= 9:
        score += 2; risks.append("Long-duration fatigue")

    score += len(pain_areas)

    if score <= 3: level = "🟢 Low Occupational Risk"
    elif score <= 7: level = "🟡 Moderate Occupational Risk"
    elif score <= 11: level = "🟠 High Occupational Risk"
    else: level = "🔴 Severe Occupational Risk"

    return level, risks, score


# ---------- 4. ANALYSIS ----------
if st.button("🧪 Analyze My Health"):

    group, ideal_sleep, ideal_water, p_min, p_max, ideal_calories = ideal_values(age, weight, lifestyle)
    bmi, bmi_status = calculate_bmi(weight, height)

    st.header("🧬 Biological Profile")
    st.write("Age group:", group)
    st.write("BMI:", bmi, "(", bmi_status, ")")

    # ---------- 4.5 HEALTH SCORE ----------
    sleep_score = min((sleep / ideal_sleep) * 100, 100)
    water_score = min((water / ideal_water) * 100, 100)
    protein_score = min((protein / p_max) * 100, 100)
    calorie_score = min((calories / ideal_calories) * 100, 100)

    if bmi_status == "Normal":
        bmi_score = 100
    elif bmi_status in ["Underweight", "Overweight"]:
        bmi_score = 70
    else:
        bmi_score = 40

    health_score = round((sleep_score + water_score + protein_score + calorie_score + bmi_score) / 5)

    st.markdown("---")
    st.subheader("🧠 LifeMode Health Score")
    st.metric("Overall Health Score", f"{health_score} / 100")
    
    # ---------- OCCUPATIONAL ANALYSIS ----------
    occ_level, occ_risks, occ_score = occupational_risk(
        lifestyle, work_type, work_hours, screen_time, pain_areas
    )    
    
    st.markdown("---")
    st.header("🦴 Occupational Health & Pain Risk")
    st.write("Risk level:", occ_level)
    st.write("Occupational risk score:", occ_score)

    if occ_risks:
        st.subheader("⚠️ Detected strain factors")
        for r in occ_risks:
            st.write("•", r)

    if pain_areas:
        st.subheader("📍 Reported pain areas")
        st.write(", ".join(pain_areas))
    
    st.subheader("🧘 Corrective & Preventive Actions")

    if "Neck" in pain_areas or "Shoulders" in pain_areas:
        st.write("• Do neck retraction and shoulder roll exercises every 60–90 minutes.")
        st.write("• Keep screen at eye level and avoid forward head posture.")

    if "Lower back" in pain_areas or "Upper back" in pain_areas:
        st.write("• Add lumbar support. Avoid slouching.")
        st.write("• Try cobra stretch, cat-cow, and seated spinal extensions.")

    if "Wrist/Hand" in pain_areas:
        st.write("• Use wrist-neutral posture. Avoid resting wrists on hard edges.")
        st.write("• Perform wrist flexor and extensor stretches.")

    if "Knees" in pain_areas or "Feet" in pain_areas:
        st.write("• Use cushioned footwear and anti-fatigue mats.")
        st.write("• Avoid locking knees while standing.")

    if screen_time >= 6:
        st.write("• Follow 20-20-20 rule for eyes: every 20 min, look 20 ft away for 20 sec.")

    st.write("• Take a 3–5 minute mobility break every hour.")
    st.write("• Weekly stretching + posture strengthening is strongly advised.")



    # ---------- 🤖 REAL AI PREDICTION ----------
    lifestyle_code = [
        "Desk / Office Worker",
        "Student / Part-time Worker",
        "Gamer / Streamer",
        "Restaurant / Retail Worker",
        "Physically Active Worker"
    ].index(lifestyle)

    ai_input = np.array([[age, bmi, sleep, water, protein, calories, lifestyle_code]])

    ai_prediction = model.predict(ai_input)[0]
    ai_prob = model.predict_proba(ai_input)[0]

    risk_map = {
        0: ("🟢 Low Risk", "Your lifestyle shows good biological balance."),
        1: ("🟡 Moderate Risk", "Some health factors need improvement."),
        2: ("🟠 High Risk", "Your current lifestyle may lead to health problems."),
        3: ("🔴 Critical Risk", "Serious lifestyle health risks detected.")
    }

    ai_risk, ai_message = risk_map[ai_prediction]

    st.markdown("---")
    st.subheader("🤖 AI Health Risk Assessment")
    st.write("Predicted Risk Level:", ai_risk)
    st.write(ai_message)

    st.subheader("📊 AI Confidence Distribution")
    st.bar_chart(pd.DataFrame(ai_prob, index=["Low", "Moderate", "High", "Critical"], columns=["Probability"]))

    # ---------- 5. COMPARISON GRAPH ----------
    data = pd.DataFrame({
        "Category": ["Sleep (hrs)", "Water (L)", "Protein (g)", "Calories (kcal)"],
        "Your Intake": [sleep, water, protein, calories],
        "Ideal": [ideal_sleep, ideal_water, p_max, ideal_calories]
    })

    st.subheader("📊 Lifestyle vs Biological Needs")
    st.bar_chart(data.set_index("Category"))

    # ---------- 6. PROGRESS ----------
    st.subheader("📈 Fulfillment Levels")

    st.progress(min(sleep / ideal_sleep, 1.0)); st.caption("Sleep fulfillment")
    st.progress(min(water / ideal_water, 1.0)); st.caption("Hydration fulfillment")
    st.progress(min(protein / p_max, 1.0)); st.caption("Protein fulfillment")
    st.progress(min(calories / ideal_calories, 1.0)); st.caption("Energy fulfillment")
