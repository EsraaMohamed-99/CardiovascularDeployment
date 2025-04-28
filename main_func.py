#!/usr/bin/env python
# coding: utf-8

from Scripts import Imports
from Scripts import Prediction_Func
from Scripts import Preprocessing_Func_File

Imports.st.title("Cardiovascular Disease Prediction")
# File path or URL of your image
image_path_ProjectLogo = "Images/Cardiovascular_disease.png"
image_DEPI_Logo="Images/Logo.PNG"
# Function to display an image at the top right
def display_logo(image_path):
    # Convert the image to base64 to display inline
    with open(image_path, "rb") as img_file:
        img_base64 = Imports.base64.b64encode(img_file.read()).decode()

    # Insert the logo with CSS to position it at the top right
    Imports.st.markdown(
        f"""
        <style>
        .top-right-logo {{
            position: fixed;
            top: 60px;  /* ?? Increase this value to move logo down */
            right: 10px;
            z-index: 999;
        }}
        </style>
        <div class="top-right-logo">
            <img src="data:image/png;base64,{img_base64}" width="100"/>
        </div>
        """,
        unsafe_allow_html=True
    )

# Example usage
display_logo(image_DEPI_Logo)

# Read and encode the image in base64
with open(image_path_ProjectLogo, "rb") as image_file:
    encoded = Imports.base64.b64encode(image_file.read()).decode()

# Display the image centered with specific width
Imports.st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{encoded}' width='300'/>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Input Fields ---
age = Imports.st.slider("Age", 29, 79, 50)
gender = Imports.st.selectbox("Gender", ["Male", "Female"])
height = Imports.st.number_input("Height (cm)", 100, 200, 170)
weight = Imports.st.number_input("Weight (kg)", 45, 190, 70)
ap_hi = Imports.st.number_input("Systolic Blood Pressure (ap_hi (mmHg))", 50, 250, 120)
ap_lo = Imports.st.number_input("Diastolic Blood Pressure (ap_lo (mmHg))", 40, 150, 80)
cholesterol = Imports.st.selectbox("Cholesterol Level", ["Normal", "Borderline High", "High"])
gluc = Imports.st.selectbox("Glucose Level", ["Normal", "Borderline High", "High"])
smoke = Imports.st.selectbox("Do you smoke?", ["No", "Yes"])
alco = Imports.st.selectbox("Do you drink alcohol?", ["No", "Yes"])
active = Imports.st.selectbox("Are you physically active?", ["No", "Yes"])

# --- Feature Engineering ---
gender_val = 1 if gender == "Female" else 2
chol_val = ["Normal", "Borderline High", "High"].index(cholesterol) + 1
gluc_val = ["Normal", "Borderline High", "High"].index(gluc) + 1
smoke_val = 1 if smoke == "Yes" else 0
alco_val = 1 if alco == "Yes" else 0
active_val = 1 if active == "Yes" else 0

bmi = weight / ((height / 100) ** 2)
MAP = (2 * ap_lo + ap_hi) / 3
PP = ap_hi - ap_lo
hypertension = 1 if ap_hi >= 140 or ap_lo >= 90 else 0
age_group = 0 if age < 30 else 1 if age < 60 else 2
bmi_category = 0 if bmi < 18.5 else 1 if bmi < 25 else 2 if bmi < 30 else 3
pp_category = 0 if PP < 40 else 1 if PP < 60 else 2


Prerocessed_DF= Preprocessing_Func_File.Preprocessing_Func(age,gender_val,height,weight,ap_hi,ap_lo,chol_val,gluc_val,smoke_val,alco_val,active_val)
    # Function to display the horizontal bar chart with numeric values
def display_feature_bar(label, value, max_value=100):
    percentage = (value / max_value) * 100
    Imports.st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>{label}: {value}</div>
            <div style="background-color: #f2f2f2; width: 80%; height: 25px; border-radius: 12px; margin-left: 10px;">
                <div style="height: 100%; width: {percentage}%; background-color: #4CAF50; border-radius: 12px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- Prediction ---
if Imports.st.button("Predict"):
    Predicted_Value = Prediction_Func.Prediction(Prerocessed_DF)
    Imports.st.markdown("---")
    Imports.st.subheader("✅ Result")  # Use the proper emoji directly here

    # Prediction result
    if Predicted_Value == 1:
        message_HighRisk = "💔 High risk of cardiovascular disease."  # Use proper emoji
        Imports.st.error(message_HighRisk)  # Display with an error message
    else:
        message_LowRisk = "💖 Low risk of cardiovascular disease."  # Use proper emoji
        Imports.st.success(message_LowRisk)  # Display with a success message
    
    # Show each computed feature with horizontal bars
    display_feature_bar("BMI", round(bmi, 2), max_value=40)  # Adjust max_value for scale
    display_feature_bar("MAP", round(MAP, 2), max_value=120)  # Adjust max_value for scale
    display_feature_bar("PP", round(PP, 2), max_value=100)   # Adjust max_value for scale
    display_feature_bar("Hypertension", hypertension, max_value=1)  # Binary (0 or 1)
    display_feature_bar("Age Group", age_group, max_value=2)  # Age group (0-2)
    display_feature_bar("BMI Category", bmi_category, max_value=3)  # BMI category (0-3)
    display_feature_bar("PP Category", pp_category, max_value=2)  # PP category (0-2)




	

	







