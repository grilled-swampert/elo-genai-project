import pandas as pd
import numpy as np

# Generate 2500 rows of yearly data
np.random.seed(42)  # For reproducibility
years = np.arange(2023, 2033)
data = []

for _ in range(2500):
    year = np.random.choice(years)
    revenue = np.random.uniform(100, 500)
    profit = np.random.uniform(10, 150)
    stock_price = np.random.uniform(50, 300)
    sentiment = np.random.choice(["Positive", "Neutral", "Negative"])
    new_customers = np.random.randint(1000, 10001)
    retention_rate = np.random.uniform(60, 90)
    expenses = np.random.uniform(50, 300)
    
    data.append([
        year,
        round(revenue, 2),
        round(profit, 2),
        round(stock_price, 2),
        sentiment,
        new_customers,
        round(retention_rate, 2),
        round(expenses, 2)
    ])

# Create DataFrame
columns = [
    "Date", "Revenue (in million $)", "Profit (in million $)", 
    "Stock Price ($)", "Market Sentiment", "Number of New Customers", 
    "Customer Retention Rate (%)", "Expenses (in million $)"
]
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv("GFC_yearly_data.csv", index=False)