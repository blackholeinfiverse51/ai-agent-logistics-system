# 🚀 Unified Core API - Deployment Guide

## Lead: Rishabh Yadav
**System**: AI + CRM + Logistics + Compliance + RL Integration

---

## Prerequisites

- Docker & Docker Compose installed
- Python 3.11+
- Node.js 18+ (for frontend)
- PostgreSQL 15+ (or use Docker)
- RabbitMQ & Redis (or use Docker)

---

## Quick Start (Docker - Recommended)

### 1. Clone and Configure

```bash
cd /Volumes/Samsung/ai-agent-logistics-system-main/backend/Unified_Core_API

# Copy environment file
cp .env.example .env

# Edit .env with your production values
nano .env
```

### 2. Build and Deploy

```bash
# Build all containers
docker-compose -f docker-compose.production.yml build

# Start all services
docker-compose -f docker-compose.production.yml up -d

# Check status
docker-compose -f docker-compose.production.yml ps
```

### 3. Verify Deployment

```bash
# Check API health
curl http://localhost:8005/health

# Check dashboard
curl http://localhost:3000

# View logs
docker-compose -f docker-compose.production.yml logs -f unified-core-api
```

---

## Manual Deployment (Without Docker)

### 1. Install Dependencies

```bash
cd /Volumes/Samsung/ai-agent-logistics-system-main/backend

# Install Python dependencies
pip install -r BHIV_Integrator_Core/requirements.txt

# Install frontend dependencies
cd dashboard-frontend
npm install
npm run build
```

### 2. Setup Database

```bash
# PostgreSQL
createdb unified_db

# Or use SQLite for testing
export DATABASE_URL=sqlite:///./unified.db
```

### 3. Start Services

```bash
# Terminal 1: Start RabbitMQ
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management-alpine

# Terminal 2: Start Redis
docker run -d -p 6379:6379 redis:7-alpine

# Terminal 3: Start Backend
cd Unified_Core_API
python unified_core.py

# Terminal 4: Start Frontend
cd dashboard-frontend
npm start
```

---

## Production Configuration

### Environment Variables

Edit `.env` file:

```env
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@db-host:5432/unified_db
RABBITMQ_URL=amqp://admin:pass@rabbitmq-host:5672/
REDIS_URL=redis://redis-host:6379
JWT_SECRET_KEY=<generate-strong-key>
```

### SSL/TLS Setup

```bash
# Generate SSL certificates
mkdir ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/nginx.key -out ssl/nginx.crt
```

### Nginx Configuration

Create `nginx.conf`:

```nginx
upstream backend {
    server unified-core-api:8005;
}

upstream frontend {
    server dashboard:80;
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/nginx.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx.key;

    location /api/ {
        proxy_pass http://backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://frontend/;
        proxy_set_header Host $host;
    }
}
```

---

## Testing the Deployment

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
  -d '{"opportunity_id": "OPP_ID", "items": [...]}'

# 4. Schedule Delivery
curl -X POST http://localhost:8005/logistics/delivery \
  -H "Content-Type: application/json" \
  -d '{"order_id": "ORDER_ID", "delivery_date": "2024-01-20"}'

# 5. Submit Feedback
curl -X POST http://localhost:8005/task/feedback \
  -H "Content-Type: application/json" \
  -d '{"order_id": "ORDER_ID", "rating": 5}'

# 6. Check Compliance Logs
curl http://localhost:8005/logs?limit=10
```

---

## Monitoring & Maintenance

### Health Checks

```bash
# API Health
curl http://localhost:8005/health

# System Status
curl http://localhost:8005/status

# Event Broker Status
curl http://localhost:8005/event/health
```

### Log Management

```bash
# View real-time logs
docker-compose logs -f unified-core-api

# Export logs
docker-compose logs unified-core-api > logs/deployment.log
```

### Database Backup

```bash
# PostgreSQL backup
docker exec unified-postgres pg_dump -U user unified_db > backup.sql

# Restore
docker exec -i unified-postgres psql -U user unified_db < backup.sql
```

---

## Scaling & Performance

### Horizontal Scaling

```yaml
# docker-compose.production.yml
services:
  unified-core-api:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
```

### Load Balancing

Add Nginx load balancing:

```nginx
upstream backend {
    least_conn;
    server unified-core-api-1:8005;
    server unified-core-api-2:8005;
    server unified-core-api-3:8005;
}
```

---

## Troubleshooting

### Common Issues

**Issue**: API not responding
```bash
# Check container status
docker-compose ps

# Restart service
docker-compose restart unified-core-api
```

**Issue**: Database connection failed
```bash
# Check database logs
docker-compose logs postgres

# Verify connection
docker exec unified-postgres psql -U user -d unified_db -c "SELECT 1"
```

**Issue**: Event broker not working
```bash
# Check RabbitMQ
docker-compose logs rabbitmq

# Access management UI
open http://localhost:15672
```

---

## Security Checklist

- [ ] Change default passwords in `.env`
- [ ] Generate strong JWT secret key
- [ ] Enable SSL/TLS certificates
- [ ] Configure firewall rules
- [ ] Enable rate limiting
- [ ] Set up audit logging
- [ ] Configure backup strategy
- [ ] Enable monitoring alerts

---

## Support & Contact

**Lead**: Rishabh Yadav  
**System**: Unified Core API v1.0.0  
**Documentation**: See README.md and HANDOVER.md

---

## Next Steps

1. Configure domain and DNS
2. Set up CI/CD pipeline
3. Enable monitoring (Prometheus/Grafana)
4. Configure automated backups
5. Set up alerting (Slack/Teams)
6. Scale based on load testing results
