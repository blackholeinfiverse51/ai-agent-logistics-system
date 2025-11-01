#!/usr/bin/env python3
"""
API Response Standardization Module
Ensures consistent JSON shapes across all endpoints for OpenAPI compliance
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum

class ResponseStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"

class StandardResponse(BaseModel):
    """Standardized response format for all API endpoints"""
    status: ResponseStatus
    message: str
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    request_id: Optional[str] = None

class PaginatedResponse(BaseModel):
    """Standardized paginated response format"""
    status: ResponseStatus
    message: str
    data: List[Dict[str, Any]]
    pagination: Dict[str, Any] = Field(default_factory=lambda: {
        "page": 1,
        "per_page": 50,
        "total": 0,
        "pages": 1
    })
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class DataFeedResponse(BaseModel):
    """Standardized data feed for Nikhil's UI integration"""
    feed_type: str
    version: str = "1.0"
    data: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    last_updated: str = Field(default_factory=lambda: datetime.now().isoformat())

def standardize_response(data: Any = None, message: str = "Success", 
                        status: ResponseStatus = ResponseStatus.SUCCESS,
                        errors: List[str] = None) -> StandardResponse:
    """Create standardized API response"""
    return StandardResponse(
        status=status,
        message=message,
        data=data if isinstance(data, dict) else {"result": data} if data else None,
        errors=errors
    )

def create_ui_data_feed(feed_type: str, data: Dict[str, Any], 
                       metadata: Dict[str, Any] = None) -> DataFeedResponse:
    """Create standardized data feed for UI"""
    return DataFeedResponse(
        feed_type=feed_type,
        data=data,
        metadata=metadata or {}
    )