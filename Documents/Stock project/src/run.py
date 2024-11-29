# File: stock_dashboard/run.py
"""
Entry point for the application.
"""
from .dashboard import StockDashboard

def main():
    dashboard = StockDashboard()
    dashboard.run(debug=True)

if __name__ == '__main__':
    main()