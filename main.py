import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from flask import Flask, render_template


main=Flask(__name__)

# Generate sample data
categories = ['Electronics', 'Clothing', 'Furniture', 'Toys']
months = pd.date_range(start='2024-01-01', periods=12, freq='MS').strftime('%b-%Y')

data = {
    'Category': random.choices(categories, k=1000),
    'Month': random.choices(months, k=1000),
    'Sales': np.random.randint(100, 10000, size=1000),
    'Profit': np.random.randint(10, 5000, size=1000)
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
df.to_excel('data.xlsx', index=False)
print("Sample data.xlsx file created.")




# Step 1: Read data from Excel
file_path = 'data.xlsx'
df = pd.read_excel(file_path)

print(df.head())


# Step 2: Bar Chart (Total Sales by Category)
sales_by_category = df.groupby('Category')['Sales'].sum()
plt.figure(figsize=(8, 5))
sales_by_category.plot(kind='bar', color='skyblue')
plt.title('Total Sales by Category')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.savefig("static/bar_chart.png")
plt.close()

# Step 3: Line Graph (Monthly Sales Trend)
monthly_sales = df.groupby('Month')['Sales'].sum()
plt.figure(figsize=(10, 6))
monthly_sales.plot(kind='line', marker='o', color='green')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.grid(True)
plt.savefig("static/line_graph.png")
plt.close()

# Step 4: Scatter Plot (Sales vs Profit)
plt.figure(figsize=(8, 5))
plt.scatter(df['Sales'], df['Profit'], color='purple', alpha=0.5)
plt.title('Relationship Between Sales and Profit')
plt.xlabel('Sales')
plt.ylabel('Profit')
plt.savefig("static/scatter_plot.png")
plt.close()

# Step 5: Flask Route
@main.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    main.run(debug=True)