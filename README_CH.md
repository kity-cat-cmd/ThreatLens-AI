# ThreatLens AI

**AI驱动的安全威胁分析平台**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/平台-Windows%20%7C%20Linux%20%7C%20Mac-orange.svg)

## 概述

ThreatLens AI 是一个智能安全威胁分析平台，利用大语言模型（LLM）对安全事件进行实时智能分析和解释。平台提供全面的威胁可视化仪表板、自动安全报告生成和安全团队可操作的安全洞察。

## 核心功能

- **AI驱动的威胁分析**：使用LLM通过自然语言分析和解释安全威胁
- **实时威胁监控**：事件采集和监控仪表板
- **威胁情报数据库**：历史威胁数据存储和检索
- **自动报告生成**：AI生成的安全分析报告
- **RESTful API**：完整的后端API，支持集成和扩展
- **前后端分离**：现代架构，关注点清晰分离

## 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                    ThreatLens AI 架构                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   前端      │───▶│   FastAPI   │───▶│   数据库    │    │
│  │  (HTML/JS)  │    │   后端      │    │  (SQLite)   │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│                            │                                │
│                            ▼                                │
│                     ┌─────────────┐                        │
│                     │   AI引擎    │                        │
│                     │  (LLM API)  │                        │
│                     └─────────────┘                        │
│                            │                                │
│                            ▼                                │
│                     ┌─────────────┐                        │
│                     │    Redis    │                        │
│                     │   (缓存)    │                        │
│                     └─────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 技术栈

| 组件 | 技术 |
|-----------|------------|
| 后端 | Python 3.9+ / FastAPI |
| 前端 | HTML5 / JavaScript / Bootstrap |
| 关系型数据库 | SQLite |
| 缓存/NoSQL | Redis |
| AI | OpenAI / Claude API 集成 |

## 快速开始

### 前置要求

- Python 3.9 或更高版本
- Redis Server（可选，用于缓存）
- OpenAI API Key 或兼容的 LLM API

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/fail-diss/ThreatLens-AI.git
cd ThreatLens-AI
```

2. **创建虚拟环境**
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境**
```bash
cp .env.example .env
# 编辑 .env 文件，添加你的 API keys
```

5. **初始化数据库**
```bash
python init_db.py
```

6. **运行应用**
```bash
python main.py
```

7. **访问仪表板**
打开浏览器访问: `http://localhost:8000`

## API 接口

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/api/v1/health` | 健康检查 |
| GET | `/api/v1/threats` | 获取所有威胁 |
| GET | `/api/v1/threats/{id}` | 获取威胁详情 |
| POST | `/api/v1/threats` | 报告新威胁 |
| POST | `/api/v1/analyze` | AI分析威胁 |
| GET | `/api/v1/stats` | 获取威胁统计 |
| GET | `/api/v1/reports` | 获取分析报告 |
| POST | `/api/v1/reports/generate` | 生成新报告 |

## 项目结构

```
ThreatLens-AI/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI应用入口
│   ├── config.py            # 配置管理
│   ├── models/
│   │   ├── __init__.py
│   │   ├── threat.py        # 威胁数据模型
│   │   └── report.py       # 报告数据模型
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── threats.py       # 威胁API路由
│   │   ├── analysis.py      # 分析API路由
│   │   └── reports.py       # 报告API路由
│   ├── services/
│   │   ├── __init__.py
│   │   ├── threat_service.py    # 威胁业务逻辑
│   │   ├── ai_service.py        # AI分析服务
│   │   └── report_service.py    # 报告生成服务
│   └── database/
│       ├── __init__.py
│       ├── connection.py    # 数据库连接
│       └── init_db.py      # 数据库初始化
├── static/
│   ├── css/
│   │   └── style.css       # 自定义样式
│   └── js/
│       └── app.js          # 前端JavaScript
├── templates/
│   └── index.html          # 仪表板HTML
├── tests/
│   ├── __init__.py
│   ├── test_threats.py     # 威胁API测试
│   └── test_analysis.py    # 分析测试
├── .env.example            # 环境变量模板
├── .gitignore
├── requirements.txt        # Python依赖
├── README.md               # 英文文档
└── README_CH.md           # 本文件
```

## 配置说明

通过环境变量配置应用：

```env
# API配置
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# AI配置
AI_PROVIDER=openai  # openai, anthropic, local
AI_API_KEY=your-api-key-here
AI_MODEL=gpt-4

# 数据库配置
DATABASE_URL=sqlite:///./threatlens.db
REDIS_URL=redis://localhost:6379/0

# 安全
SECRET_KEY=your-secret-key-here
```

## 使用示例

### 报告威胁

```bash
curl -X POST http://localhost:8000/api/v1/threats \
  -H "Content-Type: application/json" \
  -d '{
    "title": "可疑登录尝试",
    "type": "暴力破解",
    "severity": "high",
    "source_ip": "192.168.1.100",
    "description": "检测到多次失败登录尝试"
  }'
```

### 获取AI分析

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "threat_id": 1,
    "include_recommendations": true
  }'
```

## 开发

### 运行测试

```bash
pytest tests/ -v
```

### 热重载运行

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 详细文档

- [详细技术说明](detailed-explanation.md) - 技术深度解析

## 评估框架

项目效果通过以下指标评估：

| 指标 | 描述 | 目标 |
|--------|-------------|--------|
| 威胁检测率 | 正确识别的威胁百分比 | >95% |
| 分析准确度 | AI分析相关性评分 | >90% |
| 响应时间 | 平均API响应时间 | <500ms |
| 报告质量 | 用户满意度评分 | >4.5/5 |

## 贡献指南

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 作者

**fail-diss** - [GitHub](https://github.com/fail-diss)

## 致谢

- OpenAI 提供 GPT API
- Anthropic 提供 Claude API
- FastAPI 团队提供的优秀框架
- 所有贡献者和支持者
