# Manufacturing Anomaly Detection Agent

## Problem Statement
**Anomaly detection in machines**

Manufacturing equipment experiences unexpected failures, causing costly downtime and production delays. Early detection of anomalies in machine behavior (vibration, temperature, pressure, etc.) can prevent breakdowns.

## Solution
An AI agent designed to:
- **Monitor machine sensor data** in real-time
- **Detect anomalies** using statistical and ML methods
- **Alert operators** to abnormal behavior before failures occur
- **Classify anomaly types** (temperature spike, vibration increase, pressure drop, etc.)
- **Track anomaly history** and patterns

## Tech Stack
- **LangChain**: Agent orchestration
- **Google Gemini**: LLM for anomaly analysis and recommendations
- **Scikit-learn**: Isolation Forest for anomaly detection
- **Flask**: Web dashboard with real-time monitoring
- **SQLite**: Anomaly event logging

## Key Features
- Simulated sensor data generation
- Real-time anomaly detection
- Anomaly severity scoring
- Alert notifications
- Historical trend visualization
