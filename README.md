# Stock Price Forecasting using Machine Learning (Indian Market)

## Project Overview
This project focuses on building an end-to-end data analytics and machine learning pipeline to forecast the future closing prices of selected Indian stocks using historical market data. The project demonstrates practical application of data acquisition through APIs, data cleaning, exploratory data analysis, feature engineering, time-series modeling, and business-focused visualization.

The goal is not to guarantee stock price prediction, but to apply and evaluate multiple forecasting techniques and understand their performance, limitations, and real-world applicability.

---

## Objectives
- Collect historical stock market data for selected Indian companies using IndianAPI.in
- Clean, validate, and store data using Python and SQL
- Perform exploratory data analysis (EDA) to identify trends and patterns
- Engineer relevant features for time-series forecasting
- Build and compare baseline, machine learning, and time-series forecasting models
- Evaluate model performance using appropriate metrics
- Visualize insights and forecasts using Power BI dashboards
- (Optional) Deploy the forecasting pipeline using Streamlit or Flask

---

## Stocks Covered
Initial analysis is performed on the following Indian stocks:
- RELIANCE
- TCS
- HDFCBANK
- INFY

The project is designed to be scalable to additional stocks in future iterations.

---

## Data Source
- **IndianAPI.in** – Stock Market API  
Historical daily stock data including:
- Date
- Open
- High
- Low
- Close
- Volume

---

## Tech Stack
- **Programming Language**: Python
- **Libraries**: pandas, numpy, matplotlib, seaborn, scikit-learn, statsmodels
- **Database**: SQLite (SQL for data storage and cleaning)
- **Machine Learning**: Linear Regression, Random Forest, ARIMA, SARIMA
- **Visualization**: Power BI
- **Version Control**: Git & GitHub
- **Optional Deployment**: Streamlit / Flask
---

## Project Structure

stock-forecast-ml/
├── data/
│ ├── raw/ # Raw data from API
│ ├── cleaned/ # Cleaned and processed datasets
├── notebooks/ # Jupyter notebooks for EDA and modeling
├── src/ # Python scripts for data ingestion and processing
├── sql/ # SQL scripts for table creation and queries
├── powerbi/ # Power BI dashboard files
├── reports/ # Project reports and documentation
└── README.md


---

## Methodology
1. **Data Ingestion**: Fetch historical stock data using IndianAPI.in
2. **Data Storage**: Store raw and cleaned data in CSV and SQLite database
3. **Data Cleaning**: Handle missing values, outliers, and inconsistencies
4. **EDA**: Analyze trends, volatility, and volume patterns
5. **Feature Engineering**: Lag features, rolling statistics, technical indicators
6. **Modeling**:
   - Baseline models (Naive, Moving Average, Linear Regression)
   - Time-series models (ARIMA, SARIMA)
   - Machine learning models (Random Forest)
7. **Evaluation**: RMSE, MAE, MAPE
8. **Visualization**: Interactive dashboards using Power BI

---

## Evaluation Metrics
- Root Mean Squared Error (RMSE)
- Mean Absolute Error (MAE)
- Mean Absolute Percentage Error (MAPE)

---

## Limitations
- Stock market prices are influenced by external factors not included in the model
- Models rely solely on historical price data
- Forecasts are for educational and analytical purposes only

---

## Future Enhancements
- Incorporate news sentiment analysis
- Extend forecasting horizon
- Add more stocks and sectors
- Deploy as a web application using Streamlit
- Automate data pipeline

---

## Disclaimer
This project is intended for educational and learning purposes only and should not be considered financial or investment advice.
