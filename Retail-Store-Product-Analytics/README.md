# Retail Store Analytics — Product Analytics

A complete, GitHub-ready **Product Analytics module** for the Retail Store Analytics project.

> This repository contains only the **Product Analytics** part. Other project modules such as Store Performance, Customer Analytics, Inventory, Discount Analysis, Seasonal Sales, Profitability, and Store Comparison are not included here.

## What this module does

The module answers key product-business questions:

- Which products sell the most units?
- Which products generate the most revenue?
- Which products generate the most profit?
- Which product categories perform best?
- How does revenue change over time?
- What is the relationship between discount and profit?
- Which products are **Star, Volume, Potential, or Weak** performers?

## Dashboard

The interactive dashboard contains:

- KPI cards: Products, Units Sold, Revenue, Profit, Average Margin
- Top 10 Products by Revenue
- Top 10 Products by Units Sold
- Top 10 Products by Profit
- Revenue by Category
- Profit by Category
- Monthly Revenue Trend
- Discount vs Profit
- Product Performance table
- Filters for Category, Year and Store

### Dashboard preview

Open `dashboard/dashboard_preview.html` directly in a browser for a static preview.

## Dataset

The supplied dataset contains:

- **5,000 transactions**
- **20 unique products**
- **5 categories**
- **5 stores**
- **10,866 units sold**
- **₹13,329,368.50 revenue**
- **₹4,181,423.50 profit**
- **30.10% average profit margin**

## Project structure

```text
Retail-Store-Analytics-Product-Analytics/
│
├── data/
│   └── retail_store_analytics_complete_dataset.csv
│
├── analysis/
│   └── product_analysis.py
│
├── dashboard/
│   ├── app.py
│   └── dashboard_preview.html
│
├── outputs/
│   ├── kpi_summary.csv
│   ├── product_performance.csv
│   ├── category_performance.csv
│   ├── monthly_performance.csv
│   ├── discount_performance.csv
│   └── charts
│
├── docs/
│   ├── project_overview.md
│   └── viva_questions.md
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Technologies

- Python
- Pandas
- Matplotlib
- Plotly
- Streamlit

## Run the analysis

```bash
pip install -r requirements.txt
python analysis/product_analysis.py
```

## Run the interactive dashboard

```bash
streamlit run dashboard/app.py
```

## Product performance logic

Products are classified using the median revenue and median profit:

| Revenue | Profit | Classification |
|---|---|---|
| High | High | Star Product |
| High | Low | Volume Product |
| Low | High | Potential Product |
| Low | Low | Weak Product |

## Key findings from the supplied dataset

The analysis identifies product leaders by sales, revenue and profit. The generated CSV files in `outputs/` contain the exact results and can be used for reporting or further dashboard work.

## GitHub

This folder can be uploaded directly as a repository. No other Retail Store Analytics module is required inside this repository.

## Author

Product Analytics Module — Retail Store Analytics
