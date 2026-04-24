import pandas as pd
import sqlite3 as st
import csv
import argparse


parser = argparse.ArgumentParser(description="Data Cleaning")
parser.add_argument("--input", required=True, help = "Takes Database file as input")
parser.add_argument("--output",required = True, help = "Takes output file name as input")
args = parser.parse_args()

conn = st.connect(args.input)

query = """
SELECT s.company_code, dp.date, dp.open, dp.high, dp.low, dp.close, dp.volume
FROM daily_prices_data dp
JOIN Stocks_data s ON dp.stock_id = s.stock_id
ORDER BY s.company_code, dp.date;
"""

df = pd.read_sql(query, conn, parse_dates=["date"])
# parse_dates=["date"]: This is a critical argument. By default, SQLite stores dates as strings or numbers.
# This tells Pandas to automatically convert the "date" column into a 
# datetime64 object, enabling time-series analysis like filtering by month or year

# Info method could be used to find datatype of each column with repective null count in each.
print(df.info())

# .diff():This function subtracts the value of the previous row from the current row (\(Row_{n}-Row_{n-1}\)). When applied to a datetime column, the result is a Timedelta object (e.g., 1 days 04:00:00)..dt:This is the accessor 
# for datetime-like properties in Pandas. 
# It allows you to access specific components of the time difference, such as days, seconds, or microseconds..days:This extracts only the integer 
# number of days from the Timedelta, discarding any hours, minutes, or seconds. 
df["date_diff"] = df.groupby("company_code")["date"].diff().dt.days
print(df[df["date_diff"] > 3])

#This is a critical operation for financial time-series data. .groupby("ticker"): This ensures the calculation stays "siloed" within each stock. Without this, 
# the first price of MSFT would be compared to the last price of AAPL, creating a massive, incorrect "jump" in your data.["close"]: 
# This tells Pandas to only perform the math on the closing price column..pct_change(): This calculates the percentage difference between the current row and 
# the previous row:\(\text{Return}=\frac{\text{Price}_{\text{today}}-\text{Price}_{\text{yesterday}}}{\text{Price}_{\text{yesterday}}}\)Result: 
# A new column where a value of 0.02 represents a 2% gain for that day, and -0.01 represents a 1% loss. 
df["daily_return"] = df.groupby("company_code")["close"].pct_change()

df.to_csv(args.output, index=False)
