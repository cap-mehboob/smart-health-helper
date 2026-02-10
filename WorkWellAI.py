import streamlit as st
from joblib import load
import numpy as np
import pandas as pd
import os
from datetime import datetime, date
import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(page_title="LifeMode AI", layout="wide")

# =========================================================
# LOAD AI MODEL
# =========================================================
model = load("health_risk_model.pkl")

# =========================================================
# TITLE
# =========================================================
st.title("🧬 LifeMode AI – Occupational Lifestyle Intelligence System")
st.caption("AI-powered lifestyle, work strain & health optimization platform")

# =========================================================
# PERSONAL PROFILE
# =========================================================
st.subheader("🧍 Personal Profile")

name = st.text_input("Your name (optional)", value="")
height = st.number_input("Height (cm)", min_value=100, max_value=250, value=None, placeholder="Enter height")
weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=None, placeholder="Enter weight")

biological_sex = st.selectbox("Biological sex (optional)", ["Prefer not to say", "Male", "Female"])

lifestyle = st.selectbox(
    "Working lifestyle",
    ["Desk / Office Worker", "Student / Part-time Worker", "Gamer / Streamer",
     "Restaurant / Retail Worker", "Physically Active Worker"]
)

# =========================================================
# BASIC HEALTH INPUTS
# =========================================================
st.subheader("📥 Basic Health Inputs")

age = st.number_input("Age", min_value=1, max_value=120, value=None, placeholder="Enter age")
sleep = st.number_input("Sleep (hours)", min_value=0.0, max_value=24.0, value=None, placeholder="e.g. 7.5")
water = st.number_input("Water intake (liters)", min_value=0.0, max_value=10.0, value=None, placeholder="e.g. 2.5")
protein = st.number_input("Protein intake (grams)", min_value=0, max_value=300, value=None, placeholder="e.g. 90")
calories = st.number_input("Calories intake (kcal)", min_value=0, max_value=5000, value=None, placeholder="e.g. 2200")

# =========================================================
# OCCUPATIONAL INPUTS
# =========================================================
st.subheader("💼 Work & Body Strain Profile")

work_hours = st.slider("Average working hours per day", 0, 16, 8)
work_type = st.selectbox("Main work posture", ["Mostly sitting", "Mostly standing", "Mixed", "Physical / moving a lot"])
screen_time = st.slider("Daily screen time (hours)", 0, 16, 6)

pain_areas = st.multiselect(
    "Pain / discomfort areas",
    ["Neck","Shoulders","Upper back","Lower back","Wrist/Hand","Hips","Knees","Feet","Eyestrain","Headache"]
)

# =========================================================
# STRESS & BURNOUT INPUTS
# =========================================================
st.subheader("🧠 Stress & Burnout Profile")

mental_fatigue = st.slider("Mental fatigue level", 0, 10, 4)
motivation = st.slider("Motivation level", 0, 10, 6)
mood = st.selectbox("Overall mood", ["Good","Neutral","Low"])
breaks = st.slider("Breaks during workday", 0, 10, 2)

# =========================================================
# BIOLOGICAL ENGINE
# =========================================================
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
        "Desk / Office Worker":1.2,
        "Student / Part-time Worker":1.35,
        "Gamer / Streamer":1.25,
        "Restaurant / Retail Worker":1.55,
        "Physically Active Worker":1.75
    }[lifestyle]

def ideal_values(age, weight, lifestyle):
    ideal_sleep = 8 if age <= 30 else 7.5
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

# =========================================================
# PERSONA ENGINE
# =========================================================
persona_advice = {
"Gamer / Streamer":"Focus on eye care, wrist health, posture and sleep debt recovery.",
"Desk / Office Worker":"Focus on posture, spine health, stress control and burnout prevention.",
"Restaurant / Retail Worker":"Focus on knee, hip, foot care and hydration balance.",
"Physically Active Worker":"Focus on joint protection, recovery cycles and protein intake.",
"Student / Part-time Worker":"Focus on sleep discipline, stress management and nutritional stability."
}

# =========================================================
# WEEKLY TRACKING SYSTEM
# =========================================================
LOG_FILE = "weekly_log.csv"

def save_daily_log(data):
    df = pd.DataFrame([data])
    if os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(LOG_FILE, index=False)

def load_logs():
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE)
    return pd.DataFrame()

# =========================================================
# ANALYSIS BUTTON
# =========================================================
analyze = st.button("🧪 Analyze My Health")

if analyze:

    if any(v is None for v in [age, height, weight, sleep, water, protein, calories]):

        st.error("⚠️ Please fill in all health inputs before analyzing.")
    else:

        ideal_sleep, ideal_water, p_min, p_max, ideal_cal = ideal_values(age, weight, lifestyle)
        bmi, bmi_status = calculate_bmi(weight, height)

        sleep_score = min((sleep/ideal_sleep)*100,100)
        water_score = min((water/ideal_water)*100,100)
        protein_score = min((protein/p_max)*100,100)
        calorie_score = min((calories/ideal_cal)*100,100)
        bmi_score = 100 if bmi_status=="Normal" else 70 if bmi_status in ["Underweight","Overweight"] else 40

        health_score = round((sleep_score+water_score+protein_score+calorie_score+bmi_score)/5)

        burnout_score = round((mental_fatigue*10 + (10-motivation)*10 + (10-breaks)*5 + (5 if mood=="Low" else 0))/3,1)
        burnout_level = "🟢 Low" if burnout_score<30 else "🟡 Moderate" if burnout_score<60 else "🔴 High"

        occ_level, occ_score = occupational_risk(lifestyle,work_type,work_hours,screen_time,pain_areas)

        lifestyle_code = ["Desk / Office Worker","Student / Part-time Worker","Gamer / Streamer","Restaurant / Retail Worker","Physically Active Worker"].index(lifestyle)
        ai_input = np.array([[age,bmi,sleep,water,protein,calories,lifestyle_code]])
        ai_prediction = model.predict(ai_input)[0]
        ai_prob = model.predict_proba(ai_input)[0]

        risk_map = {0:"🟢 Low",1:"🟡 Moderate",2:"🟠 High",3:"🔴 Critical"}

        st.session_state["today_data"] = {
            "date": str(date.today()),
            "sleep": sleep,
            "water": water,
            "protein": protein,
            "calories": calories,
            "health_score": health_score,
            "occupational_risk": occ_score,
            "screen_time": screen_time,
            "work_hours": work_hours
        }
        burnout_health_score = max(0, 100 - burnout_score)
        occ_health_score = max(0, 100 - (occ_score * 6))
        lifemode_index = round(
    (health_score * 0.45) +
    (burnout_health_score * 0.30) +
    (occ_health_score * 0.25)
)




        # ================= DASHBOARD =================
        st.markdown("---")
        st.header("📊 LifeMode AI Dashboard")
        st.metric("Overall Health Score", f"{health_score}/100")
        st.metric("Burnout Risk", burnout_level)
        st.metric("Occupational Risk", occ_level)
        st.metric("AI Health Risk", risk_map[ai_prediction])

        st.info(f"🎯 Persona focus: {persona_advice[lifestyle]}")

        st.subheader("🤖 AI Confidence")
        st.bar_chart(pd.DataFrame(ai_prob, index=["Low","Moderate","High","Critical"], columns=["Probability"]))
        
        st.metric("🏆 LifeMode Master Index", f"{lifemode_index} / 100")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🧬 Biological Health", f"{health_score} / 100")

        with col2:
            st.metric("🔥 Nervous System Health", f"{burnout_health_score} / 100")

        with col3:
            st.metric("🦴 Occupational Health", f"{occ_health_score} / 100")

        st.markdown("### ⚠️ Risk Indicators")
        st.write("Burnout risk:", burnout_level)
        st.write("Occupational strain:", occ_level)
        st.write("AI lifestyle risk:", risk_map[ai_prediction])


        # ================= ADVANCED IMPROVEMENT ENGINE =================

        st.markdown("---")
        st.header("🧩 Personalized Improvement Plan")

        # -------------------------------------------------
        # 🛌 SLEEP OPTIMIZATION
        # -------------------------------------------------
        st.subheader("🛌 Sleep Optimization")

        if sleep < ideal_sleep:
            st.write("• Increase sleep duration gradually (30 min increments).")
            st.write("• Fix sleep timing: same bed & wake time daily.")
            st.write("• Stop screens 60 minutes before bed.")
            st.write("• Dark, cool, silent sleeping environment.")
            st.write("• Morning sunlight exposure for circadian reset.")
        else:
            st.write("• Your sleep duration is good. Maintain regular sleep rhythm.")
            st.write("• Protect sleep consistency even on weekends.")

        # -------------------------------------------------
        # 💧 HYDRATION & RECOVERY
        # -------------------------------------------------
        st.subheader("💧 Hydration & Recovery")

        if water < ideal_water:
            st.write("• Start day with 2 glasses of water.")
            st.write("• Drink water every 60–90 minutes.")
            st.write("• Add electrolytes if sweating or standing long hours.")
            st.write("• Replace sugary drinks with water or lemon water.")
        else:
            st.write("• Hydration is adequate. Maintain steady intake.")
            st.write("• Monitor urine color for hydration feedback.")

        st.write("• Stretch lightly before bed to support overnight recovery.")
        st.write("• One full rest day per week improves nervous system reset.")

        # -------------------------------------------------
        # 🍽 NUTRITION INTELLIGENCE
        # -------------------------------------------------
        st.subheader("🍽 Nutrition Intelligence")

        if protein < p_min:
            st.write("• Increase protein intake to support muscles and metabolism.")
            st.write("• Add: eggs, milk, curd, paneer, lentils, tofu, chicken, fish.")
        else:
            st.write("• Protein intake looks sufficient.")

        if calories < ideal_cal:
            st.write("• Low energy intake detected — may cause fatigue and burnout.")
            st.write("• Add complex carbs (rice, roti, oats, fruits, potatoes).")
        elif calories > ideal_cal * 1.2:
            st.write("• High calorie intake — risk of fat gain & inflammation.")
            st.write("• Reduce sugar, fried foods, late-night meals.")

        st.write("• Eat every 3–4 hours to stabilize energy.")
        st.write("• Prioritize whole foods over packaged foods.")
        st.write("• Include vegetables and fruits daily.")

        # -------------------------------------------------
        # 🏃 PHYSICAL CONDITIONING
        # -------------------------------------------------
        st.subheader("🏃 Physical Conditioning")

        if bmi_status == "Underweight":
            st.write("• Focus on strength training 3× per week.")
            st.write("• Maintain calorie surplus and progressive overload.")

        elif bmi_status == "Overweight":
            st.write("• Daily walking target: 7,000–10,000 steps.")
            st.write("• Strength training + calorie control recommended.")

        elif bmi_status == "Obese":
            st.write("• Fat loss priority: walking, cycling, swimming.")
            st.write("• Structured training & nutrition plan recommended.")

        st.write("• Move at least once every 45 minutes.")
        st.write("• Combine strength + mobility + light cardio weekly.")

        # -------------------------------------------------
        # 🦴 OCCUPATIONAL REHAB & POSTURE
        # -------------------------------------------------
        st.subheader("🦴 Occupational Rehab & Posture")

        if "Neck" in pain_areas or "Shoulders" in pain_areas:
            st.write("• Chin tucks, wall angels, band pull-aparts.")
            st.write("• Screen at eye level, shoulders relaxed.")

        if "Lower back" in pain_areas:
            st.write("• Core strengthening and hip mobility essential.")
            st.write("• Avoid prolonged static sitting.")

        if "Wrist/Hand" in pain_areas:
            st.write("• Ergonomic keyboard/mouse.")
            st.write("• Wrist mobility every 2 hours.")

        if "Knees" in pain_areas or "Feet" in pain_areas:
            st.write("• Cushion footwear, avoid knee locking.")
            st.write("• Strengthen calves, glutes, hamstrings.")

        if screen_time >= 6:
            st.write("• 20-20-20 eye rule.")
            st.write("• Blink training and brightness control.")

        st.write("• 3–5 minute posture reset every hour.")
        st.write("• Weekly mobility session strongly advised.")

        # -------------------------------------------------
        # 🔥 STRESS, BURNOUT & NERVOUS SYSTEM
        # -------------------------------------------------
        st.subheader("🔥 Stress, Burnout & Nervous System Care")

        if burnout_score > 60:
            st.write("• High burnout risk — immediate lifestyle correction advised.")
            st.write("• Reduce workload if possible.")
            st.write("• Introduce deep rest practices.")

        if mental_fatigue >= 7:
            st.write("• Cognitive overload detected.")
            st.write("• Limit multitasking, use focus blocks.")

        if motivation <= 4:
            st.write("• Low motivation may indicate nervous exhaustion.")
            st.write("• Focus on sleep, sunlight, routine, movement.")

        st.write("• Daily breathing: 4-7-8 or box breathing.")
        st.write("• Weekly digital detox period.")
        st.write("• Social interaction improves recovery hormones.")

        # -------------------------------------------------
        # 🧭 HABIT & BEHAVIOR ENGINEERING
        # -------------------------------------------------
        st.subheader("🧭 Habit Engineering")

        st.write("• Anchor habits to existing routines.")
        st.write("• Improve environment before motivation.")
        st.write("• Track streaks not perfection.")
        st.write("• Focus on consistency > intensity.")
        st.write("• Design systems, not goals.")

        # -------------------------------------------------
        # 🎯 LIFESTYLE PERSONA FOCUS
        # -------------------------------------------------
        st.subheader("🎯 Lifestyle-Specific Focus")
        st.info(persona_advice[lifestyle])

# =========================================================
# SAVE SYSTEM (ALWAYS VISIBLE)
# =========================================================
st.markdown("---")
st.subheader("💾 Weekly Health Tracker")

if "today_data" in st.session_state:
    if st.button("📅 Save Today’s Health Log"):
        save_daily_log(st.session_state["today_data"])
        st.success("✅ Today’s health data saved successfully!")
else:
    st.info("Run analysis to unlock saving.")

# =========================================================
# WEEKLY DASHBOARD
# =========================================================
st.markdown("---")
st.header("📈 Weekly Health Dashboard")

logs = load_logs()

if not logs.empty:
    logs["date"] = pd.to_datetime(logs["date"])
    logs = logs.sort_values("date")

    st.line_chart(logs.set_index("date")[["health_score"]])
    st.line_chart(logs.set_index("date")[["sleep","water"]])
    st.line_chart(logs.set_index("date")[["occupational_risk"]])

    st.subheader("🧠 Weekly Insights")
    st.write("Average health score:", round(logs["health_score"].mean(),1))
    st.write("Best day score:", logs["health_score"].max())
    st.write("Lowest day score:", logs["health_score"].min())

else:
    st.info("No weekly data yet. Save your daily health log to start tracking.")
# =========================================================
# CAMERA POSTURE DETECTION (STABLE)
# =========================================================

st.markdown("---")
st.header("🎥 AI Posture Detection")

start = st.button("Start Camera")

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

if start:
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Camera not detected")
            break

        frame = cv2.flip(frame, 1)

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)

        posture_text = "Detecting..."

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            nose = lm[mp_pose.PoseLandmark.NOSE]
            left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]

            shoulder_center_x = (left_shoulder.x + right_shoulder.x) / 2
            shoulder_center_y = (left_shoulder.y + right_shoulder.y) / 2

            head_forward = nose.x - shoulder_center_x
            head_down = nose.y - shoulder_center_y

            if abs(head_forward) < 0.03 and head_down < -0.05:
                posture_text = "🟢 Good Posture"
                color = (0,255,0)
            elif head_down > 0.02:
                posture_text = "🔴 Slouching"
                color = (0,0,255)
            else:
                posture_text = "🟡 Neck Forward"
                color = (0,255,255)

            cv2.putText(frame, posture_text, (30,50),
                        cv2.FONT_HERSHEY_SIMPLEX,1,color,2)

        st.image(frame, channels="BGR")

    cap.release()
