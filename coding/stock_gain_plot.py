# filename: stock_gain_plot.py
import yfinance as yf
import matplotlib.pyplot as plt

# Define start of year and today's date for 2025
start_date = "2025-01-01"
end_date = "2025-05-10"

# Fetch data for NVDA and TSLA
nvda_data = yf.download('NVDA', start=start_date, end=end_date)
tsla_data = yf.download('TSLA', start=start_date, end=end_date)

# Calculate YTD gains, assuming data is available
nvda_gain = (nvda_data['Close'] - nvda_data['Close'].iloc[0]) / nvda_data['Close'].iloc[0] * 100
tsla_gain = (tsla_data['Close'] - tsla_data['Close'].iloc[0]) / tsla_data['Close'].iloc[0] * 100

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(nvda_gain, label='NVDA', color='blue')
plt.plot(tsla_gain, label='TSLA', color='red')
plt.title('YTD Stock Gains for NVDA and TSLA (2025)')
plt.xlabel('Date')
plt.ylabel('Gain (%)')
plt.legend()
plt.grid(True)

# Save the figure to a file
plt.savefig('ytd_stock_gains.png')

# Show the plot in a window (optional, comment out if running as a script)
# plt.show()

print("Plot has been saved as ytd_stock_gains.png.")