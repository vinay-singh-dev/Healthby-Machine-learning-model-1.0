import streamlit as st
import numpy as np
from PIL import Image
import tempfile
import os
from ai_model import diagnose_image
from chatbot import talk_to_bot
import matplotlib.pyplot as plt
import plotly.express as px
import time
import firebase_admin
from firebase_admin import credentials, auth, firestore
import random
from streamlit_lottie import st_lottie
import json

# Firebase initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Page configuration
st.set_page_config(page_title="AI Health Tracker", layout="centered")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Function to load the Lottie animation
def load_lottie_animation(file_path: str):
    with open(file_path, "r") as f:
        return json.load(f)

# Function to apply custom theme
def apply_custom_theme():
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #f9fbfd;
            }
            .title {
                text-align: center;
                font-size: 2.5rem;
                font-weight: bold;
                color: #0b3954;
            }
            .option-card {
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
                text-align: center;
                background-color: #e6f0fa;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            }
            .chat-bubble {
                background-color: #e0f7fa;
                border-radius: 15px;
                padding: 10px 20px;
                margin: 20px 0;
                display: inline-block;
                color: #006064;
                font-weight: 600;
            }
            .float-left {
                float: left;
                margin-right: 20px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Tip of the Day
def get_tip_of_the_day():
    tips = [
        "Drink plenty of water daily to keep your skin hydrated.",
        "Use sunscreen even on cloudy days to protect your skin.",
        "Regular sleep helps your body heal and your skin glow.",
        "Avoid touching your face frequently to prevent breakouts.",
        "Moisturize your skin daily to maintain its natural barrier.",
        "Exercise boosts blood flow, nourishing skin cells.",
        "Always remove makeup before going to bed."
    ]
    random.seed(time.localtime().tm_yday)
    return random.choice(tips)

# Login Page
def login_page():
    st.markdown("<h1 class='title'>Login to AI Health Tracker</h1>", unsafe_allow_html=True)
    st.image('assets/logo.png', width=100)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.user = user
            st.session_state.logged_in = True
            store_login_history(user.uid)
            st.success(f"Welcome back, {user.email}!")
        else:
            st.error("Invalid login credentials.")

# Signup Page
def signup_page():
    st.markdown("<h1 class='title'>Create Your Account</h1>", unsafe_allow_html=True)
    st.image('assets/logo.png', width=100)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    name = st.text_input("Name")
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        elif email and password and name:
            try:
                user = auth.create_user(email=email, password=password)
                user_ref = db.collection("users").document(user.uid)
                user_ref.set({"name": name})
                st.session_state.user = user
                st.session_state.logged_in = True
                st.success(f"Account created successfully. Welcome {user.email}!")
                store_login_history(user.uid)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Fill all fields.")

def login_user(email, password):
    try:
        user = auth.get_user_by_email(email)
        return user
    except:
        return None

def store_login_history(user_id):
    db.collection("login_history").document(user_id).set({"last_login": firestore.SERVER_TIMESTAMP}, merge=True)

# Main App
def main_app():
    apply_custom_theme()

    col1, col2 = st.columns([1, 3])
    with col1:
        st.image('assets/logo.png', width=80)
    with col2:
        st.markdown("<h1 class='title'>Welcome to AI Health Tracker</h1>", unsafe_allow_html=True)
        st.markdown(f"💡 **Tip of the Day:** {get_tip_of_the_day()}")
        st.image('assets/doctor_image.jpg', caption="Your Health Companion", width=150)

    st.write("Get started by choosing one of the options below:")

    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.markdown("<div class='option-card'>", unsafe_allow_html=True)
            st.image('assets/image_diagnosis_icon.png', width=80)
            st.subheader("📷 Image Diagnosis")
            st.caption("Upload a skin image")
            if st.button("Start Image Diagnosis"):
                st.session_state.mode = "image"
            st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        with st.container():
            st.markdown("<div class='option-card'>", unsafe_allow_html=True)
            st.image('assets/text_diagnosis_icon.png', width=80)
            st.subheader("📝 Text Diagnosis")
            st.caption("Describe your symptoms")
            if st.button("Start Text Diagnosis"):
                st.session_state.mode = "text"
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='chat-bubble'>Hi there! How can I assist you today?</div>", unsafe_allow_html=True)
    st.image('assets/patient_image.jpg', caption="Patient Support", width=150)

    st.markdown("---")
    nav = st.radio("Navigation", ["🏠 Home", "📊 Dashboard", "⚙️ Settings"])
    if nav == "📊 Dashboard":
        dashboard()
    elif nav == "⚙️ Settings":
        st.info("Settings page coming soon!")

    if 'mode' in st.session_state:
        progress_bar = st.empty()
        if st.session_state.mode == "image":
            image_diagnosis(progress_bar)
        elif st.session_state.mode == "text":
            text_diagnosis(progress_bar)

# Image Diagnosis
def image_diagnosis(progress_bar):
    uploaded_file = st.file_uploader("Upload a skin image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                progress_bar.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i+1)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    diagnosis = diagnose_image(tmp_file.name)
                    clean_diagnosis = diagnosis.split('(')[0].strip()
                    st.success(f"🤖 Disease: {diagnosis}.")

                    diagnosis_data = {
                        "user_id": st.session_state.user.uid,
                        "diagnosis": clean_diagnosis,
                        "timestamp": firestore.SERVER_TIMESTAMP
                    }
                    db.collection("diagnosis_history").document(st.session_state.user.uid).set(diagnosis_data, merge=True)

                    response = talk_to_bot(f"Tell me about {clean_diagnosis}")
                    st.markdown(f"<div class='chat-bubble'>{response}</div>", unsafe_allow_html=True)
                    os.remove(tmp_file.name)

# Text Diagnosis
def text_diagnosis(progress_bar):
    symptoms = st.text_input("Describe your symptoms")
    if st.button("Ask AI"):
        if symptoms:
            with st.spinner("Consulting AI..."):
                progress_bar.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i+1)
                response = talk_to_bot(symptoms)
                st.markdown(f"<div class='chat-bubble'>{response}</div>", unsafe_allow_html=True)
        else:
            st.warning("Please describe your symptoms.")

# Dashboard
def dashboard():
    st.header("📊 Health Dashboard")
    diagnoses = db.collection("diagnosis_history").stream()
    records = [d.to_dict() for d in diagnoses]
    total = len(records)
    st.metric("Total Diagnoses", total)

    from collections import Counter
    counter = Counter([r["diagnosis"] for r in records if "diagnosis" in r])
    if counter:
        top_disease, count = counter.most_common(1)[0]
        st.metric("Most Common Disease", f"{top_disease} ({count})")

    fig = px.pie(names=list(counter.keys()), values=list(counter.values()), title="Disease Distribution")
    st.plotly_chart(fig)

    feedbacks = db.collection("feedback").stream()
    feedback_list = [f.to_dict().get("feedback") for f in feedbacks]
    positives = feedback_list.count("👍 Accurate")
    negatives = feedback_list.count("👎 Inaccurate")
    st.bar_chart({"Feedback": ["Accurate", "Inaccurate"], "Count": [positives, negatives]})

# Main Function
def main():
    apply_custom_theme()

    lottie_animation = load_lottie_animation("assets/loading_spinner.json")
    st_lottie(lottie_animation, speed=1, width=300, height=300, key="animation")

    if not st.session_state.logged_in:
        page = st.radio("Welcome", ["Login", "Signup"])
        if page == "Login":
            login_page()
        else:
            signup_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
