# filename: plot_stock_gains.py
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Define the stocks to fetch
stocks = ['NVDA', 'TSLA']
start_date = '2025-01-01'
end_date = '2025-05-10'

# Fetch historical data from Yahoo Finance
data = yf.download(stocks, start=start_date, end=end_date, auto_adjust=True)

# Calculate daily close price percentage change from the first available day of the year
relative_gains = data['Close'].pct_change().add(1).cumprod().sub(1).mul(100)

# Set up the plot
plt.figure(figsize=(10, 6))
plt.plot(relative_gains.index, relative_gains['NVDA'], label='NVDA YTD Gain %')
plt.plot(relative_gains.index, relative_gains['TSLA'], label='TSLA YTD Gain %')
plt.title('YTD Stock Gains for NVDA and TSLA')
plt.xlabel('Date')
plt.ylabel('Percentage Gain')
plt.legend(loc='best')
plt.grid(True)

# Save the plot to a file
plt.savefig('ytd_stock_gains.png')
plt.show()