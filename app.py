import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import json
from datetime import datetime

import theme
import auth
from chatbot import ask_health_question
from health_metrics import (
    calculate_bmi,
    bmi_category,
    daily_water_intake,
    calorie_estimate,
    health_score
)
from medication import (
    add_new_medication,
    list_medications,
    check_interaction
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="HealthMonAI",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(theme.inject(), unsafe_allow_html=True)

# ---------------- AUTHENTICATION ---------------- #

auth.init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:

    st.markdown(
        theme.pulse_header(
            "HealthMonAI",
            "Your AI-powered personal health monitor"
        ),
        unsafe_allow_html=True
    )

    st.markdown(theme.section_eyebrow("🔐", "SECURE ACCESS"), unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:1.3rem;'
        'font-weight:600;margin-bottom:14px;">Sign in to continue</div>',
        unsafe_allow_html=True
    )

    login_tab, signup_tab = st.tabs(["🔑 Login", "🆕 Sign Up"])

    with login_tab:

        st.markdown(theme.card_open(), unsafe_allow_html=True)

        login_username = st.text_input(
            "Username",
            key="login_username",
            placeholder="Enter your username"
        )

        login_password = st.text_input(
            "Password",
            key="login_password",
            type="password",
            placeholder="Enter your password"
        )

        if st.button("Login", key="login_btn"):

            if login_username.strip() == "" or login_password.strip() == "":
                st.warning("Please enter both username and password.")

            elif auth.verify_user(login_username, login_password):
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.rerun()

            else:
                st.error("Invalid username or password.")

        st.markdown(theme.card_close(), unsafe_allow_html=True)

    with signup_tab:

        st.markdown(theme.card_open(), unsafe_allow_html=True)

        new_username = st.text_input(
            "Choose a username",
            key="signup_username",
            placeholder="Example: john_doe"
        )

        new_password = st.text_input(
            "Choose a password",
            key="signup_password",
            type="password",
            placeholder="At least 6 characters"
        )

        confirm_password = st.text_input(
            "Confirm password",
            key="signup_confirm",
            type="password",
            placeholder="Re-enter your password"
        )

        if st.button("Create Account", key="signup_btn"):

            if new_username.strip() == "" or new_password.strip() == "":
                st.warning("Please fill in all fields.")

            elif len(new_password) < 6:
                st.warning("Password must be at least 6 characters.")

            elif new_password != confirm_password:
                st.warning("Passwords do not match.")

            elif auth.user_exists(new_username):
                st.error("Username already taken. Please choose another.")

            else:
                auth.create_user(new_username, new_password)
                st.success("Account created successfully! Please log in from the Login tab.")

        st.markdown(theme.card_close(), unsafe_allow_html=True)

    st.stop()

# ---------------- HEADER ---------------- #

st.markdown(
    theme.pulse_header(
        "HealthMonAI",
        "Your AI-powered personal health monitor"
    ),
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ---------------- #

st.sidebar.markdown(
    '<div class="pulse-title" style="font-size:1.35rem;">🫀 HealthMonAI</div>',
    unsafe_allow_html=True
)
st.sidebar.markdown(
    '<div class="pulse-caption" style="margin-bottom:14px;">Navigation</div>',
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "",
    [
        "🏠 Dashboard",
        "🤖 AI Chatbot",
        "📊 BMI Calculator",
        "💊 Medication Center",
        "📄 Health Report",
        "🎯 Health Goals",
        "🇮🇳 Indian Healthcare"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    f'<div class="pulse-caption">Signed in as <b>{st.session_state.username}</b></div>',
    unsafe_allow_html=True
)

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.success("Stay Healthy ❤️")

st.sidebar.info(
"""
✔ AI Health Chatbot

✔ BMI Calculator

✔ Medication Tracker

✔ Health Reports

✔ Goal Tracking

✔ Indian Healthcare
"""
)

# ---------------- DASHBOARD ---------------- #

if menu == "🏠 Dashboard":

    st.markdown(theme.section_eyebrow("📊", "LIVE READOUT"), unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:1.3rem;'
        'font-weight:600;margin-bottom:14px;">Personal Health Dashboard</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            theme.vital_card("❤️", "Heart Rate", "72 BPM", "Resting · steady", "steady"),
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            theme.vital_card("⚖️", "BMI", "22.4", "Normal range", "steady"),
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            theme.vital_card("💧", "Water Intake", "2.5 L", "0.3L below goal", "watch"),
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            theme.vital_card("🚶", "Daily Steps", "6,500", "3,500 to goal", "watch"),
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown(theme.section_eyebrow("💊", "TODAY'S MEDICATION"), unsafe_allow_html=True)
        st.markdown(
            theme.card_open()
            + theme.timeline_item("9:00 AM", "Vitamin D — taken", "steady")
            + theme.timeline_item("8:00 PM", "Crocin — upcoming", "watch")
            + theme.card_close(),
            unsafe_allow_html=True
        )

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown(theme.section_eyebrow("🎯", "GOAL PROGRESS"), unsafe_allow_html=True)
        st.progress(70)
        st.markdown(
            '<div class="vital-sub" style="margin-top:-8px;">70% of weekly goal completed</div>',
            unsafe_allow_html=True
        )

    with right:
        st.markdown(theme.section_eyebrow("🌞", "TODAY'S HEALTH TIP"), unsafe_allow_html=True)
        st.markdown(
            theme.card_open()
            + '<span style="color:var(--ink);">Drink at least 2.5L of water, '
              'walk for 30 minutes, and include fresh fruits in your meals.</span>'
            + theme.card_close(),
            unsafe_allow_html=True
        )

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown(theme.section_eyebrow("😊", "OVERALL HEALTH SCORE"), unsafe_allow_html=True)
        st.markdown(
            theme.vital_card("📈", "Health Score", "92%", "+3% vs last week", "steady"),
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
    st.markdown(theme.section_eyebrow("📈", "WEEKLY BMI TREND"), unsafe_allow_html=True)

    bmi_data = [22.1, 22.0, 22.3, 22.5, 22.4, 22.2, 22.4]

    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.plot(bmi_data, marker="o", color=theme.COLORS["mint"], linewidth=2,
            markerfacecolor=theme.COLORS["bg_deep"], markeredgecolor=theme.COLORS["mint"],
            markersize=7)
    ax.set_xlabel("Days")
    ax.set_ylabel("BMI")
    theme.style_chart(fig, ax)
    fig.tight_layout()
    st.pyplot(fig)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown(theme.section_eyebrow("📅", "TODAY'S SUMMARY"), unsafe_allow_html=True)

    st.markdown(
        theme.card_open()
        + theme.summary_row("Water", "Completed", "steady")
        + theme.summary_row("Exercise", "Completed", "steady")
        + theme.summary_row("Medicines", "Pending", "watch")
        + theme.summary_row("Sleep", "7 Hours", "steady")
        + theme.card_close(),
        unsafe_allow_html=True
    )
# ---------------- AI CHATBOT ---------------- #

elif menu == "🤖 AI Chatbot":

    st.markdown(theme.section_eyebrow("🤖", "AI ASSISTANT"), unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:1.3rem;'
        'font-weight:600;margin-bottom:6px;">Ask HealthMonAI</div>'
        '<div class="pulse-caption">Ask any general health-related question.</div>',
        unsafe_allow_html=True
    )

    question = st.text_area(
        "Enter your health question",
        placeholder="Example: How can I reduce my blood pressure naturally?",
        label_visibility="collapsed"
    )

    if st.button("🤖 Ask AI"):

        if question.strip() == "":
            st.warning("Please enter a question.")

        else:
            placeholder = st.empty()
            placeholder.markdown(theme.thinking_pulse("Generating response"), unsafe_allow_html=True)

            try:
                answer = ask_health_question(question)
                placeholder.empty()
                st.markdown(theme.chat_bubble("user", question), unsafe_allow_html=True)
                st.markdown(theme.chat_bubble("assistant", answer), unsafe_allow_html=True)

            except Exception:
                placeholder.empty()
                st.error("Unable to generate response.")


# ---------------- BMI CALCULATOR ---------------- #

elif menu == "📊 BMI Calculator":

    st.markdown(theme.section_eyebrow("📊", "METRICS"), unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:1.3rem;'
        'font-weight:600;margin-bottom:14px;">BMI & Health Metrics</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=22
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other"
            ]
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=250.0
        )

    with col2:

        height = st.number_input(
            "Height (cm)",
            min_value=30.0,
            max_value=250.0
        )

        activity = st.selectbox(
            "Activity Level",
            [
                "Sedentary",
                "Lightly Active",
                "Moderately Active",
                "Very Active"
            ]
        )

    st.markdown("---")

    if st.button("Calculate BMI"):

        bmi = calculate_bmi(weight, height)

        if bmi < 18.5:

            status = "Underweight"
            bmi_state = "watch"

            recommendation = """
Increase healthy calories.

Eat protein-rich foods.

Strength training is recommended.
"""

        elif bmi < 25:

            status = "Healthy"
            bmi_state = "steady"

            recommendation = """
Maintain balanced diet.

Exercise 30 minutes daily.

Drink enough water.
"""

        elif bmi < 30:

            status = "Overweight"
            bmi_state = "watch"

            recommendation = """
Reduce sugary foods.

Walk at least 45 minutes daily.

Increase vegetables.
"""

        else:

            status = "Obese"
            bmi_state = "attention"

            recommendation = """
Consult a healthcare professional.

Follow a structured exercise plan.

Reduce processed food intake.
"""

        st.markdown(
            theme.vital_card("⚖️", "Your BMI", str(bmi), status, bmi_state),
            unsafe_allow_html=True
        )

        st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
        st.markdown(theme.section_eyebrow("💡", "HEALTH RECOMMENDATION"), unsafe_allow_html=True)
        st.markdown(
            theme.card_open()
            + recommendation.replace("\n\n", "<br>")
            + theme.card_close(),
            unsafe_allow_html=True
        )

        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
        st.markdown(theme.section_eyebrow("📊", "BMI CATEGORIES"), unsafe_allow_html=True)

        bmi_chart = {
            "Underweight":18.5,
            "Healthy":24.9,
            "Overweight":29.9,
            "Obese":35
        }

        fig, ax = plt.subplots(figsize=(7,4))

        ax.bar(
            bmi_chart.keys(),
            bmi_chart.values(),
            color=[theme.COLORS["mint"], theme.COLORS["mint"],
                   theme.COLORS["amber"], theme.COLORS["coral"]]
        )

        ax.set_ylabel("BMI")

        ax.set_title("BMI Categories")

        theme.style_chart(fig, ax)
        fig.tight_layout()

        st.pyplot(fig)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown(theme.section_eyebrow("🧘", "IDEAL LIFESTYLE TIPS"), unsafe_allow_html=True)

        tips = [
            "💧 Drink 2–3 litres of water",
            "🥗 Eat fresh fruits and vegetables",
            "🏃 Exercise at least 30 minutes",
            "😴 Sleep 7–8 hours",
            "🧘 Practice stress management"
        ]

        tips_html = "".join(
            f'<div class="timeline-item"><div class="timeline-dot" '
            f'style="background:{theme.COLORS["mint"]};box-shadow:0 0 8px {theme.COLORS["mint"]};"></div>'
            f'<div class="timeline-text"><span>{tip}</span></div></div>'
            for tip in tips
        )

        st.markdown(theme.card_open() + tips_html + theme.card_close(), unsafe_allow_html=True)
# ---------------- MEDICATION CENTER ---------------- #

elif menu == "💊 Medication Center":

    st.markdown(theme.section_eyebrow("💊", "MEDICATION"), unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:1.3rem;'
        'font-weight:600;margin-bottom:14px;">Medication Center</div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "➕ Add Medicine",
            "📋 My Medicines",
            "⚠ Interaction Checker",
            "🤖 AI Medicine Info"
        ]
    )

    # ---------------- ADD MEDICINE ---------------- #

    with tab1:

        st.subheader("Add New Medication")

        med_name = st.text_input(
            "Medicine Name",
            placeholder="Example: Paracetamol"
        )

        med_time = st.time_input("Medicine Time")

        dosage = st.text_input(
            "Dosage (Example: 500mg)",
            placeholder="Example: 500mg"
        )

        if st.button("➕ Add Medication"):

            add_new_medication(
                med_name,
                str(med_time)
            )

            st.success("Medication Added Successfully!")

    # ---------------- MEDICINE LIST ---------------- #

    with tab2:

        st.subheader("Your Medication List")

        medicines = list_medications()

        if medicines:

            rows = "".join(
                theme.timeline_item(t, name, "steady") for name, t in medicines
            )
            st.markdown(theme.card_open() + rows + theme.card_close(), unsafe_allow_html=True)

        else:

            st.info("No medications added yet.")

    # ---------------- INTERACTION CHECKER ---------------- #

    with tab3:

        st.subheader("Drug Interaction Checker")

        medicine1 = st.text_input(
            "Medicine 1",
            placeholder="Example: Aspirin"
        )

        medicine2 = st.text_input(
            "Medicine 2",
            placeholder="Example: Ibuprofen"
        )

        if st.button("Check Interaction"):

            result = check_interaction(
                medicine1,
                medicine2
            )

            st.warning(result)

    # ---------------- AI MEDICINE INFORMATION ---------------- #

    with tab4:

        st.subheader("🤖 AI Medicine Information")

        medicine = st.text_input(
            "Enter Medicine Name",
            placeholder="Example: Metformin"
        )

        if st.button("Get AI Information"):

            if medicine == "":

                st.warning("Please enter medicine name.")

            else:

                try:
                    placeholder = st.empty()
                    placeholder.markdown(theme.thinking_pulse("Looking up medicine info"), unsafe_allow_html=True)

                    answer = ask_health_question(
                        f"""
Provide complete healthcare information about {medicine}.

Include:

1. Uses

2. Dosage

3. Side Effects

4. Precautions

5. Food Interactions

6. Important Warnings

Keep the response simple and easy to understand.
"""
                    )

                    placeholder.empty()
                    st.markdown(theme.chat_bubble("assistant", answer), unsafe_allow_html=True)

                except:

                    st.error(
                        "Unable to fetch medicine information."
                    )
# ---------------- HEALTH REPORT ---------------- #
elif menu == "📄 Health Report":

    st.markdown(theme.section_eyebrow("📄", "REPORT"), unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:1.3rem;'
        'font-weight:600;margin-bottom:6px;">Personal Health Report</div>',
        unsafe_allow_html=True
    )

    today = datetime.now().strftime("%d %B %Y")

    st.markdown(
        f'<div class="pulse-caption" style="margin-bottom:16px;">Generated on {today}</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(theme.vital_card("⚖️", "BMI", "22.4", "Normal range", "steady"), unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown(theme.vital_card("📈", "Health Score", "92%", "+3% vs last week", "steady"), unsafe_allow_html=True)

    with col2:
        medicines = list_medications()

        st.markdown(theme.section_eyebrow("💊", "CURRENT MEDICATIONS"), unsafe_allow_html=True)

        if medicines:
            rows = "".join(theme.timeline_item(t, name, "steady") for name, t in medicines)
            st.markdown(theme.card_open() + rows + theme.card_close(), unsafe_allow_html=True)
        else:
            st.info("No medications available.")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(theme.section_eyebrow("🤖", "AI GENERATED HEALTH TIPS"), unsafe_allow_html=True)

    if st.button("Generate Today's Tips"):

        try:
            placeholder = st.empty()
            placeholder.markdown(theme.thinking_pulse("Preparing today's tips"), unsafe_allow_html=True)

            tips = ask_health_question(f"""

Today's Date: {today}

Generate 5 different daily health tips.

Requirements:

- Keep every tip short.

- Make tips different every day.

- Include diet, exercise, sleep, hydration and mental health.

Do not repeat tips.

""")

            placeholder.empty()
            st.markdown(theme.chat_bubble("assistant", tips), unsafe_allow_html=True)

        except Exception:

            st.error("Unable to generate today's health tips.")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown(theme.section_eyebrow("📊", "OVERALL HEALTH STATUS"), unsafe_allow_html=True)

    progress = 92

    st.progress(progress)

    st.markdown(
        f'<div class="vital-sub" style="margin-top:-6px;">Overall health score: {progress}%</div>',
        unsafe_allow_html=True
    )



# ---------------- HEALTH GOALS ---------------- #

elif menu == "🎯 Health Goals":

    st.markdown(theme.section_eyebrow("🎯", "GOALS"), unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:1.3rem;'
        'font-weight:600;margin-bottom:14px;">Health Goal Tracker</div>',
        unsafe_allow_html=True
    )

    goal = st.selectbox(

        "Select Goal",

        [

            "Weight Loss",

            "Weight Gain",

            "Maintain Weight",

            "Improve Fitness",

            "Healthy Lifestyle"

        ]

    )

    target = st.number_input(

        "Target Weight (kg)",

        min_value=20,

        max_value=150,

        value=65

    )

    current = st.number_input(

        "Current Weight (kg)",

        min_value=20,

        max_value=150,

        value=70

    )

    progress = int((target/current)*100)

    progress = min(progress,100)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.progress(progress)
    st.markdown(
        f'<div class="vital-sub" style="margin-top:-6px;">Goal progress: {progress}%</div>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    if st.button("Generate Goal Plan"):

        try:
            placeholder = st.empty()
            placeholder.markdown(theme.thinking_pulse("Building your goal plan"), unsafe_allow_html=True)

            plan = ask_health_question(f"""

Generate a healthcare goal plan.

Goal: {goal}

Current Weight: {current}

Target Weight: {target}

Include:

Diet

Exercise

Water Intake

Sleep

Motivation

""")

            placeholder.empty()
            st.markdown(theme.section_eyebrow("📋", "PERSONAL GOAL PLAN"), unsafe_allow_html=True)
            st.markdown(theme.chat_bubble("assistant", plan), unsafe_allow_html=True)

        except Exception:

            st.error("Unable to generate plan.")
# ---------------- INDIAN HEALTHCARE ---------------- #

elif menu == "🇮🇳 Indian Healthcare":

    st.markdown(theme.section_eyebrow("🇮🇳", "INDIAN HEALTHCARE"), unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:\'Space Grotesk\',sans-serif;font-size:1.3rem;'
        'font-weight:600;margin-bottom:14px;">Indian Healthcare Services</div>',
        unsafe_allow_html=True
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🥗 Diet Planner",
            "🌿 Ayurvedic Assistant",
            "🩺 Doctor Finder",
            "🛡 Insurance Advisor"
        ]
    )

    # ---------------- DIET PLANNER ---------------- #

    with tab1:

        st.subheader("🥗 AI Indian Diet Planner")

        age = st.number_input("Age", 1, 100, 25)

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        weight = st.number_input(
            "Weight (kg)",
            20,
            200,
            70
        )

        height = st.number_input(
            "Height (cm)",
            50,
            250,
            170
        )

        goal = st.selectbox(
            "Health Goal",
            [
                "Weight Loss",
                "Weight Gain",
                "Maintain Weight"
            ]
        )

        diet = st.selectbox(
            "Food Preference",
            [
                "Vegetarian",
                "Non-Vegetarian"
            ]
        )

        if st.button("Generate Diet Plan"):

            placeholder = st.empty()
            placeholder.markdown(theme.thinking_pulse("Preparing your personalized diet"), unsafe_allow_html=True)

            response = ask_health_question(f"""

Create a personalized Indian diet plan.

Age: {age}

Gender: {gender}

Weight: {weight}

Height: {height}

Goal: {goal}

Food Preference: {diet}

Include:

Breakfast

Lunch

Snacks

Dinner

Water Intake

Foods to Avoid

Daily Calories

""")

            placeholder.empty()
            st.markdown(theme.chat_bubble("assistant", response), unsafe_allow_html=True)

    # ---------------- AYURVEDIC ---------------- #

    with tab2:

        st.subheader("🌿 AI Ayurvedic Assistant")

        symptoms = st.text_area(
            "Describe your symptoms",
            placeholder="Example: Frequent headaches, poor digestion, low energy in the mornings..."
        )

        if st.button("Get Ayurvedic Advice"):

            placeholder = st.empty()
            placeholder.markdown(theme.thinking_pulse("Generating Ayurvedic suggestions"), unsafe_allow_html=True)

            answer = ask_health_question(f"""

Provide Ayurvedic suggestions.

Symptoms:

{symptoms}

Include:

Natural Remedies

Foods

Lifestyle Tips

Yoga

When to Consult a Doctor

""")

            placeholder.empty()
            st.markdown(theme.chat_bubble("assistant", answer), unsafe_allow_html=True)

    # ---------------- DOCTOR FINDER ---------------- #

    with tab3:

        st.subheader("🩺 Find Doctors Near You")

        city = st.selectbox(
            "Select City",
            [
                "Hyderabad",
                "Delhi",
                "Bangalore",
                "Mumbai",
                "Chennai"
            ]
        )

        speciality = st.selectbox(
            "Select Specialization",
            [
                "General Physician",
                "Cardiologist",
                "Dermatologist",
                "Orthopedic",
                "Pediatrician",
                "Neurologist"
            ]
        )

        doctors = [

            {
                "city":"Hyderabad",
                "speciality":"Cardiologist",
                "name":"Dr. Ramesh Reddy",
                "hospital":"Apollo Hospitals",
                "experience":"15 Years",
                "rating":"⭐ 4.8",
                "phone":"+91-9876543210"
            },

            {
                "city":"Hyderabad",
                "speciality":"General Physician",
                "name":"Dr. Priya Sharma",
                "hospital":"Yashoda Hospitals",
                "experience":"10 Years",
                "rating":"⭐ 4.7",
                "phone":"+91-9123456789"
            },

            {
                "city":"Delhi",
                "speciality":"Dermatologist",
                "name":"Dr. Amit Singh",
                "hospital":"Fortis Hospital",
                "experience":"12 Years",
                "rating":"⭐ 4.9",
                "phone":"+91-9988776655"
            },

            {
                "city":"Bangalore",
                "speciality":"Orthopedic",
                "name":"Dr. Rahul Kumar",
                "hospital":"Manipal Hospital",
                "experience":"14 Years",
                "rating":"⭐ 4.8",
                "phone":"+91-9345678912"
            },

            {
                "city":"Mumbai",
                "speciality":"Neurologist",
                "name":"Dr. Neha Mehta",
                "hospital":"Kokilaben Hospital",
                "experience":"18 Years",
                "rating":"⭐ 4.9",
                "phone":"+91-9870012345"
            },

            {
                "city":"Chennai",
                "speciality":"Pediatrician",
                "name":"Dr. Lakshmi Iyer",
                "hospital":"Apollo Chennai",
                "experience":"11 Years",
                "rating":"⭐ 4.8",
                "phone":"+91-9444455555"
            }

        ]

        if st.button("🔍 Search Doctors"):

            found = False

            for doctor in doctors:

                if doctor["city"] == city and doctor["speciality"] == speciality:

                    found = True

                    with st.container():

                        st.markdown(theme.card_open(), unsafe_allow_html=True)

                        st.subheader(f"👨‍⚕️ {doctor['name']}")

                        col1,col2 = st.columns(2)

                        with col1:

                            st.write("🏥 Hospital:",doctor["hospital"])
                            st.write("🩺 Specialization:",doctor["speciality"])
                            st.write("⭐ Rating:",doctor["rating"])

                        with col2:

                            st.write("📅 Experience:",doctor["experience"])
                            st.write("📞 Contact:",doctor["phone"])
                            st.success("Available for Appointment")

                        st.markdown(theme.card_close(), unsafe_allow_html=True)

            if not found:

                st.error("No doctors found.")

    # ---------------- INSURANCE ---------------- #

    with tab4:

        st.subheader("🛡 AI Health Insurance Advisor")

        age = st.number_input(
            "Your Age",
            18,
            100,
            30
        )

        family = st.number_input(
            "Family Members",
            1,
            10,
            2
        )

        budget = st.selectbox(

            "Monthly Budget",

            [

                "₹500",

                "₹1000",

                "₹2000",

                "₹5000"

            ]

        )

        if st.button("Suggest Insurance"):

            placeholder = st.empty()
            placeholder.markdown(theme.thinking_pulse("Finding suitable insurance"), unsafe_allow_html=True)

            advice = ask_health_question(f"""

Suggest a health insurance plan.

Age:

{age}

Family Members:

{family}

Budget:

{budget}

Include:

Coverage

Benefits

Who should choose it

Precautions

""")

            placeholder.empty()
            st.markdown(theme.chat_bubble("assistant", advice), unsafe_allow_html=True)
