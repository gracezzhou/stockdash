import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from .config import DEFAULT_TIMEFRAME, DEFAULT_INTERVAL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockDataFetcher:
    def __init__(self):
        self.cache = {}
        
    def get_stock_data(self, ticker, timeframe=DEFAULT_TIMEFRAME, interval=DEFAULT_INTERVAL):
        # fetch stock data. args: ticker (i.e. symbol), timeframe (time period to fetch), interval (data interval); returns processed stock data in a dataframe
        cache_key = f"{ticker}_{timeframe}_{interval}"
        
        if cache_key in self.cache:
            logger.info(f"Returning cached data for {ticker}")
            return self.cache[cache_key].copy()
            
        try:
            logger.info(f"Fetching data for {ticker}")
            stock = yf.Ticker(ticker)
            
            # fetch history with yfinance
            df = stock.history(period=timeframe, interval=interval, auto_adjust=True)
            
            if not df.empty:
                df = self._process_data(df)
                self.cache[cache_key] = df.copy()
                logger.info(f"Successfully fetched {len(df)} rows for {ticker}")
                return df
            else:
                raise ValueError(f"No data available for {ticker}")
                
        except Exception as e:
            logger.error(f"Oops! Error fetching data for {ticker}: {str(e)}")
            raise
    
    def _process_data(self, df):
        # take technical indicators of raw data
        df = df.copy()
        
        # calculate returns
        df['Daily_Return'] = df['Close'].pct_change()
        df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
        
        # add SMAs and RSIs
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['RSI'] = self._calculate_rsi(df['Close'])
        
        return df
    
    def _calculate_rsi(self, prices, periods=14):
        delta = prices.diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def get_company_info(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            fast_info = stock.fast_info
            
            return {
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': fast_info.get('market_cap', 'N/A'),
                'pe_ratio': fast_info.get('pe_ratio', 'N/A'),
                'dividend_yield': fast_info.get('dividend_yield', 'N/A')
            }
            
        except Exception as e: 
            logger.error(f"Oops! Error fetching company info for {ticker}: {str(e)}")
            return dict.fromkeys(['name', 'sector', 'industry', 'market_cap', 
                                'pe_ratio', 'dividend_yield'], 'N/A')

    def clear_cache(self):
        """Clear the data cache."""
        self.cache.clear()
        logger.info("Cache cleared")