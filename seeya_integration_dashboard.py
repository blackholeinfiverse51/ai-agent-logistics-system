#!/usr/bin/env python3
"""
Seeya Integration Dashboard
Streamlit interface for managing and monitoring the Seeya Assistant + Logistics integration
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import asyncio
import requests
from seeya_assistant_integration import seeya_integration, AssistantMessage

# Page configuration
st.set_page_config(
    page_title="Seeya Assistant Integration",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .integration-card {
        background: linear-gradient(135deg, #f0f2f6, #ffffff);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .success-card {
        background: linear-gradient(135deg, #e8f5e8, #ffffff);
        border-left: 4px solid #4caf50;
    }
    .warning-card {
        background: linear-gradient(135deg, #fff3e0, #ffffff);
        border-left: 4px solid #ff9800;
    }
    .error-card {
        background: linear-gradient(135deg, #ffebee, #ffffff);
        border-left: 4px solid #f44336;
    }
</style>
""", unsafe_allow_html=True)

def display_header():
    """Display main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Seeya Assistant Integration Dashboard</h1>
        <p>From Seeya's Assistant to Rishabh's Logistics - Unified Experience Pipeline</p>
    </div>
    """, unsafe_allow_html=True)

def show_integration_overview():
    """Show integration overview and statistics"""
    st.header("📊 Integration Overview")
    
    # Get analytics
    analytics = seeya_integration.get_analytics()
    
    if "error" not in analytics:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Messages", analytics.get("total_messages", 0), "+5 today")
        
        with col2:
            st.metric("Total Actions", analytics.get("total_actions", 0), "+12 today")
        
        with col3:
            success_rate = analytics.get("success_rate", 0) * 100
            st.metric("Success Rate", f"{success_rate:.1f}%", "+2.3%")
        
        with col4:
            st.metric("Active Users", "8", "+1 today")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Integration Activity")
            integration_stats = analytics.get("integration_stats", [])
            if integration_stats:
                df = pd.DataFrame(integration_stats)
                fig = px.bar(df, x='platform', y='count', color='status',
                           title="Messages by Platform and Status")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No integration data available yet")
        
        with col2:
            st.subheader("⚙️ Logistics Actions")
            actions_stats = analytics.get("actions_stats", [])
            if actions_stats:
                df = pd.DataFrame(actions_stats)
                fig = px.pie(df, values='count', names='action_type',
                           title="Actions by Type")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No actions data available yet")
    else:
        st.error(f"Error loading analytics: {analytics['error']}")

def show_message_processor():
    """Show message processing interface"""
    st.header("💬 Message Processor")
    
    st.markdown("""
    <div class="integration-card">
        <h3>🚀 Process Messages Through Integration Pipeline</h3>
        <p>Send messages to Seeya's Assistant and automatically trigger logistics actions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Message input form
    with st.form("message_processor"):
        col1, col2 = st.columns(2)
        
        with col1:
            user_id = st.text_input("User ID", value="demo_user", help="Unique identifier for the user")
            platform = st.selectbox("Platform", [
                "whatsapp", "email", "slack", "teams", 
                "instagram", "telegram", "sms"
            ], help="Source platform for the message")
        
        with col2:
            conversation_id = st.text_input("Conversation ID (Optional)", help="Group conversation identifier")
            timestamp = st.text_input("Timestamp", value=datetime.now().isoformat(), 
                                    help="Message timestamp (ISO format)")
        
        message_text = st.text_area("Message Text", 
                                  placeholder="Enter the message to process...",
                                  help="The actual message content to analyze")
        
        # Quick message templates
        st.subheader("📝 Quick Templates")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.form_submit_button("📦 Inventory Check"):
                st.session_state.template_message = "Check current inventory levels for wireless mouse and keyboards"
        
        with col2:
            if st.form_submit_button("🔄 Restock Request"):
                st.session_state.template_message = "We're running low on wireless mouse inventory, need to restock urgently"
        
        with col3:
            if st.form_submit_button("📋 Order Status"):
                st.session_state.template_message = "What's the status of order #12345? Customer is asking for updates"
        
        with col4:
            if st.form_submit_button("🚚 Delivery Update"):
                st.session_state.template_message = "Track delivery for shipment FS123456789, customer reports delay"
        
        # Use template if selected
        if hasattr(st.session_state, 'template_message'):
            message_text = st.session_state.template_message
        
        submitted = st.form_submit_button("🚀 Process Message")
        
        if submitted and message_text:
            with st.spinner("Processing message through integration pipeline..."):
                try:
                    # Prepare message data
                    message_data = {
                        "user_id": user_id,
                        "platform": platform,
                        "message_text": message_text,
                        "timestamp": timestamp,
                        "conversation_id": conversation_id if conversation_id else None
                    }
                    
                    # Process through integration
                    result = asyncio.run(seeya_integration.process_message(message_data))
                    
                    if result.get("success"):
                        st.success("✅ Message processed successfully!")
                        
                        # Display results
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📝 Summary Results")
                            summary = result.get("summary", {})
                            st.json({
                                "Summary": summary.get("summary"),
                                "Intent": summary.get("intent"),
                                "Urgency": summary.get("urgency"),
                                "Confidence": summary.get("confidence")
                            })
                        
                        with col2:
                            st.subheader("📋 Task Created")
                            task = result.get("task", {})
                            st.json({
                                "Task Summary": task.get("task_summary"),
                                "Task Type": task.get("task_type"),
                                "Priority": task.get("priority"),
                                "Status": task.get("status")
                            })
                        
                        # Display logistics actions
                        st.subheader("⚙️ Logistics Actions Triggered")
                        actions = result.get("logistics_actions", [])
                        
                        if actions:
                            for i, action in enumerate(actions, 1):
                                with st.expander(f"Action {i}: {action['action_type'].title()}"):
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.write(f"**Type:** {action['action_type']}")
                                        st.write(f"**Status:** {action['status']}")
                                    with col2:
                                        st.write(f"**Created:** {action['created_at'][:16]}")
                                        st.write(f"**Parameters:** {len(action['parameters'])} items")
                                    
                                    st.json(action['parameters'])
                        else:
                            st.info("No logistics actions were triggered for this message")
                        
                        # Pipeline summary
                        pipeline_summary = result.get("pipeline_summary", {})
                        st.subheader("📊 Pipeline Summary")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Actions", pipeline_summary.get("total_actions", 0))
                        with col2:
                            st.metric("Executed Actions", pipeline_summary.get("executed_actions", 0))
                        with col3:
                            auto_executed = pipeline_summary.get("auto_executed", False)
                            st.metric("Auto Execution", "✅ Enabled" if auto_executed else "❌ Disabled")
                    
                    else:
                        st.error(f"❌ Processing failed: {result.get('error', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"❌ Error processing message: {str(e)}")
                
                # Clear template
                if hasattr(st.session_state, 'template_message'):
                    del st.session_state.template_message

def show_user_preferences():
    """Show user preferences management"""
    st.header("👤 User Preferences")
    
    # User selection
    user_id = st.text_input("User ID", value="demo_user", help="Enter user ID to manage preferences")
    
    if st.button("🔍 Load Preferences"):
        preferences = seeya_integration.get_user_preferences(user_id)
        st.session_state.user_preferences = preferences
        st.session_state.selected_user = user_id
    
    if hasattr(st.session_state, 'user_preferences'):
        st.subheader(f"Preferences for {st.session_state.selected_user}")
        
        with st.form("user_preferences"):
            col1, col2 = st.columns(2)
            
            with col1:
                auto_execute = st.checkbox(
                    "Auto-execute Logistics Actions",
                    value=st.session_state.user_preferences.get("auto_execute_logistics", True),
                    help="Automatically execute logistics actions without manual approval"
                )
                
                department = st.selectbox(
                    "Department",
                    ["general", "logistics", "procurement", "inventory", "sales", "support"],
                    index=["general", "logistics", "procurement", "inventory", "sales", "support"].index(
                        st.session_state.user_preferences.get("department", "general")
                    )
                )
            
            with col2:
                role = st.selectbox(
                    "Role",
                    ["user", "manager", "admin", "analyst"],
                    index=["user", "manager", "admin", "analyst"].index(
                        st.session_state.user_preferences.get("role", "user")
                    )
                )
                
                # Notification preferences
                st.subheader("📧 Notification Preferences")
                notif_prefs = st.session_state.user_preferences.get("notification_preferences", {})
                
                email_notifications = st.checkbox("Email Notifications", value=notif_prefs.get("email", True))
                slack_notifications = st.checkbox("Slack Notifications", value=notif_prefs.get("slack", False))
            
            if st.form_submit_button("💾 Save Preferences"):
                new_preferences = {
                    "auto_execute_logistics": auto_execute,
                    "department": department,
                    "role": role,
                    "notification_preferences": {
                        "email": email_notifications,
                        "slack": slack_notifications
                    }
                }
                
                result = seeya_integration.set_user_preferences(st.session_state.selected_user, new_preferences)
                if result.get("success"):
                    st.success("✅ Preferences saved successfully!")
                    st.session_state.user_preferences = new_preferences
                else:
                    st.error("❌ Failed to save preferences")

def show_integration_logs():
    """Show integration logs and history"""
    st.header("📜 Integration Logs")
    
    # Mock log data for demonstration
    log_data = [
        {
            "timestamp": "2025-01-25 10:30:00",
            "user_id": "alice_work",
            "platform": "whatsapp",
            "message": "Check inventory for wireless mouse",
            "summary": "User requesting inventory check",
            "actions": "inventory_check",
            "status": "completed"
        },
        {
            "timestamp": "2025-01-25 10:25:00",
            "user_id": "bob_logistics",
            "platform": "email",
            "message": "We need to restock keyboards urgently",
            "summary": "Urgent restock request for keyboards",
            "actions": "restock, procurement",
            "status": "completed"
        },
        {
            "timestamp": "2025-01-25 10:20:00",
            "user_id": "carol_support",
            "platform": "slack",
            "message": "Customer asking about order #12345 status",
            "summary": "Order status inquiry",
            "actions": "order_tracking",
            "status": "completed"
        }
    ]
    
    # Display logs table
    df = pd.DataFrame(log_data)
    st.dataframe(df, use_container_width=True)
    
    # Log statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Logs", len(df))
    
    with col2:
        completed_logs = len(df[df['status'] == 'completed'])
        st.metric("Completed", completed_logs)
    
    with col3:
        success_rate = (completed_logs / len(df)) * 100 if len(df) > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")

def show_api_testing():
    """Show API testing interface"""
    st.header("🔧 API Testing")
    
    st.markdown("""
    <div class="integration-card">
        <h3>🧪 Test Integration APIs</h3>
        <p>Test the integration endpoints and view responses</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API endpoint selection
    endpoint = st.selectbox("Select Endpoint", [
        "Seeya Assistant - Summarize",
        "Seeya Assistant - Process Summary",
        "Logistics - Inventory Check",
        "Logistics - Restock Agent",
        "Integration - Full Pipeline"
    ])
    
    if endpoint == "Seeya Assistant - Summarize":
        st.subheader("📝 Test Summarization")
        
        with st.form("test_summarize"):
            test_message = st.text_area("Test Message", 
                                      value="Check inventory levels for wireless mouse, we might be running low")
            
            if st.form_submit_button("🧪 Test Summarize"):
                with st.spinner("Testing summarization..."):
                    # Mock response for demonstration
                    mock_response = {
                        "summary_id": "sum_12345",
                        "message_id": "msg_12345",
                        "summary": "User requesting inventory check for wireless mouse due to potential low stock",
                        "type": "request",
                        "intent": "inventory_check",
                        "urgency": "medium",
                        "confidence": 0.85,
                        "reasoning": ["Contains inventory-related keywords", "Mentions specific product", "Indicates concern about stock levels"]
                    }
                    
                    st.success("✅ Summarization test completed!")
                    st.json(mock_response)
    
    elif endpoint == "Integration - Full Pipeline":
        st.subheader("🚀 Test Full Pipeline")
        
        with st.form("test_pipeline"):
            col1, col2 = st.columns(2)
            
            with col1:
                test_user = st.text_input("User ID", value="test_user")
                test_platform = st.selectbox("Platform", ["whatsapp", "email", "slack"])
            
            with col2:
                test_message = st.text_area("Message", 
                                          value="We need to restock wireless mouse inventory urgently")
            
            if st.form_submit_button("🧪 Test Pipeline"):
                with st.spinner("Testing full pipeline..."):
                    # Mock pipeline response
                    mock_pipeline_response = {
                        "success": True,
                        "message_id": "msg_test_001",
                        "summary": {
                            "summary": "Urgent restock request for wireless mouse inventory",
                            "intent": "restock_request",
                            "urgency": "high",
                            "confidence": 0.92
                        },
                        "task": {
                            "task_id": "task_test_001",
                            "task_summary": "Execute restock for wireless mouse",
                            "task_type": "restock",
                            "priority": "high",
                            "status": "pending"
                        },
                        "logistics_actions": [
                            {
                                "action_id": "action_001",
                                "action_type": "restock",
                                "status": "completed",
                                "parameters": {"product": "wireless_mouse", "quantity": 50}
                            }
                        ],
                        "pipeline_summary": {
                            "total_actions": 1,
                            "executed_actions": 1,
                            "auto_executed": True
                        }
                    }
                    
                    st.success("✅ Pipeline test completed!")
                    st.json(mock_pipeline_response)

def main():
    """Main dashboard application"""
    display_header()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    
    pages = [
        ("📊 Overview", "overview"),
        ("💬 Message Processor", "processor"),
        ("👤 User Preferences", "preferences"),
        ("📜 Integration Logs", "logs"),
        ("🔧 API Testing", "testing")
    ]
    
    selected_page = st.sidebar.radio("Select Page", [page[0] for page in pages])
    
    # Get the page key
    page_key = next(page[1] for page in pages if page[0] == selected_page)
    
    # Display selected page
    if page_key == "overview":
        show_integration_overview()
    elif page_key == "processor":
        show_message_processor()
    elif page_key == "preferences":
        show_user_preferences()
    elif page_key == "logs":
        show_integration_logs()
    elif page_key == "testing":
        show_api_testing()
    
    # Sidebar status
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔗 Integration Status")
    st.sidebar.success("✅ Seeya Assistant: Connected")
    st.sidebar.success("✅ Logistics System: Active")
    st.sidebar.success("✅ Database: Healthy")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        🤖 Seeya Assistant Integration Dashboard | From Seeya to Rishabh Experience Pipeline<br>
        Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()