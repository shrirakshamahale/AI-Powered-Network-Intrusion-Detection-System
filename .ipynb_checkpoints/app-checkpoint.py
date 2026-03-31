import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("model/model.pkl")

st.set_page_config(page_title="SentinelNet", layout="centered")

st.title("🔐 SentinelNet")
st.subheader("AI-Powered Intrusion Detection System")

st.write("Enter network traffic features:")

# Create inputs
features = []

for i in range(20):   # reduce for usability
    val = st.number_input(f"Feature {i}", value=0.0)
    features.append(val)

# Predict button
if st.button("Detect Attack"):
    try:
        prediction = model.predict([features])[0]

        if prediction == 0:
            st.success("✅ Normal Traffic")
        else:
            st.error("⚠️ Intrusion Detected")

    except:
        st.warning("⚠️ Feature mismatch. Train model with selected features.")