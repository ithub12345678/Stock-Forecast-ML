import sqlite3 as st
import pandas as pd
import csv
import os
import argparse
import yfinance as yf

conn = st.connect("MY_database.db")
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

parser = argparse.ArgumentParser(description="Database data insertion and validation")
parser.add_argument("--input", required=True,help="Path to schema SQL file")
# parser.add_argument("--output", required=True, help="Folder to store raw CSV files")
args = parser.parse_args()

# os.makedirs(args.output, exist_ok=True)

# C:\Users\Lenovo\Downloads\Stock-Forecast-ML\sql\schema_file.sql
# C:\Users\Lenovo\Downloads\Stock-Forecast-ML\Data\RAW_csv\

with open(args.input, "r") as f:
    schema_sql = f.read()

c.executescript(schema_sql)

# Define the list of stock tickers
tickers = ["INFY.NS","TCS.NS","RELIANCE.NS","SBIN.NS"]
# Define the corresponding company names
company_names = ["Infosys","TCS","Reliance","SBI"]

# Insert company data into the Company table using function
def insert_company_data(c, ticker, company_name):
    c.execute("INSERT OR IGNORE INTO Stocks_data (company_code, company_name) VALUES (?, ?)", (ticker, company_name))
    c.execute("SELECT stock_id FROM Stocks_data WHERE company_code = :company_code", {"company_code": ticker})
    return c.fetchone()[0]

# Insert daily price data into the daily_prices table using function
def insert_stock_data(c, stock_id, df):
   for Date, row in df.iterrows():
    c.execute("""
    INSERT OR IGNORE INTO daily_prices_data
    (stock_id, date, close, high, low, open, volume)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        stock_id,
        Date,
        row["Close"],
        row["High"],
        row["Low"],
        row["Open"],
        int(row["Volume"])
    ))


# Download historical stock data for each ticker

for ticker,company_name in zip(tickers,company_names):
    df = yf.download(ticker,start = "2021-01-01",interval = "1d")
    df.columns = df.columns.droplevel(1)
    df.columns.name = None
    df.index = pd.to_datetime(df.index).date
#     df.to_csv(os.path.join(args.output, f"{ticker}_raw.csv"))

# # Insert data into the database

    stock_id = insert_company_data(c, ticker,company_name)
    insert_stock_data(c, stock_id, df)


# Data validation queries

# 1. Orphaned Records Check
# c.execute("""
#     SELECT COUNT(*) 
#         FROM daily_prices_data dp
#             LEFT JOIN Stocks_data s
#                 ON dp.stock_id = s.stock_id
#                     WHERE s.stock_id IS NULL
#                     """)

# print(c.fetchone()[0])

# # 2. Sample Data Retrieval
c.execute("SELECT * FROM daily_prices_data WHERE stock_id = 3 LIMIT 2")  
print(c.fetchall())

# # 3. Aggregate Data Insights
# c.execute("SELECT COUNT(*) FROM daily_prices_data")
# print(c.fetchall())

# # 4. Date Range Verification
c.execute("SELECT MAX(date), MIN(date) FROM daily_prices_data")
print(c.fetchall())

# # 5. Rows per Stock Analysis
# c.execute("SELECT s.company_code, COUNT(*) AS rows_per_stock " \
#             "FROM daily_prices_data dp " \
#             "JOIN Stocks_data s " \
#                 "ON dp.stock_id = s.stock_id GROUP BY s.company_code")
# print(c.fetchall())

# # 6. Null Value Assessment
# c.execute("SELECT COUNT(*) FROM daily_prices_data " \
#     "WHERE close IS NULL " \
#         "OR high IS NULL " \
#             "OR low IS NULL " \
#                 "OR open IS NULL " \
#                     "OR volume IS NULL")
# print(c.fetchall())

# # 7. OHLC value consistency check
# c.execute("SELECT COUNT(*) FROM daily_prices_data " \
#           "WHERE NOT ( high >= open AND " \
#                         "high >= close AND " \
#                             "low <= open AND " \
#                                 "low <= close) ")
# print(c.fetchall())

# # 8. volume sanity check
# c.execute("SELECT COUNT(*) FROM daily_prices_data " \
#           "WHERE volume < 0")
# print(c.fetchall())

conn.commit()
conn.close()
