import streamlit as st
import pandas as pd
import joblib

# Load model and columns
model = joblib.load("final_model.pkl")
columns = joblib.load("columns.pkl")

st.title("🚗 Second Hand Car Price Prediction App")
st.info("This prediction is based on a regression model trained on real car market data.")
st.subheader("Enter Car Details")

# -------------------------------
# Extract dynamic options
# -------------------------------

model_options = [col.replace("model_", "") for col in columns if col.startswith("model_")]
fuel_options = [col.replace("fuel_type_", "") for col in columns if col.startswith("fuel_type_")]

# -------------------------------
# User Inputs
# -------------------------------

vehicle_age = st.slider("Vehicle Age (Years)", 0, 10, 5)
mileage = st.slider("Mileage (km/l)", 10, 30, 20)

fuel_type = st.selectbox("Fuel Type", fuel_options)

# Dynamic engine input
if fuel_type == "Petrol":
    engine = st.number_input("Engine (CC) - Petrol", 800, 1500, 1200)
elif fuel_type == "Diesel":
    engine = st.number_input("Engine (CC) - Diesel", 1200, 2000, 1500)
else:
    engine = st.number_input("Engine (CC)", 800, 2000, 1200)

model_name = st.selectbox("Model", model_options)
seats = st.selectbox("Seats", [5, 7])

st.caption("Note: Inputs are based on typical Indian second-hand car market trends")

# -------------------------------
# Prediction
# -------------------------------

if st.button("Predict Price"):

    # Initialize all features to 0
    input_dict = {col: 0 for col in columns}

    # Fill numeric values
    input_dict['vehicle_age'] = vehicle_age
    input_dict['mileage'] = mileage
    input_dict['engine'] = engine
    input_dict['seats'] = seats

    # One-hot encoding
    model_col = f"model_{model_name}"
    fuel_col = f"fuel_type_{fuel_type}"

    if model_col in input_dict:
        input_dict[model_col] = 1

    if fuel_col in input_dict:
        input_dict[fuel_col] = 1

    # Convert to DataFrame
    input_df = pd.DataFrame([input_dict])

    # Predict
    prediction = model.predict(input_df)[0]

    # Display result
    st.success(f"💰 Predicted Price: ₹ {int(prediction):,}")