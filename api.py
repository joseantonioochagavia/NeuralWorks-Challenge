from flask import Flask, request, jsonify
from joblib import dump, load
import pandas as pd

# Load the machine learning model from the pickle file
model = load('random_forest_simplificado.pkl')

# Load the column names from the pickle file
columns = load('rf_columns_simplificado.pkl')

# Create a Flask app
app = Flask(__name__)

# Define the API endpoint for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request. The input should be enter as a json file withe the columns names and their respective values in the same order the model was trained
    input_data = request.get_json()

    # Convert the input data to a Pandas DataFrame
    input_df = pd.DataFrame([input_data])

    # Make a prediction with the model
    prediction = model.predict(input_df)[0]

    # Return the prediction as a JSON response
    response = {'prediction': int(prediction)}

    return jsonify(response)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)