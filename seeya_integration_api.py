#!/usr/bin/env python3
"""
Seeya Integration API Endpoints
FastAPI endpoints for integrating Seeya's Assistant with the logistics system
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
import asyncio
from seeya_assistant_integration import seeya_integration, AssistantMessage

# Configure logging
logger = logging.getLogger(__name__)

# Create router for Seeya integration endpoints
seeya_router = APIRouter(prefix="/seeya", tags=["Seeya Integration"])

# Pydantic models for request/response validation
class SeeyaMessageRequest(BaseModel):
    """Request model for processing messages through Seeya integration"""
    user_id: str = Field(..., description="Unique identifier for the user")
    platform: str = Field(..., description="Source platform (whatsapp, email, slack, etc.)")
    message_text: str = Field(..., min_length=1, max_length=10000, description="The message content")
    timestamp: Optional[str] = Field(None, description="ISO 8601 timestamp of the message")
    message_id: Optional[str] = Field(None, description="Optional unique message identifier")
    conversation_id: Optional[str] = Field(None, description="Optional conversation identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional additional metadata")

class SeeyaUserPreferencesRequest(BaseModel):
    """Request model for updating user preferences"""
    auto_execute_logistics: bool = Field(True, description="Auto-execute logistics actions")
    department: str = Field("general", description="User department")
    role: str = Field("user", description="User role")
    notification_preferences: Dict[str, bool] = Field(
        default_factory=lambda: {"email": True, "slack": False},
        description="Notification preferences"
    )

class SeeyaResponse(BaseModel):
    """Standard response model for Seeya integration"""
    success: bool
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

@seeya_router.get("/health", response_model=Dict[str, Any])
async def seeya_health_check():
    """Health check for Seeya integration"""
    try:
        # Check integration components
        analytics = seeya_integration.get_analytics()
        
        return {
            "status": "healthy",
            "integration_active": True,
            "database_connected": "error" not in analytics,
            "components": {
                "seeya_assistant": "connected",
                "logistics_system": "active",
                "database": "healthy"
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Seeya health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

@seeya_router.post("/process_message", response_model=SeeyaResponse)
async def process_message_pipeline(
    request: SeeyaMessageRequest,
    background_tasks: BackgroundTasks
):
    """
    Process a message through the complete Seeya integration pipeline
    Message -> Summary -> Task -> Logistics Actions
    """
    try:
        logger.info(f"Processing message for user {request.user_id} from {request.platform}")
        
        # Convert request to message object
        message_data = {
            "user_id": request.user_id,
            "platform": request.platform,
            "message_text": request.message_text,
            "timestamp": request.timestamp or datetime.now().isoformat(),
            "message_id": request.message_id,
            "conversation_id": request.conversation_id,
            "metadata": request.metadata
        }
        
        # Process through integration pipeline
        result = await seeya_integration.process_message(message_data)
        
        if result.get("success"):
            return SeeyaResponse(
                success=True,
                message="Message processed successfully through integration pipeline",
                data=result
            )
        else:
            return SeeyaResponse(
                success=False,
                error=result.get("error", "Unknown error occurred"),
                data={"partial_result": result}
            )
    
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process message: {str(e)}"
        )

@seeya_router.get("/analytics", response_model=SeeyaResponse)
async def get_integration_analytics():
    """Get analytics and statistics for the Seeya integration"""
    try:
        analytics = seeya_integration.get_analytics()
        
        return SeeyaResponse(
            success=True,
            message="Analytics retrieved successfully",
            data=analytics
        )
    
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve analytics: {str(e)}"
        )

@seeya_router.get("/users/{user_id}/preferences", response_model=SeeyaResponse)
async def get_user_preferences(user_id: str):
    """Get user preferences for Seeya integration"""
    try:
        preferences = seeya_integration.get_user_preferences(user_id)
        
        return SeeyaResponse(
            success=True,
            message=f"Preferences retrieved for user {user_id}",
            data={"user_id": user_id, "preferences": preferences}
        )
    
    except Exception as e:
        logger.error(f"Error getting user preferences: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve user preferences: {str(e)}"
        )

@seeya_router.put("/users/{user_id}/preferences", response_model=SeeyaResponse)
async def update_user_preferences(
    user_id: str,
    preferences: SeeyaUserPreferencesRequest
):
    """Update user preferences for Seeya integration"""
    try:
        preferences_dict = preferences.dict()
        result = seeya_integration.set_user_preferences(user_id, preferences_dict)
        
        return SeeyaResponse(
            success=True,
            message=f"Preferences updated for user {user_id}",
            data={"user_id": user_id, "updated_preferences": preferences_dict}
        )
    
    except Exception as e:
        logger.error(f"Error updating user preferences: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update user preferences: {str(e)}"
        )

@seeya_router.post("/test/summarize", response_model=SeeyaResponse)
async def test_summarization(request: SeeyaMessageRequest):
    """Test message summarization without full pipeline execution"""
    try:
        # Mock summarization for testing
        mock_summary = {
            "summary_id": f"sum_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "message_id": request.message_id or f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "summary": f"User message: {request.message_text[:100]}...",
            "type": "request",
            "intent": "general_inquiry",
            "urgency": "medium",
            "confidence": 0.75,
            "reasoning": ["Message contains request keywords", "Standard user inquiry pattern"]
        }
        
        return SeeyaResponse(
            success=True,
            message="Summarization test completed",
            data={"test_mode": True, "summary": mock_summary}
        )
    
    except Exception as e:
        logger.error(f"Error in summarization test: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Summarization test failed: {str(e)}"
        )

@seeya_router.post("/test/pipeline", response_model=SeeyaResponse)
async def test_full_pipeline(request: SeeyaMessageRequest):
    """Test full integration pipeline with mock responses"""
    try:
        # Mock full pipeline response
        mock_pipeline_result = {
            "success": True,
            "message_id": request.message_id or f"msg_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "summary": {
                "summary_id": f"sum_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "summary": f"Test processing of: {request.message_text[:50]}...",
                "intent": "test_request",
                "urgency": "medium",
                "confidence": 0.85
            },
            "task": {
                "task_id": f"task_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "task_summary": f"Process test request: {request.message_text[:30]}...",
                "task_type": "test_task",
                "priority": "medium",
                "status": "pending"
            },
            "logistics_actions": [
                {
                    "action_id": f"action_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "action_type": "test_action",
                    "status": "completed",
                    "parameters": {
                        "test_mode": True,
                        "original_message": request.message_text,
                        "user_id": request.user_id,
                        "platform": request.platform
                    }
                }
            ],
            "pipeline_summary": {
                "total_actions": 1,
                "executed_actions": 1,
                "auto_executed": True,
                "test_mode": True
            }
        }
        
        return SeeyaResponse(
            success=True,
            message="Pipeline test completed successfully",
            data=mock_pipeline_result
        )
    
    except Exception as e:
        logger.error(f"Error in pipeline test: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline test failed: {str(e)}"
        )

@seeya_router.get("/status", response_model=SeeyaResponse)
async def get_integration_status():
    """Get current status of the Seeya integration"""
    try:
        analytics = seeya_integration.get_analytics()
        
        status_data = {
            "integration_active": True,
            "database_healthy": "error" not in analytics,
            "total_messages_processed": analytics.get("total_messages", 0),
            "total_actions_executed": analytics.get("total_actions", 0),
            "success_rate": analytics.get("success_rate", 0),
            "last_activity": datetime.now().isoformat(),
            "supported_platforms": [
                "whatsapp", "email", "slack", "teams", 
                "instagram", "telegram", "sms"
            ],
            "available_actions": [
                "inventory_check", "restock", "order_tracking", 
                "delivery", "procurement", "crm_task"
            ]
        }
        
        return SeeyaResponse(
            success=True,
            message="Integration status retrieved successfully",
            data=status_data
        )
    
    except Exception as e:
        logger.error(f"Error getting integration status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve integration status: {str(e)}"
        )

# Webhook endpoint for external integrations
@seeya_router.post("/webhook/message", response_model=SeeyaResponse)
async def webhook_message_handler(
    request: SeeyaMessageRequest,
    background_tasks: BackgroundTasks
):
    """
    Webhook endpoint for external systems to send messages to the integration
    Processes messages asynchronously in the background
    """
    try:
        logger.info(f"Webhook message received from {request.platform} for user {request.user_id}")
        
        # Add to background processing
        background_tasks.add_task(
            process_webhook_message,
            request.dict()
        )
        
        return SeeyaResponse(
            success=True,
            message="Message received and queued for processing",
            data={
                "message_id": request.message_id,
                "user_id": request.user_id,
                "platform": request.platform,
                "queued_at": datetime.now().isoformat()
            }
        )
    
    except Exception as e:
        logger.error(f"Error handling webhook message: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Webhook processing failed: {str(e)}"
        )

async def process_webhook_message(message_data: Dict[str, Any]):
    """Background task to process webhook messages"""
    try:
        logger.info(f"Processing webhook message for user {message_data.get('user_id')}")
        
        # Process through integration pipeline
        result = await seeya_integration.process_message(message_data)
        
        if result.get("success"):
            logger.info(f"Webhook message processed successfully: {result.get('message_id')}")
        else:
            logger.error(f"Webhook message processing failed: {result.get('error')}")
    
    except Exception as e:
        logger.error(f"Error in webhook background processing: {e}")

# Export the router for inclusion in main FastAPI app
__all__ = ["seeya_router"]