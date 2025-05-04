
# Importing required libraries
from flask import Flask, request, jsonify
import numpy as np
import pickle
import warnings
from feature import FeatureExtraction
import logging
from datetime import datetime

warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load the model
try:
    with open("newmodel.pkl", "rb") as file:
        gbc = pickle.load(file)
    logging.info("Model loaded successfully.")
except FileNotFoundError as e:
    logging.error("Model file 'newmodel.pkl' not found.")
    raise Exception("Model file 'newmodel.pkl' not found. Ensure it exists in the correct path.") from e

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the URL Safety Prediction API!"

@app.route('/api/v1/', methods=['POST'])
def predict():
    if request.method == "POST":
        data = request.get_json()
        logging.info(f"Received request data: {data}")

        # Validate input
        if 'url' not in data:
            logging.warning("Missing 'url' parameter in request.")
            return jsonify({"error": "Missing 'url' parameter"}), 400

        url = data['url']
        logging.info(f"Processing URL: {url}")

        try:
            # Extract features
            obj = FeatureExtraction(url)
            features = obj.getFeaturesList()
            x = np.array(features, dtype=np.float64).reshape(1, -1)

            # Predict
            y_pred = gbc.predict(x)[0]
            status = False if y_pred == 1 else True

            result = {
                "status": "Safe" if not status else "Not Safe",
                "message": "Safe to continue" if not status else "Still want to continue?"
            }

            logging.info(f"Prediction result for {url}: {result['status']}")
            return jsonify(result)

        except Exception as e:
            logging.exception("Error during prediction.")
            return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    logging.info("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=80)