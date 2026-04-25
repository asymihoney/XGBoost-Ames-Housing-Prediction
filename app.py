import streamlit as st
import pandas as pd
import joblib
import numpy as np

# 1. Load the model and the feature list
# Make sure these files exist in your 'models/' folder!
model = joblib.load('models/housing_model.pkl')
model_features = joblib.load('models/features.pkl')

st.set_page_config(page_title="Ames House Price Predictor", layout="centered")

st.title("Ames Housing Price Predictor")
st.write("Enter the house details below to get an estimated market price.")

# 2. Create Input Fields for the 'Big 3' drivers of price
col1, col2 = st.columns(2)

with col1:
    total_bsmt = st.number_input("Basement Area (sq ft)", value=1000)
    first_flr = st.number_input("1st Floor Area (sq ft)", value=1200)
    second_flr = st.number_input("2nd Floor Area (sq ft)", value=0)

with col2:
    gr_liv_area = st.number_input("Above Ground Living Area (sq ft)", value=1500)
    overall_qual = st.slider("Overall Quality (1-10)", 1, 10, 6)
    garage_cars = st.selectbox("Garage Capacity (Cars)", [0, 1, 2, 3, 4, 5])

# 3. Process Input
if st.button("Predict Sale Price"):
    # Create a DataFrame with 0s for all features the model expects
    input_data = pd.DataFrame(0, index=[0], columns=model_features)
    
    # Fill in the values we collected from the UI
    # Note: Use the exact column names your model saw during training!
    if 'Total Bsmt SF' in model_features: input_data['Total Bsmt SF'] = total_bsmt
    if '1st Flr SF' in model_features: input_data['1st Flr SF'] = first_flr
    if '2nd Flr SF' in model_features: input_data['2nd Flr SF'] = second_flr
    if 'Gr Liv Area' in model_features: input_data['Gr Liv Area'] = gr_liv_area
    if 'Overall Qual' in model_features: input_data['Overall Qual'] = overall_qual
    if 'Garage Cars' in model_features: input_data['Garage Cars'] = garage_cars
    
    # Calculate the engineered feature 'TotalSF' manually
    if 'TotalSF' in model_features:
        input_data['TotalSF'] = total_bsmt + first_flr + second_flr
    
    # 4. Make Prediction
    prediction = model.predict(input_data)[0]
    
    st.markdown("---")
    st.subheader(f"Estimated Price: ${prediction:,.2f}")
    
    # Show a little advice based on the prediction
    if prediction > 300000:
        st.success("This is considered a Luxury Property in Ames.")
    elif prediction < 150000:
        st.info("This is an affordable entry-level home.")