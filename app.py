from flask import Flask, render_template, jsonify
from sensor_simulator import sensor_sim
from anomaly_detector import anomaly_detector
from database import anomaly_db

app = Flask(__name__)

@app.route('/')
def index():
    """Main monitoring dashboard."""
    machines = sensor_sim.get_machine_list()
    return render_template('monitor.html', machines=machines)

@app.route('/api/readings/<machine_id>')
def get_readings(machine_id):
    """API endpoint for current sensor readings."""
    try:
        import random
        # Small chance of anomaly for demo
        include_anomaly = random.random() < 0.2
        readings = sensor_sim.get_current_readings(machine_id, include_anomaly)
        
        # Detect anomaly
        is_anomaly, anomaly_score, severity = anomaly_detector.detect_anomaly(readings)
        
        # Log if anomaly
        if is_anomaly:
            db_data = {
                **readings,
                'anomaly_score': anomaly_score,
                'severity': severity,
                'sensor_type': "Auto-detected"
            }
            anomaly_db.log_anomaly(db_data)
        
        return jsonify({
            **readings,
            'is_anomaly': is_anomaly,
            'anomaly_score': round(anomaly_score, 3),
            'severity': severity if is_anomaly else 'Normal'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/anomalies/<machine_id>')
def get_anomalies(machine_id):
    """API endpoint for anomaly history."""
    anomalies = anomaly_db.get_recent_anomalies(machine_id, limit=50)
    stats = anomaly_db.get_statistics(machine_id)
    return jsonify({
        'anomalies': anomalies,
        'stats': stats
    })

if __name__ == '__main__':
    # Train models on startup
    print("Training anomaly detection models...")
    for machine_id in sensor_sim.get_machine_list():
        normal_data = sensor_sim.generate_normal_data(machine_id, hours=24)
        anomaly_detector.train(machine_id, normal_data)
    print("Models trained! Starting server...")
    
    app.run(debug=True, port=5008)
