import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time
import plotly.express as px
import os
import requests 
MODEL_URL = "https://raw.githubusercontent.com/Prachi-02-02/co2_prediction_project/main/co2_model.pkl"
DATA_URL = "https://raw.githubusercontent.com/Prachi-02-02/co2_prediction_project/main/data.csv"


MODEL_PATH = "C:\\Users\\ADMIN\\Machine Learning\\CO2_Prediction_Project\\co2_model.pkl"
DATA_PATH = "C:\\Users\\ADMIN\\Machine Learning\\CO2_Prediction_Project\\data.csv"

def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    return False

# Download model if not found
if not os.path.exists(MODEL_PATH):
    st.info("Downloading model...")
    if download_file(MODEL_URL, MODEL_PATH):
        st.success("✅ Model downloaded successfully!")
    else:
        st.error("❌ Failed to download model.")

# Download data if not found
if not os.path.exists(DATA_PATH):
    st.info("Downloading data file...")
    if download_file(DATA_URL, DATA_PATH):
        st.success("✅ Data file downloaded successfully!")
    else:
        st.error("❌ Failed to download data file.")

# Load Model
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    st.success("✅ Model loaded successfully!")
else:
    st.error("❌ Model file missing!")

# Load Data
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    st.write("📊 Data Sample:", df.head())
else:
    st.error("❌ Data file missing!")

# ===================== New Theme & Animated Background =====================


import streamlit as st

# Custom Title with Styling
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap');
        
        .title {
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            color: #05445E; /* Dark Blue */
            font-family: 'Poppins', sans-serif;
        }
    </style>

    <div class="title"> CO₂ Emission Predictor</div>
    """,
    unsafe_allow_html=True
)

# Display Centered Image (Make sure 'car.png' is in the same folder)
st.image("image.png", width=900)

# To Center the Image (Streamlit workaround)
st.markdown(
    """
    <style>
        .stImage img {
            display: flex;
            margin-left: auto;
            margin-right: auto;
            justify-content: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        /* Background Color */
        .stApp {
            background-color:#D7F9FF;  /* Light Blue */
        }

        /* Custom Font */
        @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&display=swap');
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Comic Neue', cursive;
            color: #ff5733;
        }
        body, p, div {
            font-family: 'Comic Neue', cursive;
            color: #34495E;
        }

    </style>
    """,
    unsafe_allow_html=True,
)





# ===================== App UI =====================

#st.title("CO₂ Emission Predictor")
st.write(
    "Welcome to the **most exciting** CO₂ emission predictor!  "
    "Enter a car's **weight and engine size**, and watch the **magic happen**! "
)

# User Inputs with Sliders
st.subheader("🔢 Enter Car Details")
weight = st.slider("Choose Car Weight (kg)", 500, 3000, step=50)
volume = st.slider("Choose Engine Size (cm³)", 800, 5000, step=100)

# Predict Button
if st.button("🔍 Predict CO₂ Emission"):
    prediction = model.predict([[weight, volume]])[0]
    
    # Assign Pollution Level Colors
    if prediction < 100:
        color = "🟢 Low Emission"
    elif prediction < 200:
        color = "🟡 Medium Emission"
    else:
        color = "🔴 High Emission"
    
    # Display Prediction
    st.success(f"🌱 This car will emit **{prediction:.2f} g/km** of CO₂! {color}")

    # 📊 Animated Bar Chart
    chart_data = pd.DataFrame({"CO₂ Emission": [prediction]})
    st.bar_chart(chart_data)

    # 📈 Interactive 3D Plot (Weight vs Volume vs CO₂)
    st.subheader("📊 Interactive 3D CO₂ Visualization")
    fig = px.scatter_3d(df, x="weight", y="volume", z="CO2", color="CO2",
                         title="Weight vs Engine Volume vs CO₂ Emissions",
                         labels={"weight": "Car Weight (kg)", "volume": "Engine Volume (cm³)", "CO2": "CO₂ Emission (g/km)"},
                         opacity=0.7)
    fig.add_scatter3d(x=[weight], y=[volume], z=[prediction], mode='markers', marker=dict(size=10, color='red'), name="Your Car")
    st.plotly_chart(fig)

# ===================== 📚 Fun Quiz Section =====================
st.markdown("---")
st.header("🎓 CO₂ Knowledge Quiz")

# List of Questions
questions = [
    {"question": "What is CO₂?", "options": ["Oxygen", "Carbon Dioxide", "Hydrogen"], "answer": "Carbon Dioxide"},
    {"question": "Which fuel type emits the most CO₂?", "options": ["Petrol", "Diesel", "Electric"], "answer": "Diesel"},
    {"question": "How can we reduce CO₂ emissions?", "options": ["Drive more", "Use renewable energy", "Burn more coal"], "answer": "Use renewable energy"},
    {"question": "Which gas contributes most to global warming?", "options": ["CO₂", "Nitrogen", "Oxygen"], "answer": "CO₂"},
    {"question": "What is the main source of CO₂ emissions?", "options": ["Factories", "Cars & Transportation", "Trees"], "answer": "Cars & Transportation"},
    {"question": "Which energy source produces zero CO₂?", "options": ["Coal", "Solar", "Gasoline"], "answer": "Solar"},
    {"question": "What happens if too much CO₂ is in the atmosphere?", "options": ["Global warming", "More oxygen", "Stronger storms"], "answer": "Global warming"},
    {"question": "Which human activity emits the most CO₂?", "options": ["Watching TV", "Burning fossil fuels", "Swimming"], "answer": "Burning fossil fuels"},
    {"question": "Which of these can help reduce CO₂?", "options": ["Planting trees", "Throwing plastic in oceans", "Using more cars"], "answer": "Planting trees"},
    {"question": "Why are electric cars better for the environment?", "options": ["They fly", "They don’t use gas", "They produce more CO₂"], "answer": "They don’t use gas"}, {
        "question": "What is the **average CO₂ emission** of a petrol car?",
        "options": ["50 g/km", "150 g/km", "300 g/km", "500 g/km"],
        "answer": "150 g/km"
    },
    {
        "question": "Which car type emits the **least CO₂**?",
        "options": ["SUV", "Hybrid", "Electric", "Sports Car"],
        "answer": "Electric"
    },
]

# Initialize session state for answers
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# Allow users to select answers for all questions at once
for i, q in enumerate(questions):
    st.subheader(f"**Question {i+1}:** {q['question']}")
    selected_answer = st.radio("Choose your answer:", q["options"], key=f"q{i}", index=None)
    
    # Store user's answer in session state
    if selected_answer:
        st.session_state.quiz_answers[i] = selected_answer

# Compute final score when button is clicked
if st.button("📊 Get My Final Score"):
    correct_answers = sum(1 for i, q in enumerate(questions) if i in st.session_state.quiz_answers and st.session_state.quiz_answers[i] == q["answer"])
    
    st.info(f"🎯 Your Final Score: **{correct_answers}/{len(questions)}**")

    if correct_answers == len(questions):
        st.balloons()
        st.success("🎉 Excellent! You're a CO₂ expert! 👍")
    elif correct_answers >= len(questions) // 2:
        st.success("💡 Good Job! Keep learning!")
    else:
        st.warning("📚 Keep practicing! You'll get better!")



# 🎉 Fun Fact Section
st.info("💡 **Fun Fact**: The **Toyota Prius** emits only **43 g/km of CO₂**, while older diesel cars emit over **300 g/km**! 🚙")
st.info("💡 **Fun Fact**: **The Airplanes emit more CO₂** per passenger than a car on a long trip. ✈️🌍! 🚙")





# Footer
st.markdown(
    """
    <style>
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .footer {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            padding: 20px;
            animation: fadeIn 2s ease-in-out;
        }
    </style>
    
    <div class="footer">
        🚀 <span style="color: #ff5733;">Unlock the Power of AI!</span>  
        This <span style="color: #2c3e50;">ML Bootcamp</span> demo showcases  
        <span style="color: #27ae60;">Multilinear Regression</span> in action—predicting CO₂ emissions  
        and proving that <span style="color: #f39c12;">machine learning is not just the future, it's YOUR future! 🌍📊💡</span>
    </div>
    """,
    unsafe_allow_html=True
)
try:
    model = joblib.load(MODEL_PATH)
    st.success("✅ Model loaded successfully!")
except Exception as e:
    st.error(f"❌ Model loading failed: {e}")

