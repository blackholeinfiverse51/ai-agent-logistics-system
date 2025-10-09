# 🤖 AI Agent Unified System - Logistics + CRM + Infiverse

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 16+](https://img.shields.io/badge/node.js-16+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Express.js](https://img.shields.io/badge/Express.js-4.18-lightgrey.svg)](https://expressjs.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-red.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-supported-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive unified platform combining AI-powered logistics automation, CRM management, and employee workforce monitoring with intelligent insights and real-time analytics.

<<<<<<< HEAD
> **✅ INTEGRATION COMPLETED**: Vijay's Complete-Infiverse repository has been successfully integrated. See [Integration Task Completion Report](INTEGRATION_TASK_COMPLETION_REPORT.md) for full details.

=======
>>>>>>> 9a5d7abfa61aa2769341197651d91d368bfed338
## 🎯 Overview

The AI Agent Logistics System automates key logistics operations using intelligent agents that can sense, plan, and act autonomously while maintaining human oversight for complex decisions.

### Key Features

#### Logistics Module
- 🔄 **Autonomous Restock Agent**: Monitors returns and automatically creates restock requests
- 📦 **Procurement Automation**: Intelligent supplier management and purchase order generation
- 🚚 **Delivery Tracking**: Real-time shipment monitoring and status updates
- 📊 **Inventory Management**: Automated stock level monitoring and alerts

#### CRM Module
- 🏢 **Account Management**: Complete customer account lifecycle management
- 👥 **Contact & Lead Tracking**: Comprehensive contact database and lead conversion
- 💼 **Opportunity Pipeline**: Sales opportunity tracking and forecasting
- 📅 **Activity Management**: Task scheduling and activity logging
- 🗺️ **Visit Planning**: GPS-enabled visit scheduling and tracking

#### Infiverse Module
- 👁️ **Employee Monitoring**: Real-time workforce activity tracking and productivity analysis
- ⏰ **Attendance Management**: Automated time tracking with geolocation validation
- 🚨 **Alert System**: Intelligent alerts for policy violations and productivity issues
- 🤖 **AI Insights**: Machine learning-powered workforce analytics and recommendations
- 🔒 **Privacy Controls**: GDPR-compliant monitoring with user consent management

## 🏗️ Architecture

### High-Level System Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            AI Agent Unified System                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│  │    Leads    │───▶│Opportunities│───▶│  Accounts  │───▶│   Orders    │       │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘       │
│         │                   │                   │                   │            │
│         ▼                   ▼                   ▼                   ▼            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│  │CRM Activities│    │   Tasks     │    │ Monitoring  │    │   Alerts    │       │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘       │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                        Logistics Flow                                   │   │
│  │                                                                         │   │
│  │  Orders → Restock → Procurement → Delivery → Inventory → Analytics     │   │
│  │     ↓         ↓         ↓            ↓         ↓          ↓             │   │
│  │  AI Agents → Human Review → Notifications → Dashboards → Reports       │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      Infiverse Workflows                                │   │
│  │                                                                         │   │
│  │  Employee Monitoring → Attendance → Task Management → AI Insights      │   │
│  │         ↓                ↓              ↓              ↓                │   │
│  │      Alerts → Reports → Communication → Dashboard Integration          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Technical Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            Technical Components                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │  Data Sources   │    │   AI Agents     │    │ Human Review    │             │
│  │                 │    │                 │    │                 │             │
│  │ • Orders        │───▶│ • Restock       │───▶│ • Confidence    │             │
│  │ • Returns       │    │ • Procurement   │    │   Scoring       │             │
│  │ • Inventory     │    │ • Delivery      │    │ • Review UI     │             │
│  │ • CRM Data      │    │ • CRM Agents    │    │ • Escalation    │             │
│  │ • Employee Data │    │ • Monitoring    │    │ • Alerts        │             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│           │                       │                       │                   │
│           │                       ▼                       │                   │
│           │              ┌─────────────────┐              │                   │
│           │              │   FastAPI       │              │                   │
│           │              │   Backend       │              │                   │
│           │              │ • Logistics API │              │                   │
│           │              │ • CRM API       │              │                   │
│           │              │ • Infiverse API │              │                   │
│           │              │   (Proxied)     │              │                   │
│           │              └─────────────────┘              │                   │
│           │                       │                       │                   │
│           ▼                       ▼                       ▼                   │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐            │
│  │   Databases     │    │   Dashboards    │    │  Notifications   │            │
│  │                 │    │                 │    │                  │            │
│  │ • SQLite/       │    │ • Streamlit     │    │ • Email/Slack    │            │
│  │   PostgreSQL    │    │ • Real-time     │    │ • Push/Webhook   │            │
│  │ • MongoDB       │    │ • Analytics     │    │ • Alerts         │            │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘            │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      Deployment Options                                │   │
│  │                                                                         │   │
│  │  Docker → Railway/Render/Heroku → Vercel → AWS EC2 → Local Dev         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- Optional: Docker, OpenAI API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/blackholeinfiverse51/ai-agent-logistics-system.git
   cd ai-agent-logistics-system
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings (OpenAI API key optional)
   ```

5. **Initialize database**:
   ```bash
   python migrate_to_database.py
   ```

6. **Start the system**:
   ```bash
   python start_server.py
   ```

7. **Access the interfaces**:
   - 📊 Dashboard: http://localhost:8501
   - 🔗 API: http://localhost:8000
   - 📖 API Docs: http://localhost:8000/docs

## 🎮 Usage

### Running Individual Components

```bash
# Run main restock agent
python agent.py

# Run procurement agent
python procurement_agent.py

# Run delivery agent
python delivery_agent.py

# Start chatbot (interactive)
python chatbot_agent.py

# Human review interface
python review_interface.py

# Run comprehensive demo
python demo.py
```

### API Examples

```python
import requests

# Get system health
response = requests.get("http://localhost:8000/health")
print(response.json())

# Query chatbot
response = requests.post("http://localhost:8000/chat", 
                        json={"message": "Where is my order #101?"})
print(response.json())

# Get pending reviews
response = requests.get("http://localhost:8000/reviews/pending")
print(response.json())
```

## 🐳 Docker Deployment

### Quick Start with Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build
```bash
# Build main application
docker build -t ai-agent:latest .

# Build dashboard
docker build -f Dockerfile.dashboard -t ai-agent-dashboard:latest .

# Run containers
docker run -d -p 8000:8000 -p 8501:8501 ai-agent:latest
```

## ☁️ Cloud Deployment

### Railway.app
```bash
npm install -g @railway/cli
railway login
railway up
```

### Render.com
1. Connect GitHub repository
2. Use `render.yaml` configuration
3. Set environment variables

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

See [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📊 Performance Metrics

### Current Performance
- **Restock Processing**: <1 second average
- **Chatbot Response**: <30 seconds
- **API Response Time**: <200ms
- **System Uptime**: >99% target
- **Auto-approval Rate**: >85% for high-confidence decisions

### Test Coverage
- **Total Tests**: 34 (23 passing, 11 in progress)
- **Code Coverage**: 44% overall, 72-97% for core components
- **Test Types**: Unit, Integration, API, End-to-End

## 🔧 Configuration

### Environment Variables
```bash
# Core Settings
OPENAI_API_KEY=sk-...                    # Optional: for smart chatbot
DATABASE_URL=sqlite:///logistics_agent.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Agent Settings
AGENT_INTERVAL=300                       # 5 minutes
CONFIDENCE_THRESHOLD=0.7                 # Human review threshold

# Notifications
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
ALERT_RECIPIENTS=admin@company.com

# Features
ENABLE_SMART_CHATBOT=true
ENABLE_EMAIL_NOTIFICATIONS=true
ENABLE_HUMAN_REVIEW=true
```

## 📚 Documentation

- [📖 Consolidated API Documentation](docs/CONSOLIDATED_API_DOCUMENTATION.md)
<<<<<<< HEAD
- [� Integration Implementation Summary](INTEGRATION_IMPLEMENTATION_SUMMARY.md)
- [🤔 Integration Reflection](INTEGRATION_REFLECTION.md)
- [📮 Postman Collection](docs/AI_Agent_Unified_API.postman_collection.json)
- [🚀 Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [👤 User Manual](docs/USER_MANUAL.md)
- [� Legacy API Documentation](docs/API_DOCUMENTATION.md)
=======
- [📖 Legacy API Documentation](docs/API_DOCUMENTATION.md)
- [👤 User Manual](docs/USER_MANUAL.md)
- [🚀 Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
>>>>>>> 9a5d7abfa61aa2769341197651d91d368bfed338
- [📝 Changelog](docs/CHANGELOG.md)

## 🧪 Testing

```bash
# Run all tests
python run_tests.py

# Run specific test categories
pytest tests/test_agent.py -v
pytest tests/test_api.py -v
pytest tests/test_integration.py -v

# Run with coverage
pytest --cov=. --cov-report=html
```

## 🔍 Monitoring

### Health Checks
```bash
# System health check
python deploy.py health-check

# Start monitoring service
python monitoring.py

# View metrics
tail -f data/monitoring_metrics.json
```

### Dashboard Monitoring
- System resource usage
- Agent performance metrics
- API response times
- Error rates and alerts

## 🛠️ Development

### Project Structure
```
ai-agent_project/
├── agent.py                 # Main restock agent
├── procurement_agent.py     # Procurement automation
├── delivery_agent.py        # Delivery management
├── chatbot_agent.py         # Customer service bot
├── api_app.py              # FastAPI backend
├── dashboard_app.py        # Streamlit dashboard
├── human_review.py         # Review system
├── database/               # Database models and services
├── tests/                  # Test suite
├── data/                   # Data files and logs
├── docs/                   # Documentation
└── docker-compose.yml      # Container orchestration
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 🔒 Security

- JWT authentication for API endpoints
- Environment variable configuration
- Input validation and sanitization
- Audit logging for all operations
- Secure deployment configurations

## 📈 Roadmap

### Version 1.1 (Next Release)
- [ ] Machine learning confidence scoring
- [ ] Real-time WebSocket updates
- [ ] Advanced analytics dashboard
- [ ] Mobile app support

### Version 2.0 (Future)
- [ ] Multi-tenant support
- [ ] Advanced workflow automation
- [ ] ERP system integrations
- [ ] Predictive analytics

## 🐛 Known Issues

- Some test failures in chatbot logic (being addressed)
- API response format inconsistencies (minor)
- Memory optimization needed for large datasets

See [Issues](https://github.com/blackholeinfiverse51/ai-agent-logistics-system/issues) for full list.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- 📧 Email: support@blackholeinfiverse51.com
- 💬 GitHub Discussions: [Discussions](https://github.com/blackholeinfiverse51/ai-agent-logistics-system/discussions)
- 📖 Documentation: [docs/](docs/)
- 🐛 Issues: [GitHub Issues](https://github.com/blackholeinfiverse51/ai-agent-logistics-system/issues)

## 🙏 Acknowledgments

- OpenAI for GPT API
- FastAPI and Streamlit communities
- Contributors and testers
- Open source libraries used

---

**Built with ❤️ for autonomous logistics automation**
