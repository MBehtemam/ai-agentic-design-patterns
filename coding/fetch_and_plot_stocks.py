# filename: fetch_and_plot_stocks.py
from functions import get_stock_prices, plot_stock_prices
import pandas as pd

# Ensure all required modules are imported
import yfinance

# Define the stock symbols and date range
stock_symbols = ['NVDA', 'TSLA']
start_date = '2025-01-01'
end_date = '2025-05-10'

# Fetch the stock prices from the start of the year to today
stock_prices = get_stock_prices(stock_symbols, start_date, end_date)

# Plotting the stock prices
if not stock_prices.empty:
    plot_stock_prices(stock_prices, "stock_prices_YTD_plot.png")
else:
    print("No stock price data found.")