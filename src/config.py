# File: stock_dashboard/config.py
"""
Configuration settings for the stock dashboard application.
"""
from pathlib import Path

# directory settings
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# default settings
DEFAULT_TICKER = "AAPL"
DEFAULT_TIMEFRAME = "1y"
DEFAULT_INTERVAL = "1d"

# technical analysis parameters
MA_PERIODS = [20, 50, 200] # sma dates
RSI_PERIOD = 14 # rsi length of time
BBANDS_PERIOD = 20 # bollinger bands
BBANDS_STD = 2

# UI settings
THEME = "plotly_dark"
COLORS = {
    'background': '#0f1729',
    'text': '#ffffff',
    'primary': '#2196F3',
    'secondary': '#f50057',
    'success': '#4CAF50',
    'warning': '#ff9800',
    'danger': '#f44336'
}