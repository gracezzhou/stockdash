# File: stock_dashboard/config.py
"""
Configuration settings for the stock dashboard application.
"""
from pathlib import Path

# Directory Settings
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Default settings
DEFAULT_TICKER = "AAPL"
DEFAULT_TIMEFRAME = "1y"
DEFAULT_INTERVAL = "1d"

# Technical Analysis Parameters
MA_PERIODS = [20, 50, 200]
RSI_PERIOD = 14
BBANDS_PERIOD = 20
BBANDS_STD = 2

# UI Settings
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