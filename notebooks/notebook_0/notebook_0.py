import yfinance as yf
import pandas as pd

tickers = ["TCS.NS","RELIANCE.BO"]
company_names = ["Tata Consultancy Services Limited","Reliance Industries Limited"]

for ticker,company_name in zip(tickers,company_names):
    df = yf.download(ticker,start = "2020-01-01",interval = "1d",auto_adjust = False)
    df.columns = df.columns.droplevel(1).str.lower()
    df.columns.name = None
    print(df.head())
    break


# df = df.rename(columns={"date": "date"})

# df.to_csv("C:\\Users\\Lenovo\\Downloads\\Stock-Forecast-ML\\Data\\RAW\\TCS_yfinance.csv",index=True)
