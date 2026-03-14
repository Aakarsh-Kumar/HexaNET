# HexaNET

### AI-Powered Network Intrusion Detection System

HexaNET is a machine learning--driven network intrusion detection system
designed to monitor network traffic, detect anomalous behavior, and
provide real-time security insights through an interactive dashboard.

The system combines **network traffic analysis, anomaly detection
algorithms, and a modern monitoring interface** to help identify
suspicious activities before they escalate into security breaches.

------------------------------------------------------------------------

# Overview

Modern networks generate massive amounts of traffic, making manual
monitoring ineffective. Traditional intrusion detection systems rely
heavily on **signature-based detection**, which fails to detect new or
unknown attack patterns.

HexaNET addresses this limitation by implementing **machine
learning--based anomaly detection**, allowing the system to learn
patterns of normal network behavior and flag deviations that may
indicate malicious activity.

The project integrates:

-   Machine learning models for anomaly detection
-   A Flask-based backend API for model inference
-   A React dashboard for real-time monitoring and visualization
-   Data preprocessing pipelines for structured network analysis

------------------------------------------------------------------------

# Key Features

## Machine Learning Based Detection

Uses anomaly detection algorithms to identify suspicious network
activity without relying solely on predefined attack signatures.

## Real-Time Monitoring Dashboard

Visualizes traffic statistics, alerts, and threat summaries in a clean
interface.

## Automated Feature Processing

Raw network data is transformed into structured features suitable for
machine learning models.

## Threat Logging

Detected anomalies are recorded for further analysis and security
auditing.

## Modular Architecture

The project is structured to separate model training, prediction,
backend APIs, and frontend visualization.

------------------------------------------------------------------------

# System Architecture

    Network Data
         │
         ▼
    Data Preprocessing
         │
         ▼
    Feature Scaling + Encoding
         │
         ▼
    Dimensionality Reduction (PCA)
         │
         ▼
    Machine Learning Model
         │
         ▼
    Anomaly Prediction
         │
         ▼
    Dashboard Visualization + Alerts

------------------------------------------------------------------------

# Machine Learning Pipeline

The model training workflow includes:

1.  Loading and preparing network traffic datasets\
2.  Encoding categorical network features\
3.  Feature normalization using scalers\
4.  Dimensionality reduction with PCA\
5.  Training an anomaly detection model\
6.  Persisting trained artifacts for inference

Saved model artifacts:

    isolation_forest_model.pkl
    scaler.pkl
    pca.pkl
    scaler_pca.pkl
    label_encoder.pkl

------------------------------------------------------------------------

# Dataset

The model is trained using the **NSL-KDD dataset**, a refined version of
the KDD Cup 1999 dataset commonly used in intrusion detection research.

Dataset files included:

    KDDTrain+.txt
    KDDTest+.txt
    raw_data.csv

------------------------------------------------------------------------

# Project Structure

    HexaNET
    │
    ├── app.py
    ├── predict.py
    ├── train.py
    ├── model.ipynb
    │
    ├── isolation_forest_model.pkl
    ├── scaler.pkl
    ├── scaler_pca.pkl
    ├── pca.pkl
    ├── label_encoder.pkl
    │
    ├── KDDTrain+.txt
    ├── KDDTest+.txt
    ├── raw_data.csv
    │
    └── frontend
        ├── src
        │   ├── components
        │   ├── Dashboard.jsx
        │   └── charts
        └── package.json

------------------------------------------------------------------------

# Backend

The backend is implemented using **Flask** and serves as the inference
layer between the machine learning model and the frontend dashboard.

Responsibilities include:

-   Loading trained model artifacts
-   Running anomaly predictions
-   Aggregating network statistics
-   Providing API endpoints for dashboard data

Example API endpoint:

    GET /api/dashboard

------------------------------------------------------------------------

# Frontend

The frontend dashboard is built using modern web technologies:

-   React
-   Vite
-   TailwindCSS
-   Recharts
-   Axios

The dashboard provides visual insights into:

-   network traffic patterns
-   anomaly detection alerts
-   threat statistics
-   system health status

------------------------------------------------------------------------

# Installation

## Clone the Repository

    git clone https://github.com/yourusername/hexanet.git
    cd hexanet

------------------------------------------------------------------------

# Backend Setup

Install Python dependencies:

    pip install flask scikit-learn pandas numpy

Run the backend server:

    python app.py

Backend will start at:

    http://127.0.0.1:5000

------------------------------------------------------------------------

# Frontend Setup

Install Node dependencies:

    npm install

Run development server:

    npm run dev

Frontend runs at:

    http://localhost:5173

------------------------------------------------------------------------

# Evaluation Metrics

The model was evaluated using common intrusion detection metrics:

-   Accuracy
-   Precision
-   Recall
-   F1 Score

------------------------------------------------------------------------

# Future Enhancements

Potential improvements include:

-   Live packet capture integration using Scapy
-   Deep learning--based detection models
-   Automated IP blocking for detected threats
-   Email or push notification alerts
-   Containerized deployment with Docker
-   Cloud-based monitoring infrastructure

------------------------------------------------------------------------

# Author

**Aakarsh Kumar**
