from flask import Flask, jsonify, request
import pickle
import pandas as pd
import random
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*"])

# Load the trained Isolation Forest model
with open("isolation_forest_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Load the preprocessed test dataset (optional)
test_df = pd.read_pickle("test_df_processed.pkl")


# Function to generate network traffic data
def generate_traffic_data():
    return {
        "labels": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "datasets": [{
            "label": "Network Traffic",
            "data": [random.randint(500, 2000) for _ in range(5)],
            "borderColor": "#36A2EB",
            "backgroundColor": "rgba(54, 162, 235, 0.2)"
        }]
    }

# Function to generate random security alerts
def generate_alerts():
    return [{
        "id": str(i),
        "timestamp": datetime.now().isoformat(),
        "type": "Intrusion",
        "severity": random.choice(["Low", "Medium", "High", "Critical"]),
        "source": "192.168.1." + str(random.randint(1, 255)),
        "destination": "10.0.0." + str(random.randint(1, 255)),
        "details": "Unusual traffic detected."
    } for i in range(3)]


# Function to use Isolation Forest for anomaly detection
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json  # Expecting JSON input
        df = pd.DataFrame([data])  # Convert JSON input to DataFrame
        
        # Ensure the input data has the correct columns
        required_features = test_df.columns.drop("label")  # Drop label column
        df = df[required_features]  # Keep only relevant features

        # Predict using the Isolation Forest model
        prediction = model.predict(df)[0]
        result = "Anomaly" if prediction == -1 else "Normal"

        return jsonify({"prediction": result})
    
    except Exception as e:
        return jsonify({"error": str(e)})


# API endpoint for dashboard data
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    return jsonify({
        "traffic": generate_traffic_data(),
        "alerts": generate_alerts()
    })


if __name__ == '__main__':
    app.run(debug=True)
