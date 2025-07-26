# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 10:23:32 2025

@author: admin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load the data set

rs = pd.read_csv(r"C:\Users\admin\Desktop\Python Practice\Retail Sales Project\retail_sales_dataset.csv")

rs.head()
rs.describe()
rs.info()

# 1.Data Cleaning & Preparation:

# Change date type for date from obejct to datetime

rs['Date'] = pd.to_datetime(rs['Date'], dayfirst='True')

rs.info()

# Check the missing values

rs.isnull().sum()

print(rs.isnull().sum())

rs.isnull().values.any()

rs[rs['Customer ID'].isnull()]

# check the duplicate

rs.duplicated().any()

rs.duplicated().sum()

# 2. Sales Performance Analysis:
    
# Monthly, weekly, and daily sales trends.

rs['Month']=rs['Date'].dt.strftime('%B')
print(rs['Month'])

rs['Week'] = rs['Date'].dt.isocalendar().week
rs['Week']

rs['Day']=rs['Date'].dt.day
rs['Day']

# MOnthly Sales

Monthly_Sales = rs.groupby('Month')['Total Amount'].sum()

month_order=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

Monthly_Sales= Monthly_Sales.reindex(month_order)

Monthly_Sales

# Weekly Sales

Week_Sales = rs.groupby ('Week')['Total Amount'].sum()

Week_Sales

# Best and worst-performing products.

Best_Product = rs.groupby ('Product Category')['Total Amount'].sum().sort_values(ascending=False)

Best_Product

# 3. Customer Insights

# Top customers by revenue and quantity

Top_cust_by_rev = rs.groupby('Customer ID')['Total Amount'].sum().sort_values(ascending=False)

print("Top customer by revenue:", Top_cust_by_rev.head(5))

Top_cust_by_qty = rs.groupby ('Customer ID')['Quantity'].sum().sort_values(ascending=False)

print("Top customer by quantity", Top_cust_by_qty.head(5))

# Average order value, order frequency

Order_count = rs.groupby('Customer ID').size().sort_values(ascending=False)

print("Order count per customer", Order_count )

Avg_order_value = Top_cust_by_rev / Order_count

print("Average order value per customer", Avg_order_value.head(5))

order_freq = rs.groupby (['Customer ID', 'Month']).size().groupby('Customer ID').mean().reset_index()
order_freq.columns = ['Customer ID', 'order_freq']
print("Average monthly order frequency per customer:")
print(order_freq.head(5))


# Define age group and analysis

bins = [0,18,25,35,45,60,100]
lables= ['<18', '18-25', '26-35', '36-45', '46-60', '>100']
rs['Age group']= pd.cut(rs['Age'], bins=bins, labels=lables)

sales_age_group = rs.groupby (['Age group', 'Product Category'],observed=False) ['Total Amount'].sum().reset_index()

sales_age_group1 = rs.groupby ('Age group', observed=False) ['Total Amount'].sum().reset_index()

# 6 Visualizations:

# Line chart (sales over time - Monthly)

Monthly_Sales.plot(
    kind='line',
    xlabel='Months',
    ylabel='Total sales',
    title='Sales over month',
    color='blue',)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('Monthly_Sales.png', dpi=300, bbox_inches='tight')
plt.show()

# Line chart (sales over time - Weekly)
    
Week_Sales.plot(
    kind='line',
    xlabel='Weeks',
    ylabel='Total sales',
    title = 'Sales over week',
    color= 'pink')

plt.tight_layout()
plt.show()

 # Bar chart (top products)
 
Best_Product.plot(
     kind='bar',
     xlabel='Product',
     ylabel='Sales',
     title='Top products by sales',
     color='green')
plt.xticks(rotation=0, ha='center')
plt.tight_layout()
plt.show()

 # Bar chart (top Custmer by sales)
 
Top_cust_by_rev.head(5).plot(
     kind='bar',
     xlabel='Cusomter ID',
     ylabel='Sales',
     color='red',
     title='Top cusotmer by sales')
plt.xticks(rotation=0, ha='center')
plt.tight_layout()
plt.show()
 
 # Bar chart (top Custmer by quanitty)
 
Top_cust_by_qty.head(5).plot(
     kind= 'bar',
     xlabel='customer ID',
     ylabel= 'Quanity',
     color='purple',
     title =' Top cusotmers by quanity')
plt.xticks(rotation=0, ha='center')
plt.tight_layout()
plt.show()

# stacked bar (Age group analysis)

sns.barplot(data=sales_age_group, x ='Age group', y= 'Total Amount', hue ='Product Category')

plt.title('Sales by Age Group and Product Category')
plt.ylabel('Total Sales')
plt.xlabel('Age group')
plt.tight_layout()
plt.savefig("Sales by agegroup")
plt.show()

# Povit heatmap (Age group analysis)

heatmap_data=sales_age_group.pivot(index='Age group', columns='Product Category', values='Total Amount')

sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="RdYlGn", linewidths=0.5)

plt.title('Sales by Age Group and Product Category')
plt.ylabel('Total Sales')
plt.xlabel('Age group')
plt.tight_layout()
plt.show()


# Gender and age group based analaysis

sales_gender = rs.groupby (['Gender','Age group','Product Category'], observed=False) ['Total Amount'].sum().reset_index()

sales_gender_bar=sales_gender.pivot_table(
    index=['Gender', 'Age group'],
    columns='Product Category',
    values='Total Amount')

sales_gender_bar.plot(
    kind='bar',
    xlabel="Gender by age group",
    ylabel='Total sales')
plt.tight_layout()
plt.show()


heatmap_data1=sales_gender.pivot(index=['Gender','Age group'], columns='Product Category', values='Total Amount')

sns.heatmap(heatmap_data1,annot=True, fmt=".0f", cmap="RdYlGn")
plt.title("Sales by agegroup and gender")
plt.ylabel('Total Sales')
plt.xlabel('Age group')
plt.tight_layout()
plt.savefig("Heatmap")
plt.show()























