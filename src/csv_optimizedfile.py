from apply_recommendations import get_dataset
import pandas as pd

df = get_dataset()

def export_csv():
    df.to_csv("data/processed/optimized.csv", index=False)
    print("💾processed data saved!")

if __name__ == "__main__":
    export_csv()