import numpy as np
import pandas as pd


df = pd.read_csv(r"data/processed/supply_chain_processed.csv")



df_optimized = df.copy()
df_optimized = df_optimized.loc[df_optimized["Delivery Status"] != "Shipping canceled", :]

df_optimized["Shipping Mode"] = np.where((df_optimized["Shipping Mode"] == "Standard Class") | (df_optimized["Shipping Mode"] == "Second Class"), "Standard_Eco", df_optimized["Shipping Mode"])
df_optimized["scheduled_lead_time"] = np.where((df_optimized["scheduled_lead_time"] == 2) & (df_optimized["Shipping Mode"] == "Standard_Eco"), 4, np.where(df_optimized["scheduled_lead_time"] == 1, 2, df_optimized["scheduled_lead_time"]))
df_optimized["is_late"] = np.where(df_optimized["actual_lead_time"] - df_optimized["scheduled_lead_time"] <= 0, 0, 1 )
df_optimized["Delay_Days"] = np.where((val := (df_optimized.actual_lead_time - df_optimized.scheduled_lead_time)) < 0, 0, val)

def get_dataset():
    return df_optimized

# Overall KPI Optimized
def get_KPI_Optimized():
    Late_Rate_Perc = df_optimized.is_late.mean()
    Overall_OTD = 1 - Late_Rate_Perc
    AVG_Ac_lead_time = df_optimized.actual_lead_time.mean()
    AVG_Sc_lead_time = df_optimized.scheduled_lead_time.mean()
    AVG_delay = df_optimized.Delay_Days.mean()

    kpi_dict = {
        "Metric": [
            "Overall OTD Rate",
            "Late Delivery Rate",
            "Average Actual Lead Time",
            "Average Scheduled Lead Time",
            "Average Delay Days",
        ],
        "Value": [
            f"{Overall_OTD * 100:.2f}%",
            f"{Late_Rate_Perc * 100:.2f}%",
            f"{AVG_Ac_lead_time:.2f} day(s)",
            f"{AVG_Sc_lead_time:.2f} day(s)",
            f"{AVG_delay:.2f} day(s)",
        ],
    }

    KPI = pd.DataFrame(kpi_dict)
    return KPI

# Total orders of each Optimized Shipping mode
def Order_Info_Optimized():
    T_orders = (
        df_optimized.groupby("Shipping Mode")
        .agg(
            Order_quantity_by_mode=("order_date", "count"),
            Total_sales_by_mode=("Sales", "sum"),
        )
        .reset_index()
    )

    T_orders = T_orders.assign(
        Perc_used=T_orders.Order_quantity_by_mode
        / df_optimized.order_date.count(),
        Sales_Perc=T_orders.Total_sales_by_mode / df_optimized.Sales.sum(),
    )
    T_orders["Perc_used"] = T_orders.Perc_used.round(2)
    T_orders["Sales_Perc"] = T_orders.Sales_Perc.round(4)
    return T_orders


# Late_Perc_Group Optimized
def Late_Perc_Group_Optimized():
    Shipping_mode = (
        pd.merge(
            df_optimized.groupby("Shipping Mode")["is_late"]
            .mean()
            .reset_index(name="Perc_Delay"),
            df_optimized[["Shipping Mode", "scheduled_lead_time"]],
            how="inner",
            on="Shipping Mode",
        )
        .drop_duplicates()
        .reset_index(drop=True)
    )

    Category = (
        df_optimized.groupby("Category Name")["is_late"]
        .mean()
        .reset_index(name="Perc_Delay")
        .sort_values("Perc_Delay", ascending=False)
    )

    Market = (
        df_optimized.groupby(["Market", "Order Region"])["is_late"]
        .mean()
        .reset_index(name="Perc_Delay")
        .sort_values(
            ["Market", "Perc_Delay", "Order Region"],
            ascending=[True, False, True],
        )
    )

    Cus_Segment = (
        df_optimized.groupby(["Customer Segment", "Shipping Mode"])["is_late"]
        .mean()
        .reset_index(name="Perc_Delay")
        .sort_values(["Shipping Mode", "Perc_Delay"], ascending=[True, False])
    )

    return Shipping_mode, Category, Market, Cus_Segment


# Late_Period Optimized
def Late_Perc_Period_Optimized():
    trend_df = (
        df_optimized.groupby(["year_month", "Shipping Mode"])["is_late"]
        .mean()
        .reset_index(name="Late_delivery_risk")
    )
    Late_Perc_Qrt = (
        df_optimized.groupby("Quarter_order")["is_late"]
        .mean()
        .reset_index(name="Perc_Delay")
    )
    Late_Perc_WD = (
        df_optimized.groupby(["Week_day_order", "Day_of_week_order"])["is_late"]
        .mean()
        .reset_index(name="Perc_Delay")
        .sort_values("Day_of_week_order", ascending=True)
    )

    return trend_df, Late_Perc_Qrt, Late_Perc_WD


if __name__ == "__main__":
    trend_df, df_qrt, df_wd = Late_Perc_Period_Optimized()
    shipping_mode, category, market, cus_segment = Late_Perc_Group_Optimized()
    kpi = get_KPI_Optimized()
    order_info = Order_Info_Optimized()

    
    print("--- [OPTIMIZED] Order Insight ---")
    print(order_info)

    print("\n--- [OPTIMIZED] OVERALL KPI ---")
    print(kpi)

    print("\n--- [OPTIMIZED] Shipping Mode OTD ---")
    print(shipping_mode)

    print("\n--- [OPTIMIZED] Top 10 Category OTD ---")
    print(category.head(10))

    print("\n--- [OPTIMIZED] Region OTD ---")
    print(market)

    print("\n--- [OPTIMIZED] Customer Segment OTD ---")
    print(cus_segment)

    print("\n--- [OPTIMIZED] Trend ---")
    print(trend_df)

    print("\n--- [OPTIMIZED] Perc Late per Qrt ---")
    print(df_qrt)

    print("\n--- [OPTIMIZED] Perc Late per Dayofweek ---")
    print(df_wd)

