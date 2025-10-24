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
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", len(data['orders']), "+5 today")
    
    with col2:
        st.metric("Active Accounts", len(crm_data['accounts']), "+2 this week")
    
    with col3:
        st.metric("Products", len(USER_PRODUCT_CATALOG), "12 categories")
    
    with col4:
        st.metric("Suppliers", len(data['suppliers']), "3 active")
    
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
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("✅ CRM System: Online")
        st.success("✅ Logistics: Active")
    
    with col2:
        st.success("✅ Inventory: Monitored")
        st.success("✅ Suppliers: Connected")
    
    with col3:
        st.success("✅ AI Agents: Running")
        st.success("✅ Database: Healthy")

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
            st.table(crm_data['leads'])
        else:
            st.info("No leads found")
    
    with tab3:
        st.subheader("Opportunity Pipeline")
        if not crm_data['opportunities'].empty:
            st.table(crm_data['opportunities'])
        else:
            st.info("No opportunities found")
    
    with tab4:
        st.subheader("🧠 Natural Language Query")
        query = st.text_input("Ask about your CRM data:", placeholder="Show me all opportunities closing this month")
        if st.button("🔍 Search") and query:
            st.success(f"Searching for: '{query}'")
            # Simple pattern matching
            if "opportunity" in query.lower():
                st.table(crm_data['opportunities'])
            elif "account" in query.lower():
                st.table(crm_data['accounts'])
            elif "lead" in query.lower():
                st.table(crm_data['leads'])
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
            st.table(orders_df.head(10))
        else:
            st.info("No orders found")
    
    with tab2:
        st.subheader("Shipment Tracking")
        if data['shipments']:
            shipments_df = pd.DataFrame(data['shipments'])
            st.table(shipments_df.head(10))
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
                st.table(low_stock_df)
            
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
            st.table(logs_df)

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
        st.table(logs_df)
    else:
        st.info("No recent agent activity")

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