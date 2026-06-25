import numpy as np
import pandas as pd
from eda import Late_Perc_Group

df = pd.read_csv(r"data/processed/supply_chain_processed.csv")

# Pre-processing 
df["is_completed"] = np.where(
    df["Delivery Status"] == "Shipping canceled", 0, 1
)
df["is_late"] = np.where(
    (df["scheduled_lead_time"] - df["actual_lead_time"]) >= 0, 0, 1
)

# Masks
mask1 = df.is_completed == 0
mask2 = df.is_completed == 1


# 1. Cancelled order rate
def get_dashboard_kpi():
    completed = (df.is_completed.mean() * 100).round(2)
    cancelled = (100 - completed).round(2)
    dashboard = pd.DataFrame(
        {
            "Completion rate": [f"{completed} %"],
            "Cancellation rate": [f"{cancelled} %"],
        }
    )

    return dashboard


# 2. Cancelled order contribution analysis
def get_cancellation_analysis():
    df_cancelled = df.copy().loc[mask1, :]

    Shipping = (
        df_cancelled.groupby("Shipping Mode")
        .agg(
            Total_contribution=("order_date", "size"),
            Total_sales_lost=(
                "Sales",
                "sum",
            ),
        )
        .reset_index()
    )

    Cnxl_due_late = df_cancelled.groupby(["Shipping Mode", "is_late"])[
        "order_date"
    ].size()
    Cnxl_due_late = (
        Cnxl_due_late.unstack(fill_value=0).stack().reset_index(name="count")
    )

    return Shipping, Cnxl_due_late


# 3. Shipping lead time analysis
def get_shipping_analysis():
    df_completed = df.copy().loc[mask2, :]
    shipping_stat = (
        df_completed.groupby("Shipping Mode")
        .agg(
            max_actual=("actual_lead_time", "max"),
            min_actual=("actual_lead_time", "min"),
            median_actual=("actual_lead_time", "median"),
            avg_actual=("actual_lead_time", "mean"),
        )
        .reset_index()
    )

    shipping_merge = pd.merge(
        shipping_stat,
        df[["scheduled_lead_time", "Shipping Mode"]].drop_duplicates(),
        how="left",
        on="Shipping Mode",
    )

    return shipping_merge


# 4. Category analysis
def get_category_analysis():
    df_completed = df.copy().loc[mask2, :]
    category_stat = (
        df_completed.groupby(["Category Name", "Shipping Mode"])["order_date"]
        .size()
        .reset_index(name="nbr_order")
    )
    cate = Late_Perc_Group()[1]
    category_ana = pd.merge(
        cate[["Category Name"]].head(),
        category_stat,
        how="left",
        on="Category Name",
    )
    category_ana["total_order"] = category_ana.groupby("Category Name")[
        "nbr_order"
    ].transform("sum")

    pivot_matrix = category_ana.pivot(
        index="Category Name", columns="Shipping Mode", values="nbr_order"
    ).fillna(0)

    pivot_perc = pivot_matrix.div(pivot_matrix.sum(axis=1), axis=0)

    return pivot_perc


# 5. Region analysis
def get_region_analysis():
    df_completed = df.copy().loc[mask2, :]
    region_ana = (
        df_completed.groupby(["Market", "Order Region", "Shipping Mode"])[
            "order_date"
        ]
        .size()
        .reset_index(name="nbr_order")
    )
    market = Late_Perc_Group()[2]
    region_ana = pd.merge(
        market.sort_values("Perc_Delay", ascending=False)[
            ["Market", "Order Region"]
        ].head(),
        region_ana,
        how="left",
        on=["Market", "Order Region"],
    )
    region_ana["total_order"] = region_ana.groupby(["Market", "Order Region"])[
        "nbr_order"
    ].transform("sum")

    region_pivot = region_ana.pivot(
        index=["Market", "Order Region"],
        columns="Shipping Mode",
        values="nbr_order",
    ).fillna(0)

    region_perc = region_pivot.div(region_pivot.sum(axis=1), axis=0)

    return region_perc


if __name__ == "__main__":
    dashboard = get_dashboard_kpi()
    shipping_contrib, cnxl_due_late = get_cancellation_analysis()
    shipping_stat_summary = get_shipping_analysis()
    category_pivot = get_category_analysis()
    region_pivot = get_region_analysis()

    print("--- 1. OVERALL KPI DASHBOARD ---")
    print(dashboard)
    print("---------------")

    print("--- 2. SHIPPING CANCELLATION CONTRIBUTION ---")
    print(shipping_contrib)
    print("---------------")
    print(cnxl_due_late)

    print("--- 3. SHIPPING LEAD TIME ANALYSIS ---")
    print("---------------")
    print(shipping_stat_summary)

    print("--- 4. CATEGORY DISTRIBUTION SHARE ---")
    print("---------------")
    print(category_pivot)

    print("--- 5. REGIONAL LOGISTICS PROFILE ---")
    print("---------------")
    print(region_pivot)