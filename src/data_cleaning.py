import re
import numpy as np
import pandas as pd
from pathlib import Path


RAW_DATA_PATH = Path("data/stock_market.csv")
CLEANED_PATH = Path("data/cleaned.parquet")


def to_snake_case(col: str) -> str:
    col = col.strip()
    col = re.sub(r"[^\w]+", "_", col)
    return col.lower()


def normalize_strings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    na_tokens = {"", "na", "n/a", "null", "-", "--"}
    df = df.applymap(
        lambda x: np.nan
        if isinstance(x, str) and x.strip().lower() in na_tokens
        else x
    )
    return df


def clean_schema(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [to_snake_case(c) for c in df.columns]
    df = normalize_strings(df)

    df["trade_date"] = pd.to_datetime(df["trade_date"], format="%m/%d/%Y")

    df["open_price"] = pd.to_numeric(df["open_price"], errors="coerce")
    df["close_price"] = pd.to_numeric(df["close_price"], errors="coerce")
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce").astype("Int64")

    df["ticker"] = df["ticker"].str.upper()
    df["sector"] = df["sector"].str.title()
    df["currency"] = df["currency"].str.upper()
    df["exchange"] = df["exchange"].str.upper()
    df["notes"] = df["notes"].astype("string")

    def parse_validated(x):
        if pd.isna(x): return pd.NA
        s = str(x).strip().lower()
        if s in ("yes", "y", "true", "1"): return True
        if s in ("no", "n", "false", "0"): return False
        return pd.NA

    df["validated"] = df["validated"].apply(parse_validated).astype("boolean")

    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"Dedup: {before - after} rows removed.")

    return df


def main():
    print("Loading raw CSV...")
    df = pd.read_csv(RAW_DATA_PATH)

    print(df.head())

    df_clean = clean_schema(df)

    CLEANED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_parquet(CLEANED_PATH, index=False)
    print(f"Saved cleaned parquet → {CLEANED_PATH}")


if __name__ == "__main__":
    main()
