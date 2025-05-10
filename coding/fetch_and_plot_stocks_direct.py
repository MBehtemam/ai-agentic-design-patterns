# filename: fetch_and_plot_stocks_direct.py
import yfinance as yf
import matplotlib.pyplot as plt

# Define the stock symbols and date range
stock_symbols = ['NVDA', 'TSLA']
start_date = '2025-01-01'
end_date = '2025-05-10'

# Fetching the stock data directly using yfinance
stock_data = yf.download(stock_symbols, start=start_date, end=end_date)

# Plotting the stock prices
plt.figure(figsize=(14, 7))
for ticker in stock_symbols:
    plt.plot(stock_data['Close'][ticker], label=ticker)

plt.title('Stock Prices YTD for NVDA and TSLA')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend(title='Ticker')
plt.grid(True)
plt.savefig('stock_prices_YTD_plot.png')
plt.show()