"""
Product Analytics - Retail Store Analytics
Author: Product Analytics Module

Run:
    python analysis/product_analysis.py
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "retail_store_analytics_complete_dataset.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
df = df.drop_duplicates()

# Product-level summary
product = (
    df.groupby(["Product ID", "Product Name", "Product Category"], as_index=False)
      .agg(
          Units_Sold=("Quantity", "sum"),
          Revenue=("Total Amount", "sum"),
          Profit=("Profit", "sum"),
          Avg_Price=("Price per Unit", "mean"),
          Avg_Discount=("Discount %", "mean"),
          Avg_Margin=("Profit Margin %", "mean"),
      )
      .sort_values("Revenue", ascending=False)
)

# Category-level summary
category = (
    df.groupby("Product Category", as_index=False)
      .agg(
          Units_Sold=("Quantity", "sum"),
          Revenue=("Total Amount", "sum"),
          Profit=("Profit", "sum"),
          Avg_Discount=("Discount %", "mean"),
          Avg_Margin=("Profit Margin %", "mean"),
      )
      .sort_values("Revenue", ascending=False)
)

# Monthly summary
monthly = (
    df.groupby(["Year", "Month", "Month Name"], as_index=False)
      .agg(Units_Sold=("Quantity", "sum"),
           Revenue=("Total Amount", "sum"),
           Profit=("Profit", "sum"))
      .sort_values(["Year", "Month"])
)

# Discount summary
discount = (
    df.groupby("Discount %", as_index=False)
      .agg(Units_Sold=("Quantity", "sum"),
           Revenue=("Total Amount", "sum"),
           Profit=("Profit", "sum"))
      .sort_values("Discount %")
)

# Product performance classification
revenue_median = product["Revenue"].median()
profit_median = product["Profit"].median()

def classify(row):
    high_revenue = row["Revenue"] >= revenue_median
    high_profit = row["Profit"] >= profit_median
    if high_revenue and high_profit:
        return "Star Product"
    if high_revenue and not high_profit:
        return "Volume Product"
    if not high_revenue and high_profit:
        return "Potential Product"
    return "Weak Product"

product["Performance"] = product.apply(classify, axis=1)

# Save tables
product.to_csv(OUT / "product_performance.csv", index=False)
category.to_csv(OUT / "category_performance.csv", index=False)
monthly.to_csv(OUT / "monthly_performance.csv", index=False)
discount.to_csv(OUT / "discount_performance.csv", index=False)

# KPI summary
kpis = pd.DataFrame([{
    "Total Transactions": len(df),
    "Total Products": df["Product ID"].nunique(),
    "Units Sold": df["Quantity"].sum(),
    "Revenue": df["Total Amount"].sum(),
    "Profit": df["Profit"].sum(),
    "Average Profit Margin %": df["Profit Margin %"].mean(),
    "Categories": df["Product Category"].nunique(),
    "Stores": df["Store ID"].nunique(),
}])
kpis.to_csv(OUT / "kpi_summary.csv", index=False)

# Static charts for GitHub
def save_bar(data, label, value, title, filename, horizontal=False):
    plt.figure(figsize=(10, 6))
    d = data.copy()
    if horizontal:
        plt.barh(d[label].astype(str)[::-1], d[value][::-1])
        plt.xlabel(value.replace("_", " "))
    else:
        plt.bar(d[label].astype(str), d[value])
        plt.xticks(rotation=30, ha="right")
        plt.ylabel(value.replace("_", " "))
    plt.title(title)
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=160)
    plt.close()

save_bar(product.nlargest(10, "Revenue"), "Product Name", "Revenue",
         "Top 10 Products by Revenue", "top_10_revenue.png", True)
save_bar(product.nlargest(10, "Units_Sold"), "Product Name", "Units_Sold",
         "Top 10 Products by Units Sold", "top_10_units.png", True)
save_bar(product.nlargest(10, "Profit"), "Product Name", "Profit",
         "Top 10 Products by Profit", "top_10_profit.png", True)
save_bar(category, "Product Category", "Revenue",
         "Revenue by Product Category", "category_revenue.png")
save_bar(category, "Product Category", "Profit",
         "Profit by Product Category", "category_profit.png")

plt.figure(figsize=(10, 6))
plt.plot(monthly["Month Name"].astype(str), monthly["Revenue"], marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(OUT / "monthly_revenue.png", dpi=160)
plt.close()

print("Product Analytics completed.")
print(f"Transactions: {len(df):,}")
print(f"Products: {df['Product ID'].nunique():,}")
print(f"Units sold: {df['Quantity'].sum():,}")
print(f"Revenue: ₹{df['Total Amount'].sum():,.2f}")
print(f"Profit: ₹{df['Profit'].sum():,.2f}")
print(f"Average margin: {df['Profit Margin %'].mean():.2f}%")
