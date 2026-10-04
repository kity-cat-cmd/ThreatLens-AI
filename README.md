# ThreatLens AI

**AI-Powered Security Threat Analysis Platform**

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Mac-orange.svg)

## Overview

ThreatLens AI is an intelligent security threat analysis platform that leverages Large Language Models (LLMs) to analyze, interpret, and explain security threats in real-time. The platform provides a comprehensive threat visualization dashboard, automated security report generation, and actionable insights for security teams.

## Key Features

- **AI-Powered Threat Analysis**: Uses LLM to analyze and explain security threats with natural language
- **Real-time Threat Monitoring**: Event collection and monitoring dashboard
- **Threat Intelligence Database**: Historical threat data storage and retrieval
- **Automated Report Generation**: AI-generated security analysis reports
- **RESTful API**: Full backend API for integration and extensibility
- **Frontend-Backend Separation**: Modern architecture with clear separation of concerns

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ThreatLens AI Architecture                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Frontend  │───▶│   FastAPI   │───▶│  Database   │    │
│  │  (HTML/JS)  │    │   Backend   │    │  (SQLite)   │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│                            │                                │
│                            ▼                                │
│                     ┌─────────────┐                        │
│                     │  AI Engine  │                        │
│                     │  (LLM API)  │                        │
│                     └─────────────┘                        │
│                            │                                │
│                            ▼                                │
│                     ┌─────────────┐                        │
│                     │    Redis    │                        │
│                     │   (Cache)   │                        │
│                     └─────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.9+ / FastAPI |
| Frontend | HTML5 / JavaScript / Bootstrap |
| Database | SQLite (Relational) |
| Cache | Redis (NoSQL) |
| AI | OpenAI / Claude API Integration |

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Redis Server (optional, for caching)
- OpenAI API Key or compatible LLM API

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/fail-diss/ThreatLens-AI.git
cd ThreatLens-AI
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Initialize database**
```bash
python init_db.py
```

6. **Run the application**
```bash
python main.py
```

7. **Access the dashboard**
Open your browser and navigate to: `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/threats` | List all threats |
| GET | `/api/v1/threats/{id}` | Get threat details |
| POST | `/api/v1/threats` | Report a new threat |
| POST | `/api/v1/analyze` | AI analyze threat |
| GET | `/api/v1/stats` | Get threat statistics |
| GET | `/api/v1/reports` | List analysis reports |
| POST | `/api/v1/reports/generate` | Generate new report |

## Project Structure

```
ThreatLens-AI/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── threat.py        # Threat data models
│   │   └── report.py       # Report data models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── threats.py       # Threat API routes
│   │   ├── analysis.py      # Analysis API routes
│   │   └── reports.py       # Report API routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── threat_service.py    # Threat business logic
│   │   ├── ai_service.py        # AI analysis service
│   │   └── report_service.py    # Report generation service
│   └── database/
│       ├── __init__.py
│       ├── connection.py    # Database connection
│       └── init_db.py      # Database initialization
├── static/
│   ├── css/
│   │   └── style.css       # Custom styles
│   └── js/
│       └── app.js          # Frontend JavaScript
├── templates/
│   └── index.html          # Dashboard HTML
├── tests/
│   ├── __init__.py
│   ├── test_threats.py     # Threat API tests
│   └── test_analysis.py   # Analysis tests
├── .env.example            # Environment template
├── .gitignore
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── README_CH.md           # Chinese README
```

## Configuration

Configure the application using environment variables:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# AI Configuration
AI_PROVIDER=openai  # openai, anthropic, local
AI_API_KEY=your-api-key-here
AI_MODEL=gpt-4

# Database Configuration
DATABASE_URL=sqlite:///./threatlens.db
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here
```

## Usage Examples

### Report a Threat

```bash
curl -X POST http://localhost:8000/api/v1/threats \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Suspicious Login Attempt",
    "type": "brute_force",
    "severity": "high",
    "source_ip": "192.168.1.100",
    "description": "Multiple failed login attempts detected"
  }'
```

### Get AI Analysis

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "threat_id": 1,
    "include_recommendations": true
  }'
```

## Development

### Run Tests

```bash
pytest tests/ -v
```

### Run with Hot Reload

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Documentation

- [Chinese Documentation](README_CH.md) - 中文文档
- [Detailed Explanation](detailed-explanation.md) - Technical deep-dive

## Evaluation Framework

The project effectiveness is evaluated through:

| Metric | Description | Target |
|--------|-------------|--------|
| Threat Detection Rate | Percentage of threats correctly identified | >95% |
| Analysis Accuracy | AI analysis relevance score | >90% |
| Response Time | Average API response time | <500ms |
| Report Quality | User satisfaction score | >4.5/5 |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
