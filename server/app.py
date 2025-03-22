from flask import Flask, jsonify
import random
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
CORS(app,origins=["*"])


def get_ml_predictions():
    return random.randint(0, 100) 

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
    return [{
        "id": str(i),
        "timestamp": datetime.now().isoformat(),
        "type": "Intrusion",
        "severity": random.choice(["Low", "Medium", "High", "Critical"]),
        "source": "192.168.1." + str(random.randint(1, 255)),
        "destination": "10.0.0." + str(random.randint(1, 255)),
        "details": "Unusual traffic detected."
    } for i in range(3)]

def generate_threats():
    return [{
        "id": str(i),
        "type": "Malware",
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
    app.run(debug=True)
