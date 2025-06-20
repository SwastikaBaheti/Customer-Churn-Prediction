import pickle
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import streamlit as st

# Load the trained model
model = load_model('ann_model.h5')

# Load the proprocesing pickle file
with open('label_encoder_gender.pkl', 'rb') as f:
       label_encoder_gender = pickle.load(file=f)

with open('onehot_encoder_geography.pkl', 'rb') as f:
        onehot_encoder_geography = pickle.load(file=f)

with open('standard_scaler.pkl', 'rb') as f:
        std_scaler = pickle.load(file=f)


# Steamlit app
st.title('Churn Prediction Application')

# User input
geography = st.selectbox('Geography', onehot_encoder_geography.categories_[0])
gender = st.selectbox('Gender', label_encoder_gender.classes_)
age = st.slider('Age', 18, 92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit Score')
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0, 10)
num_of_products = st.slider('Number of Products', 1, 4)
has_cr_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])

# Input data
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

# Preprocessing the input data
onehotencoded_geography = onehot_encoder_geography.transform([[geography]])
input_data = pd.concat([pd.DataFrame(onehotencoded_geography, columns=onehot_encoder_geography.get_feature_names_out()), input_data], axis=1)

# Applying standard scaling over the input_data
input_preprocessed = std_scaler.transform(input_data)

# Model prediction
model_prediction = model.predict(input_preprocessed)
model_prediction_prob = model_prediction[0][0]

st.write('Churn probability', model_prediction_prob)

if model_prediction_prob > 0.5:
    st.write('The customer is likely to churn')
else:
    st.write('The customer is not likely to churn')