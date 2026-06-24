import pandas as pd
import numpy as np
from eda import Late_Perc_Group

df = pd.read_csv(r"data/processed/supply_chain_processed.csv")



#1. Remove clutter on cancelled order

df["is_completed"] = np.where(df["Delivery Status"] == "Shipping canceled", 0, 1)
df["is_late"] = np.where((df["scheduled_lead_time"] - df["actual_lead_time"] )>= 0, 0, 1 )


#2. Cancelled order rate
completed = (df.is_completed.mean() * 100).round(2)
cancelled = (100 - completed).round(2)
dashboard = pd.DataFrame({"Completion rate": [f"{completed} %"], "Cancellation rate": [f"{cancelled} %"]})

print(dashboard)
print("---------------")
#2.1 Verify which category contributing most in the total of cancellation rate
#2.1.1 Shipping mode

df_cancelled = df.copy()
mask1 = df.is_completed == 0
mask2 = df.is_completed == 1

df_cancelled = df_cancelled.loc[mask1, :]

Shipping = df_cancelled.groupby("Shipping Mode")["order_date"].size().reset_index(name="Total Contribution")

#2.1.2 Is Late Shipping
Cnxl_due_late = df_cancelled.groupby(["Shipping Mode", "is_late"])["order_date"].size()

Cnxl_due_late = Cnxl_due_late.unstack(fill_value=0).stack().reset_index(name="count")

print(Shipping)
print("---------------")
print(Cnxl_due_late)

#3. Shipping analysis
df_completed = df.copy().loc[mask2, :]
shipping_stat = df_completed.groupby("Shipping Mode").agg(
    max_actual = ("actual_lead_time", "max"),
    min_actual = ("actual_lead_time", "min"),
    median_actual = ("actual_lead_time", "median"),
    avg_actual = ("actual_lead_time", "mean")
).reset_index()

print("---------------")
print(pd.merge(shipping_stat, df[["scheduled_lead_time", "Shipping Mode"]].drop_duplicates(), how = "left", on = "Shipping Mode"))

#4. Category analysis 
category_stat = df_completed.groupby(["Category Name", "Shipping Mode"])["order_date"].size().reset_index(name="nbr_order")
cate = Late_Perc_Group()[1]
category_ana = pd.merge(cate[["Category Name"]].head(), category_stat, how ="left", on = "Category Name")
category_ana["total_order"] = category_ana.groupby("Category Name")["nbr_order"].transform("sum")

pivot_matrix = category_ana.pivot(
    index="Category Name", 
    columns="Shipping Mode", 
    values="nbr_order"
).fillna(0)

pivot_perc = pivot_matrix.div(pivot_matrix.sum(axis=1), axis=0)

print("---------------")
print(pivot_perc)


#5. Region analysis
region_ana = df_completed.groupby(["Market", "Order Region", "Shipping Mode"])["order_date"].size().reset_index(name="nbr_order")
market =  Late_Perc_Group()[2]
region_ana = pd.merge(market.sort_values("Perc_Delay", ascending=False)[["Market", "Order Region"]].head(), region_ana, how ="left", on = ["Market", "Order Region"])
region_ana["total_order"] = region_ana.groupby(["Market", "Order Region"])["nbr_order"].transform("sum")

region_pivot = region_ana.pivot(
    index=["Market", "Order Region"], 
    columns="Shipping Mode", 
    values="nbr_order"
).fillna(0)

region_perc = region_pivot.div(region_pivot.sum(axis=1), axis=0)

print("---------------")
print(region_perc)