import yfinance as yf
msft = yf.Ticker("MSFT")
print(msft.history(period="1d"))