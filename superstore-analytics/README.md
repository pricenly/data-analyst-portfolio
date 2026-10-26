 # Superstore Sales Analysis - Python EDA, RFM & Forecasting
 
 **Portfolio Project 2** - Junior Data Analyst | Daniil Marchenko
 
 ---
 
 ## Business Context
 
 Analyze the classic "Sample Superstore" dataset (Kaggle) to deliver:
 
 1. **Data Cleaning & Quality** - Missing values, duplicates, outliers, feature engineering
 2. **Exploratory Data Analysis** - Revenue/profit trends, category/sub-category/region/segment performance
 3. **Cohort Retention Heatmap** - Monthly cohorts, period-by-period retention %
 4. **RFM Segmentation** - Recency, Frequency, Monetary scoring (quartile-based) with 7 business segments
 5. **Forecasting** - Moving averages + linear trend projection (6-month forecast)
 6. **Customer LTV Estimation** - Historical lifetime value by cohort
 7. **Export Clean Data** - Parquet/CSV for Tableau / Power BI / further modeling
 
 ---
 
 ## Dataset
 
 | Attribute | Value |
 |-----------|-------|
 | **Source** | Kaggle "Sample Superstore" |
 | **Period** | 2014-2017 (4 years) |
 | **Rows** | ~10k orders |
 | **Columns** | 21 (Order, Customer, Product, Geographic, Sales, Profit) |
 | **Files** | SampleSuperstore.csv (or Orders/Returns/People split) |
 
 **Key Fields:** Order ID, Order Date, Ship Date, Ship Mode, Customer ID, Customer Name, Segment, Country, City, State, Postal Code, Region, Product ID, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit
 
 ---
 
 ## Tech Stack
 
 - **Python 3.11+**
 - **pandas, numpy** - data manipulation
 - **matplotlib, seaborn** - visualization
 - **scikit-learn** - linear regression forecast
 - **Jupyter Lab** - interactive notebook
 
 ---
 
 ## Quick Start
 
 ### 1. Clone & Install
 ```bash
 cd superstore-analytics
 pip install -r requirements.txt
 ```
 
 ### 2. Download Data
 - Get `SampleSuperstore.csv` from [Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
 - Place in `../data/` (or update `DATA_DIR` in notebook)
 
 ### 3. Run Notebook
 ```bash
 jupyter lab eda_notebook.py
 # Or convert to .ipynb: jupytext --to notebook eda_notebook.py
 ```
 
 ---
 
 ## Notebook Structure (eda_notebook.py)
 
 | Cell | Section | Output |
 |------|---------|--------|
 | 0 | Setup & Imports | Config, style |
 | 1 | Data Loading | Shape, dtypes, head |
 | 2 | Data Quality & Cleaning | Missing, duplicates, outliers, features |
 | 3 | EDA - KPIs & Trends | Revenue, profit, orders, margin by month |
 | 4 | Category/Sub-Category | Revenue & margin bars |
 | 5 | Regional Analysis | Region & State performance |
 | 6 | Segment & Ship Mode | Segment margin, ship mode speed |
 | 7 | Correlation Heatmap | Numeric feature correlations |
 | 8 | **Cohort Retention Heatmap** | Monthly cohorts, 12-period retention |
 | 9 | **RFM Segmentation** | R/F/M scores, 7 segments, 3D scatter |
 | 10 | **Forecasting** | MA(3), MA(6), linear trend, 6-mo forecast |
 | 11 | **Customer LTV** | Historical LTV by cohort |
 | 12 | Export Clean Data | Parquet + CSVs for BI tools |
 | 13 | Insights Summary | Auto-generated markdown |
 
 ---
 
 ## Key Visualizations (for Portfolio Screenshots)
 
 1. **Monthly Revenue/Profit/Margin Trend** (4-panel)
 2. **Top 15 Sub-Categories by Revenue** (horizontal bar)
 3. **Profit Margin by Sub-Category** (diverging bar)
 4. **Top 20 States by Revenue/Profit** (dual bar)
 5. **Cohort Retention Heatmap** (annotated, Blues colormap)
 6. **RFM Segment Distribution** (count + revenue contribution)
 7. **RFM 3D Scatter** (Recency x Frequency x Monetary)
 8. **Revenue Forecast** (Actual + MA + Trend + Future)
 
 ---
 
 ## Business Insights (Template - fill after running)
 
 - **Overall Margin:** X% | **Top Category:** [Category] ($Y revenue)
 - **Best Sub-Category Margin:** [Sub-Cat] at Z%
 - **Worst Sub-Category:** [Sub-Cat] at -Z% (investigate)
 - **Top Region:** [Region] | **Top State:** [State]
 - **Month-1 Retention:** A% | **Month-3 Retention:** B%
 - **RFM Champions:** C customers (D% of revenue)
 - **At Risk + Lost:** E customers (F% of base)
 - **6-Month Forecast:** $G total revenue
 - **Avg Historical LTV:** $H per customer
 
 ---
 
 ## Exported Files (in ../output/)
 
 | File | Description |
 |------|-------------|
 | `superstore_cleaned.parquet` | Full cleaned dataset for BI |
 | `rfm_segmentation.csv` | Customer-level RFM scores + segments |
 | `cohort_retention.csv` | Cohort retention matrix |
 | `monthly_kpis.csv` | Monthly revenue, profit, orders, customers |
 | `key_insights.md` | Auto-generated insights for README |
 
 ---
 
 ## File Structure
 
 ```
 superstore-analytics/
 ├── eda_notebook.py       # Main analysis (Jupytext format)
 ├── requirements.txt      # Python dependencies
 ├── data/                 # (gitignored) - put SampleSuperstore.csv here
 ├── output/               # (gitignored) - generated exports
 └── README.md             # This file
 ```
 
 ---
 
 ## Related Projects
 
 - Project 1: E-Commerce SQL Analytics - Same metrics in pure SQL
 - Project 3: Marketing ROI Dashboard - Tableau visualization
 
 ---
 
 *Part of Daniil Marchenko's Data Analyst Portfolio*
