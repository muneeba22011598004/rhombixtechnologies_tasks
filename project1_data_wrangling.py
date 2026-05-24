# ============================================================
# PROJECT 1: Data Wrangling & Feature Engineering
# Rhombix Technologies Internship
# ============================================================

import pandas as pd
import numpy as np

# ============================================================
# STEP 1: Sample Datasets Banana (Real world jaisi)
# ============================================================

# --- Sales Dataset ---
sales_data = {
    'order_id': [101, 102, 103, 104, 105, 106, 107, 108],
    'customer_id': [1, 2, 3, 1, 4, 2, 5, 3],
    'product_id': [201, 202, 203, 201, 204, 203, 202, 204],
    'quantity': [2, 1, 3, 1, 2, 4, 1, 2],
    'unit_price': [500, 1500, 300, 500, 800, 300, 1500, 800],
    'discount': [0.1, 0.0, 0.05, 0.15, 0.0, 0.1, 0.2, 0.05],
    'order_date': ['2024-01-05', '2024-01-10', '2024-01-12',
                   '2024-02-01', '2024-02-14', '2024-02-20',
                   '2024-03-05', '2024-03-18']
}

# --- Products Dataset ---
products_data = {
    'product_id': [201, 202, 203, 204],
    'product_name': ['Laptop Stand', 'Wireless Mouse', 'USB Hub', 'Keyboard'],
    'category': ['Accessories', 'Peripherals', 'Accessories', 'Peripherals'],
    'cost_price': [200, 800, 150, 400]
}

# --- Customers Dataset ---
customers_data = {
    'customer_id': [1, 2, 3, 4, 5],
    'customer_name': ['Ali Hassan', 'Sara Khan', 'Ahmed Raza', 'Fatima Malik', 'Usman Tariq'],
    'city': ['Lahore', 'Karachi', 'Islamabad', 'Rawalpindi', 'Peshawar'],
    'join_date': ['2023-06-01', '2023-07-15', '2023-08-20', '2023-09-10', '2023-10-05']
}

# DataFrames banao
df_sales = pd.DataFrame(sales_data)
df_products = pd.DataFrame(products_data)
df_customers = pd.DataFrame(customers_data)

# Date columns convert karo
df_sales['order_date'] = pd.to_datetime(df_sales['order_date'])
df_customers['join_date'] = pd.to_datetime(df_customers['join_date'])

print("=" * 55)
print("STEP 1: Original Datasets")
print("=" * 55)
print("\n Sales Dataset:")
print(df_sales.to_string(index=False))
print("\n  Products Dataset:")
print(df_products.to_string(index=False))
print("\n Customers Dataset:")
print(df_customers.to_string(index=False))

# ============================================================
# STEP 2: Datasets Merge Karna (Combining)
# ============================================================

# Sales + Products merge
df_merged = pd.merge(df_sales, df_products, on='product_id', how='left')

# Phir Customers add karo
df_merged = pd.merge(df_merged, df_customers, on='customer_id', how='left')

print("\n" + "=" * 55)
print("STEP 2: Merged Dataset (Sales + Products + Customers)")
print("=" * 55)
print(df_merged[['order_id', 'customer_name', 'product_name', 
                  'quantity', 'unit_price', 'discount']].to_string(index=False))

# ============================================================
# STEP 3: Naye Calculated Columns Banana (Feature Engineering)
# ============================================================

# 1. Total Revenue = quantity * unit_price * (1 - discount)
df_merged['total_revenue'] = (
    df_merged['quantity'] * df_merged['unit_price'] * (1 - df_merged['discount'])
).round(2)

# 2. Profit Margin = ((unit_price - cost_price) / unit_price) * 100
df_merged['profit_margin_%'] = (
    ((df_merged['unit_price'] - df_merged['cost_price']) / df_merged['unit_price']) * 100
).round(2)

# 3. Net Profit Per Order = (unit_price - cost_price) * quantity * (1 - discount)
df_merged['net_profit'] = (
    (df_merged['unit_price'] - df_merged['cost_price']) * 
    df_merged['quantity'] * 
    (1 - df_merged['discount'])
).round(2)

# 4. Order Month
df_merged['order_month'] = df_merged['order_date'].dt.strftime('%B %Y')

print("\n" + "=" * 55)
print("STEP 3: Naye Features (Calculated Columns)")
print("=" * 55)
print(df_merged[['order_id', 'customer_name', 'product_name',
                  'total_revenue', 'profit_margin_%', 'net_profit']].to_string(index=False))

# ============================================================
# STEP 4: Customer Lifetime Value (CLV)
# ============================================================

# Har customer ka total spend
clv_df = df_merged.groupby(['customer_id', 'customer_name']).agg(
    total_orders=('order_id', 'count'),
    total_spent=('total_revenue', 'sum'),
    total_profit=('net_profit', 'sum'),
    avg_order_value=('total_revenue', 'mean')
).reset_index()

# CLV = total_spent * (1 + repeat purchase rate)
clv_df['customer_lifetime_value'] = (clv_df['total_spent'] * 
                                      (1 + clv_df['total_orders'] * 0.1)).round(2)

# Customer Tier assign karo
def assign_tier(clv):
    if clv >= 3000:
        return ' Gold'
    elif clv >= 1500:
        return ' Silver'
    else:
        return ' Bronze'

clv_df['customer_tier'] = clv_df['customer_lifetime_value'].apply(assign_tier)

print("\n" + "=" * 55)
print("STEP 4: Customer Lifetime Value (CLV) Analysis")
print("=" * 55)
print(clv_df.to_string(index=False))

# ============================================================
# STEP 5: Summary Statistics
# ============================================================

print("\n" + "=" * 55)
print("STEP 5: Business Summary")
print("=" * 55)
print(f"   Total Revenue:       Rs. {df_merged['total_revenue'].sum():,.2f}")
print(f"   Total Net Profit:    Rs. {df_merged['net_profit'].sum():,.2f}")
print(f"   Total Orders:        {len(df_merged)}")
print(f"   Unique Customers:    {df_merged['customer_id'].nunique()}")
print(f"    Unique Products:     {df_merged['product_id'].nunique()}")
print(f"   Avg Profit Margin:   {df_merged['profit_margin_%'].mean():.2f}%")
print(f"   Best Customer:       {clv_df.loc[clv_df['customer_lifetime_value'].idxmax(), 'customer_name']}")
print(f"   Best Product:        {df_merged.groupby('product_name')['total_revenue'].sum().idxmax()}")

# ============================================================
# STEP 6: Final Dataset Save
# ============================================================
df_merged.to_csv('final_merged_dataset.csv', index=False)
clv_df.to_csv('customer_lifetime_value.csv', index=False)


print("\n Files save ho gayi hain:")
print("   → final_merged_dataset.csv")
print("   → customer_lifetime_value.csv")
print("\n" + "=" * 55)

