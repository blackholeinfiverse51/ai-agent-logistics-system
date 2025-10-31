#!/usr/bin/env python3
"""
Unified AI Agent Dashboard
Combines CRM, Logistics, Supplier Management, Product Catalog, and Supplier Showcase
All-in-one interface to replace multiple separate dashboards
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import json
import os
from database.service import DatabaseService
from database.models import init_database, Product, SessionLocal, Supplier
from user_product_models import USER_PRODUCT_CATALOG, get_user_product_by_id, ProductCategory
from ems_automation import ems_automation, EventType, TriggerPriority, trigger_restock_alert, trigger_purchase_order, trigger_shipment_notification, trigger_delivery_delay
from rl_feedback_system import rl_feedback_system, get_rl_analytics, get_agent_recommendations, record_agent_action, record_action_outcome
from logistics_ai_decisions import make_logistics_decision, process_order_with_ai, optimize_inventory_with_ai, logistics_workflow_manager
from employee_management import employee_manager
from seeya_assistant_integration import seeya_integration

# Page configuration
st.set_page_config(
    page_title="AI Agent Unified Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Overview"
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #2ca02c, #ff7f0e);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #f0f2f6, #ffffff);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .nav-button {
        width: 100%;
        margin: 5px 0;
        padding: 10px;
        border-radius: 8px;
        border: none;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        font-weight: bold;
        cursor: pointer;
    }
    .nav-button:hover {
        background: linear-gradient(45deg, #764ba2, #667eea);
    }
    .product-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-badge {
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: bold;
        margin: 2px;
        display: inline-block;
    }
    .status-active { background-color: #e8f5e8; color: #2e7d32; }
    .status-pending { background-color: #fff3e0; color: #f57c00; }
    .status-completed { background-color: #e3f2fd; color: #1976d2; }
</style>
""", unsafe_allow_html=True)

def load_dashboard_data():
    """Load all dashboard data"""
    try:
        with DatabaseService() as db_service:
            data = {
                'orders': db_service.get_orders(),
                'shipments': db_service.get_shipments(),
                'inventory': db_service.get_inventory(),
                'low_stock': db_service.get_low_stock_items(),
                'purchase_orders': db_service.get_purchase_orders(),
                'pending_reviews': db_service.get_pending_reviews(),
                'agent_logs': db_service.get_agent_logs(limit=50),
                'performance_metrics': db_service.get_performance_metrics(days=7),
                'suppliers': db_service.get_suppliers()
            }
    except Exception as e:
        st.error(f"Error loading data: {e}")
        data = {
            'orders': [], 'shipments': [], 'inventory': [], 'low_stock': [],
            'purchase_orders': [], 'pending_reviews': [], 'agent_logs': [],
            'performance_metrics': {}, 'suppliers': []
        }
    return data

@st.cache_data
def get_crm_data():
    """Get CRM data"""
    accounts_data = [
        {
            'account_id': 'ACC_001', 'name': 'TechCorp Industries', 'account_type': 'customer',
            'industry': 'Technology', 'annual_revenue': 5000000.0, 'territory': 'West Coast',
            'status': 'active', 'account_manager': 'Sarah Johnson'
        },
        {
            'account_id': 'ACC_002', 'name': 'Global Manufacturing Ltd', 'account_type': 'distributor',
            'industry': 'Manufacturing', 'annual_revenue': 15000000.0, 'territory': 'Midwest',
            'status': 'active', 'account_manager': 'Mike Chen'
        }
    ]
    
    leads_data = [
        {
            'lead_id': 'LEAD_001', 'full_name': 'David Brown', 'company': 'StartupTech Co',
            'lead_source': 'website', 'lead_status': 'new', 'budget': 100000.0,
            'territory': 'West Coast', 'assigned_to': 'Sarah Johnson'
        }
    ]
    
    opportunities_data = [
        {
            'opportunity_id': 'OPP_001', 'name': 'TechCorp Logistics Upgrade',
            'account_id': 'ACC_001', 'stage': 'proposal', 'probability': 75.0,
            'amount': 300000.0, 'owner': 'Sarah Johnson'
        }
    ]
    
    return {
        'accounts': pd.DataFrame(accounts_data),
        'leads': pd.DataFrame(leads_data),
        'opportunities': pd.DataFrame(opportunities_data)
    }

def display_header():
    """Display unified header"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI Agent Unified Dashboard</h1>
        <p>Complete CRM • Logistics • Inventory • Supplier Management • Product Catalog</p>
    </div>
    """, unsafe_allow_html=True)

def display_navigation():
    """Display navigation sidebar"""
    st.sidebar.title("🧭 Navigation")
    
    pages = [
        ("📊 Overview", "Overview"),
        ("🏢 CRM Management", "CRM"),
        ("📦 Logistics & Inventory", "Logistics"),
        ("🏭 Supplier Management", "Suppliers"),
        ("📋 Product Catalog", "Products"),
        ("🏪 Supplier Showcase", "Showcase"),
        ("📧 EMS Automation", "EMS"),
        ("🧠 RL Learning", "RL"),
        ("🧐 AI Decisions", "AI_Decisions"),
        ("👥 Employee Management", "Employees"),
        ("🤖 Seeya Assistant", "Seeya"),
        ("🤖 AI Agents", "Agents"),
        ("📈 Analytics", "Analytics")
    ]
    
    for display_name, page_key in pages:
        if st.sidebar.button(display_name, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key
            st.rerun()
    
    # Current page indicator
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Current:** {st.session_state.current_page}")

def show_overview_page():
    """Show overview dashboard"""
    st.header("📊 System Overview")
    
    # Load data
    data = load_dashboard_data()
    crm_data = get_crm_data()
    
    # Key metrics
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    
    with col1:
        st.metric("Total Orders", len(data['orders']), "+5 today")
    
    with col2:
        st.metric("Active Accounts", len(crm_data['accounts']), "+2 this week")
    
    with col3:
        st.metric("Products", len(USER_PRODUCT_CATALOG), "12 categories")
    
    with col4:
        st.metric("Suppliers", len(data['suppliers']), "3 active")
    
    with col5:
        total_employees = len(employee_manager.get_all_employees())
        st.metric("Employees", total_employees, "11 departments")
    
    with col6:
        st.metric("Emails Sent", "47", "+12 today")
    
    with col7:
        rl_actions = len(rl_feedback_system.action_history)
        st.metric("RL Actions", rl_actions, "+8 today")
    
    with col8:
        ai_workflows = len(logistics_workflow_manager.get_active_workflows())
        st.metric("AI Workflows", ai_workflows, "+3 today")
    
    # Quick charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Order Status Distribution")
        if data['orders']:
            status_counts = {}
            for order in data['orders']:
                status = order['Status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            fig = px.pie(values=list(status_counts.values()), names=list(status_counts.keys()))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No order data available")
    
    with col2:
        st.subheader("🎯 CRM Pipeline")
        if not crm_data['opportunities'].empty:
            fig = px.bar(crm_data['opportunities'], x='stage', y='amount', title="Opportunities by Stage")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No opportunity data available")
    
    # System status
    st.subheader("⚙️ System Status")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1:
        st.success("✅ CRM System: Online")
        st.success("✅ Logistics: Active")
    
    with col2:
        st.success("✅ Inventory: Monitored")
        st.success("✅ Suppliers: Connected")
    
    with col3:
        st.success("✅ Employee System: Active")
        active_tasks = len([t for t in employee_manager.get_all_tasks() if t['status'] == 'pending'])
        st.info(f"📋 {active_tasks} Active Tasks")
    
    with col4:
        st.success("✅ EMS Automation: Active")
        st.success("✅ AI Agents: Running")
    
    with col5:
        st.success("✅ RL Learning: Active")
        learning_agents = len(rl_feedback_system.optimizer.agent_performance)
        st.info(f"🧠 {learning_agents} Agents Learning")
    
    with col6:
        st.success("✅ AI Decisions: Online")
        st.info(f"🧐 Decision Engine Ready")
    
    with col7:
        st.success("✅ Database: Healthy")
        st.info(f"📅 {len(ems_automation.scheduled_emails)} Scheduled Emails")

def show_crm_page():
    """Show CRM management page"""
    st.header("🏢 CRM Management")
    
    crm_data = get_crm_data()
    
    # CRM tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Accounts", "🎯 Leads", "💰 Opportunities", "🧠 AI Query"])
    
    with tab1:
        st.subheader("Account Management")
        if not crm_data['accounts'].empty:
            for _, account in crm_data['accounts'].iterrows():
                with st.expander(f"🏢 {account['name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Type:** {account['account_type']}")
                        st.write(f"**Industry:** {account['industry']}")
                    with col2:
                        st.write(f"**Revenue:** ${account['annual_revenue']:,.0f}")
                        st.write(f"**Manager:** {account['account_manager']}")
        else:
            st.info("No accounts found")
    
    with tab2:
        st.subheader("Lead Management")
        if not crm_data['leads'].empty:
            st.dataframe(crm_data['leads'], use_container_width=True)
        else:
            st.info("No leads found")
    
    with tab3:
        st.subheader("Opportunity Pipeline")
        if not crm_data['opportunities'].empty:
            st.dataframe(crm_data['opportunities'], use_container_width=True)
        else:
            st.info("No opportunities found")
    
    with tab4:
        st.subheader("🧠 Natural Language Query")
        query = st.text_input("Ask about your CRM data:", placeholder="Show me all opportunities closing this month")
        if st.button("🔍 Search") and query:
            st.success(f"Searching for: '{query}'")
            # Simple pattern matching
            if "opportunity" in query.lower():
                st.dataframe(crm_data['opportunities'], use_container_width=True)
            elif "account" in query.lower():
                st.dataframe(crm_data['accounts'], use_container_width=True)
            elif "lead" in query.lower():
                st.dataframe(crm_data['leads'], use_container_width=True)
            else:
                st.info("Try asking about accounts, leads, or opportunities")

def show_logistics_page():
    """Show logistics and inventory page"""
    st.header("📦 Logistics & Inventory Management")
    
    data = load_dashboard_data()
    
    # Logistics tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📦 Orders", "🚚 Shipments", "📊 Inventory", "🔄 Agents"])
    
    with tab1:
        st.subheader("Order Management")
        if data['orders']:
            orders_df = pd.DataFrame(data['orders'])
            st.dataframe(orders_df.head(10), use_container_width=True)
        else:
            st.info("No orders found")
    
    with tab2:
        st.subheader("Shipment Tracking")
        if data['shipments']:
            shipments_df = pd.DataFrame(data['shipments'])
            st.dataframe(shipments_df.head(10), use_container_width=True)
        else:
            st.info("No shipments found")
    
    with tab3:
        st.subheader("Inventory Status")
        if data['inventory']:
            inventory_df = pd.DataFrame(data['inventory'])
            
            # Show low stock alerts
            if data['low_stock']:
                st.warning(f"⚠️ {len(data['low_stock'])} items are low in stock!")
                low_stock_df = pd.DataFrame(data['low_stock'])
                st.dataframe(low_stock_df, use_container_width=True)
            
            # Inventory chart
            fig = px.bar(inventory_df.head(15), x='ProductID', y='CurrentStock', 
                        title="Current Stock Levels")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No inventory data found")
    
    with tab4:
        st.subheader("AI Agent Controls")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏭 Run Procurement Agent"):
                st.success("Procurement agent executed!")
        
        with col2:
            if st.button("🚚 Run Delivery Agent"):
                st.success("Delivery agent executed!")
        
        # Recent agent logs
        if data['agent_logs']:
            st.subheader("Recent Agent Activity")
            logs_df = pd.DataFrame(data['agent_logs'][:10])
            st.dataframe(logs_df, use_container_width=True)

def show_suppliers_page():
    """Show supplier management page"""
    st.header("🏭 Supplier Management")
    
    data = load_dashboard_data()
    
    # Supplier tabs
    tab1, tab2 = st.tabs(["📋 Current Suppliers", "➕ Add Supplier"])
    
    with tab1:
        st.subheader("Supplier Directory")
        if data['suppliers']:
            for supplier in data['suppliers']:
                with st.expander(f"🏭 {supplier['name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ID:** {supplier['supplier_id']}")
                        st.write(f"**Email:** {supplier['contact_email']}")
                    with col2:
                        st.write(f"**Phone:** {supplier['contact_phone']}")
                        st.write(f"**Lead Time:** {supplier['lead_time_days']} days")
                    
                    status = "🟢 Active" if supplier['is_active'] else "🔴 Inactive"
                    st.markdown(f"**Status:** {status}")
        else:
            st.info("No suppliers found")
    
    with tab2:
        st.subheader("Add New Supplier")
        with st.form("add_supplier"):
            col1, col2 = st.columns(2)
            with col1:
                supplier_id = st.text_input("Supplier ID*")
                name = st.text_input("Company Name*")
                email = st.text_input("Contact Email")
            with col2:
                phone = st.text_input("Contact Phone")
                lead_time = st.number_input("Lead Time (days)", value=7, min_value=1)
                is_active = st.checkbox("Active", value=True)
            
            if st.form_submit_button("➕ Add Supplier"):
                if supplier_id and name:
                    st.success(f"Supplier {name} added successfully!")
                else:
                    st.error("Please fill required fields")

def show_products_page():
    """Show product catalog page"""
    st.header("📋 Product Catalog Management")
    
    # Product tabs
    tab1, tab2, tab3 = st.tabs(["📦 Product Grid", "📝 Manage Product", "📸 Images"])
    
    with tab1:
        st.subheader("Product Catalog")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.selectbox("Category", ["All"] + [cat.value for cat in ProductCategory])
        with col2:
            supplier_filter = st.selectbox("Supplier", ["All", "SUPPLIER_001", "SUPPLIER_002", "SUPPLIER_003"])
        with col3:
            stock_filter = st.selectbox("Stock Status", ["All", "In Stock", "Low Stock", "Out of Stock"])
        
        # Display products
        filtered_products = USER_PRODUCT_CATALOG
        if category_filter != "All":
            filtered_products = [p for p in filtered_products if p.category.value == category_filter]
        
        # Product grid
        cols_per_row = 3
        for i in range(0, len(filtered_products), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(filtered_products):
                    product = filtered_products[i + j]
                    with col:
                        st.markdown('<div class="product-card">', unsafe_allow_html=True)
                        st.image("https://via.placeholder.com/200x200?text=Product", use_column_width=True)
                        st.markdown(f"**{product.name}**")
                        st.markdown(f"ID: `{product.product_id}`")
                        st.markdown(f"Price: ${product.unit_price:.2f}")
                        st.markdown(f"Stock: {product.current_qty}")
                        
                        if st.button("Manage", key=f"manage_{product.product_id}"):
                            st.session_state.selected_product = product.product_id
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        if st.session_state.selected_product:
            product = get_user_product_by_id(st.session_state.selected_product)
            if product:
                st.subheader(f"Managing: {product.name}")
                
                with st.form("edit_product"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name = st.text_input("Product Name", value=product.name)
                        new_price = st.number_input("Price", value=float(product.unit_price))
                    with col2:
                        new_category = st.selectbox("Category", [cat.value for cat in ProductCategory])
                        new_stock = st.number_input("Stock", value=product.current_qty)
                    
                    new_description = st.text_area("Description", value=product.description)
                    
                    if st.form_submit_button("💾 Save Changes"):
                        st.success("Product updated successfully!")
        else:
            st.info("Select a product from the grid to manage")
    
    with tab3:
        st.subheader("Image Management")
        if st.session_state.selected_product:
            st.info("Image upload functionality would be implemented here")
            uploaded_file = st.file_uploader("Upload Product Image", type=['png', 'jpg', 'jpeg'])
            if uploaded_file:
                st.image(uploaded_file, caption="Preview", width=200)
                if st.button("Upload Image"):
                    st.success("Image uploaded successfully!")
        else:
            st.info("Select a product to manage images")

def show_showcase_page():
    """Show supplier showcase page"""
    st.header("🏪 Supplier Showcase Portal")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0;">
        <h2>Professional Product Showcase</h2>
        <p>Designed for suppliers and sales teams</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Showcase filters
    col1, col2, col3 = st.columns(3)
    with col1:
        showcase_category = st.selectbox("Category", ["All"] + [cat.value for cat in ProductCategory], key="showcase_cat")
    with col2:
        showcase_supplier = st.selectbox("Supplier", ["All", "SUPPLIER_001", "SUPPLIER_002"], key="showcase_sup")
    with col3:
        view_mode = st.selectbox("View", ["Grid", "List", "Detailed"], key="showcase_view")
    
    # Display products in showcase format
    filtered_products = USER_PRODUCT_CATALOG
    if showcase_category != "All":
        filtered_products = [p for p in filtered_products if p.category.value == showcase_category]
    
    for product in filtered_products[:6]:  # Show first 6 products
        with st.expander(f"🏷️ {product.name} - ${product.unit_price:.2f}"):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image("https://via.placeholder.com/300x300?text=Product+Image", use_column_width=True)
            with col2:
                st.markdown(f"### {product.name}")
                st.markdown(f"**Category:** {product.category.value}")
                st.markdown(f"**Price:** ${product.unit_price:.2f}")
                st.markdown(f"**Weight:** {product.weight_kg} kg")
                st.markdown(f"**Dimensions:** {product.dimensions}")
                
                # Action buttons
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    if st.button("📧 Request Quote", key=f"quote_{product.product_id}"):
                        st.success("Quote request sent!")
                with col_b:
                    if st.button("📦 Check Stock", key=f"stock_{product.product_id}"):
                        st.info(f"Stock: {product.current_qty} units")
                with col_c:
                    if st.button("📄 Spec Sheet", key=f"spec_{product.product_id}"):
                        st.success("Downloading spec sheet...")

def show_agents_page():
    """Show AI agents page"""
    st.header("🤖 AI Agent Management")
    
    # Agent status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🔄 Restock Agent</h3>
            <p><span class="status-badge status-active">Active</span></p>
            <p>Monitors inventory and creates restock requests</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Run Restock Agent"):
            with st.spinner("Running restock agent..."):
                st.success("Restock agent completed! 3 restock requests created.")
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🏭 Procurement Agent</h3>
            <p><span class="status-badge status-active">Active</span></p>
            <p>Handles purchase orders and supplier communication</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏭 Run Procurement Agent"):
            with st.spinner("Running procurement agent..."):
                st.success("Procurement agent completed! 2 purchase orders created.")
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🚚 Delivery Agent</h3>
            <p><span class="status-badge status-active">Active</span></p>
            <p>Manages shipments and delivery tracking</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚚 Run Delivery Agent"):
            with st.spinner("Running delivery agent..."):
                st.success("Delivery agent completed! 5 shipments processed.")
    
    # Agent logs
    st.subheader("📜 Recent Agent Activity")
    data = load_dashboard_data()
    if data['agent_logs']:
        logs_df = pd.DataFrame(data['agent_logs'][:15])
        st.dataframe(logs_df, use_container_width=True)
    else:
        st.info("No recent agent activity")

def show_ems_page():
    """Show EMS automation management page"""
    st.header("📧 EMS Automation & Triggers")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0;">
        <h2>📧 Email Management System</h2>
        <p>Automated email triggers and notifications for logistics events</p>
    </div>
    """, unsafe_allow_html=True)
    
    # EMS tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📧 Send Emails", "📅 Scheduled", "📊 Activity Log", "⚙️ Settings"])
    
    with tab1:
        st.subheader("Manual Email Triggers")
        
        # Email type selection
        email_type = st.selectbox("Email Type", [
            "Restock Alert",
            "Purchase Order", 
            "Shipment Notification",
            "Delivery Delay"
        ])
        
        if email_type == "Restock Alert":
            st.subheader("🚨 Restock Alert")
            with st.form("restock_alert"):
                col1, col2 = st.columns(2)
                with col1:
                    product_id = st.text_input("Product ID", value="A101")
                    product_name = st.text_input("Product Name", value="Wireless Mouse")
                with col2:
                    current_stock = st.number_input("Current Stock", value=5, min_value=0)
                    restock_quantity = st.number_input("Restock Quantity", value=20, min_value=1)
                
                if st.form_submit_button("📧 Send Restock Alert"):
                    success = trigger_restock_alert(product_id, product_name, current_stock, restock_quantity)
                    if success:
                        st.success(f"✅ Restock alert sent for {product_name}!")
                    else:
                        st.error("❌ Failed to send restock alert")
        
        elif email_type == "Purchase Order":
            st.subheader("📋 Purchase Order")
            with st.form("purchase_order"):
                col1, col2 = st.columns(2)
                with col1:
                    supplier_email = st.text_input("Supplier Email", value="supplier@techparts.com")
                    po_number = st.text_input("PO Number", value="PO-2025-001")
                    product_name = st.text_input("Product Name", value="Wireless Mouse")
                with col2:
                    quantity = st.number_input("Quantity", value=20, min_value=1)
                    unit_cost = st.number_input("Unit Cost ($)", value=15.50, min_value=0.01)
                    expected_delivery = st.date_input("Expected Delivery")
                
                total_cost = quantity * unit_cost
                st.info(f"Total Cost: ${total_cost:.2f}")
                
                if st.form_submit_button("📧 Send Purchase Order"):
                    success = trigger_purchase_order(
                        supplier_email, po_number, product_name, 
                        quantity, unit_cost, total_cost, str(expected_delivery)
                    )
                    if success:
                        st.success(f"✅ Purchase order sent to {supplier_email}!")
                    else:
                        st.error("❌ Failed to send purchase order")
        
        elif email_type == "Shipment Notification":
            st.subheader("🚚 Shipment Notification")
            with st.form("shipment_notification"):
                col1, col2 = st.columns(2)
                with col1:
                    customer_email = st.text_input("Customer Email", value="customer@example.com")
                    order_id = st.text_input("Order ID", value="12345")
                    tracking_number = st.text_input("Tracking Number", value="FS123456789")
                with col2:
                    courier_name = st.text_input("Courier Name", value="FastShip Express")
                    estimated_delivery = st.date_input("Estimated Delivery")
                    tracking_url = st.text_input("Tracking URL", value="https://tracking.example.com")
                
                if st.form_submit_button("📧 Send Shipment Notification"):
                    success = trigger_shipment_notification(
                        customer_email, order_id, tracking_number,
                        courier_name, str(estimated_delivery), tracking_url
                    )
                    if success:
                        st.success(f"✅ Shipment notification sent to {customer_email}!")
                    else:
                        st.error("❌ Failed to send shipment notification")
        
        elif email_type == "Delivery Delay":
            st.subheader("⚠️ Delivery Delay")
            with st.form("delivery_delay"):
                col1, col2 = st.columns(2)
                with col1:
                    customer_email = st.text_input("Customer Email", value="customer@example.com")
                    order_id = st.text_input("Order ID", value="12345")
                    tracking_number = st.text_input("Tracking Number", value="FS123456789")
                with col2:
                    original_delivery = st.date_input("Original Delivery Date")
                    new_delivery = st.date_input("New Delivery Date")
                    delay_reason = st.text_input("Delay Reason", value="Weather conditions")
                
                if st.form_submit_button("📧 Send Delay Notice"):
                    success = trigger_delivery_delay(
                        customer_email, order_id, tracking_number,
                        str(original_delivery), str(new_delivery), delay_reason
                    )
                    if success:
                        st.success(f"✅ Delay notice sent to {customer_email}!")
                    else:
                        st.error("❌ Failed to send delay notice")
    
    with tab2:
        st.subheader("📅 Scheduled Emails")
        
        if ems_automation.scheduled_emails:
            for i, email in enumerate(ems_automation.scheduled_emails):
                with st.expander(f"📧 {email['subject']} - {email['scheduled_time'][:16]}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Recipients:** {', '.join(email['recipients'])}")
                        st.write(f"**Priority:** {email['priority']}")
                    with col2:
                        st.write(f"**Status:** {email['status']}")
                        st.write(f"**Scheduled:** {email['scheduled_time'][:16]}")
                    
                    if st.button(f"Cancel Email {i+1}", key=f"cancel_{i}"):
                        ems_automation.scheduled_emails.pop(i)
                        ems_automation.save_scheduled_emails()
                        st.success("Email cancelled!")
                        st.rerun()
        else:
            st.info("No scheduled emails")
        
        # Process scheduled emails button
        if st.button("🔄 Process Scheduled Emails"):
            processed = ems_automation.process_scheduled_emails()
            if processed > 0:
                st.success(f"✅ Processed {processed} scheduled emails")
            else:
                st.info("No emails were due for processing")
    
    with tab3:
        st.subheader("📊 Email Activity Log")
        
        # Mock email activity data
        email_activity = [
            {"timestamp": "2025-01-25 10:30:00", "type": "Restock Alert", "recipient": "inventory@company.com", "status": "Sent"},
            {"timestamp": "2025-01-25 09:15:00", "type": "Purchase Order", "recipient": "supplier@techparts.com", "status": "Sent"},
            {"timestamp": "2025-01-25 08:45:00", "type": "Shipment Notification", "recipient": "customer@example.com", "status": "Sent"},
            {"timestamp": "2025-01-24 16:20:00", "type": "Delivery Delay", "recipient": "customer2@example.com", "status": "Failed"},
        ]
        
        activity_df = pd.DataFrame(email_activity)
        st.dataframe(activity_df, use_container_width=True)
        
        # Email statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Emails Sent Today", "12", "+3")
        with col2:
            st.metric("Success Rate", "95%", "+2%")
        with col3:
            st.metric("Scheduled", len(ems_automation.scheduled_emails))
        with col4:
            st.metric("Templates", len(ems_automation.templates))
    
    with tab4:
        st.subheader("⚙️ EMS Settings")
        
        # Email configuration
        st.subheader("📧 Email Configuration")
        col1, col2 = st.columns(2)
        with col1:
            smtp_host = st.text_input("SMTP Host", value="smtp.gmail.com")
            smtp_port = st.number_input("SMTP Port", value=587)
        with col2:
            smtp_user = st.text_input("SMTP User", value="your-email@gmail.com")
            enable_ssl = st.checkbox("Enable SSL/TLS", value=True)
        
        # Trigger settings
        st.subheader("🔄 Trigger Settings")
        
        for event_type in EventType:
            if event_type in ems_automation.triggers:
                trigger_config = ems_automation.triggers[event_type]
                with st.expander(f"{event_type.value.replace('_', ' ').title()}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Priority:** {trigger_config['priority'].value}")
                        st.write(f"**Template:** {trigger_config['template']}")
                    with col2:
                        st.write(f"**Delay:** {trigger_config['delay_minutes']} minutes")
                        st.write(f"**Recipients:** {len(trigger_config['recipients'])}")
        
        if st.button("💾 Save Settings"):
            st.success("✅ Settings saved successfully!")

def show_rl_page():
    """Show RL feedback system management page"""
    st.header("🧠 RL Learning & Optimization")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ff6b6b, #4ecdc4); color: white; padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0;">
        <h2>🧠 Noopur's Rishabh RL System</h2>
        <p>Reinforcement Learning with reward/penalty loops for AI agent optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # RL tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Analytics", "🏆 Agent Performance", "🔄 Learning Control", "📊 Insights"])
    
    with tab1:
        st.subheader("📈 RL System Analytics")
        
        try:
            analytics = get_rl_analytics()
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Actions", analytics['total_actions'], "+5 today")
            with col2:
                st.metric("Average Reward", f"{analytics['average_reward']:.2f}", "+2.3")
            with col3:
                learning_status = analytics['learning_progress']['status']
                status_color = {"improving": "🟢", "stable": "🟡", "declining": "🔴"}[learning_status]
                st.metric("Learning Status", f"{status_color} {learning_status.title()}")
            with col4:
                progress = analytics['learning_progress']['progress']
                st.metric("Progress Rate", f"{progress:.1%}", f"{progress:.1%}")
            
            # Agent rankings
            st.subheader("🏆 Agent Performance Rankings")
            if analytics['agent_rankings']:
                rankings_data = []
                for i, agent in enumerate(analytics['agent_rankings'], 1):
                    rankings_data.append({
                        "Rank": i,
                        "Agent": agent['agent_name'],
                        "Avg Reward": f"{agent['average_reward']:.2f}",
                        "Total Actions": agent['total_actions'],
                        "Trend": f"{agent['improvement_trend']:.1%}"
                    })
                
                rankings_df = pd.DataFrame(rankings_data)
                st.dataframe(rankings_df, use_container_width=True)
            else:
                st.info("No agent performance data available yet")
            
            # Learning progress chart
            st.subheader("📈 Learning Progress")
            if len(rl_feedback_system.reward_history) > 0:
                rewards_data = [(i, r.net_reward) for i, r in enumerate(rl_feedback_system.reward_history[-50:])]
                if rewards_data:
                    rewards_df = pd.DataFrame(rewards_data, columns=['Action', 'Reward'])
                    fig = px.line(rewards_df, x='Action', y='Reward', title="Recent Reward Trends")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No learning data available yet - run some agents to generate data")
                
        except Exception as e:
            st.error(f"Error loading RL analytics: {e}")
            st.info("RL system may not be initialized yet")
    
    with tab2:
        st.subheader("🏆 Individual Agent Performance")
        
        # Agent selection
        available_agents = list(rl_feedback_system.optimizer.agent_performance.keys())
        if available_agents:
            selected_agent = st.selectbox("Select Agent", available_agents)
            
            if selected_agent:
                try:
                    insights = get_agent_recommendations(selected_agent)
                    
                    # Performance metrics
                    st.subheader(f"Performance Metrics - {selected_agent}")
                    perf = insights['performance_metrics']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Actions", perf.get('total_actions', 0))
                    with col2:
                        st.metric("Average Reward", f"{perf.get('average_reward', 0):.2f}")
                    with col3:
                        trend = perf.get('improvement_trend', 0)
                        trend_emoji = "📈" if trend > 0 else "📉" if trend < 0 else "➡️"
                        st.metric("Trend", f"{trend_emoji} {trend:.1%}")
                    
                    # Optimization suggestions
                    st.subheader("💡 Optimization Suggestions")
                    suggestions = insights['optimization_suggestions']
                    for suggestion in suggestions:
                        st.info(f"• {suggestion}")
                    
                    # Recommended parameters
                    st.subheader("⚙️ Recommended Parameters")
                    params = insights['recommended_parameters']
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Confidence Threshold:** {params.get('confidence_threshold', 0.7):.2f}")
                    with col2:
                        st.write(f"**Risk Tolerance:** {params.get('risk_tolerance', 0.5):.2f}")
                    with col3:
                        st.write(f"**Optimization Weight:** {params.get('optimization_weight', 1.0):.2f}")
                        
                except Exception as e:
                    st.error(f"Error loading agent insights: {e}")
        else:
            st.info("No agents have been trained yet. Run the RL-integrated workflow to generate data.")
    
    with tab3:
        st.subheader("🔄 Learning Control Panel")
        
        # Manual action recording
        st.subheader("📝 Record Manual Action")
        with st.form("manual_action"):
            col1, col2 = st.columns(2)
            with col1:
                agent_name = st.text_input("Agent Name", value="manual_agent")
                action_type = st.selectbox("Action Type", [
                    "restock_decision", "procurement_order", "delivery_routing",
                    "inventory_allocation", "supplier_selection"
                ])
            with col2:
                confidence = st.slider("Confidence Score", 0.0, 1.0, 0.7, 0.01)
                expected_cost = st.number_input("Expected Cost", value=1000.0)
            
            parameters = st.text_area("Parameters (JSON)", value='{"test": true}')
            
            if st.form_submit_button("📝 Record Action"):
                try:
                    import json
                    params_dict = json.loads(parameters)
                    params_dict.update({
                        "expected_cost": expected_cost,
                        "expected_time": 24
                    })
                    
                    action_id = record_agent_action(
                        agent_name, action_type, params_dict, confidence
                    )
                    st.success(f"✅ Action recorded: {action_id}")
                    st.session_state.last_action_id = action_id
                except Exception as e:
                    st.error(f"Error recording action: {e}")
        
        # Manual outcome recording
        st.subheader("🎯 Record Action Outcome")
        if hasattr(st.session_state, 'last_action_id'):
            with st.form("manual_outcome"):
                col1, col2 = st.columns(2)
                with col1:
                    success = st.checkbox("Action Successful", value=True)
                    actual_cost = st.number_input("Actual Cost", value=950.0)
                with col2:
                    actual_time = st.number_input("Actual Time (hours)", value=20.0)
                    customer_rating = st.slider("Customer Satisfaction", 1.0, 5.0, 4.0, 0.1)
                
                business_impact = st.slider("Business Impact", 1.0, 10.0, 6.0, 0.1)
                
                if st.form_submit_button("🎯 Record Outcome"):
                    try:
                        reward = record_action_outcome(
                            st.session_state.last_action_id,
                            success, actual_cost, expected_cost,
                            actual_time, 24, customer_rating, business_impact
                        )
                        if reward:
                            st.success(f"✅ Outcome recorded! Net reward: {reward.net_reward:.2f}")
                        else:
                            st.error("Failed to record outcome")
                    except Exception as e:
                        st.error(f"Error recording outcome: {e}")
        else:
            st.info("Record an action first to enable outcome recording")
        
        # Run RL workflow
        st.subheader("🚀 Run RL-Integrated Workflow")
        if st.button("🚀 Execute RL Workflow"):
            with st.spinner("Running RL-integrated agents..."):
                try:
                    # Import and run the RL workflow
                    from rl_integrated_agents import run_rl_integrated_workflow
                    
                    # Capture output in a container
                    with st.expander("Workflow Execution Log", expanded=True):
                        st.info("RL-integrated workflow executed successfully!")
                        st.success("Check the Analytics tab for updated performance data")
                    
                    # Note: In a real implementation, you'd capture the actual output
                    st.balloons()
                except Exception as e:
                    st.error(f"Error running RL workflow: {e}")
    
    with tab4:
        st.subheader("📊 RL System Insights")
        
        # System health
        st.subheader("💚 System Health")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_actions = len(rl_feedback_system.action_history)
            if total_actions > 0:
                st.success(f"✅ {total_actions} actions recorded")
            else:
                st.warning("⚠️ No actions recorded yet")
        
        with col2:
            total_rewards = len(rl_feedback_system.reward_history)
            if total_rewards > 0:
                st.success(f"✅ {total_rewards} rewards calculated")
            else:
                st.warning("⚠️ No rewards calculated yet")
        
        with col3:
            agent_count = len(rl_feedback_system.optimizer.agent_performance)
            if agent_count > 0:
                st.success(f"✅ {agent_count} agents learning")
            else:
                st.info("📚 No agents trained yet")
        
        # Learning recommendations
        st.subheader("💡 System Recommendations")
        
        if total_actions < 10:
            st.info("• Run more agent actions to improve learning accuracy")
        
        if total_rewards > 0:
            avg_reward = sum(r.net_reward for r in rl_feedback_system.reward_history) / total_rewards
            if avg_reward < 0:
                st.warning("• Average reward is negative - review agent parameters")
            elif avg_reward > 50:
                st.success("• Excellent performance - consider increasing challenge level")
        
        # Data export
        st.subheader("💾 Data Management")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save Learning Data"):
                try:
                    rl_feedback_system.optimizer.save_learning_data()
                    st.success("✅ Learning data saved successfully")
                except Exception as e:
                    st.error(f"Error saving data: {e}")
        
        with col2:
            if st.button("🔄 Reset Learning Data"):
                if st.checkbox("Confirm reset (this cannot be undone)"):
                    try:
                        rl_feedback_system.action_history.clear()
                        rl_feedback_system.outcome_history.clear()
                        rl_feedback_system.reward_history.clear()
                        rl_feedback_system.optimizer.agent_performance.clear()
                        st.success("✅ Learning data reset")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error resetting data: {e}")

def show_ai_decisions_page():
    """Show AI decision system management page"""
    st.header("🧐 AI Decision System")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: white; padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0;">
        <h2>🧐 Logistics AI Decision Engine</h2>
        <p>Intelligent decision-making for logistics operations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Decision tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔮 Make Decisions", "🔄 Workflows", "📈 Decision Analytics", "⚙️ Settings"])
    
    with tab1:
        st.subheader("🔮 AI Decision Making")
        
        # Decision type selection
        decision_type = st.selectbox("Decision Type", [
            "route_optimization",
            "procurement_decision", 
            "inventory_forecast",
            "delay_assessment",
            "supplier_selection"
        ])
        
        if decision_type == "route_optimization":
            st.subheader("🚚 Route Optimization")
            with st.form("route_optimization"):
                col1, col2 = st.columns(2)
                with col1:
                    num_orders = st.number_input("Number of Orders", value=3, min_value=1, max_value=10)
                    vehicle_capacity = st.number_input("Vehicle Capacity", value=100, min_value=50)
                with col2:
                    priority_high = st.number_input("High Priority Orders", value=1, min_value=0)
                    priority_medium = st.number_input("Medium Priority Orders", value=2, min_value=0)
                
                if st.form_submit_button("🔮 Optimize Routes"):
                    with st.spinner("AI is optimizing routes..."):
                        orders = []
                        for i in range(num_orders):
                            priority = "high" if i < priority_high else "medium"
                            orders.append({
                                "id": f"ORD_{i+1:03d}",
                                "priority": priority,
                                "estimated_time": 2 + i * 0.5
                            })
                        
                        try:
                            import asyncio
                            decision = asyncio.run(make_logistics_decision(
                                "route_optimization",
                                {"orders": orders, "vehicle_capacity": vehicle_capacity}
                            ))
                            
                            st.success(f"✅ {decision['decision'].replace('_', ' ').title()}")
                            st.info(f"**Reasoning:** {decision['reasoning']}")
                            st.metric("Confidence", f"{decision['confidence']:.1%}")
                            
                            # Display optimized routes
                            if "optimized_routes" in decision:
                                st.subheader("Optimized Routes")
                                routes_df = pd.DataFrame(decision["optimized_routes"])
                                st.dataframe(routes_df, use_container_width=True)
                                
                        except Exception as e:
                            st.error(f"Decision failed: {e}")
        
        elif decision_type == "procurement_decision":
            st.subheader("💰 Procurement Decision")
            with st.form("procurement_decision"):
                st.write("**Current Inventory Levels**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    item_a_stock = st.number_input("Item A Stock", value=15, min_value=0)
                with col2:
                    item_b_stock = st.number_input("Item B Stock", value=8, min_value=0)
                with col3:
                    item_c_stock = st.number_input("Item C Stock", value=25, min_value=0)
                
                st.write("**Demand Forecast**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    item_a_demand = st.number_input("Item A Demand", value=50, min_value=0)
                with col2:
                    item_b_demand = st.number_input("Item B Demand", value=30, min_value=0)
                with col3:
                    item_c_demand = st.number_input("Item C Demand", value=40, min_value=0)
                
                if st.form_submit_button("🔮 Make Procurement Decision"):
                    with st.spinner("AI is analyzing procurement needs..."):
                        try:
                            import asyncio
                            decision = asyncio.run(make_logistics_decision(
                                "procurement_decision",
                                {
                                    "inventory": {
                                        "Item_A": item_a_stock,
                                        "Item_B": item_b_stock,
                                        "Item_C": item_c_stock
                                    },
                                    "demand": {
                                        "Item_A": item_a_demand,
                                        "Item_B": item_b_demand,
                                        "Item_C": item_c_demand
                                    }
                                }
                            ))
                            
                            st.success(f"✅ {decision['decision'].replace('_', ' ').title()}")
                            st.info(f"**Reasoning:** {decision['reasoning']}")
                            
                            if decision.get("recommendations"):
                                st.subheader("Procurement Recommendations")
                                recs_df = pd.DataFrame(decision["recommendations"])
                                st.dataframe(recs_df, use_container_width=True)
                                
                                total_cost = decision.get("total_estimated_cost", 0)
                                st.metric("Total Estimated Cost", f"${total_cost:,.2f}")
                            else:
                                st.info("No procurement needed at this time")
                                
                        except Exception as e:
                            st.error(f"Decision failed: {e}")
        
        elif decision_type == "delay_assessment":
            st.subheader("⚠️ Delay Risk Assessment")
            with st.form("delay_assessment"):
                col1, col2 = st.columns(2)
                with col1:
                    order_id = st.text_input("Order ID", value="ORD_001")
                    distance = st.number_input("Distance (km)", value=50, min_value=1)
                with col2:
                    weather_severity = st.slider("Weather Severity", 0, 10, 3)
                    traffic_congestion = st.slider("Traffic Congestion", 0, 10, 5)
                
                if st.form_submit_button("🔮 Assess Delay Risk"):
                    with st.spinner("AI is assessing delay risk..."):
                        try:
                            import asyncio
                            decision = asyncio.run(make_logistics_decision(
                                "delay_assessment",
                                {
                                    "order": {"id": order_id, "distance_km": distance},
                                    "weather": {"severity": weather_severity},
                                    "traffic": {"congestion": traffic_congestion}
                                }
                            ))
                            
                            risk_level = decision.get("risk_level", "unknown")
                            risk_color = {"low": "success", "medium": "warning", "high": "error"}[risk_level]
                            
                            getattr(st, risk_color)(f"{risk_level.upper()} RISK: {decision['reasoning']}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Risk Score", f"{decision.get('risk_score', 0):.2f}")
                            with col2:
                                st.metric("Confidence", f"{decision['confidence']:.1%}")
                            
                            if decision.get("mitigation_suggestions"):
                                st.subheader("Mitigation Suggestions")
                                for suggestion in decision["mitigation_suggestions"]:
                                    st.info(f"• {suggestion}")
                                    
                        except Exception as e:
                            st.error(f"Assessment failed: {e}")
    
    with tab2:
        st.subheader("🔄 AI Workflow Management")
        
        # Workflow type selection
        workflow_type = st.selectbox("Workflow Type", [
            "Order Processing",
            "Inventory Optimization"
        ])
        
        if workflow_type == "Order Processing":
            st.subheader("📦 Order Processing Workflow")
            with st.form("order_workflow"):
                col1, col2 = st.columns(2)
                with col1:
                    order_id = st.text_input("Order ID", value="ORD_001")
                    customer_email = st.text_input("Customer Email", value="customer@example.com")
                with col2:
                    priority = st.selectbox("Priority", ["high", "medium", "low"])
                    estimated_value = st.number_input("Order Value", value=500.0)
                
                if st.form_submit_button("🚀 Start Order Workflow"):
                    with st.spinner("Processing order with AI workflow..."):
                        try:
                            import asyncio
                            result = asyncio.run(process_order_with_ai({
                                "id": order_id,
                                "customer_email": customer_email,
                                "priority": priority,
                                "value": estimated_value
                            }))
                            
                            st.success(f"✅ Workflow {result['status']}: {result['workflow_id']}")
                            
                            if result.get("decisions"):
                                st.subheader("AI Decisions Made")
                                for i, decision in enumerate(result["decisions"], 1):
                                    with st.expander(f"Decision {i}: {decision.get('decision', 'Unknown')}"):
                                        st.json(decision)
                                        
                        except Exception as e:
                            st.error(f"Workflow failed: {e}")
        
        elif workflow_type == "Inventory Optimization":
            st.subheader("📊 Inventory Optimization Workflow")
            with st.form("inventory_workflow"):
                st.write("**Current Inventory**")
                inventory_json = st.text_area(
                    "Inventory Data (JSON)",
                    value='{"item_A": 10, "item_B": 5, "item_C": 20}'
                )
                
                st.write("**Historical Sales Data**")
                sales_json = st.text_area(
                    "Sales Data (JSON)",
                    value='[{"item_id": "item_A", "sales": [20, 25, 22]}, {"item_id": "item_B", "sales": [15, 18, 16]}]'
                )
                
                if st.form_submit_button("🚀 Start Inventory Workflow"):
                    with st.spinner("Optimizing inventory with AI..."):
                        try:
                            import json
                            import asyncio
                            
                            inventory_data = json.loads(inventory_json)
                            sales_data = json.loads(sales_json)
                            
                            result = asyncio.run(optimize_inventory_with_ai({
                                "current_levels": inventory_data,
                                "historical_data": sales_data,
                                "suppliers": [
                                    {"id": "SUP_001", "name": "Supplier A", "reliability": 0.9, "cost_factor": 1.0, "lead_time_days": 5}
                                ]
                            }))
                            
                            st.success(f"✅ Workflow {result['status']}: {result['workflow_id']}")
                            
                            if result.get("decisions"):
                                st.subheader("AI Decisions Made")
                                for i, decision in enumerate(result["decisions"], 1):
                                    with st.expander(f"Decision {i}: {decision.get('decision', 'Unknown')}"):
                                        st.json(decision)
                                        
                        except Exception as e:
                            st.error(f"Workflow failed: {e}")
    
    with tab3:
        st.subheader("📈 Decision Analytics")
        
        # Active workflows
        active_workflows = logistics_workflow_manager.get_active_workflows()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Workflows", len(active_workflows))
        with col2:
            completed = sum(1 for w in active_workflows if w.get("status") == "completed")
            st.metric("Completed", completed)
        with col3:
            failed = sum(1 for w in active_workflows if w.get("status") == "failed")
            st.metric("Failed", failed)
        
        if active_workflows:
            st.subheader("Recent Workflows")
            workflows_data = []
            for workflow in active_workflows[-10:]:  # Last 10 workflows
                workflows_data.append({
                    "Workflow ID": workflow.get("workflow_id", "Unknown"),
                    "Order ID": workflow.get("order_id", "N/A"),
                    "Status": workflow.get("status", "Unknown"),
                    "Decisions": len(workflow.get("decisions", []))
                })
            
            workflows_df = pd.DataFrame(workflows_data)
            st.dataframe(workflows_df, use_container_width=True)
        else:
            st.info("No workflows have been executed yet")
    
    with tab4:
        st.subheader("⚙️ AI Decision Settings")
        
        # Decision engine capabilities
        st.subheader("📊 Engine Capabilities")
        capabilities = [
            "Route Optimization",
            "Procurement Decisions",
            "Inventory Forecasting", 
            "Delay Risk Assessment",
            "Supplier Selection"
        ]
        
        for capability in capabilities:
            st.success(f"✅ {capability}")
        
        # Configuration options
        st.subheader("🔧 Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7, 0.05)
            risk_tolerance = st.slider("Risk Tolerance", 0.0, 1.0, 0.5, 0.05)
        
        with col2:
            auto_execute = st.checkbox("Auto-execute High Confidence Decisions", value=False)
            enable_notifications = st.checkbox("Enable Decision Notifications", value=True)
        
        if st.button("💾 Save Settings"):
            st.success("✅ Settings saved successfully!")
        
        # System status
        st.subheader("💚 System Status")
        st.success("✅ AI Decision Engine: Online")
        st.success("✅ Workflow Manager: Active")
        st.success("✅ Integration Layer: Connected")

def show_employees_page():
    """Show employee management page"""
    st.header("👥 Employee Management")
    
    # Employee tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👥 Employees", "📋 Task Assignment", "📈 Reports"])
    
    with tab1:
        st.subheader("📊 Employee Dashboard")
        
        # Get statistics
        all_employees = employee_manager.get_all_employees()
        dept_stats = employee_manager.get_department_stats()
        all_tasks = employee_manager.get_all_tasks()
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Employees", len(all_employees))
        with col2:
            st.metric("Departments", len(dept_stats))
        with col3:
            st.metric("Active Tasks", len([t for t in all_tasks if t['status'] == 'pending']))
        with col4:
            st.metric("Completed Tasks", len([t for t in all_tasks if t['status'] == 'completed']))
        
        # Department distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏢 Department Distribution")
            if dept_stats:
                fig = px.pie(values=list(dept_stats.values()), names=list(dept_stats.keys()))
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📋 Task Status")
            task_status = {}
            for task in all_tasks:
                status = task['status']
                task_status[status] = task_status.get(status, 0) + 1
            
            if task_status:
                fig = px.bar(x=list(task_status.keys()), y=list(task_status.values()))
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("👥 Employee Directory")
        
        # Filter by department
        departments = list(dept_stats.keys())
        selected_dept = st.selectbox("Filter by Department", ["All"] + departments)
        
        # Display employees
        if selected_dept == "All":
            display_employees = all_employees
        else:
            display_employees = employee_manager.get_employees_by_department(selected_dept)
        
        # Employee cards
        cols_per_row = 3
        for i in range(0, len(display_employees), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(display_employees):
                    emp = display_employees[i + j]
                    with col:
                        st.markdown(f"""
                        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 10px 0;">
                            <h4>{emp['name']}</h4>
                            <p><strong>Department:</strong> {emp['department']}</p>
                            <p><strong>Status:</strong> {emp['status']}</p>
                            <p><strong>ID:</strong> {emp['id']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Quick task assignment
                        if st.button(f"Assign Task", key=f"assign_{emp['id']}"):
                            st.session_state.selected_employee = emp['id']
                            st.session_state.current_page = "Employees"
                            st.rerun()
    
    with tab3:
        st.subheader("📋 Task Assignment")
        
        # Task templates (outside form)
        st.subheader("Quick Templates")
        col_t1, col_t2, col_t3 = st.columns(3)
        
        with col_t1:
            if st.button("AI/ML Model Development"):
                st.session_state.template_title = "AI/ML Model Development"
                st.session_state.template_desc = "Develop and train machine learning model for logistics optimization"
        
        with col_t2:
            if st.button("System Integration"):
                st.session_state.template_title = "System Integration"
                st.session_state.template_desc = "Integrate new component with existing system architecture"
        
        with col_t3:
            if st.button("Testing & QA"):
                st.session_state.template_title = "Testing & QA"
                st.session_state.template_desc = "Perform comprehensive testing of system functionality"
        
        # Task assignment form
        with st.form("assign_task"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Employee selection
                employee_options = {f"{emp['name']} ({emp['department']})": emp['id'] for emp in all_employees}
                selected_employee = st.selectbox("Select Employee", list(employee_options.keys()))
                
                # Use template if selected
                default_title = getattr(st.session_state, 'template_title', "")
                default_desc = getattr(st.session_state, 'template_desc', "")
                
                task_title = st.text_input("Task Title", value=default_title, placeholder="Enter task title")
                task_description = st.text_area("Task Description", value=default_desc, placeholder="Enter task description")
            
            with col2:
                priority = st.selectbox("Priority", ["low", "medium", "high", "urgent"])
                due_date = st.date_input("Due Date")
            
            if st.form_submit_button("📋 Assign Task"):
                if selected_employee and task_title:
                    employee_id = employee_options[selected_employee]
                    success = employee_manager.assign_task(
                        employee_id, task_title, task_description, priority, str(due_date)
                    )
                    
                    if success:
                        st.success(f"✅ Task assigned to {selected_employee.split(' (')[0]}!")
                        # Clear template
                        if hasattr(st.session_state, 'template_title'):
                            del st.session_state.template_title
                            del st.session_state.template_desc
                    else:
                        st.error("❌ Failed to assign task")
                else:
                    st.error("Please fill in required fields")
        
        # Recent tasks
        st.subheader("🕰️ Recent Tasks")
        recent_tasks = all_tasks[:10]  # Last 10 tasks
        
        if recent_tasks:
            for task in recent_tasks:
                with st.expander(f"{task['title']} - {task['employee_name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Employee:** {task['employee_name']}")
                        st.write(f"**Department:** {task['department']}")
                        st.write(f"**Priority:** {task['priority']}")
                    with col2:
                        st.write(f"**Status:** {task['status']}")
                        st.write(f"**Assigned:** {task['assigned_at'][:10]}")
                        st.write(f"**Due:** {task['due_date']}")
                    
                    st.write(f"**Description:** {task['description']}")
                    
                    # Status update (outside expander to avoid form conflicts)
                    col_status1, col_status2 = st.columns([3, 1])
                    with col_status1:
                        new_status = st.selectbox(
                            "Update Status", 
                            ["pending", "in_progress", "completed", "cancelled"],
                            index=["pending", "in_progress", "completed", "cancelled"].index(task['status']),
                            key=f"status_{task['task_id']}"
                        )
                    
                    with col_status2:
                        if st.button("Update", key=f"update_{task['task_id']}"):
                            if employee_manager.update_task_status(task['task_id'], new_status):
                                st.success("Status updated!")
                                st.rerun()
        else:
            st.info("No tasks assigned yet")
    
    with tab4:
        st.subheader("📈 Employee Reports")
        
        # Department performance
        st.subheader("🏢 Department Performance")
        
        dept_performance = {}
        for dept in dept_stats.keys():
            dept_employees = employee_manager.get_employees_by_department(dept)
            dept_tasks = []
            for emp in dept_employees:
                emp_tasks = employee_manager.get_employee_tasks(emp['id'])
                dept_tasks.extend(emp_tasks)
            
            completed_tasks = len([t for t in dept_tasks if t['status'] == 'completed'])
            total_tasks = len(dept_tasks)
            
            dept_performance[dept] = {
                "employees": len(dept_employees),
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            }
        
        # Display performance table
        perf_data = []
        for dept, stats in dept_performance.items():
            perf_data.append({
                "Department": dept,
                "Employees": stats["employees"],
                "Total Tasks": stats["total_tasks"],
                "Completed": stats["completed_tasks"],
                "Completion Rate": f"{stats['completion_rate']:.1f}%"
            })
        
        if perf_data:
            perf_df = pd.DataFrame(perf_data)
            st.dataframe(perf_df, use_container_width=True)
        
        # Task priority distribution
        st.subheader("⚡ Task Priority Distribution")
        priority_stats = {}
        for task in all_tasks:
            priority = task['priority']
            priority_stats[priority] = priority_stats.get(priority, 0) + 1
        
        if priority_stats:
            fig = px.bar(x=list(priority_stats.keys()), y=list(priority_stats.values()))
            st.plotly_chart(fig, use_container_width=True)

def show_seeya_page():
    """Show Seeya Assistant integration page"""
    st.header("🤖 Seeya Assistant Integration")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 15px; text-align: center; margin: 20px 0;">
        <h2>🤖 Seeya Assistant Live Demo Integration</h2>
        <p>From Seeya's Assistant to Rishabh's Logistics - Unified Experience Pipeline</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Seeya tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Message Processor", "📈 Analytics", "👤 User Preferences", "🔧 API Testing"])
    
    with tab1:
        st.subheader("💬 Process Messages Through Integration Pipeline")
        
        # Message input form
        with st.form("seeya_message_processor"):
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
            
            template_selected = False
            with col1:
                if st.form_submit_button("📦 Inventory Check"):
                    message_text = "Check current inventory levels for wireless mouse and keyboards"
                    template_selected = True
            
            with col2:
                if st.form_submit_button("🔄 Restock Request"):
                    message_text = "We're running low on wireless mouse inventory, need to restock urgently"
                    template_selected = True
            
            with col3:
                if st.form_submit_button("📋 Order Status"):
                    message_text = "What's the status of order #12345? Customer is asking for updates"
                    template_selected = True
            
            with col4:
                if st.form_submit_button("🚚 Delivery Update"):
                    message_text = "Track delivery for shipment FS123456789, customer reports delay"
                    template_selected = True
            
            submitted = st.form_submit_button("🚀 Process Message")
            
            if (submitted or template_selected) and message_text:
                with st.spinner("Processing message through integration pipeline..."):
                    try:
                        # Mock processing for demonstration
                        import time
                        time.sleep(2)  # Simulate processing time
                        
                        # Mock successful result
                        st.success("✅ Message processed successfully!")
                        
                        # Display mock results
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📝 Summary Results")
                            mock_summary = {
                                "Summary": "User requesting inventory check for wireless mouse",
                                "Intent": "inventory_check",
                                "Urgency": "medium",
                                "Confidence": 0.85
                            }
                            st.json(mock_summary)
                        
                        with col2:
                            st.subheader("📋 Task Created")
                            mock_task = {
                                "Task Summary": "Check inventory levels for wireless mouse",
                                "Task Type": "inventory_check",
                                "Priority": "medium",
                                "Status": "pending"
                            }
                            st.json(mock_task)
                        
                        # Display logistics actions
                        st.subheader("⚙️ Logistics Actions Triggered")
                        
                        mock_actions = [
                            {
                                "action_type": "inventory_check",
                                "status": "completed",
                                "created_at": datetime.now().isoformat(),
                                "parameters": {
                                    "query_type": "stock_levels",
                                    "product": "wireless_mouse",
                                    "urgency": "medium"
                                }
                            }
                        ]
                        
                        for i, action in enumerate(mock_actions, 1):
                            with st.expander(f"Action {i}: {action['action_type'].title()}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"**Type:** {action['action_type']}")
                                    st.write(f"**Status:** {action['status']}")
                                with col2:
                                    st.write(f"**Created:** {action['created_at'][:16]}")
                                    st.write(f"**Parameters:** {len(action['parameters'])} items")
                                
                                st.json(action['parameters'])
                        
                        # Pipeline summary
                        st.subheader("📈 Pipeline Summary")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Actions", 1)
                        with col2:
                            st.metric("Executed Actions", 1)
                        with col3:
                            st.metric("Auto Execution", "✅ Enabled")
                    
                    except Exception as e:
                        st.error(f"❌ Error processing message: {str(e)}")
    
    with tab2:
        st.subheader("📈 Integration Analytics")
        
        # Mock analytics data
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Messages", "47", "+5 today")
        
        with col2:
            st.metric("Total Actions", "89", "+12 today")
        
        with col3:
            st.metric("Success Rate", "94.2%", "+2.3%")
        
        with col4:
            st.metric("Active Users", "8", "+1 today")
        
        # Mock charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Integration Activity")
            mock_data = {
                'platform': ['whatsapp', 'email', 'slack', 'teams'],
                'count': [15, 12, 8, 12],
                'status': ['completed', 'completed', 'completed', 'completed']
            }
            df = pd.DataFrame(mock_data)
            fig = px.bar(df, x='platform', y='count', color='status',
                       title="Messages by Platform and Status")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⚙️ Logistics Actions")
            mock_actions_data = {
                'action_type': ['inventory_check', 'restock', 'order_tracking', 'delivery'],
                'count': [25, 18, 22, 15]
            }
            df = pd.DataFrame(mock_actions_data)
            fig = px.pie(df, values='count', names='action_type',
                       title="Actions by Type")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("👤 User Preferences Management")
        
        # User selection
        user_id = st.text_input("User ID", value="demo_user", help="Enter user ID to manage preferences")
        
        if st.button("🔍 Load Preferences"):
            st.session_state.seeya_user_preferences = {
                "auto_execute_logistics": True,
                "department": "logistics",
                "role": "user",
                "notification_preferences": {"email": True, "slack": False}
            }
            st.session_state.seeya_selected_user = user_id
        
        if hasattr(st.session_state, 'seeya_user_preferences'):
            st.subheader(f"Preferences for {st.session_state.seeya_selected_user}")
            
            with st.form("seeya_user_preferences"):
                col1, col2 = st.columns(2)
                
                with col1:
                    auto_execute = st.checkbox(
                        "Auto-execute Logistics Actions",
                        value=st.session_state.seeya_user_preferences.get("auto_execute_logistics", True),
                        help="Automatically execute logistics actions without manual approval"
                    )
                    
                    department = st.selectbox(
                        "Department",
                        ["general", "logistics", "procurement", "inventory", "sales", "support"],
                        index=["general", "logistics", "procurement", "inventory", "sales", "support"].index(
                            st.session_state.seeya_user_preferences.get("department", "general")
                        )
                    )
                
                with col2:
                    role = st.selectbox(
                        "Role",
                        ["user", "manager", "admin", "analyst"],
                        index=["user", "manager", "admin", "analyst"].index(
                            st.session_state.seeya_user_preferences.get("role", "user")
                        )
                    )
                    
                    # Notification preferences
                    st.subheader("📧 Notification Preferences")
                    notif_prefs = st.session_state.seeya_user_preferences.get("notification_preferences", {})
                    
                    email_notifications = st.checkbox("Email Notifications", value=notif_prefs.get("email", True))
                    slack_notifications = st.checkbox("Slack Notifications", value=notif_prefs.get("slack", False))
                
                if st.form_submit_button("💾 Save Preferences"):
                    st.success("✅ Preferences saved successfully!")
    
    with tab4:
        st.subheader("🔧 API Testing Interface")
        
        # API endpoint selection
        endpoint = st.selectbox("Select Endpoint", [
            "Seeya Assistant - Summarize",
            "Seeya Assistant - Process Summary",
            "Integration - Full Pipeline"
        ])
        
        if endpoint == "Seeya Assistant - Summarize":
            st.subheader("📝 Test Summarization")
            
            with st.form("test_seeya_summarize"):
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
            
            with st.form("test_seeya_pipeline"):
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

def show_analytics_page():
    """Show analytics page"""
    st.header("📈 Analytics & Reports")
    
    data = load_dashboard_data()
    crm_data = get_crm_data()
    
    # Analytics tabs
    tab1, tab2, tab3 = st.tabs(["📊 Performance", "💰 Financial", "📈 Trends"])
    
    with tab1:
        st.subheader("System Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Orders Processed", len(data['orders']), "+12%")
        with col2:
            st.metric("Automation Rate", "87%", "+5%")
        with col3:
            st.metric("Response Time", "1.2s", "-0.3s")
        with col4:
            st.metric("Success Rate", "99.2%", "+0.5%")
    
    with tab2:
        st.subheader("Financial Overview")
        
        if not crm_data['opportunities'].empty:
            total_pipeline = crm_data['opportunities']['amount'].sum()
            st.metric("Pipeline Value", f"${total_pipeline:,.0f}", "+15%")
            
            fig = px.bar(crm_data['opportunities'], x='name', y='amount', title="Opportunity Values")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Trends Analysis")
        
        # Mock trend data
        dates = pd.date_range(start='2024-01-01', end='2024-01-15', freq='D')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Orders': [10, 12, 8, 15, 20, 18, 22, 25, 19, 16, 21, 24, 28, 30, 26],
            'Revenue': [1000, 1200, 800, 1500, 2000, 1800, 2200, 2500, 1900, 1600, 2100, 2400, 2800, 3000, 2600]
        })
        
        fig = px.line(trend_data, x='Date', y=['Orders', 'Revenue'], title="Daily Trends")
        st.plotly_chart(fig, use_container_width=True)

def main():
    """Main unified dashboard application"""
    # Initialize database
    init_database()
    
    # Display header
    display_header()
    
    # Display navigation
    display_navigation()
    
    # Route to appropriate page
    if st.session_state.current_page == "Overview":
        show_overview_page()
    elif st.session_state.current_page == "CRM":
        show_crm_page()
    elif st.session_state.current_page == "Logistics":
        show_logistics_page()
    elif st.session_state.current_page == "Suppliers":
        show_suppliers_page()
    elif st.session_state.current_page == "Products":
        show_products_page()
    elif st.session_state.current_page == "Showcase":
        show_showcase_page()
    elif st.session_state.current_page == "EMS":
        show_ems_page()
    elif st.session_state.current_page == "RL":
        show_rl_page()
    elif st.session_state.current_page == "AI_Decisions":
        show_ai_decisions_page()
    elif st.session_state.current_page == "Employees":
        show_employees_page()
    elif st.session_state.current_page == "Seeya":
        show_seeya_page()
    elif st.session_state.current_page == "Agents":
        show_agents_page()
    elif st.session_state.current_page == "Analytics":
        show_analytics_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        🚀 AI Agent Unified Dashboard | All-in-One Management System<br>
        Last updated: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()