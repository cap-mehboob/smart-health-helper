import streamlit as st
from joblib import load
import numpy as np
import pandas as pd
from datetime import datetime

# -------------------------------
# Load trained AI model
# -------------------------------
model = load("health_risk_model.pkl")

st.title("🧬 LifeMode AI – Occupational Lifestyle Intelligence System")

# ---------- 1. PERSONAL PROFILE ----------
st.subheader("🧍 Personal Profile")

name = st.text_input("Your name (optional)")
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

# ---------- 2.5 OCCUPATIONAL INPUTS ----------
st.subheader("💼 Work & Body Strain Profile")

work_hours = st.slider("Average working hours per day", 0, 16, 8)
work_type = st.selectbox("Main work posture", ["Mostly sitting", "Mostly standing", "Mixed", "Physical / moving a lot"])
screen_time = st.slider("Daily screen time (hours)", 0, 16, 6)
pain_areas = st.multiselect("Pain / discomfort areas", ["Neck","Shoulders","Upper back","Lower back","Wrist/Hand","Hips","Knees","Feet","Eyestrain","Headache"])

# ---------- 2.6 STRESS & BURNOUT INPUTS ----------
st.subheader("🧠 Stress & Burnout Profile")

mental_fatigue = st.slider("Mental fatigue level", 0, 10, 4)
motivation = st.slider("Motivation level", 0, 10, 6)
mood = st.selectbox("Overall mood", ["Good","Neutral","Low"])
breaks = st.slider("Breaks during workday", 0, 10, 2)

# ---------- BIOLOGICAL ENGINE ----------
def calculate_bmi(weight, height_cm):
    h = height_cm / 100
    bmi = weight / (h ** 2)
    if bmi < 18.5: status="Underweight"
    elif bmi < 25: status="Normal"
    elif bmi < 30: status="Overweight"
    else: status="Obese"
    return round(bmi,2), status

def lifestyle_factor(lifestyle):
    return {
        "Desk / Office Worker":1.2,"Student / Part-time Worker":1.35,"Gamer / Streamer":1.25,
        "Restaurant / Retail Worker":1.55,"Physically Active Worker":1.75
    }[lifestyle]

def ideal_values(age, weight, lifestyle):
    ideal_sleep = 8 if age<=30 else 7.5
    factor = lifestyle_factor(lifestyle)
    return ideal_sleep, round(weight*0.035*factor,2), round(weight*0.8), round(weight*1.2), round(24*weight*factor)

def occupational_risk(lifestyle, work_type, work_hours, screen_time, pain_areas):
    score = len(pain_areas)*1.5
    if lifestyle in ["Desk / Office Worker","Gamer / Streamer"]: score+=3
    if lifestyle=="Restaurant / Retail Worker": score+=3
    if lifestyle=="Physically Active Worker": score+=3
    if work_hours>=9: score+=3
    if screen_time>=6: score+=3
    if work_type=="Mostly sitting": score+=2
    if work_type=="Mostly standing": score+=2

    if score<=5: level="🟢 Low"
    elif score<=10: level="🟡 Moderate"
    elif score<=15: level="🟠 High"
    else: level="🔴 Severe"
    return level, round(score,1)

# ---------- SMART PERSONA ENGINE ----------
persona_advice = {
"Gamer / Streamer":"Focus on eye care, wrist health, posture and sleep debt recovery.",
"Desk / Office Worker":"Focus on posture, spine health, stress control and burnout prevention.",
"Restaurant / Retail Worker":"Focus on knee, hip, foot care and hydration balance.",
"Physically Active Worker":"Focus on joint protection, recovery cycles and protein intake.",
"Student / Part-time Worker":"Focus on sleep discipline, stress management and nutritional stability."
}

# ---------- ANALYSIS ----------
if st.button("🧪 Analyze My Health"):

    ideal_sleep, ideal_water, p_min, p_max, ideal_cal = ideal_values(age, weight, lifestyle)
    bmi, bmi_status = calculate_bmi(weight, height)

    # ---------- HEALTH SCORE ----------
    sleep_score = min((sleep/ideal_sleep)*100,100)
    water_score = min((water/ideal_water)*100,100)
    protein_score = min((protein/p_max)*100,100)
    calorie_score = min((calories/ideal_cal)*100,100)
    bmi_score = 100 if bmi_status=="Normal" else 70 if bmi_status in ["Underweight","Overweight"] else 40

    health_score = round((sleep_score+water_score+protein_score+calorie_score+bmi_score)/5)

    # ---------- STRESS & BURNOUT SCORE ----------
    burnout_score = round((mental_fatigue*10 + (10-motivation)*10 + (10-breaks)*5 + (5 if mood=="Low" else 0))/3,1)
    burnout_level = "🟢 Low" if burnout_score<30 else "🟡 Moderate" if burnout_score<60 else "🔴 High"

    # ---------- OCCUPATIONAL SCORE ----------
    occ_level, occ_score = occupational_risk(lifestyle,work_type,work_hours,screen_time,pain_areas)

    # ---------- AI PREDICTION ----------
    lifestyle_code = ["Desk / Office Worker","Student / Part-time Worker","Gamer / Streamer","Restaurant / Retail Worker","Physically Active Worker"].index(lifestyle)
    ai_input = np.array([[age,bmi,sleep,water,protein,calories,lifestyle_code]])
    ai_prediction = model.predict(ai_input)[0]
    ai_prob = model.predict_proba(ai_input)[0]
    risk_map={0:"🟢 Low",1:"🟡 Moderate",2:"🟠 High",3:"🔴 Critical"}

    # ---------- DASHBOARD ----------
    st.header("📊 LifeMode AI Dashboard")
    st.metric("Overall Health Score",f"{health_score}/100")
    st.metric("Burnout Risk",burnout_level)
    st.metric("Occupational Risk",occ_level)
    st.metric("AI Risk Level",risk_map[ai_prediction])

    st.info(f"🎯 Persona focus: {persona_advice[lifestyle]}")

    st.subheader("🤖 AI Confidence")
    st.bar_chart(pd.DataFrame(ai_prob,index=["Low","Moderate","High","Critical"],columns=["Probability"]))

    # ---------- AUTO REPORT ----------
    report = f"""
LifeMode AI – Health Intelligence Report
Name: {name if name else 'User'}
Date: {datetime.now().strftime('%d %B %Y')}

Health Score: {health_score}/100
Burnout Risk: {burnout_level}
Occupational Risk: {occ_level}
AI Health Risk: {risk_map[ai_prediction]}

Lifestyle Persona: {lifestyle}
Focus Area: {persona_advice[lifestyle]}

BMI: {bmi} ({bmi_status})
Pain Areas: {", ".join(pain_areas) if pain_areas else "None reported"}
"""

    st.subheader("📄 Auto-Generated Health Report")
    st.text_area("Your report", report, height=280)
    st.download_button("⬇️ Download Report", report, file_name="LifeMode_AI_Report.txt")

