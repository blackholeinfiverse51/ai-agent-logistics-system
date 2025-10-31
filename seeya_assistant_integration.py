#!/usr/bin/env python3
"""
Seeya Assistant Integration Module
Integrates Seeya's Assistant Live Demo with Rishabh's AI Agent Logistics System
Creates a unified experience pipeline for message processing, task creation, and logistics automation
"""

import asyncio
import json
import logging
import os
import sqlite3
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
from dataclasses import dataclass, asdict
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AssistantMessage:
    """Message structure from Seeya's Assistant"""
    user_id: str
    platform: str
    message_text: str
    timestamp: str
    message_id: Optional[str] = None
    conversation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class AssistantSummary:
    """Summary structure from Seeya's Assistant"""
    summary_id: str
    message_id: str
    summary: str
    type: str
    intent: str
    urgency: str
    confidence: float
    reasoning: List[str]
    timestamp: str

@dataclass
class AssistantTask:
    """Task structure from Seeya's Assistant"""
    task_id: str
    user_id: str
    task_summary: str
    task_type: str
    scheduled_for: Optional[str]
    status: str
    priority: str
    recommendations: List[str]

@dataclass
class LogisticsAction:
    """Logistics action triggered by assistant tasks"""
    action_id: str
    task_id: str
    action_type: str  # restock, procurement, delivery, inventory_check
    parameters: Dict[str, Any]
    status: str
    created_at: str
    executed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

class SeeyaAssistantIntegration:
    """Main integration class connecting Seeya's Assistant with Logistics System"""
    
    def __init__(self, assistant_api_url: str = "http://127.0.0.1:8000", 
                 logistics_api_url: str = "http://127.0.0.1:8000"):
        self.assistant_api_url = assistant_api_url
        self.logistics_api_url = logistics_api_url
        self.db_path = "seeya_integration.db"
        self.init_database()
        
        # Integration mappings
        self.intent_to_logistics_mapping = {
            "inventory_check": "inventory_query",
            "restock_request": "restock_agent",
            "order_status": "order_tracking",
            "delivery_update": "delivery_agent",
            "supplier_inquiry": "supplier_management",
            "procurement": "procurement_agent",
            "schedule_meeting": "crm_activity",
            "follow_up": "crm_follow_up"
        }
        
        self.urgency_to_priority_mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }
    
    def init_database(self):
        """Initialize integration database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Integration tracking table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS integration_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id TEXT UNIQUE,
                    user_id TEXT,
                    platform TEXT,
                    message_text TEXT,
                    summary_id TEXT,
                    task_id TEXT,
                    logistics_actions TEXT,
                    status TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            
            # Logistics actions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logistics_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_id TEXT UNIQUE,
                    task_id TEXT,
                    action_type TEXT,
                    parameters TEXT,
                    status TEXT,
                    created_at TEXT,
                    executed_at TEXT,
                    result TEXT
                )
            """)
            
            # User preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    user_id TEXT PRIMARY KEY,
                    auto_execute_logistics BOOLEAN DEFAULT 1,
                    notification_preferences TEXT,
                    department TEXT,
                    role TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("Integration database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    async def process_message_pipeline(self, message: AssistantMessage) -> Dict[str, Any]:
        """
        Complete pipeline: Message -> Summary -> Task -> Logistics Actions
        """
        try:
            logger.info(f"Processing message pipeline for user {message.user_id}")
            
            # Step 1: Send to Seeya's Assistant for summarization
            summary = await self.call_assistant_summarize(message)
            if not summary:
                return {"success": False, "error": "Summarization failed"}
            
            # Step 2: Create task from summary
            task = await self.call_assistant_process_summary(summary)
            if not task:
                return {"success": False, "error": "Task creation failed"}
            
            # Step 3: Determine logistics actions
            logistics_actions = await self.determine_logistics_actions(task, message)
            
            # Step 4: Execute logistics actions if auto-execute is enabled
            executed_actions = []
            user_prefs = self.get_user_preferences(message.user_id)
            
            if user_prefs.get("auto_execute_logistics", True):
                for action in logistics_actions:
                    result = await self.execute_logistics_action(action)
                    executed_actions.append(result)
            
            # Step 5: Store integration record
            integration_record = {
                "message_id": message.message_id or str(uuid.uuid4()),
                "user_id": message.user_id,
                "platform": message.platform,
                "message_text": message.message_text,
                "summary_id": summary.summary_id,
                "task_id": task.task_id,
                "logistics_actions": json.dumps([asdict(action) for action in logistics_actions]),
                "status": "completed",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            self.store_integration_record(integration_record)
            
            return {
                "success": True,
                "message_id": integration_record["message_id"],
                "summary": asdict(summary),
                "task": asdict(task),
                "logistics_actions": [asdict(action) for action in logistics_actions],
                "executed_actions": executed_actions,
                "pipeline_summary": {
                    "total_actions": len(logistics_actions),
                    "executed_actions": len(executed_actions),
                    "auto_executed": user_prefs.get("auto_execute_logistics", True)
                }
            }
            
        except Exception as e:
            logger.error(f"Pipeline processing failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def call_assistant_summarize(self, message: AssistantMessage) -> Optional[AssistantSummary]:
        """Call Seeya's Assistant API for message summarization"""
        try:
            url = f"{self.assistant_api_url}/summarize"
            payload = {
                "user_id": message.user_id,
                "platform": message.platform,
                "message_text": message.message_text,
                "timestamp": message.timestamp,
                "message_id": message.message_id,
                "metadata": message.metadata
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return AssistantSummary(
                    summary_id=data.get("summary_id"),
                    message_id=data.get("message_id"),
                    summary=data.get("summary"),
                    type=data.get("type"),
                    intent=data.get("intent"),
                    urgency=data.get("urgency"),
                    confidence=data.get("confidence", 0.0),
                    reasoning=data.get("reasoning", []),
                    timestamp=data.get("timestamp")
                )
            else:
                logger.error(f"Assistant summarize failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling assistant summarize: {e}")
            return None
    
    async def call_assistant_process_summary(self, summary: AssistantSummary) -> Optional[AssistantTask]:
        """Call Seeya's Assistant API for task creation"""
        try:
            url = f"{self.assistant_api_url}/process_summary"
            payload = {
                "summary_id": summary.summary_id,
                "user_id": summary.message_id.split("_")[0] if "_" in summary.message_id else "unknown",
                "platform": "logistics",
                "summary": summary.summary,
                "intent": summary.intent,
                "urgency": summary.urgency,
                "type": summary.type,
                "confidence": summary.confidence,
                "reasoning": summary.reasoning
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return AssistantTask(
                    task_id=data.get("task_id"),
                    user_id=data.get("user_id"),
                    task_summary=data.get("task_summary"),
                    task_type=data.get("task_type"),
                    scheduled_for=data.get("scheduled_for"),
                    status=data.get("status", "pending"),
                    priority=data.get("priority", "medium"),
                    recommendations=data.get("recommendations", [])
                )
            else:
                logger.error(f"Assistant process_summary failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling assistant process_summary: {e}")
            return None
    
    async def determine_logistics_actions(self, task: AssistantTask, message: AssistantMessage) -> List[LogisticsAction]:
        """Determine what logistics actions to take based on the task"""
        actions = []
        
        try:
            # Map intent to logistics actions
            intent = task.task_type.lower()
            
            if "inventory" in intent or "stock" in task.task_summary.lower():
                actions.append(LogisticsAction(
                    action_id=str(uuid.uuid4()),
                    task_id=task.task_id,
                    action_type="inventory_check",
                    parameters={
                        "query_type": "stock_levels",
                        "urgency": task.priority,
                        "user_request": task.task_summary
                    },
                    status="pending",
                    created_at=datetime.now().isoformat()
                ))
            
            if "restock" in task.task_summary.lower() or "low stock" in task.task_summary.lower():
                actions.append(LogisticsAction(
                    action_id=str(uuid.uuid4()),
                    task_id=task.task_id,
                    action_type="restock",
                    parameters={
                        "trigger_reason": task.task_summary,
                        "priority": self.urgency_to_priority_mapping.get(task.priority, 2),
                        "auto_approve": task.priority in ["high", "critical"]
                    },
                    status="pending",
                    created_at=datetime.now().isoformat()
                ))
            
            if "order" in task.task_summary.lower() and "status" in task.task_summary.lower():
                actions.append(LogisticsAction(
                    action_id=str(uuid.uuid4()),
                    task_id=task.task_id,
                    action_type="order_tracking",
                    parameters={
                        "query_type": "status_check",
                        "user_id": task.user_id,
                        "platform": message.platform
                    },
                    status="pending",
                    created_at=datetime.now().isoformat()
                ))
            
            if "delivery" in task.task_summary.lower() or "shipment" in task.task_summary.lower():
                actions.append(LogisticsAction(
                    action_id=str(uuid.uuid4()),
                    task_id=task.task_id,
                    action_type="delivery",
                    parameters={
                        "action": "track_delivery",
                        "user_query": task.task_summary,
                        "priority": task.priority
                    },
                    status="pending",
                    created_at=datetime.now().isoformat()
                ))
            
            if "supplier" in task.task_summary.lower() or "procurement" in task.task_summary.lower():
                actions.append(LogisticsAction(
                    action_id=str(uuid.uuid4()),
                    task_id=task.task_id,
                    action_type="procurement",
                    parameters={
                        "request_type": "supplier_inquiry",
                        "details": task.task_summary,
                        "urgency": task.priority
                    },
                    status="pending",
                    created_at=datetime.now().isoformat()
                ))
            
            # If no specific logistics actions, create a general CRM task
            if not actions:
                actions.append(LogisticsAction(
                    action_id=str(uuid.uuid4()),
                    task_id=task.task_id,
                    action_type="crm_task",
                    parameters={
                        "task_type": task.task_type,
                        "summary": task.task_summary,
                        "scheduled_for": task.scheduled_for,
                        "recommendations": task.recommendations
                    },
                    status="pending",
                    created_at=datetime.now().isoformat()
                ))
            
            return actions
            
        except Exception as e:
            logger.error(f"Error determining logistics actions: {e}")
            return []
    
    async def execute_logistics_action(self, action: LogisticsAction) -> Dict[str, Any]:
        """Execute a logistics action using the existing logistics system"""
        try:
            result = {"action_id": action.action_id, "success": False, "executed_at": datetime.now().isoformat()}
            
            if action.action_type == "inventory_check":
                # Call inventory API
                response = requests.get(f"{self.logistics_api_url}/inventory", timeout=30)
                if response.status_code == 200:
                    inventory_data = response.json()
                    result.update({
                        "success": True,
                        "data": inventory_data,
                        "message": "Inventory check completed"
                    })
            
            elif action.action_type == "restock":
                # Trigger restock agent
                payload = {
                    "trigger_reason": action.parameters.get("trigger_reason"),
                    "priority": action.parameters.get("priority", 2),
                    "auto_approve": action.parameters.get("auto_approve", False)
                }
                response = requests.post(f"{self.logistics_api_url}/agents/restock", json=payload, timeout=30)
                if response.status_code == 200:
                    result.update({
                        "success": True,
                        "data": response.json(),
                        "message": "Restock agent executed"
                    })
            
            elif action.action_type == "order_tracking":
                # Query order status
                response = requests.get(f"{self.logistics_api_url}/orders", timeout=30)
                if response.status_code == 200:
                    orders_data = response.json()
                    result.update({
                        "success": True,
                        "data": orders_data,
                        "message": "Order tracking completed"
                    })
            
            elif action.action_type == "delivery":
                # Trigger delivery agent
                response = requests.post(f"{self.logistics_api_url}/agents/delivery", json=action.parameters, timeout=30)
                if response.status_code == 200:
                    result.update({
                        "success": True,
                        "data": response.json(),
                        "message": "Delivery agent executed"
                    })
            
            elif action.action_type == "procurement":
                # Trigger procurement agent
                response = requests.post(f"{self.logistics_api_url}/agents/procurement", json=action.parameters, timeout=30)
                if response.status_code == 200:
                    result.update({
                        "success": True,
                        "data": response.json(),
                        "message": "Procurement agent executed"
                    })
            
            elif action.action_type == "crm_task":
                # Create CRM task
                payload = {
                    "task_type": action.parameters.get("task_type"),
                    "summary": action.parameters.get("summary"),
                    "scheduled_for": action.parameters.get("scheduled_for"),
                    "status": "pending"
                }
                response = requests.post(f"{self.logistics_api_url}/crm/tasks", json=payload, timeout=30)
                if response.status_code == 200:
                    result.update({
                        "success": True,
                        "data": response.json(),
                        "message": "CRM task created"
                    })
            
            # Update action in database
            action.status = "completed" if result["success"] else "failed"
            action.executed_at = result["executed_at"]
            action.result = result
            self.store_logistics_action(action)
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing logistics action {action.action_id}: {e}")
            action.status = "failed"
            action.executed_at = datetime.now().isoformat()
            action.result = {"success": False, "error": str(e)}
            self.store_logistics_action(action)
            return {"action_id": action.action_id, "success": False, "error": str(e)}
    
    def store_integration_record(self, record: Dict[str, Any]):
        """Store integration record in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO integration_messages 
                (message_id, user_id, platform, message_text, summary_id, task_id, 
                 logistics_actions, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record["message_id"], record["user_id"], record["platform"],
                record["message_text"], record["summary_id"], record["task_id"],
                record["logistics_actions"], record["status"],
                record["created_at"], record["updated_at"]
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing integration record: {e}")
    
    def store_logistics_action(self, action: LogisticsAction):
        """Store logistics action in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO logistics_actions 
                (action_id, task_id, action_type, parameters, status, created_at, executed_at, result)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                action.action_id, action.task_id, action.action_type,
                json.dumps(action.parameters), action.status,
                action.created_at, action.executed_at,
                json.dumps(action.result) if action.result else None
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing logistics action: {e}")
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM user_preferences WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    "user_id": row[0],
                    "auto_execute_logistics": bool(row[1]),
                    "notification_preferences": json.loads(row[2]) if row[2] else {},
                    "department": row[3],
                    "role": row[4]
                }
            else:
                # Create default preferences
                default_prefs = {
                    "user_id": user_id,
                    "auto_execute_logistics": True,
                    "notification_preferences": {"email": True, "slack": False},
                    "department": "general",
                    "role": "user"
                }
                self.set_user_preferences(user_id, default_prefs)
                return default_prefs
                
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return {"auto_execute_logistics": True}
    
    def set_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Set user preferences in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO user_preferences 
                (user_id, auto_execute_logistics, notification_preferences, department, role, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                preferences.get("auto_execute_logistics", True),
                json.dumps(preferences.get("notification_preferences", {})),
                preferences.get("department", "general"),
                preferences.get("role", "user"),
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error setting user preferences: {e}")
    
    def get_integration_analytics(self) -> Dict[str, Any]:
        """Get analytics for the integration"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get integration statistics
            integration_df = pd.read_sql_query("""
                SELECT platform, status, COUNT(*) as count,
                       DATE(created_at) as date
                FROM integration_messages 
                WHERE created_at >= datetime('now', '-7 days')
                GROUP BY platform, status, DATE(created_at)
            """, conn)
            
            # Get logistics actions statistics
            actions_df = pd.read_sql_query("""
                SELECT action_type, status, COUNT(*) as count
                FROM logistics_actions 
                WHERE created_at >= datetime('now', '-7 days')
                GROUP BY action_type, status
            """, conn)
            
            conn.close()
            
            return {
                "integration_stats": integration_df.to_dict('records') if not integration_df.empty else [],
                "actions_stats": actions_df.to_dict('records') if not actions_df.empty else [],
                "total_messages": len(integration_df),
                "total_actions": len(actions_df),
                "success_rate": len(actions_df[actions_df['status'] == 'completed']) / len(actions_df) if len(actions_df) > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error getting integration analytics: {e}")
            return {"error": str(e)}

# Integration API wrapper
class SeeyaIntegrationAPI:
    """FastAPI wrapper for the integration"""
    
    def __init__(self):
        self.integration = SeeyaAssistantIntegration()
    
    async def process_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a message through the integration pipeline"""
        message = AssistantMessage(
            user_id=message_data.get("user_id"),
            platform=message_data.get("platform"),
            message_text=message_data.get("message_text"),
            timestamp=message_data.get("timestamp", datetime.now().isoformat()),
            message_id=message_data.get("message_id"),
            conversation_id=message_data.get("conversation_id"),
            metadata=message_data.get("metadata")
        )
        
        return await self.integration.process_message_pipeline(message)
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get integration analytics"""
        return self.integration.get_integration_analytics()
    
    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences"""
        return self.integration.get_user_preferences(user_id)
    
    def set_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Set user preferences"""
        self.integration.set_user_preferences(user_id, preferences)
        return {"success": True, "message": "Preferences updated"}

# Initialize global integration instance
seeya_integration = SeeyaIntegrationAPI()

if __name__ == "__main__":
    # Test the integration
    async def test_integration():
        test_message = {
            "user_id": "test_user",
            "platform": "whatsapp",
            "message_text": "Check inventory levels for wireless mouse, we might need to restock",
            "timestamp": datetime.now().isoformat()
        }
        
        result = await seeya_integration.process_message(test_message)
        print("Integration Test Result:")
        print(json.dumps(result, indent=2))
    
    asyncio.run(test_integration())