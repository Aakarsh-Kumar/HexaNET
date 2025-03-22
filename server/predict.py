import pandas as pd
import numpy as np
import joblib
from flask import Flask, jsonify
from scapy.all import sniff, IP, TCP, UDP
from sklearn.preprocessing import MinMaxScaler
import threading

app = Flask(__name__)

# Load the trained Isolation Forest model and preprocessors
model = joblib.load("isolation_forest_model.pkl")
scaler = joblib.load("scaler.pkl")

# Define a function to extract packet features
def extract_features(packet):
    """Extracts numerical features from a network packet."""
    features = {
        "src_ip": hash(packet[IP].src) if packet.haslayer(IP) else 0,
        "dst_ip": hash(packet[IP].dst) if packet.haslayer(IP) else 0,
        "src_port": packet[TCP].sport if packet.haslayer(TCP) else (packet[UDP].sport if packet.haslayer(UDP) else 0),
        "dst_port": packet[TCP].dport if packet.haslayer(TCP) else (packet[UDP].dport if packet.haslayer(UDP) else 0),
        "packet_len": len(packet),
    }
    return features

# Store live packets
live_data = []

def capture_traffic():
    """Captures network traffic and stores extracted features."""
    def process_packet(packet):
        global live_data
        features = extract_features(packet)
        live_data.append(features)

    # Start sniffing packets in a separate thread
    sniff(prn=process_packet, store=False)

@app.route("/predict", methods=["GET"])
def predict():
    """Fetches captured packets, preprocesses, and predicts anomalies."""
    global live_data

    if not live_data:
        return jsonify({"message": "No live traffic data captured yet"}), 400

    # Convert captured data into a DataFrame
    df_live = pd.DataFrame(live_data)

    # Preprocess data (ensure all columns exist)
    if "packet_len" not in df_live.columns:
        return jsonify({"error": "Missing required fields in captured data"}), 500

    # Normalize data
    df_live_scaled = scaler.transform(df_live)

    # Predict anomalies
    predictions = model.predict(df_live_scaled)
    anomalies = [1 if pred == -1 else 0 for pred in predictions]  # Convert -1 (anomaly) to 1

    # Attach predictions to live data
    for i in range(len(live_data)):
        live_data[i]["anomaly"] = anomalies[i]

    # Return detected anomalies
    return jsonify({"live_traffic": live_data})

# Start packet capturing in a background thread
threading.Thread(target=capture_traffic, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)
