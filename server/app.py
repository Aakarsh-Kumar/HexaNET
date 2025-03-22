from flask import Flask, jsonify
from flask_cors import CORS
import os
import random
import pickle
import scapy.all as scapy
import numpy as np
from datetime import datetime
import yagmail
import pickle
import sklearn
import pickle

print(f"Scikit-learn version: {sklearn.__version__}")

app = Flask(__name__)
CORS(app, origins=["*"])

with open("label_encoder.pkl", "rb") as le_file:
    label_encoder = pickle.load(le_file)
with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)
with open("isolation_forest_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

ATTACK_TYPES = ["DDoS", "SQL Injection", "Brute Force", "Phishing", "Malware"]

def capture_live_traffic():
    packets= scapy.sniff(timeout=10)
    traffic_data = []

    for pkt in packets:
        packet_length = len(pkt)
        protocol = pkt[scapy.IP].proto if pkt.haslayer(scapy.IP) else 0  

        service = str(pkt[scapy.IP].proto) if pkt.haslayer(scapy.IP) else "unknown"
        flag = "SYN" if pkt.haslayer(scapy.TCP) and pkt[scapy.TCP].flags == 2 else "other"
        src_bytes = pkt[scapy.IP].len if pkt.haslayer(scapy.IP) else 0
        difficulty = random.choice(["low", "medium", "high"]) 

        traffic_data.append([packet_length, protocol, service, flag, src_bytes, difficulty])

    return traffic_data


# def predict_threats():
#     live_data = capture_live_traffic()
#     if len(live_data) == 0:
#         return []
    
#     live_data_scaled = scaler.transform(live_data)
#     predictions = model.predict(live_data_scaled)
#     threats = []
    
#     for i, pred in enumerate(predictions):
#         if pred == -1: 
#             attack_type = random.choice(ATTACK_TYPES)
#             threats.append({
#                 "id": str(i),
#                 "type": attack_type,
#                 "source": "192.168.1." + str(random.randint(1, 255)),
#                 "firstDetected": datetime.now().isoformat(),
#                 "status": random.choice(["Active", "Mitigated", "Investigating"]),
#                 "confidence": f"{random.randint(70, 99)}%",
#                 "impact": random.choice(["Low", "Moderate", "Severe"])
#             })
#     return threats

# def predict_threats():
#     live_data = capture_live_traffic()

#     if len(live_data) == 0:
#         return []

#     # Convert to DataFrame
#     import pandas as pd
#     live_df = pd.DataFrame(live_data, columns=["packet_length", "protocol", "service", "flag", "src_bytes", "difficulty"])

#     # Apply Label Encoding (same as training)
#     live_df["service"] = live_df["service"].apply(
#     lambda x: x if x in label_encoder.classes_ else "unknown"
#     )
#     label_encoder.classes_ = np.append(label_encoder.classes_, "unknown")
#     live_df["service"] = label_encoder.transform(live_df["service"])

#     # Convert to numpy array
#     live_data_encoded = live_df.values

#     # Scale the data
#     live_data_scaled = scaler.transform(live_data_encoded)

#     # Predict threats
#     predictions = model.predict(live_data_scaled)
#     threats = []

#     for i, pred in enumerate(predictions):
#         if pred == -1:  # Anomalous traffic
#             attack_type = random.choice(ATTACK_TYPES)
#             threats.append({
#                 "id": str(i),
#                 "type": attack_type,
#                 "source": "192.168.1." + str(random.randint(1, 255)),
#                 "firstDetected": datetime.now().isoformat(),
#                 "status": random.choice(["Active", "Mitigated", "Investigating"]),
#                 "confidence": f"{random.randint(70, 99)}%",
#                 "impact": random.choice(["Low", "Moderate", "Severe"])
#             })
    
#     return threats
# def predict_threats():
    live_data = capture_live_traffic()

    if len(live_data) == 0:
        return []

    import pandas as pd
    live_df = pd.DataFrame(live_data, columns=[ "service", "flag", "src_bytes", "difficulty"])

    # Encode "service"
    if "unknown" not in label_encoder.classes_:
        label_encoder.classes_ = np.append(label_encoder.classes_, "unknown")
    live_df["service"] = live_df["service"].apply(lambda x: x if x in label_encoder.classes_ else "unknown")
    live_df["service"] = label_encoder.transform(live_df["service"])

    # Manually encode "flag" (since it's categorical)
    flag_mapping = {"SYN": 1, "other": 0}  # Map "SYN" -> 1, "other" -> 0
    live_df["flag"] = live_df["flag"].map(flag_mapping)

    # Manually encode "difficulty"
    difficulty_mapping = {"low": 0, "medium": 1, "high": 2}  # Convert difficulty to numeric values
    live_df["difficulty"] = live_df["difficulty"].map(difficulty_mapping)

    # Convert to numpy array
    live_data_encoded = live_df.values

    # Scale the data
    live_data_scaled = scaler.transform(live_data_encoded)

    # Predict threats
    predictions = model.predict(live_data_scaled)
    threats = []

    for i, pred in enumerate(predictions):
        if pred == -1:  # Anomalous traffic
            attack_type = random.choice(ATTACK_TYPES)
            threats.append({
                "id": str(i),
                "type": attack_type,
                "source": "192.168.1." + str(random.randint(1, 255)),
                "firstDetected": datetime.now().isoformat(),
                "status": random.choice(["Active", "Mitigated", "Investigating"]),
                "confidence": f"{random.randint(70, 99)}%",
                "impact": random.choice(["Low", "Moderate", "Severe"])
            })
    
    return threats

# def predict_threats(new_data):
    """
    Predicts threats using a pre-trained Isolation Forest model.
    
    Args:
        new_data (pd.DataFrame): The new incoming data (same structure as training set).
    
    Returns:
        np.ndarray: Prediction results (-1 for anomaly, 1 for normal)
    """
    
    # Load the trained model and preprocessing objects
    with open("scaler.pkl", "rb") as scaler_file:
        scaler = pickle.load(scaler_file)

    with open("isolation_forest_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)

    # Original feature columns used during training
    df = pd.read_csv("raw_data.csv")
    if "label" in df.columns:
        df = df.drop(columns=["label"])
    trained_columns = df.columns

    # Separate categorical and numerical columns based on training
    cat_cols = new_data.select_dtypes(include=['object']).columns.tolist()
    num_cols = new_data.select_dtypes(include=['int64', 'float64']).columns.tolist()

    # Apply one-hot encoding, ensuring all training categories exist
    new_data_encoded = pd.get_dummies(new_data, columns=cat_cols, drop_first=True)

    # Ensure new data has the same columns as training data
    missing_cols = set(trained_columns) - set(new_data_encoded.columns)
    for col in missing_cols:
        new_data_encoded[col] = 0  # Add missing columns with default value

    # Reorder columns to match training data
    new_data_encoded = new_data_encoded[trained_columns]

    # Scale the numerical features
    new_data_scaled = scaler.transform(new_data_encoded)

    # Make predictions
    predictions = model.predict(new_data_scaled)

    return predictions  # Returns array with -1 (anomaly) or 1 (normal)

import pandas as pd

# # def predict_threats(live_data):
#     if len(live_data) == 0:
#         return []

#     live_df = pd.DataFrame(live_data, columns=["packet_length", "protocol", "service", "flag", "src_bytes", "difficulty"])

#     if "unknown" not in label_encoder.classes_:
#         label_encoder.classes_ = np.append(label_encoder.classes_, "unknown")
#     live_df["service"] = live_df["service"].apply(lambda x: x if x in label_encoder.classes_ else "unknown")
#     live_df["service"] = label_encoder.transform(live_df["service"])

#     flag_mapping = {"SYN": 1, "other": 0}  
#     live_df["flag"] = live_df["flag"].map(flag_mapping)

#     difficulty_mapping = {"low": 0, "medium": 1, "high": 2}  
#     live_df["difficulty"] = live_df["difficulty"].map(difficulty_mapping)

#     live_data_encoded = live_df.values
#     print("Expected features:", scaler.n_features_in_)
#     print("Live data features:", live_data_encoded.shape[1])

#     live_data_scaled = scaler.transform(live_data_encoded)

#     predictions = model.predict(live_data_scaled)

#     threats = []
#     for i, pred in enumerate(predictions):
#         if pred == -1: 
#             attack_type = random.choice(ATTACK_TYPES)
#             threats.append({
#                 "id": str(i),
#                 "type": attack_type,
#                 "source": f"192.168.1.{random.randint(1, 255)}",
#                 "firstDetected": datetime.now().isoformat(),
#                 "status": random.choice(["Active", "Mitigated", "Investigating"]),
#                 "confidence": f"{random.randint(70, 99)}%",
#                 "impact": random.choice(["Low", "Moderate", "Severe"])
#             })

#     return threats
def predict_threats(live_data):
    # Load artifacts
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("pca.pkl", "rb") as f:
        pca = pickle.load(f)
    with open("isolation_forest_model.pkl", "rb") as f:
        model = pickle.load(f)
    
    # Preprocess live data (same as training)
    live_data_encoded = pd.get_dummies(live_data, columns=["protocol_type", "service", "flag"])
    
    # Align columns with training data
    train_columns = scaler.feature_names_in_  # Saved during training
    live_data_encoded = live_data_encoded.reindex(columns=train_columns, fill_value=0)
    
    # Apply transformations IN ORDER
    live_data_scaled = scaler.transform(live_data_encoded)  # 728 ➔ 728
    live_data_pca = pca.transform(live_data_scaled)         # 728 ➔ 6
    
    # Predict
    predictions = model.predict(live_data_pca)
    return predictions

def generate_summary(threats):
    return {
        "totalTraffic": random.randint(5000, 20000),
        "activeThreats": len(threats),
        "criticalAlerts": sum(1 for t in threats if t["impact"] == "Severe"),
        "systemStatus": "Critical" if len(threats) > 3 else "Stable"
    }


def send_alert(email, message):
    yag = yagmail.SMTP("your_email@gmail.com", "your_app_password")
    yag.send(email, "Security Alert", message)
    print("Alert Sent Successfully")


def block_ip(ip):
    os.system(f"sudo ufw deny from {ip}")
    print(f"Blocked IP: {ip}")


@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    threats = predict_threats(capture_live_traffic())
    summary = generate_summary(threats)
    return jsonify({
        "traffic": {"labels": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                    "datasets": [{"label": "Network Traffic",
                                   "data": [random.randint(500, 2000) for _ in range(5)],
                                   "borderColor": "#36A2EB",
                                   "backgroundColor": "rgba(54, 162, 235, 0.2)"}]},
        "alerts": threats,
        "threats": threats,
        "summary": summary
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
