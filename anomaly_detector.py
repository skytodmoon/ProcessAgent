import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from typing import Dict, Tuple

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = {}
        self.feature_columns = ['temperature', 'vibration', 'pressure', 'rpm', 'power_consumption']
    
    def train(self, machine_id: str, normal_data: pd.DataFrame):
        """Train the anomaly detection model on normal operating data."""
        X = normal_data[self.feature_columns].values
        self.model.fit(X)
        self.is_trained[machine_id] = True
    
    def detect_anomaly(self, readings: Dict) -> Tuple[bool, float, str]:
        """
        Detect if sensor readings are anomalous.
        
        Args:
            readings: Dict with sensor values
        
        Returns:
            Tuple of (is_anomaly, anomaly_score, severity)
        """
        # Extract features
        features = np.array([[
            readings['temperature'],
            readings['vibration'],
            readings['pressure'],
            readings['rpm'],
            readings['power_consumption']
        ]])
        
        # Predict
        prediction = self.model.predict(features)[0]
        anomaly_score = self.model.score_samples(features)[0]
        
        # -1 means anomaly, 1 means normal
        is_anomaly = bool(prediction == -1)
        
        # Determine severity based on anomaly score
        # More negative scores = more anomalous
        if anomaly_score < -0.5:
            severity = "Critical"
        elif anomaly_score < -0.3:
            severity = "High"
        elif anomaly_score < -0.1:
            severity = "Medium"
        else:
            severity = "Low"
        
        return is_anomaly, abs(anomaly_score), severity
    
    def analyze_anomaly_type(self, readings: Dict, baseline: Dict) -> str:
        """Determine which sensor triggered the anomaly."""
        anomalies = []
        
        # Temperature
        if abs(readings['temperature'] - baseline['base_temp']) > 10:
            anomalies.append("Temperature")
        
        # Vibration
        if abs(readings['vibration'] - baseline['base_vibration']) > 0.2:
            anomalies.append("Vibration")
        
        # Pressure
        if abs(readings['pressure'] - baseline['base_pressure']) > 15:
            anomalies.append("Pressure")
        
        # RPM
        if abs(readings['rpm'] - baseline['base_rpm']) > 200:
            anomalies.append("RPM")
        
        if anomalies:
            return ", ".join(anomalies)
        else:
            return "Multiple Sensors"

# Global detector instance
anomaly_detector = AnomalyDetector()
