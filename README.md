📈 Stock Market Data Pipeline & Dashboard

This project processes raw stock market data, cleans it, generates analytical aggregations, and displays them using a Streamlit dashboard.

🚀 Features
1. Data Cleaning

Loads stock_market.csv

Normalizes schema (snake_case, trims, cleans nulls)

Fixes date formats

Deduplicates rows

Saves cleaned.parquet

2. Aggregations

Generates three parquet files:

agg_daily_avg_close_by_ticker.parquet

agg_avg_volume_by_sector.parquet

agg_daily_simple_return_by_ticker.parquet

3. Streamlit Dashboard

Interactive filters and charts:

Daily average close by ticker

Average trading volume by sector

Daily simple return by ticker

4. Tech Stack

Python

Pandas / PyArrow

Streamlit

UV package manager

VSCode

🗂 Project Structure
project/
│
├── data/
│   ├── stock_market.csv
│   ├── cleaned.parquet
│   ├── agg_daily_avg_close_by_ticker.parquet
│   ├── agg_avg_volume_by_sector.parquet
│   └── agg_daily_simple_return_by_ticker.parquet
│
├── src/
│   ├── data_cleaning.py
│   ├── make_aggregations.py
│   └── app_streamlit.py
│
├── screenshots/
│   ├── chart1.png
│   ├── chart2.png
│   └── chart3.png
│
├── README.md
├── pyproject.toml
└── uv.lock

▶️ Running the Project
1. Activate environment
uv venv
& .\.venv\Scripts\Activate.ps1

2. Run data cleaning
uv run python src/data_cleaning.py

3. Run aggregations
uv run python src/make_aggregations.py

4. Launch Streamlit app
uv run streamlit run src/app_streamlit.py

📸 Screenshots
![alt text](<screenshots/Screenshot 2025-11-18 175237.png>)

![alt text](<screenshots/Screenshot 2025-11-18 175317.png>)

![alt text](<screenshots/Screenshot 2025-11-18 175331.png>)
✔️ Finished