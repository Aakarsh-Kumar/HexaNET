import pandas as pd
import numpy as np
import joblib
from flask import Flask, jsonify
from scapy.all import sniff, IP, TCP, UDP
from sklearn.preprocessing import MinMaxScaler
import threading

app = Flask(__name__)

model = joblib.load("isolation_forest_model.pkl")
scaler = joblib.load("scaler.pkl")

def extract_features(packet):
    features = {
        "src_ip": hash(packet[IP].src) if packet.haslayer(IP) else 0,
        "dst_ip": hash(packet[IP].dst) if packet.haslayer(IP) else 0,
        "src_port": packet[TCP].sport if packet.haslayer(TCP) else (packet[UDP].sport if packet.haslayer(UDP) else 0),
        "dst_port": packet[TCP].dport if packet.haslayer(TCP) else (packet[UDP].dport if packet.haslayer(UDP) else 0),
        "packet_len": len(packet),
    }
    return features

live_data = []

def capture_traffic():
    def process_packet(packet):
        global live_data
        features = extract_features(packet)
        live_data.append(features)

    sniff(prn=process_packet, store=False)

@app.route("/predict", methods=["GET"])
def predict():
    global live_data

    if not live_data:
        return jsonify({"message": "No live traffic data captured yet"}), 400

    df_live = pd.DataFrame(live_data)

    if "packet_len" not in df_live.columns:
        return jsonify({"error": "Missing required fields in captured data"}), 500

    df_live_scaled = scaler.transform(df_live)

    predictions = model.predict(df_live_scaled)
    anomalies = [1 if pred == -1 else 0 for pred in predictions] 

    for i in range(len(live_data)):
        live_data[i]["anomaly"] = anomalies[i]

    return jsonify({"live_traffic": live_data})

threading.Thread(target=capture_traffic, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)