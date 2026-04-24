import yfinance as yf
import sqlite3
import csv
import pandas as pd

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

with open("C:\\Users\\Lenovo\\Downloads\\Stock-Forecast-ML\\sql\\schema.sql", "r") as f:
    schema_sql = f.read()

c.executescript(schema_sql)

c.execute("INSERT INTO Stocks (company_code, company_name) VALUES (?, ?)", ("TCS.NS", "Tata Consultancy Services Limited"))

c.execute("SELECT stock_id FROM Stocks WHERE company_code = :company_code", {"company_code":"TCS.NS"})
stock_id = c.fetchone()[0]

df = pd.read_csv("C:/Users/Lenovo/Downloads/Stock-Forecast-ML/Data/RAW/TCS_yfinance.csv")
print(df.head())

for _, row in df.iterrows():
    c.execute("""
    INSERT OR IGNORE INTO daily_prices
    (stock_id, date, close, high, low, open, volume)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        stock_id,
        row["Date"],
        row["Close"],
        row["High"],
        row["Low"],
        row["Open"],
        int(row["Volume"])
    ))

# c.execute("""
# SELECT COUNT(*) 
# FROM daily_prices dp
# LEFT JOIN stocks s
# ON dp.stock_id = s.stock_id
# WHERE s.stock_id IS NULL
# """)

# orphan_count = c.fetchone()[0]
# print("Orphane records in daily_prices:", orphan_count)

# c.execute("SELECT COUNT(*) FROM daily_prices")
# print(c.fetchall())

# c.execute("SELECT MAX(date), MIN(date) FROM daily_prices")
# print(c.fetchall())

# c.execute("SELECT COUNT(*) FROM daily_prices WHERE close IS NULL")
# print(c.fetchall())

# c.execute("SELECT * FROM daily_prices WHERE close = :close", {"close":1276.6951021174527})
# print(c.fetchall())

conn.commit()
conn.close()



