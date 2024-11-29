"""
Handle technical analysis calculations.
"""
import pandas as pd
import numpy as np

class TechnicalAnalyzer:
    # add SMAs to dataframe
    def add_moving_averages(self, df):
        df = df.copy()
        
        # calculate SMAs with common periods
        df['SMA_20'] = df['Close'].rolling(window=20, min_periods=1).mean()  # 20-day SMA
        df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()  # 50-day SMA
        df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()  # 200-day SMA
        
        return df
        
    def add_bollinger_bands(self, df, window=20, num_std=2):
        df = df.copy()
        
        # calculate rolling mean and standard deviation
        df['BB_middle'] = df['Close'].rolling(window=window).mean()
        rolling_std = df['Close'].rolling(window=window).std()
        
        # calculate upper and lower bands
        df['BB_upper'] = df['BB_middle'] + (rolling_std * num_std)
        df['BB_lower'] = df['BB_middle'] - (rolling_std * num_std)
        
        return df
        
    def add_rsi(self, df, periods=14):
        df = df.copy()
        
        # calculate price changes
        delta = df['Close'].diff()
        
        # separate gains and losses
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        
        # calculate RS and RSI
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df