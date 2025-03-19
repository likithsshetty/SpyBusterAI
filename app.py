# Importing required libraries
from flask import Flask, request, jsonify
import numpy as np
import pickle
import warnings
from feature import FeatureExtraction

warnings.filterwarnings('ignore')

# Load the model
try:
    with open("newmodel.pkl", "rb") as file:
        gbc = pickle.load(file)
except FileNotFoundError:
    raise Exception("Model file 'newmodel.pkl' not found. Ensure it exists in the correct path.")

# Initialize Flask app
app = Flask(__name__)

@app.route('/api/v1/', methods=['POST'])
def predict():
    if request.method == "POST":
        # Get JSON data
        data = request.get_json()

        # Validate input
        if 'url' not in data:
            return jsonify({"error": "Missing 'url' parameter"}), 400

        url = data['url']
        print("Received URL:", url)

        # Extract features
        obj = FeatureExtraction(url)
        features = obj.getFeaturesList()

        # Ensure it's a NumPy array of standard Python types
        x = np.array(features, dtype=np.float64).reshape(1, -1)  # Use float64 to avoid int64 issue

        # Predict
        y_pred = gbc.predict(x)[0]  # Convert to Python native type
        status = False if y_pred == 1 else True

        if status == False:
            data = jsonify({
                "status": "Safe",
                "message": "Safe to continue",
            })
        else:
            data = jsonify({
                "status": "Not Safe",
                "message": "Still want to continue?",
            })

        # Return response
        return data

if __name__ == "__main__":
    app.run(debug=True)
