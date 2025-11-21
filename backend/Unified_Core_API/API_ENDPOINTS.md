# 📡 API Endpoints Reference

**Unified Core API v1.0.0**  
**Base URL**: `http://localhost:8005`  
**Lead**: Rishabh Yadav

---

## Table of Contents
1. [System Endpoints](#system-endpoints)
2. [CRM Module](#crm-module)
3. [Logistics Module](#logistics-module)
4. [Task Management](#task-management)
5. [Employee Management](#employee-management)
6. [Event System](#event-system)
7. [Compliance](#compliance)
8. [BHIV Core Integration](#bhiv-core-integration)

---

## System Endpoints

### GET /
**Description**: System information  
**Owner**: Rishabh Yadav  
**Auth**: None  

**Response**:
```json
{
  "system": "Unified Core API",
  "version": "1.0.0",
  "status": "operational",
  "modules": ["AI Backend", "CRM", "Logistics", "Compliance", "RL", "Dashboard"],
  "lead": "Rishabh Yadav",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### GET /health
**Description**: Health check endpoint  
**Owner**: Rishabh Yadav  
**Auth**: None  

**Response**:
```json
{
  "status": "healthy",
  "modules": {
    "ai_backend": "active",
    "compliance": "active",
    "workflow": "active",
    "rl_system": "active",
    "dashboard": "active",
    "event_broker": "active"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### GET /status
**Description**: Detailed system status  
**Owner**: Rishabh Yadav  
**Auth**: Required (Monitor permission)  

**Response**:
```json
{
  "system": "Unified Core API",
  "orchestration": "active",
  "data_flow": "synchronized",
  "compliance": "enforced",
  "rl_feedback": "operational",
  "dashboard_integration": "live",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### GET /logs
**Description**: Unified log viewer  
**Owner**: Rishabh Yadav  
**Auth**: Required  
**Query Params**: `limit` (default: 100)  

**Response**:
```json
{
  "logs": [
    {
      "task_id": "TASK_001",
      "user_id": "USER_123",
      "event_type": "task_completed",
      "rl_score": 0.85,
      "consent_flag": true,
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 1
}
```

---

## CRM Module

### POST /crm/leads
**Description**: Create new lead  
**Owner**: Vijay  
**Auth**: Required (CRM write permission)  

**Request Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "source": "website",
  "company": "Acme Corp"
}
```

**Response**:
```json
{
  "id": "LEAD_001",
  "name": "John Doe",
  "email": "john@example.com",
  "status": "new",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### GET /crm/leads
**Description**: List all leads  
**Owner**: Vijay  
**Auth**: Required (CRM read permission)  
**Query Params**: `status`, `limit`, `offset`  

**Response**:
```json
{
  "leads": [
    {
      "id": "LEAD_001",
      "name": "John Doe",
      "email": "john@example.com",
      "status": "qualified"
    }
  ],
  "total": 1,
  "page": 1
}
```

---

### POST /crm/opportunities
**Description**: Create opportunity from lead  
**Owner**: Vijay  
**Auth**: Required (CRM write permission)  

**Request Body**:
```json
{
  "lead_id": "LEAD_001",
  "value": 10000,
  "stage": "qualification",
  "probability": 0.5,
  "expected_close_date": "2024-02-15"
}
```

**Response**:
```json
{
  "id": "OPP_001",
  "lead_id": "LEAD_001",
  "value": 10000,
  "stage": "qualification",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### GET /crm/opportunities
**Description**: List all opportunities  
**Owner**: Vijay  
**Auth**: Required (CRM read permission)  
**Query Params**: `stage`, `limit`, `offset`  

**Response**:
```json
{
  "opportunities": [
    {
      "id": "OPP_001",
      "lead_id": "LEAD_001",
      "value": 10000,
      "stage": "negotiation",
      "probability": 0.75
    }
  ],
  "total": 1
}
```

---

### GET /crm/accounts
**Description**: List all accounts  
**Owner**: Vijay  
**Auth**: Required (CRM read permission)  

**Response**:
```json
{
  "accounts": [
    {
      "id": "ACC_001",
      "name": "Acme Corp",
      "type": "customer",
      "status": "active"
    }
  ],
  "total": 1
}
```

---

## Logistics Module

### POST /logistics/procurement
**Description**: Create procurement order  
**Owner**: Vijay  
**Auth**: Required (Logistics write permission)  

**Request Body**:
```json
{
  "opportunity_id": "OPP_001",
  "customer_id": "LEAD_001",
  "items": [
    {
      "product": "Widget A",
      "quantity": 10,
      "price": 500
    }
  ],
  "total": 5000,
  "priority": "standard"
}
```

**Response**:
```json
{
  "id": "ORDER_001",
  "status": "pending",
  "total": 5000,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### POST /logistics/delivery
**Description**: Schedule delivery  
**Owner**: Vijay  
**Auth**: Required (Logistics write permission)  

**Request Body**:
```json
{
  "order_id": "ORDER_001",
  "delivery_date": "2024-01-20T14:00:00Z",
  "address": "123 Main St, City, State 12345",
  "priority": "standard",
  "special_instructions": "Ring doorbell"
}
```

**Response**:
```json
{
  "id": "DELIVERY_001",
  "order_id": "ORDER_001",
  "delivery_date": "2024-01-20T14:00:00Z",
  "status": "scheduled",
  "tracking_number": "TRK123456"
}
```

---

### GET /logistics/inventory
**Description**: Check inventory levels  
**Owner**: Vijay  
**Auth**: Required (Logistics read permission)  
**Query Params**: `product_id`, `location`  

**Response**:
```json
{
  "inventory": [
    {
      "product_id": "PROD_001",
      "product_name": "Widget A",
      "quantity": 150,
      "location": "Warehouse A",
      "reorder_level": 50
    }
  ]
}
```

---

### GET /logistics/orders
**Description**: List all orders  
**Owner**: Vijay  
**Auth**: Required (Logistics read permission)  
**Query Params**: `status`, `customer_id`, `limit`  

**Response**:
```json
{
  "orders": [
    {
      "id": "ORDER_001",
      "customer_id": "LEAD_001",
      "total": 5000,
      "status": "processing"
    }
  ],
  "total": 1
}
```

---

## Task Management

### POST /task/review
**Description**: Submit task review  
**Owner**: Parth  
**Auth**: Required (Task write permission)  

**Request Body**:
```json
{
  "task_id": "TASK_001",
  "reviewer_id": "USER_123",
  "status": "approved",
  "comments": "Looks good",
  "dhi_score": 0.9
}
```

**Response**:
```json
{
  "id": "REVIEW_001",
  "task_id": "TASK_001",
  "status": "approved",
  "reviewed_at": "2024-01-15T10:30:00Z"
}
```

---

### POST /task/feedback
**Description**: Submit customer feedback  
**Owner**: Parth  
**Auth**: Required  

**Request Body**:
```json
{
  "order_id": "ORDER_001",
  "rating": 5,
  "comment": "Excellent service!",
  "categories": ["delivery", "quality"]
}
```

**Response**:
```json
{
  "id": "FEEDBACK_001",
  "order_id": "ORDER_001",
  "rating": 5,
  "submitted_at": "2024-01-15T10:30:00Z"
}
```

---

### GET /task/workflow-state
**Description**: Get workflow state  
**Owner**: Parth  
**Auth**: Required  
**Query Params**: `task_id`  

**Response**:
```json
{
  "task_id": "TASK_001",
  "current_state": "in_progress",
  "previous_state": "pending",
  "transitions": [
    {
      "from": "pending",
      "to": "in_progress",
      "timestamp": "2024-01-15T10:00:00Z"
    }
  ]
}
```

---

### POST /task/tasks
**Description**: Create new task  
**Owner**: Parth  
**Auth**: Required (Task write permission)  

**Request Body**:
```json
{
  "title": "Process Order",
  "description": "Process order ORDER_001",
  "assignee_id": "USER_123",
  "priority": "high",
  "due_date": "2024-01-20"
}
```

**Response**:
```json
{
  "id": "TASK_001",
  "title": "Process Order",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Employee Management

### GET /employee/monitoring
**Description**: Get employee monitoring data  
**Owner**: Vijay  
**Auth**: Required (Admin permission)  
**Query Params**: `employee_id`, `date_range`  

**Response**:
```json
{
  "employee_id": "EMP_001",
  "metrics": {
    "tasks_completed": 25,
    "average_completion_time": 120,
    "quality_score": 0.92
  }
}
```

---

### GET /employee/attendance
**Description**: Get attendance records  
**Owner**: Vijay  
**Auth**: Required (Admin permission)  

**Response**:
```json
{
  "attendance": [
    {
      "employee_id": "EMP_001",
      "date": "2024-01-15",
      "status": "present",
      "hours_worked": 8
    }
  ]
}
```

---

### GET /employee/performance
**Description**: Get performance metrics  
**Owner**: Vijay  
**Auth**: Required (Admin permission)  

**Response**:
```json
{
  "employee_id": "EMP_001",
  "performance": {
    "productivity": 0.88,
    "quality": 0.92,
    "timeliness": 0.95,
    "overall_score": 0.91
  }
}
```

---

## Event System

### POST /event/publish
**Description**: Publish event to broker  
**Owner**: Parth  
**Auth**: Required  

**Request Body**:
```json
{
  "event_type": "order_created",
  "source_system": "logistics",
  "target_systems": ["crm", "task"],
  "payload": {
    "order_id": "ORDER_001",
    "customer_id": "LEAD_001"
  },
  "priority": "high"
}
```

**Response**:
```json
{
  "event_id": "EVT_001",
  "status": "published",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### POST /event/subscribe
**Description**: Subscribe to event types  
**Owner**: Parth  
**Auth**: Required  

**Request Body**:
```json
{
  "subscriber_id": "dashboard",
  "event_types": ["order_created", "delivery_scheduled"],
  "callback_url": "http://dashboard:3000/webhook"
}
```

**Response**:
```json
{
  "subscription_id": "SUB_001",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### GET /event/events
**Description**: Get event history  
**Owner**: Parth  
**Auth**: Required  
**Query Params**: `event_type`, `limit`, `since`  

**Response**:
```json
{
  "events": [
    {
      "event_id": "EVT_001",
      "event_type": "order_created",
      "timestamp": "2024-01-15T10:30:00Z",
      "payload": {}
    }
  ],
  "total": 1
}
```

---

### POST /event/unified
**Description**: Unified event with RL + Compliance  
**Owner**: Rishabh Yadav  
**Auth**: Required  

**Request Body**:
```json
{
  "task_id": "TASK_001",
  "user_id": "USER_123",
  "rl_score": 0.85,
  "consent_flag": true,
  "event_type": "task_completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "metadata": {
    "source_system": "task",
    "priority": "high"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "event_id": "TASK_001",
  "processed_at": "2024-01-15T10:30:00Z"
}
```

---

## Compliance

### POST /consent/revoke
**Description**: Revoke user consent  
**Owner**: Sankalp  
**Auth**: Required (Admin permission)  

**Request Body**:
```json
{
  "consent_type": "data_processing",
  "user_id": "USER_123"
}
```

**Response**:
```json
{
  "status": "consent_revoked",
  "user_id": "USER_123",
  "consent_type": "data_processing",
  "revoked_at": "2024-01-15T10:30:00Z"
}
```

---

### GET /compliance/audit-report
**Description**: Get compliance audit report  
**Owner**: Sankalp  
**Auth**: Required (Admin permission)  
**Query Params**: `start_date`, `end_date`  

**Response**:
```json
{
  "report_type": "audit_log_summary",
  "period": {
    "start": "2024-01-01",
    "end": "2024-01-15"
  },
  "total_events": 1250,
  "security_events": 45,
  "access_denials": 12,
  "compliance_status": "compliant",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## BHIV Core Integration

### POST /bhiv/agent/register
**Description**: Register agent with BHIV Core  
**Owner**: Vijay  
**Auth**: Required  

**Request Body**:
```json
{
  "agent_id": "logistics_agent",
  "agent_type": "logistics",
  "capabilities": ["order_processing", "inventory_management"],
  "endpoint": "http://localhost:8005/logistics"
}
```

**Response**:
```json
{
  "agent_id": "logistics_agent",
  "status": "registered",
  "registered_at": "2024-01-15T10:30:00Z"
}
```

---

### POST /bhiv/agent/decide
**Description**: Request AI decision from BHIV Core  
**Owner**: Vijay  
**Auth**: Required  

**Request Body**:
```json
{
  "query": "Should we approve order ORDER_001?",
  "context": {
    "order_id": "ORDER_001",
    "customer_id": "LEAD_001",
    "value": 10000
  }
}
```

**Response**:
```json
{
  "decision": "approved",
  "confidence": 0.92,
  "reasoning": "Customer has good history, order within limits",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### POST /bhiv/query-uniguru
**Description**: Query UniGuru knowledge system  
**Owner**: Vijay  
**Auth**: Required  

**Request Body**:
```json
{
  "query": "What is the return policy?",
  "context": {
    "customer_id": "LEAD_001"
  }
}
```

**Response**:
```json
{
  "answer": "30-day return policy for all products",
  "sources": ["policy_doc_v2.pdf"],
  "confidence": 0.95
}
```

---

### POST /bhiv/query-gurukul
**Description**: Query Gurukul pipeline system  
**Owner**: Vijay  
**Auth**: Required  

**Request Body**:
```json
{
  "query": "Process customer onboarding",
  "pipeline": "onboarding"
}
```

**Response**:
```json
{
  "pipeline_id": "onboarding",
  "status": "processing",
  "steps_completed": 2,
  "steps_total": 5
}
```

---

### GET /bhiv/status
**Description**: Get BHIV Core system status  
**Owner**: Vijay  
**Auth**: Required  

**Response**:
```json
{
  "bhiv_core_status": "operational",
  "registered_agents": 5,
  "active_decisions": 12,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Error Responses

All endpoints may return these error responses:

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Invalid request body",
  "details": "Field 'email' is required"
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid authentication credentials"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Insufficient permissions",
  "required_permission": "admin"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found",
  "resource_id": "LEAD_999"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate Limit Exceeded",
  "message": "Too many requests",
  "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "request_id": "REQ_123"
}
```

---

## Rate Limits

- **Default**: 100 requests per 60 seconds per IP
- **Authenticated**: 1000 requests per 60 seconds per user
- **Admin**: Unlimited

---

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

---

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Lead**: Rishabh Yadav
