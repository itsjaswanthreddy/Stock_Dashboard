import pandas as pd
from pathlib import Path

CLEANED_PATH = Path("data/cleaned.parquet")
AGG1_PATH = Path("data/agg_daily_avg_close_by_ticker.parquet")
AGG2_PATH = Path("data/agg_avg_volume_by_sector.parquet")
AGG3_PATH = Path("data/agg_daily_simple_return_by_ticker.parquet")


def main():
    print(f"Loading cleaned data from {CLEANED_PATH}...")
    df = pd.read_parquet(CLEANED_PATH)

    df["simple_return"] = df["close_price"] / df["open_price"] - 1

    agg1 = df.groupby(["trade_date", "ticker"])["close_price"].mean().reset_index()
    agg1.rename(columns={"close_price": "avg_close_price"}, inplace=True)

    agg2 = df.groupby("sector")["volume"].mean().reset_index()
    agg2.rename(columns={"volume": "avg_volume"}, inplace=True)

    agg3 = df.groupby(["trade_date", "ticker"])["simple_return"].mean().reset_index()

    AGG1_PATH.parent.mkdir(parents=True, exist_ok=True)
    agg1.to_parquet(AGG1_PATH, index=False)
    agg2.to_parquet(AGG2_PATH, index=False)
    agg3.to_parquet(AGG3_PATH, index=False)

    print("Aggregation parquet files created!")


if __name__ == "__main__":
    main()
