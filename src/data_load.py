import os
import time
import pandas as pd
from sqlalchemy.exc import OperationalError
from db_engine import get_engine

CSV_PATH = "data/raw/SupplyChainDT.csv"

engine = get_engine()

def load_data():
    if not os.path.exists(CSV_PATH):
        print(f"❌ CSV file not found at: {CSV_PATH}")
        print("Please place the CSV file in the 'data/raw/' directory and verify the file name!")
        return
    
    try:
        print("📂 Reading CSV file...")
        # Load data
        df = pd.read_csv(CSV_PATH, encoding='latin1')
        print(f"✅ Successfully read! Shape: {df.shape}")
        print(f"   Number of columns: {len(df.columns)}")
        
        # Check and wait for MySQL connection to be ready
        print("📤 Checking connection to MySQL...")
        retries = 6
        while retries > 0:
            try:
                with engine.connect() as connection:
                    print("⚙️ Internal network connection successful! MySQL is ready.")
                    break
            except OperationalError:
                retries -= 1
                print(f"⏳ MySQL is busy or starting up, waiting 5 seconds... ({retries} retries remaining)")
                time.sleep(5)
                
        if retries == 0:
            print("❌ Failure: Unable to connect to the database.")
            return

        # Ingest data into MySQL
        print("📤 Loading data into MySQL...")
        start_time = time.time()
        
        df.to_sql(
            name="supply_chain_raw",
            con=engine,
            if_exists="append", 
            index=False,
            chunksize=2000
        )
        
        end_time = time.time()
        execution_time = (end_time - start_time) / 60
        
        print("🎉 All data loaded successfully!")
        print(f"   Total rows loaded: {len(df):,}")
        print(f"   Execution time: {execution_time:.2f} minutes")
        
    except Exception as e:
        print(f"❌ Error occurred while loading data: {e}")





if __name__ == "__main__":
    load_data()