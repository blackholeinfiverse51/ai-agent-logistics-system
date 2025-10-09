# AI Agent Logistics + CRM API Contracts

## Overview
This document outlines the complete API contracts for the unified AI Agent Logistics + CRM system, including all endpoints, request/response formats, and sample JSON payloads.

## Base URL
```
http://localhost:8000
```

## Authentication
All endpoints require JWT authentication via Bearer token in the Authorization header.
```
Authorization: Bearer <jwt_token>
```

## API Endpoints

### Authentication Endpoints

#### POST /auth/login
User login endpoint.

**Request Body:**
```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### POST /auth/register
Register new user (admin only).

**Request Body:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "securepassword123",
  "role": "user"
}
```

### CRM Endpoints

#### Accounts

##### POST /accounts
Create a new account.

**Request Body:**
```json
{
  "name": "TechCorp Solutions",
  "account_type": "customer",
  "industry": "Technology",
  "website": "https://techcorp.com",
  "phone": "+1-555-0123",
  "email": "contact@techcorp.com",
  "billing_address": "123 Tech Street",
  "city": "San Francisco",
  "state": "CA",
  "country": "USA",
  "postal_code": "94105",
  "annual_revenue": 5000000.0,
  "employee_count": 150
}
```

**Response:**
```json
{
  "account_id": "ACC_A1B2C3D4",
  "name": "TechCorp Solutions",
  "account_type": "customer",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

##### GET /accounts
Get accounts with optional filters.

**Query Parameters:**
- `account_type`: customer, prospect, partner
- `status`: active, inactive
- `territory`: sales territory
- `limit`: max 1000

**Response:**
```json
{
  "accounts": [
    {
      "account_id": "ACC_A1B2C3D4",
      "name": "TechCorp Solutions",
      "industry": "Technology",
      "annual_revenue": 5000000.0,
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 1
}
```

##### GET /accounts/{account_id}
Get account by ID with full details.

**Response:**
```json
{
  "account_id": "ACC_A1B2C3D4",
  "name": "TechCorp Solutions",
  "account_type": "customer",
  "industry": "Technology",
  "website": "https://techcorp.com",
  "phone": "+1-555-0123",
  "email": "contact@techcorp.com",
  "billing_address": "123 Tech Street",
  "city": "San Francisco",
  "state": "CA",
  "country": "USA",
  "postal_code": "94105",
  "annual_revenue": 5000000.0,
  "employee_count": 150,
  "territory": "West Coast",
  "status": "active",
  "lifecycle_stage": "customer",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "contacts": [...],
  "opportunities": [...],
  "activities": [...]
}
```

#### Contacts

##### POST /contacts
Create a new contact.

**Request Body:**
```json
{
  "account_id": "ACC_A1B2C3D4",
  "first_name": "John",
  "last_name": "Smith",
  "title": "CTO",
  "department": "Engineering",
  "email": "john.smith@techcorp.com",
  "phone": "+1-555-0199",
  "mobile": "+1-555-0200",
  "contact_role": "decision_maker",
  "is_primary": true
}
```

**Response:**
```json
{
  "contact_id": "CON_E5F6G7H8",
  "account_id": "ACC_A1B2C3D4",
  "first_name": "John",
  "last_name": "Smith",
  "full_name": "John Smith",
  "email": "john.smith@techcorp.com",
  "status": "active",
  "created_at": "2024-01-15T10:35:00Z"
}
```

##### GET /contacts
Get contacts with optional filters.

**Query Parameters:**
- `account_id`: filter by account
- `contact_role`: decision_maker, influencer, contact
- `status`: active, inactive
- `limit`: max 1000

#### Leads

##### POST /leads
Create a new lead.

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "company": "StartupXYZ",
  "title": "CEO",
  "email": "jane.doe@startupxyz.com",
  "phone": "+1-555-0300",
  "lead_source": "website",
  "lead_status": "new",
  "lead_stage": "inquiry",
  "budget": 100000.0,
  "timeline": "Q2 2024",
  "need": "Logistics automation solution"
}
```

**Response:**
```json
{
  "lead_id": "LEAD_I9J0K1L2",
  "first_name": "Jane",
  "last_name": "Doe",
  "company": "StartupXYZ",
  "email": "jane.doe@startupxyz.com",
  "lead_status": "new",
  "lead_stage": "inquiry",
  "created_at": "2024-01-15T11:00:00Z"
}
```

##### GET /leads
Get leads with optional filters.

**Query Parameters:**
- `lead_status`: new, contacted, qualified, proposal, negotiation
- `lead_source`: website, referral, trade_show, cold_call
- `assigned_to`: user ID
- `converted`: true/false
- `limit`: max 1000

##### POST /leads/{lead_id}/convert
Convert lead to opportunity.

**Request Body:**
```json
{
  "account_id": "ACC_A1B2C3D4",
  "name": "Enterprise Logistics Solution",
  "description": "Complete automation package",
  "stage": "prospecting",
  "amount": 250000.0,
  "probability": 30.0,
  "expected_revenue": 75000.0,
  "close_date": "2024-06-30T00:00:00Z"
}
```

#### Opportunities

##### POST /opportunities
Create a new opportunity.

**Request Body:**
```json
{
  "account_id": "ACC_A1B2C3D4",
  "primary_contact_id": "CON_E5F6G7H8",
  "name": "Enterprise Logistics Upgrade",
  "description": "Complete warehouse automation",
  "stage": "prospecting",
  "probability": 25.0,
  "amount": 500000.0,
  "currency": "USD",
  "expected_revenue": 125000.0,
  "close_date": "2024-12-31T00:00:00Z",
  "requirements": "Integration with existing ERP",
  "products_interested": "Automated conveyor system"
}
```

**Response:**
```json
{
  "opportunity_id": "OPP_M3N4O5P6",
  "account_id": "ACC_A1B2C3D4",
  "name": "Enterprise Logistics Upgrade",
  "stage": "prospecting",
  "amount": 500000.0,
  "probability": 25.0,
  "is_closed": false,
  "created_at": "2024-01-15T11:30:00Z"
}
```

##### GET /opportunities
Get opportunities with optional filters.

**Query Parameters:**
- `stage`: prospecting, qualification, proposal, negotiation, closed_won, closed_lost
- `owner_id`: opportunity owner
- `account_id`: related account
- `is_closed`: true/false
- `close_date_from`: ISO date
- `close_date_to`: ISO date
- `limit`: max 1000

##### PUT /opportunities/{opportunity_id}/stage
Update opportunity stage.

**Request Body:**
```json
{
  "stage": "proposal",
  "probability": 60.0
}
```

#### Activities (Messaging/Notes)

##### POST /activities
Create a new activity (note, call, email, meeting, etc.).

**Request Body:**
```json
{
  "subject": "Initial Discovery Call",
  "description": "Discussed requirements and timeline",
  "activity_type": "call",
  "status": "completed",
  "priority": "high",
  "due_date": "2024-01-15T14:00:00Z",
  "start_time": "2024-01-15T14:00:00Z",
  "end_time": "2024-01-15T14:30:00Z",
  "duration_minutes": 30,
  "account_id": "ACC_A1B2C3D4",
  "contact_id": "CON_E5F6G7H8",
  "assigned_to": "user123",
  "outcome": "Positive feedback, moving to proposal stage",
  "next_steps": "Send proposal by Friday"
}
```

**Response:**
```json
{
  "activity_id": "ACT_Q7R8S9T0",
  "subject": "Initial Discovery Call",
  "activity_type": "call",
  "status": "completed",
  "created_at": "2024-01-15T14:35:00Z"
}
```

##### GET /activities
Get activities with optional filters.

**Query Parameters:**
- `activity_type`: call, email, meeting, task, note, visit
- `status`: planned, completed, cancelled
- `assigned_to`: user ID
- `account_id`: account ID
- `opportunity_id`: opportunity ID
- `lead_id`: lead ID
- `limit`: max 1000

##### PUT /activities/{activity_id}/complete
Mark activity as completed.

**Request Body:**
```json
{
  "outcome": "Successful meeting, client interested",
  "next_steps": "Follow up with proposal"
}
```

#### Tasks (Tasks/Reminders)

##### POST /tasks
Create a new task.

**Request Body:**
```json
{
  "title": "Send Proposal to TechCorp",
  "description": "Prepare and send detailed proposal for logistics upgrade",
  "priority": "high",
  "due_date": "2024-01-20T17:00:00Z",
  "reminder_date": "2024-01-19T09:00:00Z",
  "assigned_to": "user123",
  "account_id": "ACC_A1B2C3D4",
  "opportunity_id": "OPP_M3N4O5P6"
}
```

**Response:**
```json
{
  "task_id": "TASK_U1V2W3X4",
  "title": "Send Proposal to TechCorp",
  "status": "pending",
  "priority": "high",
  "due_date": "2024-01-20T17:00:00Z",
  "created_at": "2024-01-15T15:00:00Z"
}
```

##### GET /tasks
Get tasks with optional filters.

**Query Parameters:**
- `status`: pending, in_progress, completed, cancelled
- `assigned_to`: user ID
- `priority`: low, medium, high, urgent
- `account_id`: account ID
- `opportunity_id`: opportunity ID
- `limit`: max 1000

### Consolidated Endpoints

#### GET /account/view/{account_id}
Get comprehensive account view with all related data.

**Response:**
```json
{
  "account": {...},
  "contacts": [...],
  "opportunities": [...],
  "orders": [...],
  "tasks": [...],
  "recent_activities": [...]
}
```

#### GET /lead/pipeline
Get all leads organized by stage/status.

**Response:**
```json
{
  "pipeline": {
    "inquiry": {
      "new": [...],
      "contacted": [...]
    },
    "qualified": {
      "qualified": [...]
    }
  },
  "summary": {
    "inquiry": {
      "new": 5,
      "contacted": 3
    }
  },
  "total_leads": 8
}
```

#### GET /opportunity/status
Get opportunities with current stage and linked tasks.

**Response:**
```json
{
  "opportunities_by_stage": {
    "prospecting": [
      {
        "opportunity_id": "OPP_M3N4O5P6",
        "name": "Enterprise Upgrade",
        "stage": "prospecting",
        "amount": 500000.0,
        "linked_tasks": [...]
      }
    ]
  },
  "total_opportunities": 1
}
```

#### POST /llm_query
Process natural language queries against CRM data.

**Request Body:**
```json
{
  "query": "Show me all opportunities closing this month",
  "context": {
    "user_id": "user123",
    "filters": {}
  }
}
```

**Response:**
```json
{
  "query": "Show me all opportunities closing this month",
  "result": {
    "opportunities": [...],
    "count": 3
  },
  "natural_response": "You have 3 opportunities closing this month with a total value of $1.2M",
  "timestamp": "2024-01-15T16:00:00Z"
}
```

### Integration Endpoints

#### POST /integrations/office365/email
Send email via Office 365 integration.

**Request Body:**
```json
{
  "to_email": "client@techcorp.com",
  "subject": "Proposal for Logistics Upgrade",
  "body": "<html><body><h2>Proposal Details</h2><p>Please find attached our proposal...</p></body></html>",
  "cc_emails": ["manager@techcorp.com"],
  "attachments": ["/path/to/proposal.pdf"]
}
```

**Response:**
```json
{
  "status": "sent",
  "message": "Email sent successfully"
}
```

#### POST /integrations/google-maps/visit
Plan a visit using Google Maps integration.

**Request Body:**
```json
{
  "account_id": "ACC_A1B2C3D4",
  "purpose": "Product demonstration",
  "scheduled_time": "2024-01-20T14:00:00Z"
}
```

**Response:**
```json
{
  "visit_id": "VISIT_20240115160000",
  "account_id": "ACC_A1B2C3D4",
  "purpose": "Product demonstration",
  "scheduled_time": "2024-01-20T14:00:00Z",
  "location": {
    "address": "123 Tech Street, San Francisco, CA 94105",
    "latitude": 37.7749,
    "longitude": -122.4194
  },
  "status": "planned"
}
```

#### POST /integrations/bos/order
Create order from opportunity (BOS integration).

**Request Body:**
```json
{
  "opportunity_id": "OPP_M3N4O5P6",
  "order_details": {
    "product_id": "LOGISTICS_PKG_001",
    "quantity": 1,
    "special_requirements": "Custom integration"
  }
}
```

**Response:**
```json
{
  "message": "Order created from opportunity",
  "order_id": "ORD_20240115170000",
  "opportunity_id": "OPP_M3N4O5P6",
  "status": "created"
}
```

### Dashboard Endpoints

#### GET /dashboard/crm
Get comprehensive CRM dashboard data.

**Response:**
```json
{
  "accounts": {
    "total": 150,
    "active": 142
  },
  "leads": {
    "total": 89,
    "new": 23,
    "converted": 45,
    "conversion_rate": 50.6
  },
  "opportunities": {
    "total": 67,
    "open": 52,
    "won": 15,
    "win_rate": 22.4,
    "pipeline_value": 8500000.0
  },
  "recent_activities": [...],
  "pending_tasks": [...]
}
```

### Logistics Endpoints (Existing)

#### GET /orders
Get orders from logistics system.

**Query Parameters:**
- `limit`: max records

**Response:**
```json
{
  "orders": [
    {
      "order_id": 12345,
      "customer_id": "CUST001",
      "product_id": "PROD001",
      "quantity": 10,
      "status": "confirmed",
      "order_date": "2024-01-15T10:00:00Z"
    }
  ],
  "count": 1
}
```

### System Endpoints

#### GET /health
System health check.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "modules": {
    "logistics": "operational",
    "crm": "operational",
    "infiverse": "operational",
    "integrations": {
      "office365": "configured",
      "google_maps": "configured",
      "llm_query": "operational"
    }
  },
  "timestamp": "2024-01-15T16:30:00Z",
  "version": "3.2.0"
}
```

## Error Responses

All endpoints return standard HTTP status codes and error messages:

```json
{
  "detail": "Error description"
}
```

Common status codes:
- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

## Rate Limiting

API endpoints are rate limited based on user role and endpoint type. Contact administrator for specific limits.

## Versioning

Current API version: 3.2.0

All endpoints are backward compatible within major version 3.x.x.