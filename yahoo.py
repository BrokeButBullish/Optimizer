import yfinance as yf
import pandas as pd

tickers = ["AAPL", "MSFT", "GOOGL", "NVDA", "META", "TSM", "TSLA", "LLY", "BSX", "GS", "SHOP", "UNH", "DINO", "DVN", "XOM", "SLB", "CCJ", "LEU", "NLR", "URNM","JPM","NEE","DUK","GLD","SLV","PFE"]
start_date = "2020-01-01"
end_date = "2024-01-01"

# Download data
data = yf.download(tickers, start=start_date, end=end_date)

# Check if data is empty
if data.empty:
    print("Data download failed! Check ticker symbols or internet connection.")
else:
    # Handle MultiIndex columns
    if isinstance(data.columns, pd.MultiIndex):
        # Extract "Adj Close" prices
        if "Adj Close" in data.columns.levels[0]:
            adj_close = data["Adj Close"]
        else:
            print("Using 'Close' prices instead of 'Adj Close'")
            adj_close = data["Close"]
    else:
        # Handle single ticker case
        if "Adj Close" in data.columns:
            adj_close = data["Adj Close"]
        else:
            print("Using 'Close' prices instead of 'Adj Close'")
            adj_close = data["Close"]

    # Check for missing tickers
    downloaded_tickers = adj_close.columns.tolist()
    missing_tickers = [ticker for ticker in tickers if ticker not in downloaded_tickers]

    if missing_tickers:
        print(f"Missing data for tickers: {missing_tickers}")
    else:
        print("All tickers downloaded successfully!")

    # Drop rows with missing data
    adj_close = adj_close.dropna(how="all")

    # Save to CSV
    adj_close.to_csv("stock_prices.csv")
    print("Data successfully saved!")
    print(f"Number of rows saved: {len(adj_close)}")