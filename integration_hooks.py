#!/usr/bin/env python3
"""
Integration Hooks Module
Provides hooks for Compliance, Karma Tracker, and Communication Layer integrations
"""

import requests
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ComplianceHook:
    """Integration hook for Sankalp's Compliance system"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url

    async def validate_action(self, action_type: str, parameters: Dict[str, Any], 
                            user_id: str) -> Dict[str, Any]:
        """Validate action against compliance rules"""
        try:
            response = requests.post(f"{self.base_url}/compliance/validate", json={
                "action_type": action_type,
                "parameters": parameters,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat()
            }, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"approved": True, "message": "Compliance service unavailable"}
        except Exception as e:
            logger.warning(f"Compliance validation failed: {e}")
            return {"approved": True, "message": "Compliance check bypassed"}

class KarmaTrackerHook:
    """Integration hook for Siddhesh's Karma Tracker system"""
    
    def __init__(self, base_url: str = "http://localhost:8002"):
        self.base_url = base_url

    async def track_action(self, user_id: str, action: str, result: str, 
                          metadata: Dict[str, Any] = None) -> bool:
        """Track user action in karma system"""
        try:
            response = requests.post(f"{self.base_url}/karma/track_action", json={
                "user_id": user_id,
                "action": action,
                "result": result,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat()
            }, timeout=5)
            
            return response.status_code in [200, 201]
        except Exception as e:
            logger.warning(f"Karma tracking failed: {e}")
            return False

class CommunicationHook:
    """Integration hook for Parth's Communication Layer"""
    
    def __init__(self, base_url: str = "http://localhost:8003"):
        self.base_url = base_url

    async def send_notification(self, recipient: str, notification_type: str, 
                              message: str, metadata: Dict[str, Any] = None) -> bool:
        """Send notification through communication layer"""
        try:
            response = requests.post(f"{self.base_url}/communication/send_notification", json={
                "recipient": recipient,
                "type": notification_type,
                "message": message,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat()
            }, timeout=5)
            
            return response.status_code in [200, 201]
        except Exception as e:
            logger.warning(f"Communication failed: {e}")
            return False

class IntegrationOrchestrator:
    """Orchestrates all integration hooks"""
    
    def __init__(self):
        self.compliance = ComplianceHook()
        self.karma_tracker = KarmaTrackerHook()
        self.communication = CommunicationHook()

    async def execute_with_hooks(self, action_type: str, parameters: Dict[str, Any], 
                                user_id: str) -> Dict[str, Any]:
        """Execute action with all integration hooks"""
        
        # 1. Compliance validation
        compliance_result = await self.compliance.validate_action(action_type, parameters, user_id)
        
        if not compliance_result.get("approved", True):
            return {
                "success": False,
                "error": "Action blocked by compliance",
                "details": compliance_result
            }
        
        # 2. Execute main action (placeholder)
        action_result = {"success": True, "action_id": f"action_{datetime.now().strftime('%Y%m%d_%H%M%S')}"}
        
        # 3. Track in karma system
        karma_tracked = await self.karma_tracker.track_action(
            user_id, action_type, "success" if action_result["success"] else "failure"
        )
        
        # 4. Send notification
        notification_sent = await self.communication.send_notification(
            f"{user_id}@company.com",
            f"{action_type}_completed",
            f"Action {action_type} completed successfully"
        )
        
        return {
            "success": action_result["success"],
            "action_id": action_result.get("action_id"),
            "compliance_approved": compliance_result.get("approved", True),
            "karma_tracked": karma_tracked,
            "notification_sent": notification_sent
        }

# Global orchestrator instance
integration_orchestrator = IntegrationOrchestrator()