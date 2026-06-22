import pandas as pd
from data_load import get_engine
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

def data_processing(verbose=True):
    engine = get_engine()
    query = """
    SELECT 
        `order date (DateOrders)` AS order_date,
        `shipping date (DateOrders)` AS shipping_date,
        `Days for shipping (real)` AS actual_lead_time,
        `Days for shipment (scheduled)` AS scheduled_lead_time,
        `Delivery Status`,
        `Late_delivery_risk`,
        `Shipping Mode`,
        `Category Name`,
        `Market`,
        `Order Region`,
        `Customer Segment`,
        `Sales`
    FROM supply_chain_raw
    """

    df = pd.read_sql(query, engine)

    dtype_mapping = {
        # === Time columns ===
        'order_date': 'datetime64[ns]',
        'shipping_date': 'datetime64[ns]',
        
        # === Lead Time ===
        'actual_lead_time': 'int16',
        'scheduled_lead_time': 'int16',
        
        # === Categorical columns ===
        'Delivery Status': 'category',
        'Shipping Mode': 'category',
        'Category Name': 'category',
        'Market': 'category',
        'Order Region': 'category',
        'Customer Segment': 'category',
        
        # === Binary / Small int ===
        'Late_delivery_risk': 'int8',     
        
        # === Numeric ===
        'Sales': 'float32'                  
    }

    df_processed = df.copy()

    # Convert as per mapping
    
    for col, dtype in dtype_mapping.items():
        if col in df_processed.columns:
            try:
                df_processed[col] = df_processed[col].astype(dtype)
                if verbose:
                    print(f"✅ Converted {col:25} → {dtype}")
            except Exception as e:
                if verbose:
                    print(f"❌ Converted Failed {col} → {dtype}: {e}")

    # result
    if verbose:
        print("\n" + "="*60)
        print("MEMORY USAGE AFTER OPTIMIZED:")
        print(df_processed.info(memory_usage='deep'))

        print(f"\nMemory usage: {df_processed.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    #enrich_datatime

    df_processed = df_processed.assign(
        Month_order = df_processed.order_date.dt.month,
        Year_order = df_processed.order_date.dt.year,
        Quarter_order = df_processed.order_date.dt.quarter,
        Week_day_order = df_processed.order_date.dt.day_name(),
        Month_name_order = df_processed.order_date.dt.month_name(),
        Day_of_week_order = df_processed.order_date.dt.day_of_week,
        year_month = df_processed.order_date.dt.to_period("M")
    )
    return df_processed

    
def get_data():
    return data_processing(verbose=False)

if __name__ == "__main__":
    df = get_data()
    # Save df as csv file
    df.to_csv("data/processed/supply_chain_processed.csv", index=False)
    print("💾processed data saved!")