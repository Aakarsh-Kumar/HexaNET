from flask import Flask, jsonify
from flask_cors import CORS
import os

import pickle
import scapy.all as scapy
import numpy as np
from datetime import datetime
import yagmail
import pandas as pd

app = Flask(__name__)
CORS(app, origins=["*"])

with open("label_encoder.pkl", "rb") as le_file:
    label_encoder = pickle.load(le_file)
with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)
with open("pca.pkl", "rb") as pca_file:
    pca = pickle.load(pca_file)
with open("isolation_forest_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

ATTACK_TYPES = ["DDoS", "Phishing", "Malware"]
import random
def capture_live_traffic():
    packets = scapy.sniff(timeout=1)
    print(f"Captured {len(packets)} packets")
    print(f"Captured {packets} ")
    traffic_data = []

    for pkt in packets:
        packet_length = len(pkt)
        protocol = pkt[scapy.IP].proto if pkt.haslayer(scapy.IP) else 0
        service = str(pkt[scapy.IP].proto) if pkt.haslayer(scapy.IP) else "unknown"
        flag = "SYN" if pkt.haslayer(scapy.TCP) and pkt[scapy.TCP].flags == 2 else "other"
        src_bytes = pkt[scapy.IP].len if pkt.haslayer(scapy.IP) else 0
        
        difficulty = random.choice(["low", "medium", "high"])
        print(f"packet_length: {packet_length}, protocol: {protocol}, service: {service}, flag: {flag}, src_bytes: {src_bytes}, difficulty: {difficulty}")
        traffic_data.append([packet_length, protocol, service, flag, src_bytes, difficulty])

    return traffic_data

def predict_threats(live_data):
    if len(live_data) == 0:
        return []

    live_df = pd.DataFrame(live_data, columns=["packet_length", "protocol", "service", "flag", "src_bytes", "difficulty"])

    live_df["service"] = live_df["service"].apply(lambda x: x if x in label_encoder.classes_ else "unknown")
    if "unknown" not in label_encoder.classes_:
        label_encoder.classes_ = np.append(label_encoder.classes_, "unknown")
    live_df["service"] = label_encoder.transform(live_df["service"])

    flag_mapping = {"SYN": 1, "other": 0}
    live_df["flag"] = live_df["flag"].map(flag_mapping)
    difficulty_mapping = {"low": 0, "medium": 1, "high": 2}
    live_df["difficulty"] = live_df["difficulty"].map(difficulty_mapping)

    live_df = live_df.reindex(columns=scaler.feature_names_in_, fill_value=0)

    live_data_scaled = scaler.transform(live_df)
    live_data_pca = pca.transform(live_data_scaled)

    predictions = model.predict(live_data_pca)
    threats = []
    print(f"Predictions: {predictions}")
    for i, pred in enumerate(predictions):
        if pred == -1:  
            attack_type = random.choice(ATTACK_TYPES)
            threats.append({
                "id": str(i),
                "type": attack_type,
                "source": f"192.168.1.{random.randint(1, 255)}",
                "firstDetected": datetime.now().isoformat(),
                "status": random.choice(["Active", "Mitigated", "Investigating"]),
                "confidence": f"{random.randint(70, 99)}%",
                "impact": random.choice(["Low", "Moderate", "Severe"]),
                "src_bytes": live_data[i][4]
            })
    return threats
    

def generate_summary(threats):
    total_traffic = sum(t["src_bytes"] for t in threats)
    print(threats)
    return {
        "totalTraffic": total_traffic,
        "activeThreats": round(len(threats)/10,0),
        "criticalAlerts": sum(1 for t in threats if t["impact"] == "Severe"),
        "systemStatus": "Critical" if sum(1 for t in threats if t["impact"] == "Severe") > 4 else "Stable"
    }

def send_alert(email, message):
    yag = yagmail.SMTP("kushagragoel75@gmail.com", "smes rtip hbdb ncwh")
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
        "traffic": {
            "labels": [f"Connection {i}" for i in range(1, 6)],
            "datasets": [{
                "label": "Network Traffic",
                "data": [random.randint(500, 2000) for _ in range(5)],
                "borderColor": "#36A2EB",
                "backgroundColor": "rgba(54, 162, 235, 0.2)"
            }]
        },
        "alerts": threats,
        "threats": threats,
        "summary": summary
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)