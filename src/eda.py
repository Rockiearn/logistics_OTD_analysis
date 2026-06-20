import pandas as pd
from data_processing import get_data
import time


df = pd.read_csv(r"data/processed/supply_chain_processed.csv")

print(df.head(10).to_string())

