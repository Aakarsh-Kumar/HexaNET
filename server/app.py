from flask import Flask, request, jsonify
import os
import random
import yagmail
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*"])


ATTACK_TYPES = ["DDoS", "SQL Injection", "Brute Force", "Phishing", "Malware"]


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

def generate_alerts():
    for i in range(3):
        data = {
            "id": str(i),
            "timestamp": datetime.now().isoformat(),
            "type": "Intrusion",
            "severity": random.choice(["Low", "Medium", "High", "Critical"]),
            "source": "192.168.1." + str(random.randint(1, 255)),
            "destination": "10.0.0." + str(random.randint(1, 255)),
            "details": "Unusual traffic detected."
            }
        if data["severity"] == "Critical":
            send_alert("aakarsh2504@gmail.com", f"ALERT: {data['type']} detected from {data['source']} to {data['destination']}! Immediate action required!")
            block_ip(data["source"])

    return [data]

def generate_threats():
    return [{
        "id": str(i),
        "type": random.choice(["Malware", "Trojan", "Ransomware"]),
        "source": "192.168.1." + str(random.randint(1, 255)),
        "firstDetected": datetime.now().isoformat(),
        "status": random.choice(["Active", "Mitigated", "Investigating"]),
        "confidence": f"{random.randint(70, 99)}%",
        "impact": random.choice(["Low", "Moderate", "Severe"])
    } for i in range(2)]

def generate_summary():
    return {
        "totalTraffic": random.randint(5000, 20000),
        "activeThreats": random.randint(1, 10),
        "criticalAlerts": random.randint(0, 5),
        "systemStatus": random.choice(["Stable", "At Risk", "Critical"])
    }

def send_alert(email, message):
    yag = yagmail.SMTP("kushagragoel75@gmail.com", "smes rtip hbdb ncwh")
    yag.send(email, "Security Alert", message)
    print("Alert Sent Successfully")

def block_ip(ip):
    os.system(f"sudo ufw deny from {ip}")
    print(f"Blocked IP: {ip}")

@app.route('/api/generate_threat', methods=['POST'])
def generate_threat():

    data = request.get_json()
    ip_address = data.get("ip")  

    if not ip_address:
        return jsonify({"error": "No IP provided"}), 400

    attack_type = random.choice(ATTACK_TYPES)

    alert_message = f"ALERT: {attack_type} detected from {ip_address}! IP blocked and action required!"
    send_alert("aakarsh2504@gmail.com", alert_message)

    block_ip(ip_address)

    return jsonify({
        "message": f"Threat '{attack_type}' detected from {ip_address}. IP blocked and alert sent.",
        "attack_type": attack_type,
        "ip_blocked": ip_address
    })

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    return jsonify({
        "traffic": generate_traffic_data(),
        "alerts": generate_alerts(),
        "threats": generate_threats(),
        "summary": generate_summary()
    })

@app.route('/api/traffic', methods=['GET'])
def get_traffic():
    return jsonify(generate_traffic_data())

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    return jsonify(generate_alerts())

@app.route('/api/threats', methods=['GET'])
def get_threats():
    return jsonify(generate_threats())

@app.route('/api/summary', methods=['GET'])
def get_summary():
    return jsonify(generate_summary())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
