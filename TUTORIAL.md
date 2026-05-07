# 🏭 异常检测代理系统 - 教学文档

## 一、项目概述

本项目是一个**工业设备异常检测智能代理系统**，结合了机器学习、传感器模拟、数据库存储和Web可视化技术，实现自动化的设备健康监控与异常预警。

### 核心功能

| 功能模块 | 描述 |
|---------|------|
| 传感器模拟 | 生成正常/异常的设备传感器数据 |
| 异常检测 | 使用Isolation Forest算法检测异常 |
| 数据持久化 | SQLite存储异常事件记录 |
| Web监控 | 实时仪表盘展示设备状态 |
| LLM代理 | 智能问答与分析助手 |

### 技术栈

- **Python 3.x** - 主开发语言
- **Flask** - Web框架
- **scikit-learn** - 机器学习（Isolation Forest）
- **LangChain** - LLM代理框架
- **Google Gemini** - 大语言模型
- **SQLite** - 轻量级数据库

---

## 二、项目架构

```
┌─────────────────────────────────────────────────────────────┐
│                     用户交互层                              │
│  ┌──────────────┐          ┌──────────────────────────┐    │
│  │ Web Dashboard│          │   LLM Agent (CLI)       │    │
│  │  (monitor.html)│        │   (main.py)             │    │
│  └──────┬───────┘          └───────────┬────────────┘    │
└─────────┼───────────────────────────────┼─────────────────┘
          │                               │
┌─────────▼───────────────────────────────▼─────────────────┐
│                     应用服务层                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Flask API (app.py)                      │  │
│  │  /api/readings/{machine_id}  → 获取传感器数据        │  │
│  │  /api/anomalies/{machine_id} → 获取异常历史          │  │
│  └─────────────────┬────────────────────────────────────┘  │
└────────────────────┼───────────────────────────────────────┘
                     │
┌────────────────────▼───────────────────────────────────────┐
│                     核心业务层                              │
│  ┌──────────────┐  ┌──────────────────┐  ┌─────────────┐  │
│  │sensor_sim    │  │anomaly_detector │  │anomaly_db   │  │
│  │(传感器模拟)  │  │(异常检测引擎)   │  │(数据存储)   │  │
│  └──────────────┘  └──────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、核心组件详解

### 3.1 传感器模拟器 (`sensor_simulator.py`)

负责生成模拟的设备传感器数据，支持正常数据生成和异常注入。

#### 核心类：`SensorSimulator`

**初始化方法**：定义三台模拟设备的基准参数

```python
self.machines = {
    'MACHINE-01': {'base_temp': 75, 'base_vibration': 0.5, 'base_pressure': 100, 'base_rpm': 1500},
    'MACHINE-02': {'base_temp': 80, 'base_vibration': 0.6, 'base_pressure': 110, 'base_rpm': 1800},
    'MACHINE-03': {'base_temp': 70, 'base_vibration': 0.4, 'base_pressure': 95, 'base_rpm': 1200}
}
```

**关键方法**：

| 方法 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `generate_normal_data()` | 生成指定时长的正常数据 | `machine_id`, `hours` | DataFrame |
| `inject_anomaly()` | 注入异常数据 | `df`, `anomaly_type` | DataFrame |
| `get_current_readings()` | 获取当前传感器读数 | `machine_id`, `include_anomaly` | Dict |

**异常类型支持**：
- `temperature_spike` - 温度突升
- `vibration_increase` - 振动逐渐增加
- `pressure_drop` - 压力骤降
- `rpm_fluctuation` - 转速波动

---

### 3.2 异常检测器 (`anomaly_detector.py`)

使用**Isolation Forest**孤立森林算法进行无监督异常检测。

#### 核心类：`AnomalyDetector`

**初始化配置**：

```python
self.model = IsolationForest(contamination=0.1, random_state=42)
self.feature_columns = ['temperature', 'vibration', 'pressure', 'rpm', 'power_consumption']
```

**关键方法**：

| 方法 | 功能 |
|------|------|
| `train()` | 使用正常数据训练模型 |
| `detect_anomaly()` | 检测异常并返回评分和严重程度 |
| `analyze_anomaly_type()` | 分析触发异常的传感器类型 |

**异常评分机制**：

| 分数范围 | 严重程度 | 说明 |
|---------|---------|------|
| < -0.5 | Critical | 严重异常，需立即处理 |
| -0.5 ~ -0.3 | High | 高度异常，紧急关注 |
| -0.3 ~ -0.1 | Medium | 中等异常，持续监控 |
| >= -0.1 | Low | 轻微异常，信息提示 |

**技术原理**：Isolation Forest通过随机划分特征空间，异常点会被更快孤立出来，评分越负表示越可能是异常。

---

### 3.3 数据库模块 (`database.py`)

使用SQLite存储异常事件，提供数据持久化和统计查询功能。

#### 数据库表结构：`anomalies`

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | INTEGER | 主键，自增 |
| `machine_id` | TEXT | 设备ID |
| `sensor_type` | TEXT | 传感器类型 |
| `temperature` | REAL | 温度值 |
| `vibration` | REAL | 振动值 |
| `pressure` | REAL | 压力值 |
| `rpm` | REAL | 转速 |
| `power_consumption` | REAL | 功耗 |
| `anomaly_score` | REAL | 异常评分 |
| `severity` | TEXT | 严重程度 |
| `created_at` | TIMESTAMP | 创建时间 |

**关键方法**：

| 方法 | 功能 |
|------|------|
| `log_anomaly()` | 记录异常事件 |
| `get_recent_anomalies()` | 获取最近异常列表 |
| `get_statistics()` | 获取统计数据 |

---

### 3.4 Web应用 (`app.py`)

Flask后端服务，提供REST API接口。

**API端点**：

| 端点 | 方法 | 功能 |
|------|------|------|
| `/` | GET | 返回监控仪表盘页面 |
| `/api/readings/{machine_id}` | GET | 获取当前传感器读数 |
| `/api/anomalies/{machine_id}` | GET | 获取异常历史和统计 |

**启动流程**：
1. 训练异常检测模型（24小时正常数据）
2. 启动Flask服务器（端口5008）

---

### 3.5 LLM智能代理 (`main.py`)

基于LangChain构建的智能问答代理，集成Google Gemini模型。

**代理工具**：

| 工具 | 功能 | 参数 |
|------|------|------|
| `analyze_sensor_data` | 分析传感器数据 | `machine_id` |
| `get_machine_status` | 获取设备状态 | `machine_id` |
| `get_recent_anomalies` | 获取异常历史 | `machine_id`, `limit` |

**配置要求**：需要在环境变量中设置 `GOOGLE_API_KEY`

---

## 四、快速开始

### 4.1 环境配置

```bash
# 安装依赖
pip install flask numpy pandas scikit-learn langchain langchain-google-genai python-dotenv

# 设置环境变量
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### 4.2 运行Web监控

```bash
python app.py
```

访问：http://localhost:5008

### 4.3 运行LLM代理

```bash
python main.py
```

---

## 五、使用示例

### 5.1 Web仪表盘使用

1. 选择目标设备（MACHINE-01/02/03）
2. 查看实时传感器数据
3. 观察异常检测状态
4. 浏览历史异常记录

### 5.2 LLM代理交互

```python
from main import agent_executor

# 查询设备状态
result = agent_executor.invoke({
    "input": "Check the current status of MACHINE-01 and analyze its sensor data"
})
print(result['output'])
```

---

## 六、扩展建议

### 6.1 功能扩展

| 方向 | 建议 |
|------|------|
| 更多传感器类型 | 添加湿度、电流、噪声等 |
| 模型优化 | 尝试AutoEncoder、LSTM等时序模型 |
| 告警机制 | 集成邮件/短信/钉钉告警 |
| 预测维护 | 基于历史数据预测故障概率 |

### 6.2 性能优化

- 使用Redis缓存高频查询
- 异步处理数据写入
- 模型预热和持久化

### 6.3 部署建议

- 使用Gunicorn作为生产服务器
- Docker容器化部署
- Nginx反向代理

---

## 七、项目文件结构

```
Anomaly-Detection-Agent/
├── templates/
│   └── monitor.html          # Web监控仪表盘
├── anomaly_detector.py       # 异常检测引擎
├── app.py                    # Flask Web应用
├── database.py               # SQLite数据库模块
├── main.py                   # LLM智能代理
├── sensor_simulator.py       # 传感器模拟器
└── README.md                 # 项目说明
```

---

## 八、总结

本项目展示了一个完整的工业设备异常检测系统架构，融合了：
- **数据模拟**：传感器数据生成与异常注入
- **机器学习**：无监督异常检测算法
- **数据存储**：SQLite轻量级数据库
- **Web可视化**：实时监控仪表盘
- **AI助手**：LLM智能问答代理

适合作为工业物联网、智能制造领域的学习和研究基础框架。