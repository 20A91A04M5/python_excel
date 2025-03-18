# import pandas as pd
# import numpy as np
# import random
# import matplotlib.pyplot as plt
# from flask import Flask, render_template


# main=Flask(__name__)

# categories = ['Electronics', 'Clothing', 'Furniture', 'Toys']
# months = pd.date_range(start='2024-01-01', periods=12, freq='MS').strftime('%b-%Y')

# data = {
#     'Category': random.choices(categories, k=1000),
#     'Month': random.choices(months, k=1000),
#     'Sales': np.random.randint(100, 10000, size=1000),
#     'Profit': np.random.randint(10, 5000, size=1000)
# }

# df = pd.DataFrame(data)

# df.to_excel('data.xlsx', index=False)
# print("Sample data.xlsx file created.")




# file_path = 'data.xlsx'
# df = pd.read_excel(file_path)

# print(df.head())



# sales_by_category = df.groupby('Category')['Sales'].sum()
# plt.figure(figsize=(8, 5))
# sales_by_category.plot(kind='bar', color='skyblue')
# plt.title('Total Sales by Category')
# plt.xlabel('Category')
# plt.ylabel('Total Sales')
# plt.xticks(rotation=45)
# plt.savefig("static/bar_chart.png")
# plt.close()


# monthly_sales = df.groupby('Month')['Sales'].sum()
# plt.figure(figsize=(10, 6))
# monthly_sales.plot(kind='line', marker='o', color='green')
# plt.title('Monthly Sales Trend')
# plt.xlabel('Month')
# plt.ylabel('Sales')
# plt.grid(True)
# plt.savefig("static/line_graph.png")
# plt.close()


# plt.figure(figsize=(8, 5))
# plt.scatter(df['Sales'], df['Profit'], color='purple', alpha=0.5)
# plt.title('Relationship Between Sales and Profit')
# plt.xlabel('Sales')
# plt.ylabel('Profit')
# plt.savefig("static/scatter_plot.png")
# plt.close()

# grouped = df.groupby('Month')['Sales'].sum()

# plt.figure(figsize=(8, 6))
# plt.pie(grouped, labels=grouped.index, autopct='%1.1f%%', colors=plt.cm.Set3(range(len(grouped))))
# plt.title('Sales Distribution by Month')
# plt.savefig("static/pie_chart.png")
# plt.close()


# @main.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     main.run(host='0.0.0.0', port=5000)


import pandas as pd
import numpy as np
import random
import os
from dash import Dash, dcc, html
import plotly.express as px

# -------------------------------
# Step 1: Create Sample Excel Data
# -------------------------------
DATA_FILE = 'data.xlsx'

# Create sample data only if the file doesn't exist
if not os.path.exists(DATA_FILE):
    categories = ['Electronics', 'Clothing', 'Furniture', 'Toys']
    months = pd.date_range(start='2024-01-01', periods=12, freq='MS').strftime('%b-%Y')
    
    data = {
        'Category': random.choices(categories, k=1000),
        'Month': random.choices(months, k=1000),
        'Sales': np.random.randint(100, 10000, size=1000),
        'Profit': np.random.randint(10, 5000, size=1000)
    }
    
    df_sample = pd.DataFrame(data)
    df_sample.to_excel(DATA_FILE, index=False)
    print("✅ Sample data.xlsx file created.")

# -------------------------------
# Step 2: Read Excel Data using Pandas
# -------------------------------
if os.path.exists(DATA_FILE):
    df = pd.read_excel(DATA_FILE, engine='openpyxl')
    print("✅ Data loaded successfully from Excel file.")
else:
    raise FileNotFoundError("❌ data.xlsx file not found!")

# -------------------------------
# Step 3: Create Interactive Visualizations using Plotly Express
# -------------------------------

# 1. Bar Chart: Total Sales by Category
df_bar = df.groupby('Category', as_index=False)['Sales'].sum()
bar_chart = px.bar(
    df_bar, 
    x='Category', 
    y='Sales', 
    color='Category', 
    title="Total Sales by Category",
    labels={'Sales': 'Total Sales'},
    hover_data={'Sales': ':.2f'}
)

# 2. Line Graph: Monthly Sales Trend
df_line = df.groupby('Month', as_index=False)['Sales'].sum()
line_chart = px.line(
    df_line, 
    x='Month', 
    y='Sales', 
    markers=True,
    title="Monthly Sales Trend",
    labels={'Sales': 'Sales'},
    hover_data={'Sales': ':.2f'}
)

# 3. Scatter Plot: Relationship between Sales and Profit
scatter_plot = px.scatter(
    df,
    x='Sales',
    y='Profit',
    color='Category',
    title="Relationship between Sales and Profit",
    labels={'Sales': 'Sales', 'Profit': 'Profit'},
    hover_name='Category'
)

# 4. Pie Chart: Sales Distribution by Month
df_pie = df.groupby('Month', as_index=False)['Sales'].sum()
pie_chart = px.pie(
    df_pie, 
    values='Sales', 
    names='Month', 
    title="Sales Distribution by Month",
    hover_data={'Sales': True}
)
pie_chart.update_traces(textposition='inside', textinfo='percent+label')

# 5. Heatmap: Sales by Category and Month
df_heat = df.pivot_table(index='Category', columns='Month', values='Sales', aggfunc='sum', fill_value=0)
heatmap = px.imshow(
    df_heat,
    labels=dict(x="Month", y="Category", color="Sales"),
    x=df_heat.columns,
    y=df_heat.index,
    title="Sales Heatmap by Category and Month",
    aspect="auto",
    color_continuous_scale='Blues'
)

# 6. Box Plot: Profit Distribution by Category
box_plot = px.box(
    df,
    x='Category',
    y='Profit',
    color='Category',
    title="Profit Distribution by Category",
    labels={'Profit': 'Profit'}
)

# -------------------------------
# Step 4: Create an Interactive Dashboard using Dash
# -------------------------------
app = Dash(__name__)
server = app.server  # For Render deployment

app.layout = html.Div([
    html.H1("Excel Data Visualization Dashboard", style={'textAlign': 'center'}),
    dcc.Markdown("### Interactive Visualizations", style={'textAlign': 'center'}),
    
    dcc.Graph(figure=bar_chart),
    dcc.Graph(figure=line_chart),
    dcc.Graph(figure=scatter_plot),
    dcc.Graph(figure=pie_chart),
    dcc.Graph(figure=heatmap),
    dcc.Graph(figure=box_plot),
    
    html.Footer("Dashboard by L Tirumalaprasad", style={'textAlign': 'center', 'padding': '20px'})
])

# -------------------------------
# Step 5: Run Server on Render-Compatible Port
# -------------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Ensure port binding on Render
    app.run(debug=True,  port=port)
