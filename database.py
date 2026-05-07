import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

class AnomalyDatabase:
    def __init__(self, db_path: str = "anomalies.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create anomalies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                machine_id TEXT NOT NULL,
                sensor_type TEXT,
                temperature REAL,
                vibration REAL,
                pressure REAL,
                rpm REAL,
                power_consumption REAL,
                anomaly_score REAL,
                severity TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_anomaly(self, data: Dict) -> int:
        """Log an anomaly event and return its ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO anomalies (machine_id, sensor_type, temperature, vibration, 
                                 pressure, rpm, power_consumption, anomaly_score, severity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['machine_id'],
            data.get('sensor_type', 'Multiple'),
            data.get('temperature'),
            data.get('vibration'),
            data.get('pressure'),
            data.get('rpm'),
            data.get('power_consumption'),
            data.get('anomaly_score', 0.0),
            data.get('severity', 'Medium')
        ))
        
        anomaly_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return anomaly_id
    
    def get_recent_anomalies(self, machine_id: str = None, limit: int = 50) -> List[Dict]:
        """Get recent anomalies, optionally filtered by machine."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if machine_id:
            cursor.execute('''
                SELECT * FROM anomalies 
                WHERE machine_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (machine_id, limit))
        else:
            cursor.execute('''
                SELECT * FROM anomalies 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_statistics(self, machine_id: str = None) -> Dict:
        """Get anomaly statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        if machine_id:
            cursor.execute('SELECT COUNT(*) FROM anomalies WHERE machine_id = ?', (machine_id,))
        else:
            cursor.execute('SELECT COUNT(*) FROM anomalies')
        stats['total'] = cursor.fetchone()[0]
        
        # By severity
        if machine_id:
            cursor.execute('''
                SELECT severity, COUNT(*) 
                FROM anomalies 
                WHERE machine_id = ?
                GROUP BY severity
            ''', (machine_id,))
        else:
            cursor.execute('SELECT severity, COUNT(*) FROM anomalies GROUP BY severity')
        stats['by_severity'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        return stats

# Global database instance
anomaly_db = AnomalyDatabase()
