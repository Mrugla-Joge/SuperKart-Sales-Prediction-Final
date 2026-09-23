
# Import necessary libraries
import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app
superkart_api = Flask("SuperKart")

# Load the trained model
model = joblib.load("superkart_model.joblib")

# Home route
@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart System"


# Single prediction endpoint
@superkart_api.post("/v1/predict")
def predict_sales():

    # Get JSON data
    data = request.get_json()

    # Extract the 10 features required by the model
    sample = {
        "Product_Weight": data["Product_Weight"],
        "Product_Sugar_Content": data["Product_Sugar_Content"],
        "Product_Allocated_Area": data["Product_Allocated_Area"],
        "Product_MRP": data["Product_MRP"],
        "Store_Size": data["Store_Size"],
        "Store_Location_City_Type": data["Store_Location_City_Type"],
        "Store_Type": data["Store_Type"],
        "Product_Id_char": data["Product_Id_char"],
        "Store_Age_Years": data["Store_Age_Years"],
        "Product_Type_Category": data["Product_Type_Category"]
    }

    # Convert input into DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    prediction = model.predict(input_data).tolist()[0]

    # Return prediction
    return jsonify({"Sales": prediction})


# Batch prediction endpoint
@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():

    # Get uploaded CSV file
    file = request.files["file"]

    # Read CSV
    input_data = pd.read_csv(file)

    # Make predictions
    predictions = model.predict(input_data).tolist()

    # Create output dictionary
    output_dict = {
        str(i): round(pred, 2)
        for i, pred in enumerate(predictions)
    }

    return output_dict


# Run Flask app
if __name__ == "__main__":
    superkart_api.run(debug=True)
