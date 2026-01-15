import streamlit as st

# ---------- 1. APP BRANDING ----------
st.set_page_config(page_title="Smart Health Helper", page_icon="🧬", layout="centered")

st.title("🧬 Smart Health Helper")
st.caption("A mini health analysis app by Mehboob (CS) + Biotech Team")
st.markdown("---")

# ---------- 2. INPUT SECTION ----------
st.header("📥 Enter Your Health Details")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name")
    age = st.number_input("Age", 1, 120)
    sleep = st.number_input("Sleep (hours)", 0.0, 24.0)

with col2:
    water = st.number_input("Water (glasses)", 0, 20)
    protein = st.number_input("Protein (grams)", 0, 300)
    calories = st.number_input("Calories (kcal)", 0, 4000)

# ---------- 3. LOGIC SECTION ----------
def calculate_score(age, water, sleep, protein, calories):
    score = 0
    if age < 30: score += 1
    if water >= 8: score += 1
    if sleep >= 7: score += 1
    if protein >= 100: score += 1
    if calories >= 1500: score += 1
    return score


def health_risk_level(score):
    if score == 5:
        return "Low Risk 🟢", "Your lifestyle indicators are very healthy."
    elif score == 4:
        return "Moderate Risk 🟡", "Some habits are good, but there is room for improvement."
    elif score == 3:
        return "High Risk 🟠", "Multiple health factors are below recommended levels."
    else:
        return "Very High Risk 🔴", "Your current lifestyle may increase health risks. Immediate changes are recommended."


# ---------- 4. OUTPUT + TIPS ----------
if st.button("🧪 Analyze My Health"):

    score = calculate_score(age, water, sleep, protein, calories)
    risk, explanation = health_risk_level(score)

    st.markdown("---")
    st.header("📊 Health Report")
    st.write(f"👤 Name: {name}")
    st.write(f"✅ Healthy habits followed: {score} / 5")

    st.subheader("🧠 Health Risk Analysis")
    st.write("Risk Level:", risk)
    st.write("Explanation:", explanation)

    if score == 5:
        st.success("Excellent health habits! 🔥")
    elif score == 4:
        st.info("Good, but can improve 🙂")
    elif score == 3:
        st.warning("Your body needs better routine 🥗😴")
    else:
        st.error("High health risk. Immediate lifestyle improvement needed ⚠️")

    st.progress(score / 5)

    # ---------- 5. PERSONALIZED TIPS ----------
    st.markdown("---")
    st.header("🩺 Personalized Health Tips")

    # 💧 WATER
    if water < 8:
        st.subheader("💧 Hydration Tips")
        st.write("Aim for 9–13 cups daily. Carry a bottle, sip hourly, eat water-rich fruits, and drink extra in Pune’s heat.")

    # 😴 SLEEP
    if sleep < 7:
        st.subheader("😴 Sleep Tips")
        st.write("Fix sleep times, reduce screens before bed, get morning sunlight, and keep your room dark & cool.")

    # 🥗 PROTEIN
    if protein < 100:
        st.subheader("🥗 Protein Tips")
        st.write("Add eggs, dairy, legumes, soy, nuts, tuna, and protein smoothies. Aim 20–30g protein every 3–4 hours.")

    # 🍽️ CALORIES
    if calories < 1500:
        st.subheader("🍽️ Calorie Tips")
        st.write("Use calorie-dense snacks like trail mix, peanut butter, smoothies, oats with milk, and nuts.")
