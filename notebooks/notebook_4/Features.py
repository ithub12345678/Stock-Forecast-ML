import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

def features_engineering(df):
    # Feature Engineering
    # --------------------------------------------------
    # --------------------------------------------------
    # Compute daily percentage return
    # Formula: (Close_t - Close_{t-1}) / Close_{t-1}
    # --------------------------------------------------
    df["daily_return"] = (
        df.groupby("company_code")["close"]
        .pct_change()
    )

    # --------------------------------------------------
    # Target = Next day's return
    # shift(-1) aligns tomorrow's return as today's target
    # --------------------------------------------------
    df["target"] = (
        df.groupby("company_code")["daily_return"]
        .shift(-1)
    )

    # --------------------------------------------------
    # Create lagged return features
    # These capture autoregressive behavior
    # Taking lag of 1, 5 and 10 days prevent tunnel vision on just the 
    # previous day and allow model to learn from multiple past points

    # --------------------------------------------------
    for lag in [1, 5, 10]:
        df[f"lag_return_{lag}"] = (
            df.groupby("company_code")["daily_return"]
            .shift(lag)
        )

    # --------------------------------------------------
    # Extract day of week from date
    # Monday = 0, Sunday = 6 (but stock market uses Mon–Fri)
    # --------------------------------------------------
    df["day_of_week"] = df["date"].dt.dayofweek

    # --------------------------------------------------
    # Convert day_of_week into dummy variables
    # drop_first=True prevents multicollinearity
    # --------------------------------------------------
    df = pd.get_dummies(
        df,
        columns=["day_of_week"],
        prefix="dow",
        drop_first=True,
        dtype=int
    ).drop(columns=['dow_5'])

    # Drop columns that have only one unique 
    # value dow_sat only has 0s and is not useful for modeling

    # --------------------------------------------------
    # Rolling 20-day standard deviation of returns
    # Captures short-term volatility regime
    # --------------------------------------------------
    df["roll_vol_20"] = (
        df.groupby("company_code")["daily_return"]
        .rolling(20)
        .std()
        .reset_index(level=0, drop=True)
    )
    
    # --------------------------------------------------
    # 10-day Relative momentum
    # Measures trend strength over 10 days
    # --------------------------------------------------
    df["momentum_10"] = (
        df.groupby("company_code")["close"]
        .pct_change(10)
    )
       
    # --------------------------------------------------
    # Calculate 20-day rolling average volume
    # Group by ticker to prevent cross-stock contamination
    # --------------------------------------------------
    df['avg_volume_20d'] = (
        df.groupby("company_code")["volume"]
        .rolling(window=20)
        .mean()
        .reset_index(level=0, drop=True)
    )

    # --------------------------------------------------
    # Volume Shock feature
    # Measures abnormal trading intensity
    # --------------------------------------------------
    df['volume_shock'] = df['volume'] / df['avg_volume_20d']

    # --------------------------------------------------
    # Drop rows containing NaN values
    # This ensures model-ready dataset
    # --------------------------------------------------
    df = df.dropna().reset_index(drop=True)

    return df.head(15)
# Features enginerring completed successfully. 
# The first 15 rows of the processed DataFrame are returned for inspection.

