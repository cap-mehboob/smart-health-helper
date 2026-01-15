import streamlit as st

st.set_page_config(page_title="Smart Health Helper", page_icon="🧬", layout="centered")

st.title("🧬 Smart Health Helper")
st.caption("A mini health analysis app by Mehboob (CS) + Biotech Team")

st.header("📥 Enter Your Health Details")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name")
    age = st.number_input("Age", 1, 120)
    sleep = st.number_input("Sleep (hours)", 0.0, 24.0)

with col2:
    water = st.number_input("Water (glasses)", 0, 20)
    protein = st.number_input("Protein (grams)", 0, 300)
    
def calculate_score(age, water, sleep, protein):
    score = 0
    if age < 30: score += 1
    if water >= 8: score += 1
    if sleep >= 7: score += 1
    if protein >= 100: score += 1
    return score

    if water<8:
        st.subheader("💧 Hydration tip")
        st.write("Drink at least 8 cups of fluids daily when unwell, sipping small amounts frequently (e.g., 30ml every 3-5 minutes) rather than large gulps to avoid nausea. Prioritize water, adding lemon or cucumber for flavor if plain water feels unappealing, and include broth or clear sports drinks. Avoid caffeine and alcohol, listening to thirst cues while increasing intake if symptoms like fever worsen dehydration")
        st.write("Drink more fluids...")
    if sleep >= 7:
        score += 1
    if sleep < 7:
        st.subheader("😴 Sleep Tip")
        st.write("Maintain a consistent sleep schedule with fixed bed and wake times to regulate your internal clock. Create a dark, quiet, cool bedroom environment and avoid screens, caffeine, and heavy meals before bed to boost melatonin. Practice relaxation like reading or deep breathing, and limit naps to improve nighttime sleep quality.")
        st.write("Maintain a consistent sleep schedule...")
    if protein >= 100:
        score += 1
    if protein < 100:
        st.subheader("🥗 Protein Tip")
        st.write("Aim for 0.8 grams of protein per kilogram of body weight daily, increasing during recovery for tissue repair. Include high-quality sources like eggs, lean meats, fish, dairy, legumes, nuts, and seeds in every meal, targeting 20–30 grams per meal for optimal absorption. Add protein to breakfast with options like eggs, Greek yogurt, or smoothies if appetite is low.")
        st.write("Aim for 0.8g protein per kg body weight...")
    st.subheader("📊 Health Report")
    st.write("Name:", name)
    st.write("Score:", score, "/4")

if st.button("🧪 Analyze My Health"):

    score = calculate_score(age, water, sleep, protein)

    st.markdown("---")
    st.header("📊 Health Report")

    st.write(f"👤 Name: {name}")
    st.write(f"✅ Healthy habits followed: {score} / 4")

    if score == 4:
        st.success("Excellent health habits! 🔥")
    elif score == 3:
        st.info("Good, but can improve 🙂")
    elif score == 2:
        st.warning("Your body needs better routine 🥗😴")
    else:
        st.error("High health risk. Immediate lifestyle improvement needed ⚠️")

    
