import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import requests
import plotly.express as px
from sklearn.linear_model import LinearRegression

# Define paths
MODEL_URL = "https://raw.githubusercontent.com/Prachi-02-02/co2_prediction_project/main/co2_model.pkl"
DATA_URL = "https://raw.githubusercontent.com/Prachi-02-02/co2_prediction_project/main/data.csv"

MODEL_PATH = "co2_model.pkl"
DATA_PATH = "data.csv"

# Function to download files
def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    return False

# Check if model exists, if not download it
if not os.path.exists(MODEL_PATH):
    st.info("Downloading model...")
    if download_file(MODEL_URL, MODEL_PATH):
        st.success("✅ Model downloaded successfully!")
    else:
        st.error("❌ Failed to download model.")

# Check if data exists, if not download it
if not os.path.exists(DATA_PATH):
    st.info("Downloading data file...")
    if download_file(DATA_URL, DATA_PATH):
        st.success("✅ Data file downloaded successfully!")
    else:
        st.error("❌ Failed to download data file.")


# Train or load model
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)  # Load the existing model
    
else:
    st.warning("Model not found. Training new model...")
    # Simulate training (replace this with your actual model training code)
    X_train = df[['weight', 'volume']]  # Features
    y_train = df['CO2']  # Target
    model = LinearRegression()
    model.fit(X_train, y_train)  # Train the model
    joblib.dump(model, MODEL_PATH)  # Save the trained model
    st.success("✅ Model trained and saved successfully!")

# ===================== New Theme & Animated Background =====================

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

# Display Centered Image (Make sure 'image.png' is in the same folder)
st.image("image.png", width=900)

# ===================== App UI =====================

st.write(
    "Welcome to the **most exciting** CO₂ emission predictor!  "
    "Enter a car's **weight and engine size**, and watch the **magic happen**! "
)

# User Inputs with Sliders
st.subheader("🔢 Enter Car Details")
weight = st.slider("Choose Car Weight (kg)", 500, 3000, step=50)
volume = st.slider("Choose Engine Size (cm³)", 800, 5000, step=100)

# Predict Button
prediction = None  # Initialize before use
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

   # Load dataset after downloading it
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)  # Load dataset
else:
    st.error("❌ Data file not found.")

# Interactive 3D Plot
# Ensure prediction exists before using it in the plot
if prediction is not None:
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
    {"question": "Why are electric cars better for the environment?", "options": ["They fly", "They don’t use gas", "They produce more CO₂"], "answer": "They don’t use gas"}
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
