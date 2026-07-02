import streamlit as st
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv, find_dotenv  

from eda import get_KPI, Order_Info
from analysis import get_dashboard_kpi, get_cancellation_analysis
from apply_recommendations import get_KPI_Optimized

load_dotenv(find_dotenv())
# ==========================================
# CONFIG & THEME CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Supply Chain OTD Optimization Story",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Directory path to the visual assets
VISUAL_BOX_DIR = "visual_box"

# ==========================================
# SIDEBAR - GLOBAL FILTERS OR PROJECT INFO
# ==========================================
with st.sidebar:
    st.image("https://img.shields.io/badge/License-MIT-yellow.svg", width="content")
    st.title("🚚 Logistics Pipeline")
    st.markdown("""
    Analysis and simulation application for optimizing **On-Time Delivery (OTD)** performance.
    
    * **Primary Dataset:** DataCo Supply Chain Dataset (2015-2018)
    * **Tech Stack:** Python, MySQL, Docker
    """)
    st.markdown("---")
    st.info("💡 Tip: Navigate through the tabs above to move from Current Baseline to Root Cause Diagnosis and Optimization Simulation.")
    st.markdown("---")
    note = os.environ.get("note", "...")
    st.info(note)


# ==========================================
# MAIN DASHBOARD TITLE
# ==========================================
st.title("🚚 Logistics On-Time Delivery (OTD) Root Cause Analysis")
st.markdown("---")


# ==========================================
# INITIALIZE DASHBOARD TABS
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "📊 Operational KPIs (Baseline)", 
    "🔍 Root Cause Analysis", 
    "🚀 Optimization Simulation"
])


# ==========================================
# TAB 1: OPERATIONAL KPIs (BASELINE)
# ==========================================
with tab1:
    st.subheader("1. Order Index")
    try:
        index = Order_Info()
        
        cols = st.columns(len(index))

        for idx, col in enumerate(cols):
            with col:
                # Extract row data using .iloc
                mode_name = index.iloc[idx]["Shipping Mode"]
                quantity = index.iloc[idx]["Order_quantity_by_mode"]
                sales = index.iloc[idx]["Total_sales_by_mode"]
                perc_used = index.iloc[idx]["Perc_used"] * 100 
                
                # Design UI block for each Shipping Mode
                st.markdown(f"#### 🚚 {mode_name}")
                
                # Display Order Quantity (With percentage distribution as delta)
                st.metric(
                    label="Order Quantity", 
                    value=f"{int(quantity):,}", 
                    delta=f"{perc_used:.0f}% of total volume",
                    delta_color="off"
                )
                
                # Display Revenue (Currency formatted with $ and thousands separators)
                st.metric(
                    label="Total Sales", 
                    value=f"${sales:,.2f}"
                )
            
    except Exception as e:
        st.error(f"Failed to load Order Index data: {e}")
    
    st.markdown("---")

    st.subheader("2. Current Shipping Performance Metrics")
    
    # Retrieve current KPIs from eda.py
    try:
        kpi_df = get_KPI()
        
        # Create 3 columns for executive metric cards
        col1, col2, col3 = st.columns(3)
        with col1:
            # Baseline OTD Rate
            st.metric(label="Overall OTD Rate", value=kpi_df.loc[kpi_df["Metric"] == "Overall OTD Rate", "Value"].values[0])
        with col2:
            # Late Delivery Rate
            st.metric(label="Late Delivery Rate", value=kpi_df.loc[kpi_df["Metric"] == "Late Delivery Rate", "Value"].values[0], delta="High Risk", delta_color="inverse")
        with col3:
            # Average Delay Days
            st.metric(label="Average Delay Days", value=kpi_df.loc[kpi_df["Metric"] == "Average Delay Days", "Value"].values[0])
            
    except Exception as e:
        st.error(f"Failed to load Operational KPIs: {e}")
        
    st.markdown("---")
    

    # Display baseline visual insights
    st.subheader("3. Shipping Performance and Trend Visualization")
    try:
        c1, c2 = st.columns(2)
        
        with c1:
            img_path = os.path.join(VISUAL_BOX_DIR, "shipping_performance_chart.png")
            if os.path.exists(img_path):
                st.image(img_path, width="content")  
                
        with c2:
            img_path = os.path.join(VISUAL_BOX_DIR, "shipping_mode_trend.png")
            if os.path.exists(img_path):
                st.image(img_path, width="content") 
    except Exception as e:
        st.error(f"Failed to load visual images: {e}")
    

# ==========================================
# TAB 2: ROOT CAUSE DIAGNOSTICS
# ==========================================
with tab2:
    st.subheader("🔍 Operational Crisis in Express & Premium Logistics Channels")
    st.markdown("""
    * **The First Class Paradox:** Despite being designated as a premium, high-priority service, it suffers from a systemic bottleneck, with delays breaching the critical **95%+** threshold.
    * **Hidden Delay Triggering Cancellations:** 100% of customer-initiated cancellations within the First Class segment directly correlate with backend, uncommunicated shipping delays.
    """)
    
    st.info("""
    💡 **Executive Summary:** This tab diagnostic isolates why premium delivery tiers are underperforming. 
    The metrics below pinpoint the strict correlation between SLA breaches, automated customer attrition (cancellations), and the subsequent financial leakage across core regions and categories.
    """)

    st.markdown("---")
    st.subheader("Overall Fulfillment vs. Cancellation Rates")

    try:
        cnxl_rate = get_dashboard_kpi()
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Order Completion Rate", value=cnxl_rate.iloc[0,0])
        with col2:
            st.metric(label="Order Cancellation Rate", value=cnxl_rate.iloc[0,1], delta="Action Required", delta_color="inverse")
    except Exception as e:
        st.error(f"Failed to load Cancellation Dashboard KPIs: {e}")


    st.markdown("---")
    st.subheader("SLA Gap Analysis Across Shipping Modes")
    
    st.caption("📈 **Visualizing the Breakdown:** The charts below highlight the magnitude of target vs. actual transit times (SLA Gap) and quantify how severely delayed shipments escalate cancellation behaviors.")

    try:
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            img_path = os.path.join(VISUAL_BOX_DIR, "SLA_gap.png")
            if os.path.exists(img_path):
                st.image(img_path, width="content")  
        with chart_col2:
            img_path = os.path.join(VISUAL_BOX_DIR, "delay_rate_canceled_orders.png")
            if os.path.exists(img_path):
                st.image(img_path, width="content") 
    except Exception as e:
        st.error(f"Failed to load visual charts: {e}")

    st.markdown("---")
    st.subheader("Revenue Leakage: Financial Impact of Canceled Orders")

    try:
        RL_index = get_cancellation_analysis()[0]
        
        cols = st.columns(len(RL_index))

        for idx, col in enumerate(cols):
            with col:
                # Extract row data using .iloc
                mode_name = RL_index.iloc[idx]["Shipping Mode"]
                Total_contribution = RL_index.iloc[idx]["Total_contribution"]
                Total_sales_lost = RL_index.iloc[idx]["Total_sales_lost"]
                Loss_Proportion = RL_index.iloc[idx]["Loss_Proportion"]

                # Design UI block for each Shipping Mode
                st.markdown(f"#### 🚚 {mode_name}")
                
                # Display Order Quantity (With percentage distribution as delta)
                st.metric(
                    label="Cancellation Volume", 
                    value=f"{int(Total_contribution):,}"
                )
                
                # Display Revenue (Currency formatted with $ and thousands separators)
                st.metric(
                    label="Total Sales Lost", 
                    value=f"${Total_sales_lost:,.2f}",
                    delta=f"{Loss_Proportion:.0f}% of total loss",
                    delta_color="inverse"
                )
            
    except Exception as e:
        st.error(f"Failed to load Revenue Loss (RL) Index data: {e}")


    st.markdown("---")
    st.subheader("Risk Exposure: Category & Regional Dependencies")
    
    st.warning("⚠️ **Vulnerability Alert:** Particular product segments and geography clusters act as multipliers for shipping delays, making them focal points for immediate operational restructuring.")

    try:
        chart_col3, chart_col4 = st.columns(2)
        with chart_col3:
            img_path = os.path.join(VISUAL_BOX_DIR, "category_dependency_FC.png")
            if os.path.exists(img_path):
                # Translated caption to English
                st.image(img_path, caption="Product Category Dependency & Operational Delay Risks", width="content")
        with chart_col4:
            img_path = os.path.join(VISUAL_BOX_DIR, "region_dependency_FC.png")
            if os.path.exists(img_path):
                # Translated caption to English
                st.image(img_path, caption="Geographical Dependency & Regional Logistics Delay Risks", width="content")
    except Exception as e:
        st.error(f"Failed to load dependency charts: {e}")

# ==========================================
# TAB 3: OPTIMIZATION SCENARIO SIMULATION
# ==========================================
with tab3:
    st.subheader("🚀 What-If Simulation: 3 Pillars of Logistics Optimization")
    st.markdown("""
    The system reconfigures the dataset based on three core strategic levers:
    1. **SLA Buffer Realignment:** Injecting a +1 day realistic operational buffer to the *First Class* target.
    2. **Network Consolidation:** Merging *Second Class* and *Standard Class* into a single tier (**Standard_Eco**) due to a lack of statistically significant performance variance.
    3. **Operational Segregation:** Isolating and dedicating custom technical workflows exclusively for high-priority *Same Day* deliveries.
    """)
    

    st.info("""
    💡 **Simulation Framework:** This comparative layout projects data outcomes if structural changes are deployed. 
    By stabilizing the *First Class* target margins and consolidating low-variance channels, the model estimates major recoveries in reliability and margin protection.
    """)
    
    # Visualizing the Before vs. After comparison table
    try:
        kpi_before = get_KPI()
        kpi_after = get_KPI_Optimized()
        
        # Merge dataframes for direct side-by-side comparison
        comparison_df = pd.merge(kpi_before, kpi_after, on="Metric", suffixes=(" (Pre-Optimization)", " (Post-Simulation)"))
        st.dataframe(comparison_df, width="content")
        
    except Exception as e:
        st.error(f"Failed to load simulation benchmarking matrix: {e}")
        
    st.markdown("---")
    st.subheader("📈 Projected Recovery: Global Fleet Fulfillment Metrics")
    
    st.caption("🎯 **Key Takeaway:** Notice the structural recovery shift below. The modeled baseline narrows the gap between promised delivery windows and actual execution capacity.")

    # Core charts proving Before vs After efficacy
    try:
        chart_col5, chart_col6 = st.columns(2)
        with chart_col5:
            img_path = os.path.join(VISUAL_BOX_DIR, "Before_After_SLA.png")
            if os.path.exists(img_path):
                st.image(img_path, caption="Comparative Assessment: Logistics Operational Capacity Recovery (Pre vs. Post)", width="content")
        with chart_col6:
            img_path = os.path.join(VISUAL_BOX_DIR, "Shipping_trend_optimized.png")
            if os.path.exists(img_path):
                st.image(img_path, caption="Recovered Shipping Mode Trend", width="content")
    except Exception as e:
        st.error(f"Failed to load optimized charts: {e}")