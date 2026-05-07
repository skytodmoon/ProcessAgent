# Manufacturing Anomaly Detection Agent

## 工业设备异常检测智能代理

---

## Problem Statement / 问题描述

**Anomaly detection in machines**

Manufacturing equipment experiences unexpected failures, causing costly downtime and production delays. Early detection of anomalies in machine behavior (vibration, temperature, pressure, etc.) can prevent breakdowns.

**设备异常检测**

制造设备经常发生意外故障，导致昂贵的停机时间和生产延误。及早检测机器行为异常（振动、温度、压力等）可以预防故障发生。

---

## Solution / 解决方案

An AI agent designed to:
- **Monitor machine sensor data** in real-time
- **Detect anomalies** using statistical and ML methods
- **Alert operators** to abnormal behavior before failures occur
- **Classify anomaly types** (temperature spike, vibration increase, pressure drop, etc.)
- **Track anomaly history** and patterns

AI智能代理功能：
- **实时监控**机器传感器数据
- **使用机器学习方法检测异常**
- **在故障发生前向操作员发出警报**
- **分类异常类型**（温度突升、振动增加、压力下降等）
- **跟踪异常历史**和模式

---

## Tech Stack / 技术栈

| Category | Technology | Description |
| :--- | :--- | :--- |
| **Agent Orchestration** | LangChain | 代理编排框架 |
| **LLM** | SiliconFlow (DeepSeek) | 大语言模型用于异常分析 |
| **ML Model** | Scikit-learn (Isolation Forest) | 孤立森林算法进行异常检测 |
| **Web Framework** | Flask | 实时监控仪表盘 |
| **Database** | SQLite | 异常事件日志存储 |

---

## Key Features / 主要功能

- **Simulated Sensor Data Generation** - 模拟传感器数据生成
- **Real-time Anomaly Detection** - 实时异常检测
- **Anomaly Severity Scoring** - 异常严重程度评分
- **Alert Notifications** - 警报通知
- **Historical Trend Visualization** - 历史趋势可视化
- **LLM-powered Analysis** - 大语言模型驱动的分析

---

## Quick Start / 快速开始

### Prerequisites / 前提条件

```bash
# Install dependencies
pip install flask numpy pandas scikit-learn langchain langchain-openai python-dotenv
```

### Configuration / 配置

Create `.env` file with your API key:

创建 `.env` 文件并配置API密钥：

```env
SILICONFLOW_API_KEY="your_api_key_here"
```

### Run / 运行

```bash
# Start Web Dashboard
python app.py
# Access at: http://localhost:5008

# Run LLM Agent
python main.py
```

---

## Project Structure / 项目结构

```
Anomaly-Detection-Agent/
├── templates/
│   └── monitor.html        # Web监控仪表盘
├── anomaly_detector.py     # 异常检测引擎
├── app.py                  # Flask Web应用
├── database.py             # SQLite数据库模块
├── main.py                 # LLM智能代理
├── sensor_simulator.py     # 传感器模拟器
├── TUTORIAL.md             # 教学文档
└── README.md               # 项目说明
```

---

## API Endpoints / API接口

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | GET | 返回监控仪表盘页面 |
| `/api/readings/{machine_id}` | GET | 获取当前传感器读数 |
| `/api/anomalies/{machine_id}` | GET | 获取异常历史和统计 |

---

## Usage / 使用方法

### Web Dashboard / Web仪表盘

1. Open browser at http://localhost:5008
2. Select machine from dropdown
3. View real-time sensor readings
4. Monitor anomaly status

1. 打开浏览器访问 http://localhost:5008
2. 从下拉菜单选择设备
3. 查看实时传感器数据
4. 监控异常状态

### LLM Agent / 智能代理

```python
from main import agent_executor

# Query machine status
result = agent_executor.invoke({
    "input": "Check the current status of MACHINE-01 and analyze its sensor data"
})
print(result['output'])
```

---

## Anomaly Severity / 异常严重程度

| Score Range | Severity | Description |
| :--- | :--- | :--- |
| < -0.5 | Critical | 严重异常，需立即处理 |
| -0.5 ~ -0.3 | High | 高度异常，紧急关注 |
| -0.3 ~ -0.1 | Medium | 中等异常，持续监控 |
| >= -0.1 | Low | 轻微异常，信息提示 |

---

## License / 许可证

MIT License

---

## Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献代码！请随时提交Pull Request。