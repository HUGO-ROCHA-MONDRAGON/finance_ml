import yfinance as yf
import pandas as pd

tickers = ["AAPL"]
data = yf.download(
    tickers,
    start="2007-01-01",
    interval="1mo",
    auto_adjust=True
)["Adj Close"]

returns = data.pct_change().dropna()
print(returns.tail())
