import pandas as pd
from data_processing import get_data
import numpy as np


df = pd.read_csv(r"data/processed/supply_chain_processed.csv")

df["Delay_Days"] = np.where((val:=(df.actual_lead_time - df.scheduled_lead_time)) < 0,  0, val)


#Overall KPI
def get_KPI():
    Late_Rate_Perc = df.Late_delivery_risk.mean()
    Overall_OTD = 1 - Late_Rate_Perc
    AVG_Ac_lead_time = df.actual_lead_time.mean()
    AVG_Sc_lead_time = df.scheduled_lead_time.mean()
    AVG_delay = df.Delay_Days.mean()

    kpi_dict = {
        "Metric": [
            "Overall OTD Rate", 
            "Late Delivery Rate", 
            "Average Actual Lead Time", 
            "Average Scheduled Lead Time", 
            "Average Delay Days"
        ],
        "Value": [
            f"{Overall_OTD * 100:.2f}%", 
            f"{Late_Rate_Perc * 100:.2f}%", 
            f"{AVG_Ac_lead_time:.2f} day(s)", 
            f"{AVG_Sc_lead_time:.2f} day(s)", 
            f"{AVG_delay:.2f} day(s)"
        ]
    }

    KPI = pd.DataFrame(kpi_dict)

    return KPI

#Late_Perc_Group
def Late_Perc_Group():
    Shipping_mode = pd.merge(
                            df.groupby("Shipping Mode")["Late_delivery_risk"].mean().reset_index(name="Perc_Delay"), 
                            df[["Shipping Mode", "scheduled_lead_time"]],
                            how ="inner", 
                            on="Shipping Mode"
    ).drop_duplicates().reset_index(drop=True)
    Category = df.groupby("Category Name")["Late_delivery_risk"].mean().reset_index(name="Perc_Delay").sort_values("Perc_Delay", ascending=False)
    Market = df.groupby(["Market", "Order Region"])["Late_delivery_risk"].mean().reset_index(name="Perc_Delay").sort_values(["Market", "Order Region", "Perc_Delay"], ascending=[True, True, False])
    Cus_Segment = df.groupby(["Customer Segment", "Shipping Mode"])["Late_delivery_risk"].mean().reset_index(name="Perc_Delay").sort_values(["Shipping Mode", "Perc_Delay"], ascending=[True, False])


    return Shipping_mode, Category, Market, Cus_Segment

#Late_Period
def Late_Perc_Period():
    trend_df = df.groupby(["year_month", "Shipping Mode"])["Late_delivery_risk"].mean().reset_index()
    Late_Perc_Qrt = df.groupby("Quarter_order")["Late_delivery_risk"].mean().reset_index(name="Perc_Delay")
    Late_Perc_WD = df.groupby(["Week_day_order", "Day_of_week_order"])["Late_delivery_risk"].mean().reset_index(name="Perc_Delay").sort_values("Day_of_week_order", ascending=True)

    return trend_df, Late_Perc_Qrt, Late_Perc_WD

if __name__ == "__main__":
    trend_df, df_qrt, df_wd = Late_Perc_Period()
    shipping_mode, category, market, cus_segment = Late_Perc_Group()
    kpi = get_KPI()
#KPI
    print("--- OVERALL KPI ---")
    print(kpi)
#Category
    print("--- Shipping Mode OTD ---")
    print(shipping_mode)

    print("--- Top 10 Category OTD ---")
    print(category.head(10))

    print("--- Region OTD ---")
    print(market)

    print("--- Customer Segment OTD ---")
    print(cus_segment)
#Timeline
    print("--- Trend ---")
    print(trend_df)

    print("\n--- Perc Late per Qrt ---")
    print(df_qrt)

    print("\n--- Perc Late per Dayofweek ---")
    print(df_wd)