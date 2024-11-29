"""
Handle technical analysis calculations.
"""
import pandas as pd
import numpy as np

class TechnicalAnalyzer:
    def add_moving_averages(self, df):
        """Add Simple Moving Averages to the dataframe."""
        df = df.copy()
        
        # Calculate SMAs with common periods
        df['SMA_20'] = df['Close'].rolling(window=20, min_periods=1).mean()  # 20-day SMA
        df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()  # 50-day SMA
        df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()  # 200-day SMA
        
        return df
        
    def add_bollinger_bands(self, df, window=20, num_std=2):
        """Add Bollinger Bands to the dataframe."""
        df = df.copy()
        
        # Calculate rolling mean and standard deviation
        df['BB_middle'] = df['Close'].rolling(window=window).mean()
        rolling_std = df['Close'].rolling(window=window).std()
        
        # Calculate upper and lower bands
        df['BB_upper'] = df['BB_middle'] + (rolling_std * num_std)
        df['BB_lower'] = df['BB_middle'] - (rolling_std * num_std)
        
        return df
        
    def add_rsi(self, df, periods=14):
        """Add Relative Strength Index to the dataframe."""
        df = df.copy()
        
        # Calculate price changes
        delta = df['Close'].diff()
        
        # Separate gains and losses
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        
        # Calculate RS and RSI
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df