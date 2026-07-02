import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import functools
import numpy as np

from eda import Late_Perc_Group, Order_Info, Late_Perc_Period
from analysis import get_shipping_analysis, get_cancellation_analysis, get_category_analysis, get_region_analysis
from apply_recommendations import Late_Perc_Period_Optimized
#======================================================
def save_chart_automatically(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

        file_name = f"{func.__name__}.png"
        output_dir = "visual_box"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, file_name)

        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        print(f"🚀 The image exported: {file_path}")

    return wrapper

#EDA
@save_chart_automatically
def shipping_performance_chart():
    # 1. Initialize data fromthe EDA module
    df = Late_Perc_Group()[0]

    # Sort by SLA (scheduled_lead_time) ascending for a clean upward line trend
    df = df.sort_values("scheduled_lead_time").reset_index(drop=True)

    # 2. Initialize Figure and Canvas
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=100)
    fig.patch.set_facecolor("#ffffff")
    ax1.set_facecolor("#ffffff")

    # --- COLOR PALETTE ---
    COLOR_BAR = "#1B365D"   # Deep Navy Blue 
    COLOR_LINE = "#D9A05B"  # Soft Amber / Muted Gold 

    # Turn off gridlines
    ax1.grid(False)

    # 3. PLOT BARS (Left Y-Axis - Delay Rate %)
    bars = ax1.bar(
        df["Shipping Mode"],
        df["Perc_Delay"] * 100,
        color=COLOR_BAR,
        alpha=0.9,
        width=0.4,
        label="Delay Rate (%)",
    )

    ax1.set_xlabel("Shipping Mode", fontsize=11, fontweight="bold", labelpad=12, color="#333333")
    ax1.set_ylabel("Delay Rate (%)", color=COLOR_BAR, fontsize=11, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor=COLOR_BAR)
    ax1.set_ylim(0, 110)

    # Add Data Labels on top of each Bar
    for bar in bars:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 2,
            f"{height:.1f}%",
            ha="center",
            va="bottom",
            fontweight="bold",
            color=COLOR_BAR,
        )

    # 4. PLOT LINE (Right Y-Axis - SLA Lead Time Days)
    ax2 = ax1.twinx()
    ax2.grid(False) # Ensure the secondary axis doesn't generate a grid

    line = ax2.plot(
        df["Shipping Mode"],
        df["scheduled_lead_time"],
        color=COLOR_LINE,
        marker="o",
        linewidth=3.5,
        markersize=9,
        label="Scheduled Lead Time (Days)",
    )

    ax2.set_ylabel("Scheduled Lead Time (Days)", color=COLOR_LINE, fontsize=11, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor=COLOR_LINE)
    ax2.set_ylim(-0.5, 5)

    # Add Data Labels right above the Line markers
    for i, txt in enumerate(df["scheduled_lead_time"]):
        ax2.annotate(
            f"{txt} Day(s)",
            (df["Shipping Mode"][i], df["scheduled_lead_time"][i]),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontweight="bold",
            color=COLOR_LINE,
        )

    # 5. Title & Aesthetics Clean-up
    plt.title(
        "SHIPPING PERFORMANCE ANALYSIS\nDelay Rate and Scheduled Lead Time (SLA)",
        fontsize=13,
        fontweight="bold",
        pad=22,
        color="#1B365D",
    )

    # Hide unnecessary chart borders (Spines) for an executive look
    for ax in [ax1, ax2]:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_color("#ffffff") # Clean base line
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
@save_chart_automatically
def order_insights():
    # 1. Initialize data fromthe EDA module
    df = Order_Info()

    # 2. Initialize side-by-side subplots (1 row, 2 columns) sharing the Y-axis
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), sharey=True, dpi=100)
    fig.patch.set_facecolor("#ffffff")

    # --- EXECUTIVE COLOR PALETTE ---
    COLOR_QTY = "#4A7BB0"    # Muted Slate Blue for Order Quantity
    COLOR_SALES = "#1B365D"  # Deep Navy Blue for Total Sales Volume

    # --- SUBPLOT 1: TOTAL ORDER QUANTITY (Left) ---
    ax1.set_facecolor("#ffffff")
    ax1.grid(False)
    bars1 = ax1.barh(df["Shipping Mode"], df["Order_quantity_by_mode"], color=COLOR_QTY, height=0.55)
    ax1.set_title("TOTAL ORDER QUANTITY", fontsize=11, fontweight="bold", color="#555555", pad=15)

    # Add Data Labels for the left subplot
    for bar in bars1:
        width = bar.get_width()
        ax1.text(
            width + max(df["Order_quantity_by_mode"]) * 0.02,
            bar.get_y() + bar.get_height()/2,
            f"{int(width):,}",
            ha="left", va="center", fontsize=10, fontweight="bold", color=COLOR_QTY
        )

    # --- SUBPLOT 2: TOTAL SALES VOLUME (Right) ---
    ax2.set_facecolor("#ffffff")
    ax2.grid(False)
    bars2 = ax2.barh(df["Shipping Mode"], df["Total_sales_by_mode"], color=COLOR_SALES, height=0.55)
    ax2.set_title("TOTAL SALES VOLUME ($)", fontsize=11, fontweight="bold", color="#1B365D", pad=15)

    # Add Data Labels for the right subplot (Formatted in Millions of USD)
    for bar in bars2:
        width = bar.get_width()
        ax2.text(
            width + max(df["Total_sales_by_mode"]) * 0.02,
            bar.get_y() + bar.get_height()/2,
            f"${width/1e6:.2f}M",
            ha="left", va="center", fontsize=10, fontweight="bold", color=COLOR_SALES
        )

    # 3. Clean up axes and spines
    for ax in [ax1, ax2]:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_color("#cccccc")
        ax.get_xaxis().set_visible(False)  # Hide X-axis completely since data labels are visible

    # Format the shared Y-axis labels
    ax1.tick_params(axis="y", labelsize=11, color="#333333")
    for label in ax1.get_yticklabels():
        label.set_weight("bold")

    # Extend X-axis limits slightly to prevent data labels from being clipped
    ax1.set_xlim(0, max(df["Order_quantity_by_mode"]) * 1.2)
    ax2.set_xlim(0, max(df["Total_sales_by_mode"]) * 1.2)

    # 4. Add the overarching main title
    plt.suptitle(
        "ORDER INSIGHTS BY SHIPPING MODE\nSide-by-Side Distribution Analysis",
        fontsize=14, fontweight="bold", color="#1B365D", y=1.05
    )
@save_chart_automatically
def overall_KPI_dashboard():
    # 1. Initialize raw data from the OVERALL KPI table
    data_kpi = {
        "Metric": [
            "Overall OTD Rate", 
            "Late Delivery Rate", 
            "Average Actual Lead Time", 
            "Average Scheduled Lead Time", 
            "Average Delay Days"
        ],
        "Value": [45.17, 54.83, 3.50, 2.93, 0.93]
    }
    df_all = pd.DataFrame(data_kpi)

    # Split the dataset into two subsets for the independent subplots
    df_left = df_all.iloc[0:2].copy()   # OTD and Late Rates (%)
    df_right = df_all.iloc[2:5].copy()  # Time-based metrics (Days)

    # 2. Initialize dual-plot canvas (1 row, 2 columns)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5), dpi=100)
    fig.patch.set_facecolor("#ffffff")

    # --- NAVY COLOR PALETTE ---
    NAVY_DARK = "#1B365D"   # Deep Navy for OTD and Actual Lead Time (Primary)
    NAVY_LIGHT = "#4A7BB0"  # Light Navy/Slate for Scheduled Lead Time
    AMBER_ALERT = "#D9A05B" # Amber/Sand gold for Late/Delay metrics 

    # Completely disable grid lines on both subplots
    ax1.grid(False)
    ax2.grid(False)

    # =========================================================
    # 📊 LEFT SUBPLOT: COMPARING OTD VS LATE DELIVERY RATE
    # =========================================================
    ax1.set_facecolor("#ffffff")

    # Render horizontal bar chart using Seaborn
    sns.barplot(
        x="Value", 
        y="Metric", 
        data=df_left, 
        ax=ax1, 
        palette=[NAVY_DARK, AMBER_ALERT],
        hue="Metric",           
        legend=False,
        height=0.5
    )

    ax1.set_title("DELIVERY PERFORMANCE RATIO", fontsize=11, fontweight="bold", color="#555555", pad=15)
    ax1.set_xlim(0, 100) # Percentage scale from 0 to 100

    # Add Data Labels (%) directly onto the horizontal bars
    for p in ax1.patches:
        width = p.get_width()
        ax1.text(
            width + 2, 
            p.get_y() + p.get_height() / 2, 
            f"{width:.2f}%", 
            ha="left", va="center", fontsize=10, fontweight="bold",
            color=NAVY_DARK if width < 50 else AMBER_ALERT
        )

    # =========================================================
    # 📊 RIGHT SUBPLOT: LEAD TIME DETAILS & DELAY DAYS
    # =========================================================
    ax2.set_facecolor("#ffffff")

    # Render vertical bar chart using Seaborn
    sns.barplot(
        x="Metric", 
        y="Value", 
        data=df_right, 
        ax=ax2, 
        palette=[NAVY_DARK, NAVY_LIGHT, AMBER_ALERT],
        hue="Metric",
        legend=False,
        width=0.45
    )

    ax2.set_title("CYCLE TIME ANALYSIS (DAYS)", fontsize=11, fontweight="bold", color=NAVY_DARK, pad=15)
    # Shorten X-axis labels for a cleaner corporate presentation layout
    ax2.set_xticks([0, 1, 2])
    ax2.set_xticklabels(["Actual Lead Time", "Scheduled Lead Time", "Average Delay"], fontsize=10, fontweight="bold")

    # Add Data Labels (Days) on top of the vertical bars
    for p in ax2.patches:
        height = p.get_height()
        if height > 0:
            ax2.text(
                p.get_x() + p.get_width() / 2., 
                height + 0.1, 
                f"{height:.2f} d", 
                ha="center", va="bottom", fontsize=10, fontweight="bold", color="#333333"
            )

    # =========================================================
    # 🛠️ EXECUTIVE STYLE AESTHETIC REFINEMENTS
    # =========================================================
    for ax in [ax1, ax2]:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color("#cccccc")
        ax.spines["left"].set_visible(False)
        ax.get_xaxis().set_visible(False) if ax == ax1 else ax.get_yaxis().set_visible(False)

    # Custom formatting for the left subplot's Y-axis labels
    ax1.tick_params(axis="y", labelsize=11, color="#333333")
    for label in ax1.get_yticklabels():
        label.set_weight("bold")

    # Expand Y-axis headroom for the right subplot to avoid data label clipping
    ax2.set_ylim(0, max(df_right["Value"]) * 1.15)

    # Main overarching title for the KPI Dashboard
    plt.suptitle(
        "LOGISTICS OPERATIONS OVERALL KPI DASHBOARD\nPerformance Rates & Lead Time Benchmarks",
        fontsize=14, fontweight="bold", color=NAVY_DARK, y=1.05
    )
@save_chart_automatically
def category_OTD_rank():
    # 1. Load data
    df = Late_Perc_Group()[1]
    df = df.head(10)
    # 2. Initialize canvas
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    # Disable grid lines
    ax.grid(False)

    # color pallete
    COLOR_NAVY_DARK = "#1B365D"

    # 3. Render horizontal bar chart using Seaborn (Swapping x and y)
    sns.barplot(
        x="Perc_Delay", 
        y="Category Name", 
        data=df, 
        ax=ax, 
        color=COLOR_NAVY_DARK,
        height=0.55  # Use height instead of width for horizontal bars
    )

    # 4. Title and Axis adjustments
    ax.set_title("TOP 10 PRODUCT CATEGORIES WITH HIGHEST DELAY RATE", fontsize=12, fontweight="bold", color=COLOR_NAVY_DARK, pad=20)
    ax.set_ylabel("", visible=False)  # Hide redundant Y-axis label
    ax.set_xlabel("", visible=False)  # Hide redundant X-axis label

    # Format Y-axis tick labels (Category names are now perfectly horizontal)
    ax.tick_params(axis="y", labelsize=10, color="#333333")
    for label in ax.get_yticklabels():
        label.set_weight("bold")

    # 5. Add Data Labels (%) to the right end of each bar
    for p in ax.patches:
        width = p.get_width()
        ax.text(
            width + 0.015,  # Slight offset to the right of the bar tip
            p.get_y() + p.get_height() / 2, 
            f"{width*100:.1f}%", 
            ha="left", va="center", fontsize=10, fontweight="bold", color=COLOR_NAVY_DARK
        )

    # 6.  Style Clean-up
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)  # Hide bottom spine since data labels are used
    ax.spines["left"].set_color("#cccccc")  # Keep a clean left border line
    ax.get_xaxis().set_visible(False)       # Hide X-axis entirely

    # Extend X-axis headroom to prevent data labels from being clipped
    ax.set_xlim(0, max(df["Perc_Delay"]) * 1.15)
@save_chart_automatically
def shipping_mode_trend():
    # 1. Load trend dataset from the EDA module
    df_trend = Late_Perc_Period()[0]

    # 2. Initialize a single-plot canvas
    fig, ax = plt.subplots(figsize=(14, 6), dpi=100)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    # Disable grid lines
    ax.grid(False)

    # Distinct color palette 
    PALETTE_TREND = {
        "First Class": "#D9A05B",     # Amber (Highest risk category)
        "Second Class": "#4A7BB0",    # Slate Blue
        "Standard Class": "#1B365D",  # Standard Deep Navy
        "Same Day": "#708090"         # Charcoal Gray
    }

    # 3. Render the trend lines using Seaborn
    sns.lineplot(
        x="year_month", 
        y="Late_delivery_risk", 
        hue="Shipping Mode", 
        data=df_trend, 
        ax=ax, 
        palette=PALETTE_TREND,
        linewidth=2.5,
        marker="o",
        markersize=5
    )

    # 4. Configure title and axis labels
    COLOR_NAVY_DARK = "#1B365D"
    ax.set_title("LATE DELIVERY RISK TREND BY SHIPPING MODE (2015 - 2018)", fontsize=12, fontweight="bold", color=COLOR_NAVY_DARK, pad=20)
    ax.set_xlabel("Timeline (Year-Month)", fontsize=10, fontweight="bold", labelpad=12)
    ax.set_ylabel("Late Delivery Risk Rate", fontsize=10, fontweight="bold")

    # Format Y-axis to display as percentages
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda y, loc: f"{int(y*100)}%"))

    # Thin out X-axis tick labels (display every 3 months) to prevent overlapping text
    all_ticks = df_trend["year_month"].unique()
    thinned_ticks = all_ticks[::3]
    ax.set_xticks(thinned_ticks)
    ax.set_xticklabels(thinned_ticks, rotation=35, ha="right", fontsize=9, color="#333333")

    # 5. Fine-tune the legend placement
    ax.legend(title="Shipping Mode", title_fontsize=10, fontsize=9, loc="upper left", bbox_to_anchor=(1, 1), frameon=False)

    # 6. Clean up chart borders (spines)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.spines["bottom"].set_color("#cccccc")
    ax.set_ylim(0, 1.05)

#Analysis
@save_chart_automatically
def SLA_gap():
    df = get_shipping_analysis()

    df_sla = df.reindex(columns=["Shipping Mode", "frequent_actual", "scheduled_lead_time"]).rename(columns={"frequent_actual": "Common_lead_time", "scheduled_lead_time": "Scheduled Time"})


    x = np.arange(len(df_sla["Shipping Mode"]))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    # Plot the pair of scheduled vs. actual delivery bars
    rects1 = ax.bar(x - width/2, df_sla["Scheduled Time"], width, label="Scheduled Lead Time", color="#BACAD6")
    rects2 = ax.bar(x + width/2, df_sla["Common_lead_time"], width, label="Common_lead_time", color="#1B365D")

    # Highlight the First Class section with a dashed bounding box
    rect = plt.Rectangle((-0.4, -0.1), 0.8, 2.4, fill=False, edgecolor="#D94E4E", linestyle="--", linewidth=1.5)
    ax.add_patch(rect)
    ax.text(0, 2.45, "SLA BREACHED: TIME DOUBLED!", ha="center", va="bottom", color="#D94E4E", fontsize=9, fontweight="bold")

    # Format axes and text styling
    ax.set_title("OPERATIONAL SLA GAP: SCHEDULED VS ACTUAL DELIVERY DAYS WITHIN CANCELED ORDERS", fontsize=11.5, fontweight="bold", color="#1B365D", pad=50)
    ax.set_xticks(x)
    ax.set_xticklabels(df_sla["Shipping Mode"], fontsize=10, fontweight="bold", color="#333333")
    ax.set_ylabel("Days", fontsize=10, fontweight="bold")
    ax.legend(frameon=False, loc="upper left")

    # Clean up border spines to optimize whitespace
    for spine in ["top", "right", "left"]: ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#cccccc")

    # Add data labels on top of each bar
    ax.bar_label(rects1, padding=3, fmt="%.1f", fontsize=9)
    ax.bar_label(rects2, padding=3, fmt="%.1f", fontsize=9, fontweight="bold")
@save_chart_automatically
def delay_rate_canceled_orders():
    total_cont, is_late_df = get_cancellation_analysis()

    is_late_df = is_late_df.loc[is_late_df.is_late != 0, :]

    df = (pd.merge(is_late_df, total_cont, how="inner", on="Shipping Mode")).assign(Delay_Rate_In_Cancelled = lambda x: x["count"]/x["Total_contribution"]).reindex(columns=["Shipping Mode", "Delay_Rate_In_Cancelled"]).sort_values("Delay_Rate_In_Cancelled", ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    # Pre-attentive color palette: Vivid red for the target focus, other elements muted to gray
    PRE_ATTENTIVE_COLORS = ["#D9A05B", "#888888", "#A6A6A6", "#C0C0C0"]

    bars = ax.barh(df["Shipping Mode"], df["Delay_Rate_In_Cancelled"], color=PRE_ATTENTIVE_COLORS, height=0.55)

    # Configure chart title and clean layout
    ax.set_title("DELAY RATE WITHIN CANCELLED ORDERS", fontsize=11.5, fontweight="bold", color="#1B365D", pad=30)
    ax.get_xaxis().set_visible(False)

    # Format Y-axis labels
    for i, label in enumerate(ax.get_yticklabels()):
        label.set_fontsize(10)
        if i == 0:  # First Class
            label.set_fontweight("bold")
            label.set_color("#124174")

    # Add targeted data labels
    for i, bar in enumerate(bars):
        width = bar.get_width()
        text_weight = "bold" if i == 0 else "normal"
        text_color = "#124174" if i == 0 else "#555555"
        text_size = 11 if i == 0 else 9
        
        ax.text(
            width + 0.02, bar.get_y() + bar.get_height()/2, 
            f"{width*100:.1f}% Late", 
            ha="left", va="center", fontsize=text_size, fontweight=text_weight, color=text_color
        )

    # Remove distracting outer border spines
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.set_xlim(0, 1.15)
@save_chart_automatically
def category_dependency_FC():
    df = get_category_analysis().reset_index()

    categories = df["Category Name"].unique()
    y_indices = np.arange(len(categories))
    bar_height = 0.18

    fig, ax = plt.subplots(figsize=(11, 7), dpi=100)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    # Tailored color palette: Bold First Class, other classes muted to dark gray
    PALETTE_DARK_GRAY = {
        "First Class": "#1B365D", 
        "Second Class": "#999999",
        "Standard Class": "#999999",  
        "Same Day": "#999999" 
    }

    for i, mode in enumerate(["Same Day" ,"Standard Class", "Second Class", "First Class"]):
        offsets = y_indices - (4 * bar_height)/2 + i * bar_height + bar_height/2
        lengths = df[mode].values
        
        bars = ax.barh(offsets, lengths, height=bar_height, color=PALETTE_DARK_GRAY[mode], edgecolor="none", label=mode)
        
        # Only display Data Labels for First Class
        if mode == "First Class":
            for j, bar in enumerate(bars):
                val = bar.get_width()
                ax.text(val + 0.01, bar.get_y() + bar.get_height()/2, f"{val*100:.1f}%", 
                        ha="left", va="center", fontsize=9, fontweight="bold", color="#1B365D")

    ax.set_title("BUSINESS IMPLICATION: CATEGORY DEPENDENCY ON FIRST CLASS", fontsize=13.5, fontweight="bold", color="#1B365D", pad=30)
    ax.set_yticks(y_indices)
    ax.set_yticklabels(categories, fontsize=10, fontweight="bold", color="#333333")
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x*100)}%"))

    # Clean up border spacing
    for spine in ["top", "right"]: ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.spines["bottom"].set_color("#cccccc")
    ax.set_xlim(0, 0.75)

    # Add legend for corporate color scheme
    ax.legend(loc="best", frameon=False, fontsize=9)
@save_chart_automatically
def region_dependency_FC():
    df = get_region_analysis().reset_index()

    Region = df["Order Region"].unique()
    y_indices = np.arange(len(Region))
    bar_height = 0.18

    fig, ax = plt.subplots(figsize=(11, 7), dpi=100)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    # Tailored color palette: Bold First Class, other classes muted to dark gray
    PALETTE_DARK_GRAY = {
        "First Class": "#1B365D", 
        "Second Class": "#999999",
        "Standard Class": "#999999",  
        "Same Day": "#999999" 
    }

    for i, mode in enumerate(["Same Day" ,"Standard Class", "Second Class", "First Class"]):
        offsets = y_indices - (4 * bar_height)/2 + i * bar_height + bar_height/2
        lengths = df[mode].values
        
        bars = ax.barh(offsets, lengths, height=bar_height, color=PALETTE_DARK_GRAY[mode], edgecolor="none", label=mode)
        
        # Only display Data Labels for First Class
        if mode == "First Class":
            for j, bar in enumerate(bars):
                val = bar.get_width()
                ax.text(val + 0.01, bar.get_y() + bar.get_height()/2, f"{val*100:.1f}%", 
                        ha="left", va="center", fontsize=9, fontweight="bold", color="#1B365D")

    ax.set_title("BUSINESS IMPLICATION: CATEGORY DEPENDENCY ON FIRST CLASS", fontsize=13.5, fontweight="bold", color="#1B365D", pad=30)
    ax.set_yticks(y_indices)
    ax.set_yticklabels(Region, fontsize=10, fontweight="bold", color="#333333")
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x*100)}%"))

    # Clean up border spacing
    for spine in ["top", "right"]: ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.spines["bottom"].set_color("#cccccc")
    ax.set_xlim(0, 0.75)

    # Add legend for corporate color scheme
    ax.legend(loc="lower right", frameon=False, fontsize=9)

#Optimized
@save_chart_automatically
def Shipping_trend_optimized():

    # 1. Fetch optimized shipping_trend df 
    df_trend = Late_Perc_Period_Optimized()[0]

    # 2. Initialize canvas
    fig, ax = plt.subplots(figsize=(14, 6), dpi=100)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    # Disable grid lines
    ax.grid(False)

    # Color palette to distinguish shipping modes
    PALETTE_TREND = {
        "First Class": "#D9A05B",    
        "Standard_Eco": "#124174", 
        "Same Day": "#708090"     
    }

    # 3. Render trend lines using Seaborn
    sns.lineplot(
        x="year_month", 
        y="Late_delivery_risk", 
        hue="Shipping Mode", 
        data=df_trend, 
        ax=ax, 
        palette=PALETTE_TREND,
        linewidth=2.5,
        marker="o",
        markersize=5,
    )

    # 4. Title and Axis adjustments
    COLOR_NAVY_DARK = "#1B365D"
    ax.set_title("LATE DELIVERY RISK TREND BY SHIPPING MODE (OPTIMIZED) (2015 - 2018)", fontsize=12, fontweight="bold", color=COLOR_NAVY_DARK, pad=20)
    ax.set_xlabel("Timeline (Year-Month)", fontsize=10, fontweight="bold", labelpad=12)
    ax.set_ylabel("Late Delivery Risk Rate", fontsize=10, fontweight="bold")

    # Format Y-axis tick labels as percentages
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda y, loc: f"{int(y*100)}%"))

    # Thin out X-axis labels (display every 3 months) to prevent overlapping text
    all_ticks = df_trend["year_month"].unique()
    thinned_ticks = all_ticks[::3]
    ax.set_xticks(thinned_ticks)
    ax.set_xticklabels(thinned_ticks, rotation=35, ha="right", fontsize=9, color="#333333")

    # 5. Position the legend outside the top-right corner for a clean layout
    ax.legend(title="Shipping Mode", title_fontsize=10, fontsize=9, loc="upper left", bbox_to_anchor=(1, 1), frameon=False)

    # 6. Spine clean-up
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.spines["bottom"].set_color("#cccccc")
    ax.set_ylim(0, 1.05)
@save_chart_automatically
def Before_After_SLA():

    # 1. DATA PREPARATION 
    df_orig = pd.read_csv("data/processed/supply_chain_processed.csv")
    df_opt = pd.read_csv("data/processed/optimized.csv")

    # Calculate metrics for Original Dataset (Before)
    df_orig["Delay_Days"] = np.where(
        (val := (df_orig.actual_lead_time - df_orig.scheduled_lead_time)) < 0, 0, val
    )
    df_orig["is_late_calculated"] = np.where(
        (df_orig["scheduled_lead_time"] - df_orig["actual_lead_time"]) >= 0, 0, 1
    )

    before_otd = (1 - df_orig["is_late_calculated"].mean())
    before_late = df_orig["is_late_calculated"].mean()
    before_delay = df_orig["Delay_Days"].mean()

    # Calculate metrics for Optimized Dataset (After)
    after_otd = (1 - df_opt["is_late"].mean())
    after_late = df_opt["is_late"].mean()
    after_delay = df_opt["Delay_Days"].mean()

    # Restructure DataFrames
    df_kpi_rates = pd.DataFrame(
        {
            "Status": ["Before", "After", "Before", "After"],
            "Metric": [
                "On-Time Delivery (OTD)",
                "On-Time Delivery (OTD)",
                "Late Delivery Rate",
                "Late Delivery Rate",
            ],
            "Value": [before_otd, after_otd, before_late, after_late],
        }
    )

    df_kpi_days = pd.DataFrame(
        {
            "Status": ["Before", "After"],
            "Avg Delay Days": [before_delay, after_delay],
        }
    )

# 2. CANVAS & INTERFACE INITIALIZATION
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), dpi=100, gridspec_kw={"width_ratios": [2, 1]})
    fig.patch.set_facecolor("#ffffff")

    # Corporate Style Palette Configuration
    COLOR_NAVY_DARK = "#1B365D"
    PALETTE_BEFORE_AFTER = {
        "Before": "#D9A05B",  
        "After": "#124174"   
    }

    # --- SUBPLOT 1: GLOBAL OPERATIONAL RATES (%) ---
    ax1 = axes[0]
    ax1.set_facecolor("#ffffff")
    ax1.grid(False)

    sns.barplot(
        data=df_kpi_rates,
        x="Metric",
        y="Value",
        hue="Status",        
        ax=ax1,
        palette=PALETTE_BEFORE_AFTER,
        legend=True,         
        edgecolor="none"
    )

    ax1.set_title("OVERALL OPERATIONAL PERFORMANCE RECOVERY (%)", fontsize=12, fontweight="bold", color=COLOR_NAVY_DARK, pad=20)
    ax1.set_ylabel("", visible=False)
    ax1.set_xlabel("", visible=False)
    ax1.get_xaxis().set_visible(True)
    ax1.get_yaxis().set_visible(False)  # Hide Y axis lines entirely as we use data labels

    # Style X-axis ticks
    ax1.tick_params(axis="x", labelsize=10, colors="#333333")
    for label in ax1.get_xticklabels():
        label.set_weight("bold")

    # Add Data Labels (%) right above the bar tips with subtle offsets
    for p in ax1.patches:
        height = p.get_height()
        if height > 0:
            ax1.text(
                p.get_x() + p.get_width() / 2.0,
                height + 0.02,  # Slight headroom offset
                f"{height*100:.2f}%",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color=COLOR_NAVY_DARK
            )

    # Clean-up borders for Subplot 1
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["bottom"].set_color("#cccccc")
    ax1.spines["left"].set_visible(False)
    ax1.set_ylim(0, 1.15)  # Add dynamic ceiling to avoid clipping labels

    # Re-position legend inside Subplot 1 cleanly
    ax1.legend(title="Status", title_fontsize=10, fontsize=9, loc="upper right", frameon=False)


    # --- SUBPLOT 2: AVERAGE DELAY DAYS PER ORDER ---
    ax2 = axes[1]
    ax2.set_facecolor("#ffffff")
    ax2.grid(False)

    sns.barplot(
        data=df_kpi_days,
        x="Status",
        y="Avg Delay Days",
        hue="Status",         
        ax=ax2,
        palette=PALETTE_BEFORE_AFTER,
        legend=False,         
        edgecolor="none"
    )

    ax2.set_title("AVERAGE DELAY PER ORDER (DAYS)", fontsize=12, fontweight="bold", color=COLOR_NAVY_DARK, pad=20)
    ax2.set_ylabel("", visible=False)
    ax2.set_xlabel("", visible=False)
    ax2.get_xaxis().set_visible(True)
    ax2.get_yaxis().set_visible(False)

    # Style X-axis ticks for Subplot 2
    ax2.tick_params(axis="x", labelsize=10, colors="#333333")
    for label in ax2.get_xticklabels():
        label.set_weight("bold")

    # Add Data Labels (Days) right above the bar tips
    for p in ax2.patches:
        height = p.get_height()
        if height > 0:  
            ax2.text(
                p.get_x() + p.get_width() / 2.0,
                height + max(df_kpi_days["Avg Delay Days"]) * 0.02,
                f"{height:.2f} days",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
                color=COLOR_NAVY_DARK
            )

    # Clean-up borders for Subplot 2
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["bottom"].set_color("#cccccc")
    ax2.spines["left"].set_visible(False)
    ax2.set_ylim(0, max(df_kpi_days["Avg Delay Days"]) * 1.15)


    # --- GLOBAL FIGURE PLOTTING ---
    plt.suptitle(
        "SUPPLY CHAIN PERFORMANCE EVALUATION REPORT (BEFORE VS. AFTER OPTIMIZATION)",
        fontsize=14,
        weight="bold",
        color=COLOR_NAVY_DARK,
        y=1.02,
    )
    
#======================================================
if __name__ == "__main__":
    shipping_performance_chart()
    order_insights()
    overall_KPI_dashboard()
    category_OTD_rank()
    shipping_mode_trend()
    SLA_gap()
    delay_rate_canceled_orders()
    category_dependency_FC()
    region_dependency_FC()
    Shipping_trend_optimized()
    Before_After_SLA()