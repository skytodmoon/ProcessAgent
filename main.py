import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import json

from sensor_simulator import sensor_sim
from anomaly_detector import anomaly_detector
from database import anomaly_db

# Load environment variables
load_dotenv("../.env")

# Set Google API key
if not os.environ.get('GOOGLE_API_KEY'):
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Train anomaly detectors for each machine
print("Training anomaly detection models...")
for machine_id in sensor_sim.get_machine_list():
    normal_data = sensor_sim.generate_normal_data(machine_id, hours=24)
    anomaly_detector.train(machine_id, normal_data)
print("Models trained successfully!")

@tool
def analyze_sensor_data(machine_id: str) -> str:
    """
    Analyze current sensor readings for anomalies.
    Args:
        machine_id: Machine identifier (e.g., 'MACHINE-01')
    Returns:
        JSON string with anomaly analysis
    """
    try:
        # Get current readings (with small chance of anomaly)
        import random
        include_anomaly = random.random() < 0.3  # 30% chance
        readings = sensor_sim.get_current_readings(machine_id, include_anomaly)
        
        # Detect anomaly
        is_anomaly, anomaly_score, severity = anomaly_detector.detect_anomaly(readings)
        
        result = {
            "machine_id": machine_id,
            "timestamp": readings['timestamp'],
            "readings": readings,
            "is_anomaly": is_anomaly,
            "anomaly_score": round(anomaly_score, 3),
            "severity": severity
        }
        
        # Log anomaly if detected
        if is_anomaly:
            db_data = {
                **readings,
                'anomaly_score': anomaly_score,
                'severity': severity,
                'sensor_type': "Auto-detected"
            }
            anomaly_db.log_anomaly(db_data)
            result['message'] = f"⚠️ ANOMALY DETECTED - Severity: {severity}"
        else:
            result['message'] = "✅ Normal operation"
        
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def get_machine_status(machine_id: str) -> str:
    """
    Get the current operational status of a machine.
    Args:
        machine_id: Machine identifier
    Returns:
        JSON string with machine status
    """
    try:
        recent_anomalies = anomaly_db.get_recent_anomalies(machine_id, limit=10)
        stats = anomaly_db.get_statistics(machine_id)
        
        # Determine health status
        if stats['total'] == 0:
            health = "Excellent"
        elif stats['total'] < 5:
            health = "Good"
        elif stats['total'] < 15:
            health = "Fair"
        else:
            health = "Concerning"
        
        return json.dumps({
            "machine_id": machine_id,
            "health_status": health,
            "total_anomalies": stats['total'],
            "recent_anomalies_count": len(recent_anomalies),
            "severity_breakdown": stats.get('by_severity', {})
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def get_recent_anomalies(machine_id: str = None, limit: int = 20) -> str:
    """
    Get recent anomaly events.
    Args:
        machine_id: Optional machine filter
        limit: Number of records to return
    Returns:
        JSON string with anomaly list
    """
    try:
        anomalies = anomaly_db.get_recent_anomalies(machine_id, limit)
        return json.dumps({"anomalies": anomalies, "count": len(anomalies)})
    except Exception as e:
        return json.dumps({"error": str(e)})

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)

# Define Tools
tools = [analyze_sensor_data, get_machine_status, get_recent_anomalies]

# Define Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Machine Monitoring AI Assistant for manufacturing operations.

Your role is to help operators monitor machine health and detect anomalies before failures occur.

Available machines: MACHINE-01, MACHINE-02, MACHINE-03

When analyzing machines:
- Use analyze_sensor_data to check current sensor readings
- Use get_machine_status for overall health assessment
- Use get_recent_anomalies to review anomaly history
- Explain what the anomalies mean and recommend actions
- Severity levels: Critical (immediate action), High (urgent), Medium (monitor), Low (informational)

Provide clear, actionable recommendations to prevent equipment failures."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Create Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def main():
    """Test the anomaly detection agent."""
    print("\nAnomaly Detection Agent")
    print("=" * 50)
    
    test_input = "Check the current status of MACHINE-01 and analyze its sensor data"
    
    print(f"\nUser: {test_input}")
    result = agent_executor.invoke({"input": test_input})
    print(f"\nAgent: {result['output']}")

if __name__ == '__main__':
    main()
