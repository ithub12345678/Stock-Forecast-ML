import pandas as pd
import numpy as np
import argparse
import sqlite3
from Features import features_engineering

parser = argparse.ArgumentParser(description =" Take database input and perform feature engineering for stock price prediction")
parser.add_argument("--input", required=True, help="Database file path (e.g., data/stocks.db)")
args = parser.parse_args()


# --------------------------------------------------
# Connect to SQLite database
# --------------------------------------------------
conn = sqlite3.connect(args.input)

# --------------------------------------------------
# Load cleaned OHLCV dataset
# (Assumes Week 4 cleaning is complete)
# --------------------------------------------------
query = """
SELECT s.company_code,
       dp.date,
       dp.open,
       dp.high,
       dp.low,
       dp.close,
       dp.volume
FROM daily_prices_data dp
JOIN Stocks_data s ON dp.stock_id = s.stock_id
ORDER BY s.company_code, dp.date;
"""

df = pd.read_sql(query, conn, parse_dates=["date"])
# Parse_dates ensures 'date' column is in timestamp format 
# and not just a string, which is crucial for time-series analysis.

# Ensure correct sorting (very important for time-series)
df = df.sort_values(["company_code", "date"]).reset_index(drop=True)

# print(features_engineering(df))

print(features_engineering(df)) 
