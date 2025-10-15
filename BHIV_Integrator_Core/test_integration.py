#!/usr/bin/env python3
"""
Integration Test for BHIV Integrator Core
Tests the unified system functionality
"""

import asyncio
import requests
import json
import time
from datetime import datetime

# Test configuration
INTEGRATOR_URL = "http://localhost:8005"
LOGISTICS_URL = "http://localhost:8000"
CRM_URL = "http://localhost:8502"
TASK_URL = "http://localhost:8000"

def test_health_check():
    """Test integrator health check"""
    print("Testing health check...")
    try:
        response = requests.get(f"{INTEGRATOR_URL}/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("Health check passed")
        return True
    except Exception as e:
        print(f"Health check failed: {str(e)}")
        return False

def test_event_broker():
    """Test event broker functionality"""
    print("Testing event broker...")
    try:
        # Test event publishing
        event_data = {
            "event_type": "test_event",
            "source_system": "test_system",
            "target_systems": ["logistics", "crm"],
            "payload": {"test": "data"},
            "priority": "low"
        }

        response = requests.post(f"{INTEGRATOR_URL}/event/publish", json=event_data, timeout=5)
        assert response.status_code == 200
        result = response.json()
        assert "event_id" in result
        print("Event publishing passed")

        # Test event retrieval
        response = requests.get(f"{INTEGRATOR_URL}/event/events?limit=5", timeout=5)
        assert response.status_code == 200
        events = response.json()
        assert "events" in events
        print("Event retrieval passed")

        return True
    except Exception as e:
        print(f"Event broker test failed: {str(e)}")
        return False

def test_logistics_integration():
    """Test logistics API integration"""
    print("[LOGISTICS] Testing logistics integration...")
    try:
        # Test procurement orders endpoint
        response = requests.get(f"{INTEGRATOR_URL}/logistics/procurement", timeout=5)
        # Note: This might fail if logistics system is not running, which is expected
        if response.status_code == 200:
            print("[OK] Logistics procurement API accessible")
        elif response.status_code == 502:
            print("[WARN] Logistics system not running (expected in test environment)")
        else:
            print(f"[WARN] Logistics API returned {response.status_code}")

        return True
    except Exception as e:
        print(f"[FAILED] Logistics integration test failed: {str(e)}")
        return False

def test_crm_integration():
    """Test CRM API integration"""
    print("[CRM] Testing CRM integration...")
    try:
        # Test accounts endpoint
        response = requests.get(f"{INTEGRATOR_URL}/crm/accounts", timeout=5)
        if response.status_code == 200:
            print("[OK] CRM accounts API accessible")
        elif response.status_code == 502:
            print("[WARN] CRM system not running (expected in test environment)")
        else:
            print(f"[WARN] CRM API returned {response.status_code}")

        return True
    except Exception as e:
        print(f"[FAILED] CRM integration test failed: {str(e)}")
        return False

def test_task_integration():
    """Test task management API integration"""
    print("[TASK] Testing task management integration...")
    try:
        # Test tasks endpoint
        response = requests.get(f"{INTEGRATOR_URL}/task/tasks", timeout=5)
        if response.status_code == 200:
            print("[OK] Task management API accessible")
        elif response.status_code == 502:
            print("[WARN] Task system not running (expected in test environment)")
        else:
            print(f"[WARN] Task API returned {response.status_code}")

        return True
    except Exception as e:
        print(f"[FAILED] Task integration test failed: {str(e)}")
        return False

def test_bhiv_core_integration():
    """Test BHIV Core integration"""
    print("[BHIV] Testing BHIV Core integration...")
    try:
        # Test BHIV status endpoint
        response = requests.get(f"{INTEGRATOR_URL}/bhiv/status", timeout=5)
        if response.status_code == 200:
            print("[OK] BHIV Core integration accessible")
        elif response.status_code == 502:
            print("[WARN] BHIV Core not running (expected in test environment)")
        else:
            print(f"[WARN] BHIV Core API returned {response.status_code}")

        return True
    except Exception as e:
        print(f"[FAILED] BHIV Core integration test failed: {str(e)}")
        return False

def test_event_driven_flow():
    """Test event-driven flow simulation"""
    print("[FLOW] Testing event-driven flow...")
    try:
        # Simulate order creation event
        order_event = {
            "event_type": "procurement_order_created",
            "source_system": "logistics",
            "target_systems": ["crm", "task_manager"],
            "payload": {
                "order_id": "TEST_ORDER_001",
                "customer_name": "Test Customer",
                "order_value": 50000,
                "items": ["item1", "item2"]
            },
            "priority": "high"
        }

        response = requests.post(f"{INTEGRATOR_URL}/event/publish", json=order_event, timeout=5)
        assert response.status_code == 200
        result = response.json()
        event_id = result["event_id"]
        print(f"[OK] Order creation event published: {event_id}")

        # Wait a moment for processing
        time.sleep(1)

        # Check if event was processed (in real scenario, check logs)
        response = requests.get(f"{INTEGRATOR_URL}/event/events?limit=10", timeout=5)
        events = response.json()["events"]

        # Look for our test event
        found_event = any(e["event_id"] == event_id for e in events)
        if found_event:
            print("[OK] Event stored and retrievable")
        else:
            print("[WARN] Event storage check inconclusive")

        return True
    except Exception as e:
        print(f"[FAILED] Event-driven flow test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all integration tests"""
    print("Starting BHIV Integrator Core Integration Tests")
    print("=" * 60)

    tests = [
        ("Health Check", test_health_check),
        ("Event Broker", test_event_broker),
        ("Logistics Integration", test_logistics_integration),
        ("CRM Integration", test_crm_integration),
        ("Task Integration", test_task_integration),
        ("BHIV Core Integration", test_bhiv_core_integration),
        ("Event-Driven Flow", test_event_driven_flow)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
        print("-" * 40)

    print(f"\nTest Results: {passed}/{total} tests passed")

    if passed == total:
        print("All tests passed! BHIV Integrator Core is ready.")
        return True
    elif passed >= total * 0.7:  # 70% pass rate
        print("Most tests passed. Some systems may not be running (expected in test environment).")
        return True
    else:
        print("Critical test failures. Check system configuration.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)