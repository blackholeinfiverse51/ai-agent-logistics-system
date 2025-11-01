#!/usr/bin/env python3
"""
UI Data Contracts Module
Standardized data feed contracts for Nikhil's UI integration
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class UIDataType(str, Enum):
    DASHBOARD = "dashboard"
    INVENTORY = "inventory"
    ORDERS = "orders"
    SHIPMENTS = "shipments"
    ANALYTICS = "analytics"
    NOTIFICATIONS = "notifications"

class DashboardData(BaseModel):
    """Dashboard data contract"""
    metrics: Dict[str, Any] = Field(default_factory=lambda: {
        "total_orders": 0,
        "pending_shipments": 0,
        "low_stock_items": 0,
        "active_agents": 0
    })
    charts: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict)
    alerts: List[Dict[str, Any]] = Field(default_factory=list)
    recent_activity: List[Dict[str, Any]] = Field(default_factory=list)

class InventoryData(BaseModel):
    """Inventory data contract"""
    items: List[Dict[str, Any]]
    categories: List[str]
    low_stock_threshold: int = 10
    total_items: int
    last_updated: str = Field(default_factory=lambda: datetime.now().isoformat())

class OrdersData(BaseModel):
    """Orders data contract"""
    orders: List[Dict[str, Any]]
    statuses: List[str] = ["pending", "processing", "shipped", "delivered", "cancelled"]
    total_orders: int
    filters: Dict[str, List[str]] = Field(default_factory=dict)

class ShipmentsData(BaseModel):
    """Shipments data contract"""
    shipments: List[Dict[str, Any]]
    tracking_info: Dict[str, Any] = Field(default_factory=dict)
    delivery_stats: Dict[str, Any] = Field(default_factory=dict)

class AnalyticsData(BaseModel):
    """Analytics data contract"""
    performance_metrics: Dict[str, Any]
    trends: Dict[str, List[Dict[str, Any]]]
    comparisons: Dict[str, Any]
    time_range: str

class NotificationsData(BaseModel):
    """Notifications data contract"""
    notifications: List[Dict[str, Any]]
    unread_count: int
    categories: List[str]

class UIDataProvider:
    """Provides standardized data feeds for UI"""
    
    def get_dashboard_data(self) -> DashboardData:
        """Get dashboard data feed"""
        return DashboardData(
            metrics={
                "total_orders": 156,
                "pending_shipments": 23,
                "low_stock_items": 8,
                "active_agents": 4
            },
            charts={
                "orders_trend": [
                    {"date": "2025-01-20", "orders": 12},
                    {"date": "2025-01-21", "orders": 15},
                    {"date": "2025-01-22", "orders": 18}
                ]
            },
            alerts=[
                {"type": "warning", "message": "Low stock: Wireless Mouse", "timestamp": datetime.now().isoformat()}
            ]
        )
    
    def get_inventory_data(self, filters: Dict[str, Any] = None) -> InventoryData:
        """Get inventory data feed"""
        return InventoryData(
            items=[
                {"id": "A101", "name": "Wireless Mouse", "stock": 5, "category": "Electronics"},
                {"id": "A102", "name": "Keyboard", "stock": 15, "category": "Electronics"}
            ],
            categories=["Electronics", "Office Supplies", "Accessories"],
            total_items=2
        )
    
    def get_orders_data(self, filters: Dict[str, Any] = None) -> OrdersData:
        """Get orders data feed"""
        return OrdersData(
            orders=[
                {"id": "ORD001", "customer": "John Doe", "status": "shipped", "total": 299.99},
                {"id": "ORD002", "customer": "Jane Smith", "status": "processing", "total": 149.99}
            ],
            total_orders=2,
            filters={"status": ["pending", "processing", "shipped"], "date_range": ["today", "week", "month"]}
        )
    
    def get_shipments_data(self, filters: Dict[str, Any] = None) -> ShipmentsData:
        """Get shipments data feed"""
        return ShipmentsData(
            shipments=[
                {"id": "SHP001", "tracking": "TRK123456", "status": "in_transit", "eta": "2025-01-26"}
            ],
            tracking_info={"TRK123456": {"location": "Distribution Center", "status": "in_transit"}},
            delivery_stats={"on_time": 95, "delayed": 5}
        )
    
    def get_analytics_data(self, time_range: str = "week") -> AnalyticsData:
        """Get analytics data feed"""
        return AnalyticsData(
            performance_metrics={"efficiency": 92, "accuracy": 98, "speed": 85},
            trends={"orders": [{"date": "2025-01-20", "value": 12}]},
            comparisons={"vs_last_week": 15},
            time_range=time_range
        )
    
    def get_notifications_data(self, user_id: str = None) -> NotificationsData:
        """Get notifications data feed"""
        return NotificationsData(
            notifications=[
                {"id": "NOT001", "message": "Restock completed", "type": "success", "read": False}
            ],
            unread_count=1,
            categories=["alerts", "updates", "system"]
        )

# Global UI data provider
ui_data_provider = UIDataProvider()