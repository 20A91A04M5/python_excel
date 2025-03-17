import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from flask import Flask, render_template


main=Flask(__name__)

categories = ['Electronics', 'Clothing', 'Furniture', 'Toys']
months = pd.date_range(start='2024-01-01', periods=12, freq='MS').strftime('%b-%Y')

data = {
    'Category': random.choices(categories, k=1000),
    'Month': random.choices(months, k=1000),
    'Sales': np.random.randint(100, 10000, size=1000),
    'Profit': np.random.randint(10, 5000, size=1000)
}

df = pd.DataFrame(data)

df.to_excel('data.xlsx', index=False)
print("Sample data.xlsx file created.")




file_path = 'data.xlsx'
df = pd.read_excel(file_path)

print(df.head())



sales_by_category = df.groupby('Category')['Sales'].sum()
plt.figure(figsize=(8, 5))
sales_by_category.plot(kind='bar', color='skyblue')
plt.title('Total Sales by Category')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.savefig("static/bar_chart.png")
plt.close()


monthly_sales = df.groupby('Month')['Sales'].sum()
plt.figure(figsize=(10, 6))
monthly_sales.plot(kind='line', marker='o', color='green')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.grid(True)
plt.savefig("static/line_graph.png")
plt.close()


plt.figure(figsize=(8, 5))
plt.scatter(df['Sales'], df['Profit'], color='purple', alpha=0.5)
plt.title('Relationship Between Sales and Profit')
plt.xlabel('Sales')
plt.ylabel('Profit')
plt.savefig("static/scatter_plot.png")
plt.close()

grouped = df.groupby('Month')['Sales'].sum()

plt.figure(figsize=(8, 6))
plt.pie(grouped, labels=grouped.index, autopct='%1.1f%%', colors=plt.cm.Set3(range(len(grouped))))
plt.title('Sales Distribution by Month')
plt.savefig("static/pie_chart.png")
plt.close()


@main.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    main.run(host='0.0.0.0', port=5000)
