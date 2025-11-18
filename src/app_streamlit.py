import pandas as pd
import streamlit as st
from pathlib import Path

AGG1_PATH = Path("data/agg_daily_avg_close_by_ticker.parquet")
AGG2_PATH = Path("data/agg_avg_volume_by_sector.parquet")
AGG3_PATH = Path("data/agg_daily_simple_return_by_ticker.parquet")


@st.cache_data
def load_agg1():
    df = pd.read_parquet(AGG1_PATH)
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    return df


@st.cache_data
def load_agg2():
    return pd.read_parquet(AGG2_PATH)


@st.cache_data
def load_agg3():
    df = pd.read_parquet(AGG3_PATH)
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    return df


def main():
    st.set_page_config(page_title="Stock Dashboard", layout="wide")
    st.title("📈 Stock Market Aggregates Dashboard")

    tab1, tab2, tab3 = st.tabs(
        ["Avg Close by Ticker", "Avg Volume by Sector", "Daily Returns"]
    )

    # --- TAB 1 ---
    with tab1:
        st.subheader("Daily Average Close Price by Ticker")
        agg1 = load_agg1()

        min_date = agg1["trade_date"].min().date()
        max_date = agg1["trade_date"].max().date()

        date_range = st.date_input("Select Date Range", (min_date, max_date))

        tickers = sorted(agg1["ticker"].unique())
        selected_tickers = st.multiselect(
            "Select Tickers",
            options=tickers,
            default=tickers[:3] if len(tickers) >= 3 else tickers
        )

        mask = (
            agg1["trade_date"].dt.date.between(date_range[0], date_range[1]) &
            agg1["ticker"].isin(selected_tickers)
        )

        filtered = agg1[mask]

        st.line_chart(
            filtered.pivot(index="trade_date", columns="ticker", values="avg_close_price")
        )

        st.dataframe(filtered)

    # --- TAB 2 ---
    with tab2:
        st.subheader("Average Volume by Sector")
        agg2 = load_agg2()

        st.bar_chart(agg2.set_index("sector")["avg_volume"])

        st.dataframe(agg2)

    # --- TAB 3 ---
    with tab3:
        st.subheader("Daily Return by Ticker")

        agg3 = load_agg3()

        min_date = agg3["trade_date"].min().date()
        max_date = agg3["trade_date"].max().date()

        date_range = st.date_input(
            "Select Date Range (Returns)",
            (min_date, max_date),
            key="returns_date",
        )

        tickers = sorted(agg3["ticker"].unique())
        selected_tickers = st.multiselect(
            "Select Tickers (Returns)",
            options=tickers,
            default=tickers[:3] if len(tickers) >= 3 else tickers,
            key="returns_ticker",
        )

        mask = (
            agg3["trade_date"].dt.date.between(date_range[0], date_range[1]) &
            agg3["ticker"].isin(selected_tickers)
        )

        filtered = agg3[mask]

        st.line_chart(
            filtered.pivot(index="trade_date", columns="ticker", values="simple_return")
        )

        st.dataframe(filtered)


if __name__ == "__main__":
    main()
