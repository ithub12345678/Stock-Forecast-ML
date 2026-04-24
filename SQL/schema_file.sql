-- =====================================================
-- Database Schema for Stock Forecasting Project
-- =====================================================


-- -------------------------
-- Table: Stocks
-- -------------------------
CREATE TABLE IF NOT EXISTS Stocks_data (
    stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_code TEXT UNIQUE NOT NULL,
    company_name TEXT
);

-- -------------------------
-- Table: daily_prices
-- -------------------------
CREATE TABLE IF NOT EXISTS daily_prices_data (
    price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_id INTEGER NOT NULL,
    date DATE NOT NULL,
    close REAL,
    high REAL,
    low REAL,
    open REAL,
    volume INTEGER,
    UNIQUE (stock_id, date),
    FOREIGN KEY (stock_id) REFERENCES Stocks_data(stock_id)
);