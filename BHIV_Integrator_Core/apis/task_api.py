"""
Task Manager API Router for BHIV Integrator Core
Proxies requests to the task management system and triggers events
"""

from fastapi import APIRouter, HTTPException, Request
import requests
from typing import Dict, Any
from datetime import datetime
from config.settings import settings
from event_broker.event_broker import EventBroker
from unified_logging.logger import UnifiedLogger
from compliance.compliance_hooks import ComplianceHooks

router = APIRouter()
event_broker = EventBroker()
logger = UnifiedLogger()
compliance = ComplianceHooks()

TASK_BASE_URL = settings.get("task_base_url", "http://localhost:8000")

@router.get("/review")
async def get_reviews():
    """Get task reviews"""
    try:
        response = requests.get(f"{TASK_BASE_URL}/review", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task API error: {str(e)}")

@router.post("/review")
async def create_review(request: Request):
    """Create task review and trigger events"""
    try:
        body = await request.json()

        # Create review in task system
        response = requests.post(f"{TASK_BASE_URL}/review", json=body, timeout=10)
        response.raise_for_status()
        review_data = response.json()

        # Log API call
        await logger.log_api_call({
            "method": "POST",
            "endpoint": "/review",
            "status_code": 200,
            "source": "integrator",
            "target": "task_manager",
            "response_time": 0.1
        })

        # Trigger event
        await event_broker.publish_event({
            "event_type": "review_created",
            "source_system": "task_manager",
            "target_systems": ["crm"],
            "payload": review_data,
            "priority": "medium"
        })

        return review_data

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Task service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.get("/feedback")
async def get_feedback():
    """Get task feedback"""
    try:
        response = requests.get(f"{TASK_BASE_URL}/feedback", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task API error: {str(e)}")

@router.post("/feedback")
async def create_feedback(request: Request):
    """Create task feedback and trigger events"""
    try:
        body = await request.json()

        # Create feedback in task system
        response = requests.post(f"{TASK_BASE_URL}/feedback", json=body, timeout=10)
        response.raise_for_status()
        feedback_data = response.json()

        # Log transaction
        await logger.log_transaction({
            "system": "task_manager",
            "type": "feedback_submission",
            "transaction_id": feedback_data.get("feedback_id"),
            "amount": 0,  # Feedback doesn't have monetary value
            "status": "created",
            "parties": [body.get("user_id")],
            "metadata": feedback_data
        })

        # Trigger event based on feedback type
        feedback_type = body.get("type", "general")
        if feedback_type == "complaint":
            await event_broker.publish_event({
                "event_type": "complaint_received",
                "source_system": "task_manager",
                "target_systems": ["crm", "compliance"],
                "payload": feedback_data,
                "priority": "high"
            })
        elif feedback_type == "escalation":
            await event_broker.publish_event({
                "event_type": "task_escalated",
                "source_system": "task_manager",
                "target_systems": ["crm", "logistics"],
                "payload": feedback_data,
                "priority": "high"
            })
        else:
            await event_broker.publish_event({
                "event_type": "feedback_received",
                "source_system": "task_manager",
                "target_systems": ["crm"],
                "payload": feedback_data,
                "priority": "low"
            })

        return feedback_data

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Task service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.get("/workflow-state")
async def get_workflow_states():
    """Get workflow states"""
    try:
        response = requests.get(f"{TASK_BASE_URL}/workflow-state", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task API error: {str(e)}")

@router.post("/workflow-state")
async def update_workflow_state(request: Request):
    """Update workflow state and trigger events"""
    try:
        body = await request.json()

        # Update workflow state in task system
        response = requests.post(f"{TASK_BASE_URL}/workflow-state", json=body, timeout=10)
        response.raise_for_status()
        workflow_data = response.json()

        # Log API call
        await logger.log_api_call({
            "method": "POST",
            "endpoint": "/workflow-state",
            "status_code": 200,
            "source": "integrator",
            "target": "task_manager",
            "response_time": 0.1
        })

        # Trigger events based on state changes
        new_state = body.get("state")
        if new_state == "completed":
            await event_broker.publish_event({
                "event_type": "task_completed",
                "source_system": "task_manager",
                "target_systems": ["crm", "logistics"],
                "payload": workflow_data,
                "priority": "medium"
            })
        elif new_state == "escalated":
            await event_broker.publish_event({
                "event_type": "task_escalated",
                "source_system": "task_manager",
                "target_systems": ["crm", "compliance"],
                "payload": workflow_data,
                "priority": "high"
            })
        elif new_state == "blocked":
            await event_broker.publish_event({
                "event_type": "task_blocked",
                "source_system": "task_manager",
                "target_systems": ["crm"],
                "payload": workflow_data,
                "priority": "medium"
            })

        return workflow_data

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Task service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.get("/tasks")
async def get_tasks():
    """Get all tasks"""
    try:
        response = requests.get(f"{TASK_BASE_URL}/tasks", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task API error: {str(e)}")

@router.post("/tasks")
async def create_task(request: Request):
    """Create task and trigger events"""
    try:
        body = await request.json()

        # Check access control
        access_result = await compliance.check_access_control(
            body.get("created_by", "unknown"),
            "task_creation",
            "create"
        )

        if not access_result.get("allowed", False):
            raise HTTPException(status_code=403, detail="Access denied for task creation")

        # Create task in task system
        response = requests.post(f"{TASK_BASE_URL}/tasks", json=body, timeout=10)
        response.raise_for_status()
        task_data = response.json()

        # Log audit trail
        await compliance.audit_trail_log(
            "create",
            body.get("created_by", "system"),
            f"task_{task_data.get('task_id')}",
            {"task_data": task_data}
        )

        # Trigger event
        await event_broker.publish_event({
            "event_type": "task_created",
            "source_system": "task_manager",
            "target_systems": ["crm"],
            "payload": task_data,
            "priority": "medium"
        })

        return task_data

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Task service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.put("/tasks/{task_id}")
async def update_task(task_id: str, request: Request):
    """Update task and trigger events"""
    try:
        body = await request.json()

        # Update task in task system
        response = requests.put(f"{TASK_BASE_URL}/tasks/{task_id}", json=body, timeout=10)
        response.raise_for_status()
        task_data = response.json()

        # Check for status changes
        if body.get("status") == "completed":
            await event_broker.publish_event({
                "event_type": "task_completed",
                "source_system": "task_manager",
                "target_systems": ["crm", "logistics"],
                "payload": task_data,
                "priority": "medium"
            })
        elif body.get("priority") == "high":
            await event_broker.publish_event({
                "event_type": "task_priority_increased",
                "source_system": "task_manager",
                "target_systems": ["crm"],
                "payload": task_data,
                "priority": "high"
            })

        return task_data

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Task service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.post("/webhooks/events")
async def receive_task_events(request: Request):
    """Receive events from task management system"""
    try:
        event_data = await request.json()

        # Log incoming event
        await logger.log_event({
            "event_type": f"task_{event_data.get('event_type', 'unknown')}",
            "source_system": "task_manager",
            "payload": event_data,
            "status": "received"
        })

        # Process specific events
        event_type = event_data.get("event_type")
        if event_type == "task_overdue":
            # Trigger escalation
            await event_broker.publish_event({
                "event_type": "task_overdue",
                "source_system": "task_manager",
                "target_systems": ["crm", "compliance"],
                "payload": event_data.get("payload", {}),
                "priority": "high"
            })

        elif event_type == "task_assigned":
            # Trigger notification
            await event_broker.publish_event({
                "event_type": "task_assigned",
                "source_system": "task_manager",
                "target_systems": ["crm"],
                "payload": event_data.get("payload", {}),
                "priority": "low"
            })

        return {"status": "processed"}

    except Exception as e:
        print(f"❌ Error processing task webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Webhook processing error: {str(e)}")