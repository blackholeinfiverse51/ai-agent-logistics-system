# 🎯 Unified Core API - Production System

**Lead Integrator**: Rishabh Yadav  
**Version**: 1.0.0  
**Status**: Production Ready ✅

---

## 🚀 Overview

The Unified Core API consolidates all modular systems into a single production-grade platform:

- ✅ **AI Backend** (Vijay) - Orchestration & EMS
- ✅ **Compliance** (Sankalp) - Consent & audit logs
- ✅ **Workflow Automation** (Parth) - Event triggers
- ✅ **RL System** (Noopur) - Reward/penalty loops
- ✅ **Dashboard** (Nisarg) - Analytics & visualization
- ✅ **Frontend** (Yash, Nikhil) - UI/UX & deployment

---

## 📋 Quick Start

### Docker Deployment (Recommended)

```bash
# 1. Configure environment
cp .env.example .env
nano .env

# 2. Start all services
docker-compose -f docker-compose.production.yml up -d

# 3. Verify deployment
curl http://localhost:8005/health
```

### Manual Setup

```bash
# 1. Install dependencies
pip install -r ../BHIV_Integrator_Core/requirements.txt

# 2. Start services
python unified_core.py

# 3. Access API
open http://localhost:8005/docs
```

---

## 🔗 Key Endpoints

### System
- `GET /` - System information
- `GET /health` - Health check
- `GET /status` - Detailed status
- `GET /logs` - Unified logs

### Logistics (Vijay)
- `POST /logistics/procurement` - Procurement orders
- `POST /logistics/delivery` - Delivery scheduling
- `GET /logistics/inventory` - Inventory tracking

### CRM (Vijay)
- `POST /crm/leads` - Create leads
- `POST /crm/opportunities` - Create opportunities
- `GET /crm/accounts` - List accounts

### Task Management (Parth)
- `POST /task/review` - Submit reviews
- `POST /task/feedback` - Submit feedback
- `GET /task/workflow-state` - Workflow state

### Events (Parth)
- `POST /event/publish` - Publish events
- `POST /event/unified` - Unified event flow
- `GET /event/events` - Event history

### Compliance (Sankalp)
- `POST /consent/revoke` - Revoke consent
- `GET /compliance/audit-report` - Audit reports

### BHIV Core (Vijay)
- `POST /bhiv/agent/decide` - AI decisions
- `POST /bhiv/query-uniguru` - UniGuru queries
- `POST /bhiv/query-gurukul` - Gurukul queries

---

## 📊 Data Flow

```
Task/Order → AI → RL → Workflow → Compliance → Dashboard
```

### Event Schema

```json
{
  "task_id": "TASK_001",
  "user_id": "USER_123",
  "rl_score": 0.85,
  "consent_flag": true,
  "event_type": "task_completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "metadata": {}
}
```

---

## 🧪 Testing

### Full Pipeline Test

```bash
# 1. Create Lead
curl -X POST http://localhost:8005/crm/leads \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Customer", "email": "test@example.com"}'

# 2. Convert to Opportunity
curl -X POST http://localhost:8005/crm/opportunities \
  -H "Content-Type: application/json" \
  -d '{"lead_id": "LEAD_ID", "value": 10000}'

# 3. Create Order
curl -X POST http://localhost:8005/logistics/orders \
  -H "Content-Type: application/json" \
  -d '{"opportunity_id": "OPP_ID", "items": []}'

# 4. Schedule Delivery
curl -X POST http://localhost:8005/logistics/delivery \
  -H "Content-Type: application/json" \
  -d '{"order_id": "ORDER_ID", "delivery_date": "2024-01-20"}'

# 5. Submit Feedback
curl -X POST http://localhost:8005/task/feedback \
  -H "Content-Type: application/json" \
  -d '{"order_id": "ORDER_ID", "rating": 5}'

# 6. Check Compliance
curl http://localhost:8005/logs?limit=10
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│        Unified Core API (8005)          │
├─────────────────────────────────────────┤
│  Logistics │ CRM │ Task │ Employee      │
├─────────────────────────────────────────┤
│           Event Broker                  │
├─────────────────────────────────────────┤
│  Compliance │ RL │ Logging │ BHIV      │
└─────────────────────────────────────────┘
         │              │
    ┌────▼────┐    ┌───▼────┐
    │Dashboard│    │Frontend│
    └─────────┘    └────────┘
```

---

## 📦 Deployment

### Production Stack
- **Backend**: Docker (FastAPI/Python)
- **Frontend**: Vercel (React)
- **Database**: PostgreSQL
- **Message Broker**: RabbitMQ
- **Cache**: Redis
- **Proxy**: Nginx

### Scaling
- 3 API replicas
- Load balancing
- Auto-scaling enabled

---

## 🔐 Security

- JWT authentication
- RBAC authorization
- Rate limiting (100 req/min)
- Consent enforcement
- Audit logging
- ISO 27001 compliant

---

## 📈 Monitoring

- Health checks: `/health`
- System status: `/status`
- Event monitoring: `/event/events`
- Logs: `/logs`

---

## 📚 Documentation

- **Deployment**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Handover**: [HANDOVER.md](HANDOVER.md)
- **API Docs**: http://localhost:8005/docs
- **Event Schema**: [event_schema.json](event_schema.json)

---

## 👥 Team

| Name | Role | Module |
|------|------|--------|
| Rishabh Yadav | Lead Integrator | Unified Core |
| Vijay | AI Backend | Logistics, CRM, BHIV |
| Sankalp | Compliance | Consent, Audit |
| Parth | Workflow | Events, Automation |
| Noopur | RL System | Rewards, Penalties |
| Nisarg | Dashboard | Analytics, Visualization |
| Yash | Frontend | API Integration |
| Nikhil | UI/UX | Design, Deployment |

---

## 🎯 Success Metrics

- ✅ All modules integrated
- ✅ End-to-end data flow verified
- ✅ Compliance enforced
- ✅ Dashboard live
- ✅ Dockerized deployment
- ✅ Documentation complete

---

## 🚀 Next Steps

1. Configure production domain
2. Enable monitoring (Prometheus/Grafana)
3. Set up CI/CD pipeline
4. Scale based on load
5. Expand RL algorithms

---

## 📞 Support

**Lead**: Rishabh Yadav  
**Email**: rishabh@example.com  
**Docs**: See HANDOVER.md for detailed ownership

---

**Status**: ✅ Production Ready | **Version**: 1.0.0 | **Date**: January 2024
