import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
import random

class SensorSimulator:
    def __init__(self):
        self.machines = {
            'MACHINE-01': {'base_temp': 75, 'base_vibration': 0.5, 'base_pressure': 100, 'base_rpm': 1500},
            'MACHINE-02': {'base_temp': 80, 'base_vibration': 0.6, 'base_pressure': 110, 'base_rpm': 1800},
            'MACHINE-03': {'base_temp': 70, 'base_vibration': 0.4, 'base_pressure': 95, 'base_rpm': 1200}
        }
        
    def generate_normal_data(self, machine_id: str, hours: int = 24) -> pd.DataFrame:
        """Generate normal operating sensor data."""
        if machine_id not in self.machines:
            raise ValueError(f"Machine {machine_id} not found")
        
        base = self.machines[machine_id]
        
        # Generate timestamps (every 5 minutes)
        num_points = hours * 12
        timestamps = [datetime.now() - timedelta(minutes=5*i) for i in range(num_points)]
        timestamps.reverse()
        
        # Generate normal sensor readings with small random fluctuations
        data = {
            'timestamp': timestamps,
            'machine_id': [machine_id] * num_points,
            'temperature': np.random.normal(base['base_temp'], 2, num_points),
            'vibration': np.random.normal(base['base_vibration'], 0.05, num_points),
            'pressure': np.random.normal(base['base_pressure'], 3, num_points),
            'rpm': np.random.normal(base['base_rpm'], 50, num_points),
            'power_consumption': np.random.normal(1000, 30, num_points)
        }
        
        return pd.DataFrame(data)
    
    def inject_anomaly(self, df: pd.DataFrame, anomaly_type: str = 'random') -> pd.DataFrame:
        """Inject anomalies into the data."""
        df = df.copy()
        
        if anomaly_type == 'temperature_spike':
            # Sudden temperature increase
            idx = random.randint(len(df)//2, len(df)-1)
            df.loc[idx:idx+5, 'temperature'] += random.uniform(15, 30)
            
        elif anomaly_type == 'vibration_increase':
            # Gradual vibration increase
            idx = random.randint(len(df)//2, len(df)-10)
            increase = np.linspace(0, 0.5, 10)
            df.loc[idx:idx+10, 'vibration'] += increase
            
        elif anomaly_type == 'pressure_drop':
            # Sudden pressure drop
            idx = random.randint(len(df)//2, len(df)-1)
            df.loc[idx:idx+3, 'pressure'] -= random.uniform(20, 40)
            
        elif anomaly_type == 'rpm_fluctuation':
            # RPM instability
            idx = random.randint(len(df)//2, len(df)-5)
            df.loc[idx:idx+5, 'rpm'] += np.random.uniform(-300, 300, 6)
            
        else:  # random
            # Random anomaly type
            anomaly_types = ['temperature_spike', 'vibration_increase', 'pressure_drop', 'rpm_fluctuation']
            chosen = random.choice(anomaly_types)
            return self.inject_anomaly(df, chosen)
        
        return df
    
    def get_current_readings(self, machine_id: str, include_anomaly: bool = False) -> Dict:
        """Get current sensor readings for a machine."""
        if machine_id not in self.machines:
            raise ValueError(f"Machine {machine_id} not found")
        
        base = self.machines[machine_id]
        
        readings = {
            'machine_id': machine_id,
            'timestamp': datetime.now().isoformat(),
            'temperature': float(round(np.random.normal(base['base_temp'], 2), 2)),
            'vibration': float(round(np.random.normal(base['base_vibration'], 0.05), 3)),
            'pressure': float(round(np.random.normal(base['base_pressure'], 3), 2)),
            'rpm': int(round(np.random.normal(base['base_rpm'], 50), 0)),
            'power_consumption': float(round(np.random.normal(1000, 30), 2))
        }
        
        # Inject anomaly if requested
        if include_anomaly:
            anomaly_choice = random.choice(['temperature', 'vibration', 'pressure', 'rpm'])
            if anomaly_choice == 'temperature':
                readings['temperature'] = float(readings['temperature'] + random.uniform(15, 25))
            elif anomaly_choice == 'vibration':
                readings['vibration'] = float(readings['vibration'] + random.uniform(0.3, 0.8))
            elif anomaly_choice == 'pressure':
                readings['pressure'] = float(readings['pressure'] - random.uniform(20, 35))
            elif anomaly_choice == 'rpm':
                readings['rpm'] = int(readings['rpm'] + random.uniform(-400, 400))
        
        return readings
    
    def get_machine_list(self) -> List[str]:
        """Get list of available machines."""
        return list(self.machines.keys())

# Global simulator instance
sensor_sim = SensorSimulator()
