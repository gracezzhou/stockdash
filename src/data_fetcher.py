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
        """
        Fetch stock data using the modern yfinance API.
        
        Args:
            ticker (str): Stock ticker symbol (e.g., 'AAPL')
            timeframe (str): Time period to fetch (e.g., '1y', '6mo')
            interval (str): Data interval (e.g., '1d', '1h')
            
        Returns:
            pd.DataFrame: Processed stock data
        """
        cache_key = f"{ticker}_{timeframe}_{interval}"
        
        if cache_key in self.cache:
            logger.info(f"Returning cached data for {ticker}")
            return self.cache[cache_key].copy()
            
        try:
            logger.info(f"Fetching data for {ticker}")
            stock = yf.Ticker(ticker)
            
            # Use the new API to fetch history
            df = stock.history(period=timeframe, interval=interval, auto_adjust=True)
            
            if not df.empty:
                df = self._process_data(df)
                self.cache[cache_key] = df.copy()
                logger.info(f"Successfully fetched {len(df)} rows for {ticker}")
                return df
            else:
                raise ValueError(f"No data available for {ticker}")
                
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {str(e)}")
            raise
    
    def _process_data(self, df):
        """Process raw stock data with technical indicators."""
        df = df.copy()
        
        # Calculate returns using pandas methods
        df['Daily_Return'] = df['Close'].pct_change()
        df['Log_Return'] = np.log(df['Close'] / df['Close'].shift(1))
        
        # Add common technical indicators (now using pandas calculations)
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['RSI'] = self._calculate_rsi(df['Close'])
        
        return df
    
    def _calculate_rsi(self, prices, periods=14):
        """Calculate RSI using pandas operations."""
        delta = prices.diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def get_company_info(self, ticker):
        """Fetch company info using the modern yfinance API."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Use the new fast_info attribute for quick access to common metrics
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
            logger.error(f"Error fetching company info for {ticker}: {str(e)}")
            return dict.fromkeys(['name', 'sector', 'industry', 'market_cap', 
                                'pe_ratio', 'dividend_yield'], 'N/A')

    def clear_cache(self):
        """Clear the data cache."""
        self.cache.clear()
        logger.info("Cache cleared")