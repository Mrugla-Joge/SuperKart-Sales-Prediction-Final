
# Import required libraries
import streamlit as st
import requests
import pandas as pd


# ------------------------------------------------------------
# Backend API URL

# "backend" is the Docker container name for the Flask backend
BACKEND_URL = "http://backend:7860"



# Page title and description

st.title("SuperKart Sales Prediction System")

st.write(
    "Enter the product and store details below to predict the total sales."
)


# ============================================================
# SINGLE SALES PREDICTION


st.subheader("Single Sales Prediction")

# Input fields for product information


# Product weight
Product_Weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.66
)

# Product sugar content
Product_Sugar_Content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

# Product allocated area
Product_Allocated_Area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.027
)

# Product MRP
Product_MRP = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=117.08
)


# ------------------------------------------------------------
# Input fields for store information


# Store Size
Store_Size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

# Store location city type
Store_Location_City_Type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

# Store type
Store_Type = st.selectbox(
    "Store Type",
    [
        "Supermarket Type1",
        "Supermarket Type2",
        "Supermarket Type3",
        "Departmental Store",
        "Food Mart"
    ]
)

# Product ID character
Product_Id_char = st.selectbox(
    "Product ID Character",
    ["FD", "DR", "NC"]
)

# Store age in years
Store_Age_Years = st.number_input(
    "Store Age (Years)",
    min_value=0,
    value=16
)

# Product type category
Product_Type_Category = st.selectbox(
    "Product Type Category",
    ["Perishables", "Non Perishables"]
)


# ------------------------------------------------------------
# Prepare input data for the backend API



product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}


# ------------------------------------------------------------
# Send single prediction request to Flask backend


if st.button("Predict Sales"):

    try:

        response = requests.post(
            f"{BACKEND_URL}/v1/predict",
            json=product_data
        )

        # Check if backend returned successful response
        if response.status_code == 200:

            prediction = response.json()

            st.success(
                f"Predicted Sales: "
                f"{prediction['predicted_product_store_sales']}"
            )

        else:

            st.error("Unable to generate prediction.")
            st.write(response.text)

    except requests.exceptions.RequestException as e:

        st.error(
            f"Unable to connect to the backend API: {e}"
        )


# ============================================================
# BATCH SALES PREDICTION


st.subheader("Batch Sales Prediction")

st.write(
    "Upload a CSV file to generate predictions for multiple products."
)


# Upload batch CSV file


uploaded_file = st.file_uploader(
    "Upload Batch CSV File",
    type=["csv"]
)


# Send uploaded CSV file to Flask backend


if uploaded_file is not None:

    if st.button("Predict Batch Sales"):

        try:

            # Prepare uploaded CSV file for the API
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "text/csv"
                )
            }

            # Send CSV to batch prediction endpoint
            response = requests.post(
                f"{BACKEND_URL}/v1/predictbatch",
                files=files
            )


          
            # Display batch prediction results
          

            if response.status_code == 200:

                predictions = response.json()

                st.success(
                    "Batch prediction completed successfully!"
                )

                # Convert prediction dictionary into a DataFrame
                prediction_df = pd.DataFrame(
                    list(predictions.items()),
                    columns=["Row", "Predicted Sales"]
                )

                # Display predictions
                st.dataframe(prediction_df)

            else:

                st.error(
                    f"Batch prediction failed. "
                    f"Status code: {response.status_code}"
                )

                # Display backend error message
                st.write(response.text)


        except requests.exceptions.RequestException as e:

            st.error(
                f"Unable to connect to the backend API: {e}"
            )
