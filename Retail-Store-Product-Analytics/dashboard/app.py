"""
Interactive Product Analytics Dashboard
Run:
    streamlit run dashboard/app.py
"""

from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "retail_store_analytics_complete_dataset.csv"

st.set_page_config(
    page_title="Retail Store Analytics | Product Analytics",
    page_icon="📊",
    layout="wide",
)

@st.cache_data
def load_data():
    df = pd.read_csv(DATA)
    return df.drop_duplicates()

df = load_data()

st.title("Retail Store Analytics")
st.subheader("Product Analytics Dashboard")
st.caption("Product-level sales, revenue, profit, category and discount analysis")

# Sidebar filters
st.sidebar.header("Filters")

categories = sorted(df["Product Category"].dropna().unique())
years = sorted(df["Year"].dropna().unique())
stores = sorted(df["Store Name"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Product Category", categories, default=categories
)
selected_years = st.sidebar.multiselect(
    "Year", years, default=years
)
selected_stores = st.sidebar.multiselect(
    "Store", stores, default=stores
)

filtered = df[
    df["Product Category"].isin(selected_categories)
    & df["Year"].isin(selected_years)
    & df["Store Name"].isin(selected_stores)
].copy()

# KPI cards
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Products", f"{filtered['Product ID'].nunique():,}")
c2.metric("Units Sold", f"{filtered['Quantity'].sum():,.0f}")
c3.metric("Revenue", f"₹{filtered['Total Amount'].sum():,.0f}")
c4.metric("Profit", f"₹{filtered['Profit'].sum():,.0f}")
c5.metric("Avg Margin", f"{filtered['Profit Margin %'].mean():.1f}%")

st.divider()

# Product aggregation
product = (
    filtered.groupby(["Product ID", "Product Name", "Product Category"], as_index=False)
    .agg(
        Units_Sold=("Quantity", "sum"),
        Revenue=("Total Amount", "sum"),
        Profit=("Profit", "sum"),
        Avg_Discount=("Discount %", "mean"),
        Avg_Margin=("Profit Margin %", "mean"),
    )
)

category = (
    filtered.groupby("Product Category", as_index=False)
    .agg(
        Units_Sold=("Quantity", "sum"),
        Revenue=("Total Amount", "sum"),
        Profit=("Profit", "sum"),
    )
)

monthly = (
    filtered.groupby(["Year", "Month", "Month Name"], as_index=False)
    .agg(Revenue=("Total Amount", "sum"), Profit=("Profit", "sum"))
    .sort_values(["Year", "Month"])
)

# Main charts
left, right = st.columns(2)

with left:
    st.markdown("### Top 10 Products by Revenue")
    top = product.nlargest(10, "Revenue").sort_values("Revenue")
    fig = px.bar(top, x="Revenue", y="Product Name", orientation="h",
                 labels={"Revenue": "Revenue", "Product Name": "Product"})
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("### Top 10 Products by Units Sold")
    top = product.nlargest(10, "Units_Sold").sort_values("Units_Sold")
    fig = px.bar(top, x="Units_Sold", y="Product Name", orientation="h",
                 labels={"Units_Sold": "Units Sold", "Product Name": "Product"})
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    st.markdown("### Revenue by Category")
    fig = px.bar(category, x="Product Category", y="Revenue")
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("### Profit by Category")
    fig = px.bar(category, x="Product Category", y="Profit")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("### Monthly Revenue Trend")
fig = px.line(monthly, x="Month Name", y="Revenue", markers=True,
              labels={"Month Name": "Month", "Revenue": "Revenue"})
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Discount vs Profit")
discount = (
    filtered.groupby("Discount %", as_index=False)
    .agg(Revenue=("Total Amount", "sum"),
         Profit=("Profit", "sum"),
         Units_Sold=("Quantity", "sum"))
)
fig = px.scatter(
    discount, x="Discount %", y="Profit", size="Revenue",
    hover_data=["Units_Sold"],
    labels={"Discount %": "Discount %", "Profit": "Profit"}
)
st.plotly_chart(fig, use_container_width=True)

# Product performance
st.markdown("### Product Performance")
rev_med = product["Revenue"].median()
profit_med = product["Profit"].median()

def classify(row):
    if row["Revenue"] >= rev_med and row["Profit"] >= profit_med:
        return "Star Product"
    elif row["Revenue"] >= rev_med:
        return "Volume Product"
    elif row["Profit"] >= profit_med:
        return "Potential Product"
    return "Weak Product"

product["Performance"] = product.apply(classify, axis=1)

st.dataframe(
    product.sort_values("Revenue", ascending=False),
    use_container_width=True,
    hide_index=True
)

st.caption("Built for the Product Analytics module of Retail Store Analytics.")
