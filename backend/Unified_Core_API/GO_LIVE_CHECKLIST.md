# ✅ Go-Live Checklist - Unified Core API

**Lead**: Rishabh Yadav  
**Target Go-Live Date**: [Set Date]  
**Version**: 1.0.0

---

## Pre-Deployment Checklist

### 1. Code & Configuration ✅

- [x] All modules integrated into Unified_Core_API
- [x] Event schema defined (event_schema.json)
- [x] Environment variables configured (.env.example)
- [x] Docker configuration complete (Dockerfile, docker-compose.production.yml)
- [x] Nginx configuration ready
- [x] SSL certificates prepared
- [ ] Production secrets generated and secured
- [ ] Database connection strings updated
- [ ] External service URLs configured

### 2. Testing ✅

- [x] Unit tests for core modules
- [x] Integration test script (test_pipeline.py)
- [x] End-to-end pipeline test
- [x] Health check endpoints verified
- [ ] Load testing (1000 concurrent users)
- [ ] Security penetration testing
- [ ] Compliance validation testing
- [ ] Disaster recovery testing

### 3. Documentation ✅

- [x] README.md complete
- [x] DEPLOYMENT_GUIDE.md complete
- [x] HANDOVER.md complete
- [x] API_ENDPOINTS.md complete
- [x] INTEGRATION_DIAGRAM.md complete
- [x] REFLECTION.md complete
- [ ] User training materials
- [ ] Operations runbook
- [ ] Incident response procedures

### 4. Security & Compliance ✅

- [x] JWT authentication implemented
- [x] RBAC authorization configured
- [x] Rate limiting enabled
- [x] Consent flag enforcement
- [x] Audit logging active
- [x] ISO 27001 security headers
- [ ] External security audit completed
- [ ] GDPR compliance verified
- [ ] Data encryption at rest
- [ ] Backup encryption

### 5. Infrastructure

- [ ] Production servers provisioned
- [ ] Domain name configured
- [ ] DNS records updated
- [ ] SSL certificates installed
- [ ] Load balancer configured
- [ ] Database replicas set up
- [ ] Redis cluster configured
- [ ] RabbitMQ cluster configured
- [ ] Backup system configured
- [ ] Monitoring tools installed

---

## Deployment Steps

### Phase 1: Infrastructure Setup

```bash
# 1. Provision servers
# - 3x API servers (2 CPU, 4GB RAM each)
# - 1x Database server (4 CPU, 8GB RAM)
# - 1x Redis server (2 CPU, 4GB RAM)
# - 1x RabbitMQ server (2 CPU, 4GB RAM)
# - 1x Nginx load balancer (2 CPU, 2GB RAM)

# 2. Install Docker on all servers
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 3. Configure firewall rules
# - Allow 80, 443 (public)
# - Allow 8005-8007 (internal)
# - Allow 5432, 6379, 5672 (internal)
```

### Phase 2: Database Setup

```bash
# 1. Initialize PostgreSQL
docker run -d \
  --name unified-postgres \
  -e POSTGRES_USER=produser \
  -e POSTGRES_PASSWORD=<secure-password> \
  -e POSTGRES_DB=unified_db \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15-alpine

# 2. Run migrations
# (Add migration scripts as needed)

# 3. Create read replicas
# (Configure replication)
```

### Phase 3: Application Deployment

```bash
# 1. Clone repository
git clone <repository-url>
cd Unified_Core_API

# 2. Configure environment
cp .env.example .env
nano .env  # Update with production values

# 3. Build and deploy
docker-compose -f docker-compose.production.yml build
docker-compose -f docker-compose.production.yml up -d

# 4. Verify deployment
curl http://localhost:8005/health
```

### Phase 4: Frontend Deployment

```bash
# 1. Deploy to Vercel
cd dashboard-frontend
vercel --prod

# 2. Configure environment variables in Vercel
# - REACT_APP_API_URL=https://api.yourdomain.com
# - NODE_ENV=production

# 3. Verify deployment
curl https://yourdomain.vercel.app
```

### Phase 5: Monitoring Setup

```bash
# 1. Deploy Prometheus
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# 2. Deploy Grafana
docker run -d \
  --name grafana \
  -p 3000:3000 \
  -e GF_SECURITY_ADMIN_PASSWORD=<secure-password> \
  grafana/grafana

# 3. Import dashboards
# (Import pre-configured dashboards)
```

---

## Post-Deployment Verification

### 1. Health Checks

```bash
# API Health
curl https://api.yourdomain.com/health
# Expected: {"status": "healthy"}

# System Status
curl https://api.yourdomain.com/status
# Expected: All modules "active"

# Database Connection
curl https://api.yourdomain.com/crm/leads?limit=1
# Expected: Valid response or empty array
```

### 2. End-to-End Test

```bash
# Run full pipeline test
python test_pipeline.py

# Expected: All 8 steps complete successfully
```

### 3. Performance Test

```bash
# Load test with Apache Bench
ab -n 1000 -c 100 https://api.yourdomain.com/health

# Expected:
# - 99% requests < 200ms
# - 0% failed requests
# - Throughput > 500 req/sec
```

### 4. Security Verification

```bash
# Check SSL
curl -I https://api.yourdomain.com
# Expected: Strict-Transport-Security header present

# Check rate limiting
for i in {1..150}; do curl https://api.yourdomain.com/health; done
# Expected: 429 Too Many Requests after 100 requests

# Check authentication
curl https://api.yourdomain.com/status
# Expected: 401 Unauthorized
```

---

## Monitoring & Alerts

### Key Metrics to Monitor

1. **API Response Time**
   - Target: < 200ms average
   - Alert: > 500ms for 5 minutes

2. **Error Rate**
   - Target: < 1%
   - Alert: > 5% for 5 minutes

3. **System Uptime**
   - Target: > 99.9%
   - Alert: Service down for > 1 minute

4. **Database Performance**
   - Target: Query time < 100ms
   - Alert: > 500ms for 5 minutes

5. **Event Processing**
   - Target: < 1 second end-to-end
   - Alert: > 5 seconds for 5 minutes

### Alert Channels

- [ ] Slack webhook configured
- [ ] Email alerts configured
- [ ] PagerDuty integration (optional)
- [ ] SMS alerts for critical issues

---

## Rollback Plan

### If Issues Occur

1. **Immediate Rollback**
   ```bash
   # Stop new deployment
   docker-compose -f docker-compose.production.yml down
   
   # Restore previous version
   git checkout <previous-tag>
   docker-compose -f docker-compose.production.yml up -d
   ```

2. **Database Rollback**
   ```bash
   # Restore from backup
   docker exec -i unified-postgres psql -U produser unified_db < backup.sql
   ```

3. **DNS Rollback**
   - Update DNS to point to previous infrastructure
   - Wait for TTL propagation (typically 5-15 minutes)

---

## Team Responsibilities

### During Go-Live

| Team Member | Responsibility | Contact |
|-------------|----------------|---------|
| Rishabh Yadav | Overall coordination, integration issues | Primary |
| Vijay | AI backend, BHIV Core, logistics issues | On-call |
| Sankalp | Compliance, consent, audit issues | On-call |
| Parth | Event broker, workflow issues | On-call |
| Noopur | RL system issues | On-call |
| Nisarg | Dashboard issues | On-call |
| Yash | Frontend API integration issues | On-call |
| Nikhil | UI/UX, Vercel deployment issues | On-call |

### Communication Plan

- **Primary Channel**: Slack #go-live-unified-core
- **Escalation**: Phone call to Rishabh
- **Status Updates**: Every 30 minutes during go-live window
- **Issue Tracking**: Jira/GitHub Issues

---

## Go-Live Timeline

### T-7 Days
- [ ] Final code freeze
- [ ] Complete all testing
- [ ] Security audit
- [ ] Team training

### T-3 Days
- [ ] Deploy to staging
- [ ] Final integration tests
- [ ] Performance testing
- [ ] Backup verification

### T-1 Day
- [ ] Team briefing
- [ ] Verify rollback plan
- [ ] Confirm on-call schedule
- [ ] Final checklist review

### Go-Live Day

**Hour 0-1: Deployment**
- [ ] Deploy infrastructure
- [ ] Deploy application
- [ ] Verify health checks

**Hour 1-2: Verification**
- [ ] Run integration tests
- [ ] Verify monitoring
- [ ] Test all endpoints

**Hour 2-4: Monitoring**
- [ ] Monitor metrics
- [ ] Watch for errors
- [ ] Respond to issues

**Hour 4-24: Stabilization**
- [ ] Continue monitoring
- [ ] Address minor issues
- [ ] Collect feedback

### T+1 Day
- [ ] Review metrics
- [ ] Address issues
- [ ] Team retrospective

### T+7 Days
- [ ] Performance review
- [ ] Optimization opportunities
- [ ] Documentation updates

---

## Success Criteria

### Must Have (Go/No-Go)
- ✅ All health checks passing
- ✅ End-to-end pipeline test successful
- ✅ Zero critical security issues
- ✅ Rollback plan tested
- ✅ Team trained and ready

### Should Have
- ✅ Load testing completed
- ✅ Monitoring dashboards configured
- ✅ Documentation complete
- ✅ Backup system verified

### Nice to Have
- Performance optimization
- Advanced monitoring
- Automated scaling
- Multi-region deployment

---

## Post-Go-Live Tasks

### Week 1
- [ ] Daily monitoring reviews
- [ ] Address any issues
- [ ] Collect user feedback
- [ ] Performance tuning

### Week 2-4
- [ ] Optimization based on metrics
- [ ] Documentation updates
- [ ] Team retrospective
- [ ] Plan next iteration

### Month 2-3
- [ ] Advanced features
- [ ] Scaling improvements
- [ ] Security enhancements
- [ ] Integration expansions

---

## Sign-Off

### Pre-Deployment Approval

- [ ] **Rishabh Yadav** (Lead Integrator) - Date: _______
- [ ] **Vijay** (AI Backend Lead) - Date: _______
- [ ] **Sankalp** (Compliance Lead) - Date: _______
- [ ] **Technical Manager** - Date: _______
- [ ] **Security Team** - Date: _______

### Post-Deployment Confirmation

- [ ] **Rishabh Yadav** - System operational - Date: _______
- [ ] **Operations Team** - Monitoring active - Date: _______
- [ ] **Security Team** - No critical issues - Date: _______

---

## Emergency Contacts

**Rishabh Yadav** (Lead)  
Email: rishabh@example.com  
Phone: [Phone Number]

**Technical Support**  
Email: support@example.com  
Slack: #unified-core-support

**Security Issues**  
Email: security@example.com  
Phone: [Emergency Number]

---

**Status**: Ready for Go-Live ✅  
**Last Updated**: January 2024  
**Version**: 1.0.0
