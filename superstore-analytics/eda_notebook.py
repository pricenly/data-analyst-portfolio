# %% [markdown]
# Superstore Sales Analysis — EDA, RFM Segmentation & Forecasting
#
# **Author:** Daniil Marchenko | Junior Data Analyst Portfolio
# **Dataset:** Kaggle "Sample Superstore" (Orders, Returns, People)
# **Stack:** Python 3.11+, pandas, numpy, matplotlib, seaborn, scikit-learn
# **Environment:** Jupyter Lab / VS Code / Google Colab

# %%
# =============================================================================
# 0. SETUP & IMPORTS
# =============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from pathlib import Path
from datetime import datetime

# Visualization settings
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 11
warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
FIG_DIR = BASE_DIR / "images"
FIG_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_plot(filename: str) -> None:
    """Persist the current figure so results are visible outside a notebook."""
    plt.savefig(FIG_DIR / filename, dpi=150, bbox_inches="tight")

# Reproducibility
np.random.seed(42)

# %%
# =============================================================================
# 1. DATA LOADING
# =============================================================================
# Expected file: ./data/SampleSuperstore.csv (bundled with this project)
# Source: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

# Load main orders file
df = pd.read_csv(DATA_DIR / "SampleSuperstore.csv", encoding="latin1", parse_dates=["Order Date", "Ship Date"])

print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
df.head()

# %%
# =============================================================================
# 2. DATA QUALITY & CLEANING
# =============================================================================

# 2.1 Basic info
print("=== DTYPES ===")
print(df.dtypes)
print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

# 2.2 Data quality validation on the raw input. These checks report issues
# before transformations; they intentionally do not silently discard anomalies.
required_columns = {
    "Order ID", "Order Date", "Ship Date", "Customer ID",
    "Sales", "Quantity", "Discount", "Profit"
}
missing_columns = sorted(required_columns - set(df.columns))
if missing_columns:
    raise ValueError(f"Required dataset columns are missing: {missing_columns}")

duplicate_rows = int(df.duplicated().sum())
invalid_dates = int((df["Order Date"].isna() | df["Ship Date"].isna()).sum())
ship_before_order = int((df["Ship Date"] < df["Order Date"]).fillna(False).sum())
negative_sales = int((df["Sales"] < 0).sum())
nonpositive_quantity = int((df["Quantity"] <= 0).sum())
invalid_discount = int((~df["Discount"].between(0, 1)).sum())
missing_customer_ids = int(df["Customer ID"].isna().sum())

sales_q1, sales_q3 = df["Sales"].quantile([0.25, 0.75])
sales_iqr = sales_q3 - sales_q1
sales_low, sales_high = sales_q1 - 1.5 * sales_iqr, sales_q3 + 1.5 * sales_iqr
sales_outlier_count = int((~df["Sales"].between(sales_low, sales_high)).sum())
profit_q1, profit_q3 = df["Profit"].quantile([0.25, 0.75])
profit_iqr = profit_q3 - profit_q1
profit_low, profit_high = profit_q1 - 1.5 * profit_iqr, profit_q3 + 1.5 * profit_iqr
profit_outlier_count = int((~df["Profit"].between(profit_low, profit_high)).sum())

dq_checks = pd.DataFrame([
    ("Exact duplicate rows", duplicate_rows, "Review; exact duplicates are removed below"),
    ("Rows with missing order/ship date", invalid_dates, "Investigate; exclude from time analysis"),
    ("Ship date before order date", ship_before_order, "Anomalous chronology"),
    ("Negative sales", negative_sales, "Review transactions; do not assume these are errors"),
    ("Non-positive quantity", nonpositive_quantity, "Review returns/invalid quantities"),
    ("Discount outside [0, 1]", invalid_discount, "Invalid discount range"),
    ("Missing customer ID", missing_customer_ids, "Cannot use for customer-level metrics"),
    ("Sales IQR outliers", sales_outlier_count, f"Outside [{sales_low:.2f}, {sales_high:.2f}]"),
    ("Profit IQR outliers", profit_outlier_count, f"Outside [{profit_low:.2f}, {profit_high:.2f}]"),
], columns=["check", "rows_flagged", "interpretation"])
print("\n=== DATA QUALITY CHECK ===")
print(dq_checks.to_string(index=False))

# 2.3 Remove exact duplicate records after recording the raw count.
df = df.drop_duplicates().reset_index(drop=True)

# 2.3b Drop rows that carry no order identity (e.g. the appended Returns
# block in this Kaggle export has empty Order ID / dates / Customer ID).
rows_before_drop = len(df)
df = df.dropna(subset=["Order Date", "Customer ID"]).reset_index(drop=True)
rows_dropped = rows_before_drop - len(df)
print(f"\nRows without Order Date / Customer ID excluded: {rows_dropped}")

# 2.4 Handle missing Postal Code (fill with mode per City/State)
if df["Postal Code"].isnull().any():
    df["Postal Code"] = df.groupby(["City", "State"])["Postal Code"].transform(
        lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else np.nan)
    )
# Keep a single dtype so the Parquet export does not mix strings and floats.
df["Postal Code"] = pd.to_numeric(df["Postal Code"], errors="coerce").astype("Int64").astype("string")

# 2.5 Feature engineering: time dimensions
df["Order Year"] = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month
df["Order Quarter"] = df["Order Date"].dt.quarter
df["Order YearMonth"] = df["Order Date"].dt.to_period("M")
df["Ship Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

# 2.6 Revenue & profit per row
df["Revenue"] = df["Sales"]
df["Profit Margin"] = df["Profit"] / df["Sales"].replace(0, np.nan)

# 2.7 Outlier detection (IQR method on Sales)
Q1, Q3 = df["Sales"].quantile([0.25, 0.75])
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df["Sales"] < lower_bound) | (df["Sales"] > upper_bound)]
print(f"Outliers (IQR): {len(outliers)} rows ({100*len(outliers)/len(df):.1f}%)")

# Keep outliers but flag them
df["is_outlier"] = (df["Sales"] < lower_bound) | (df["Sales"] > upper_bound)

print("✅ Cleaning complete")
df.info()

# %%
# =============================================================================
# 3. EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================

# 3.1 Overall KPIs
total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()
avg_order_value = total_revenue / total_orders

print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Profit:  ${total_profit:,.2f}")
print(f"Profit Margin: {total_profit/total_revenue*100:.1f}%")
print(f"Total Orders:  {total_orders:,}")
print(f"Customers:     {total_customers:,}")
print(f"Avg Order Val: ${avg_order_value:,.2f}")

# 3.2 Revenue trend by month
monthly = df.groupby("Order YearMonth").agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),
    Customers=("Customer ID", "nunique")
).reset_index()
monthly["Order YearMonth"] = monthly["Order YearMonth"].dt.to_timestamp()

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Revenue trend
axes[0,0].plot(monthly["Order YearMonth"], monthly["Revenue"], marker="o", linewidth=2)
axes[0,0].set_title("Monthly Revenue Trend")
axes[0,0].set_ylabel("Revenue ($)")
axes[0,0].tick_params(axis="x", rotation=45)

# Profit trend
axes[0,1].plot(monthly["Order YearMonth"], monthly["Profit"], marker="o", color="green", linewidth=2)
axes[0,1].set_title("Monthly Profit Trend")
axes[0,1].set_ylabel("Profit ($)")
axes[0,1].tick_params(axis="x", rotation=45)

# Orders trend
axes[1,0].bar(monthly["Order YearMonth"].astype(str), monthly["Orders"], alpha=0.7)
axes[1,0].set_title("Monthly Orders")
axes[1,0].tick_params(axis="x", rotation=45)

# Profit margin trend
monthly["Margin"] = monthly["Profit"] / monthly["Revenue"]
axes[1,1].plot(monthly["Order YearMonth"], monthly["Margin"], marker="o", color="red", linewidth=2)
axes[1,1].set_title("Monthly Profit Margin")
axes[1,1].set_ylabel("Margin")
axes[1,1].tick_params(axis="x", rotation=45)

plt.tight_layout()
save_plot("01_monthly_trends.png")
plt.show()

# %%
# 3.3 Category / Sub-Category Analysis
cat_perf = df.groupby(["Category", "Sub-Category"]).agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),
    Quantity=("Quantity", "sum")
).reset_index().sort_values("Revenue", ascending=False)

cat_perf["Margin"] = cat_perf["Profit"] / cat_perf["Revenue"]

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Revenue by Sub-Category
top_subcats = cat_perf.nlargest(15, "Revenue")
sns.barplot(data=top_subcats, y="Sub-Category", x="Revenue", hue="Category", ax=axes[0])
axes[0].set_title("Top 15 Sub-Categories by Revenue")

# Margin by Sub-Category (min 10 orders)
margin_subcats = cat_perf[cat_perf["Orders"] >= 10].sort_values("Margin")
sns.barplot(data=margin_subcats, y="Sub-Category", x="Margin", hue="Category", ax=axes[1])
axes[1].set_title("Profit Margin by Sub-Category (min 10 orders)")
axes[1].axvline(0, color="black", linestyle="--", alpha=0.5)

plt.tight_layout()
save_plot("02_category_performance.png")
plt.show()

# %%
# 3.4 Regional Analysis
region_perf = df.groupby("Region").agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique"),
    Customers=("Customer ID", "nunique")
).reset_index()
region_perf["Margin"] = region_perf["Profit"] / region_perf["Revenue"]
region_perf["Revenue per Customer"] = region_perf["Revenue"] / region_perf["Customers"]

print(region_perf.to_string(index=False))

# State-level heatmap (top 20)
state_perf = df.groupby("State").agg(
    Revenue=("Revenue", "sum"),
    Profit=("Profit", "sum"),
    Orders=("Order ID", "nunique")
).reset_index().nlargest(20, "Revenue")

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.barplot(data=state_perf, y="State", x="Revenue", ax=axes[0], palette="Blues_d")
axes[0].set_title("Top 20 States by Revenue")
sns.barplot(data=state_perf.sort_values("Profit"), y="State", x="Profit", ax=axes[1], palette="RdYlGn")
axes[1].set_title("Top 20 States by Profit")
plt.tight_layout()
save_plot("03_regional_performance.png")
plt.show()

# %%
# 3.5 Segment & Ship Mode Analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# Segment
seg = df.groupby("Segment").agg(Revenue=("Revenue","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique")).reset_index()
seg["Margin"] = seg["Profit"] / seg["Revenue"]
sns.barplot(data=seg, x="Segment", y="Revenue", ax=axes[0,0])
axes[0,0].set_title("Revenue by Segment")
sns.barplot(data=seg, x="Segment", y="Margin", ax=axes[0,1])
axes[0,1].set_title("Margin by Segment")

# Ship Mode
ship = df.groupby("Ship Mode").agg(Revenue=("Revenue","sum"), Orders=("Order ID","nunique"), AvgShipDays=("Ship Days","mean")).reset_index()
sns.barplot(data=ship, x="Ship Mode", y="Revenue", ax=axes[1,0])
axes[1,0].set_title("Revenue by Ship Mode")
sns.barplot(data=ship, x="Ship Mode", y="AvgShipDays", ax=axes[1,1])
axes[1,1].set_title("Avg Ship Days by Mode")

plt.tight_layout()
save_plot("04_segment_and_ship_mode.png")
plt.show()

# %%
# 3.6 Correlation Heatmap (numeric features)
numeric_cols = ["Sales", "Quantity", "Discount", "Profit", "Ship Days"]
corr = df[numeric_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="RdBu_r", center=0, fmt=".2f")
plt.title("Correlation Matrix — Numeric Features")
save_plot("05_correlation_matrix.png")
plt.show()

# %%
# =============================================================================
# 4. COHORT ANALYSIS — RETENTION HEATMAP
# =============================================================================

# Cohort = customer's first order month
customer_cohort = df.groupby("Customer ID")["Order Date"].min().dt.to_period("M").rename("CohortMonth")
df = df.merge(customer_cohort, on="Customer ID", how="left")

# Order month
df["OrderMonth"] = df["Order Date"].dt.to_period("M")

# Period number (months since cohort)
df["PeriodNumber"] = (df["OrderMonth"] - df["CohortMonth"]).apply(lambda x: x.n)

# Cohort pivot: count unique customers per cohort per period
cohort_pivot = df.groupby(["CohortMonth", "PeriodNumber"])["Customer ID"].nunique().reset_index()
cohort_pivot = cohort_pivot.pivot(index="CohortMonth", columns="PeriodNumber", values="Customer ID")

# Cohort sizes
cohort_sizes = cohort_pivot[0]

# Retention rate (% of cohort active in each period)
retention = cohort_pivot.div(cohort_sizes, axis=0) * 100
retention = retention.round(1)

# Plot retention heatmap
plt.figure(figsize=(14, 8))
sns.heatmap(
    retention.iloc[:, :13],  # first 12 periods + cohort month
    annot=True, fmt=".1f", cmap="Blues", cbar_kws={"label": "Retention %"}
)
plt.title("Customer Retention Cohort Heatmap (% of cohort active)")
plt.xlabel("Months Since First Order")
plt.ylabel("Cohort Month")
plt.tight_layout()
save_plot("06_cohort_retention.png")
plt.show()

# %%
# =============================================================================
# 5. RFM SEGMENTATION
# =============================================================================

# Reference date = max order date in dataset + 1 day
snapshot_date = df["Order Date"].max() + pd.Timedelta(days=1)

rfm = df.groupby("Customer ID").agg(
    Recency=("Order Date", lambda x: (snapshot_date - x.max()).days),
    Frequency=("Order ID", "nunique"),
    Monetary=("Revenue", "sum")
).reset_index()

# RFM Scores using quartiles (1=worst, 4=best)
rfm["R_Score"] = pd.qcut(rfm["Recency"], q=4, labels=[4,3,2,1]).astype(int)  # lower recency = better
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=4, labels=[1,2,3,4]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"], q=4, labels=[1,2,3,4]).astype(int)

rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)
rfm["RFM_Total"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

# Segment mapping
def assign_segment(row):
    r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
    if r >= 3 and f >= 3 and m >= 3:
        return "Champions"
    elif r >= 3 and f >= 2:
        return "Loyal Customers"
    elif r >= 3 and f == 1:
        return "New Customers"
    elif r == 2 and f >= 2:
        return "Potential Loyalists"
    elif r == 1 and f >= 3:
        return "At Risk"
    elif r == 1 and f == 1:
        return "Lost"
    else:
        return "Others"

rfm["Segment"] = rfm.apply(assign_segment, axis=1)

# Segment summary
seg_summary = rfm.groupby("Segment").agg(
    Count=("Customer ID", "count"),
    Avg_Recency=("Recency", "mean"),
    Avg_Frequency=("Frequency", "mean"),
    Avg_Monetary=("Monetary", "mean"),
    Total_Revenue=("Monetary", "sum")
).reset_index()
seg_summary["Pct_Customers"] = (seg_summary["Count"] / seg_summary["Count"].sum() * 100).round(1)
seg_summary["Pct_Revenue"] = (seg_summary["Total_Revenue"] / seg_summary["Total_Revenue"].sum() * 100).round(1)

print("=== RFM Segment Summary ===")
print(seg_summary.to_string(index=False))

# Customer Lifetime Value (CLV) by RFM segment.
# This is observed historical customer revenue in the dataset, not a forecast
# of future value. It is gross sales and does not subtract returns or costs.
customer_value = df.groupby("Customer ID").agg(
    Observed_CLV=("Revenue", "sum"),
    Orders=("Order ID", "nunique"),
    First_Order=("Order Date", "min"),
    Last_Order=("Order Date", "max"),
).reset_index()
customer_value["Observed_Lifetime_Days"] = (
    customer_value["Last_Order"] - customer_value["First_Order"]
).dt.days
customer_value = customer_value.merge(
    rfm[["Customer ID", "Segment"]], on="Customer ID", how="inner", validate="one_to_one"
)

clv_by_segment = customer_value.groupby("Segment").agg(
    Customers=("Customer ID", "nunique"),
    Mean_Observed_CLV=("Observed_CLV", "mean"),
    Median_Observed_CLV=("Observed_CLV", "median"),
    Total_Observed_Revenue=("Observed_CLV", "sum"),
    Mean_Orders=("Orders", "mean"),
    Median_Lifetime_Days=("Observed_Lifetime_Days", "median"),
).reset_index()
clv_by_segment["Revenue_Share_Pct"] = (
    clv_by_segment["Total_Observed_Revenue"]
    / clv_by_segment["Total_Observed_Revenue"].sum() * 100
).round(2)
clv_by_segment = clv_by_segment.sort_values("Mean_Observed_CLV", ascending=False)

print("\n=== OBSERVED HISTORICAL CLV BY RFM SEGMENT ===")
print("CLV here means observed gross revenue per customer in this dataset, not predicted future value.")
print(clv_by_segment.to_string(index=False, formatters={
    "Mean_Observed_CLV": "${:,.2f}".format,
    "Median_Observed_CLV": "${:,.2f}".format,
    "Total_Observed_Revenue": "${:,.2f}".format,
    "Revenue_Share_Pct": "{:.2f}%".format,
}))

# Visualize segments
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Count
seg_plot = seg_summary.sort_values("Count", ascending=True)
axes[0].barh(seg_plot["Segment"], seg_plot["Count"], color=sns.color_palette("husl", len(seg_plot)))
axes[0].set_title("Customers per RFM Segment")
axes[0].set_xlabel("Count")

# Revenue contribution
seg_plot2 = seg_summary.sort_values("Total_Revenue", ascending=True)
axes[1].barh(seg_plot2["Segment"], seg_plot2["Total_Revenue"], color=sns.color_palette("husl", len(seg_plot2)))
axes[1].set_title("Revenue per RFM Segment")
axes[1].set_xlabel("Revenue ($)")

plt.tight_layout()
save_plot("07_rfm_segments.png")
plt.show()

# RFM 3D scatter (Recency vs Frequency vs Monetary)
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")
scatter = ax.scatter(
    rfm["Recency"], rfm["Frequency"], rfm["Monetary"],
    c=rfm["RFM_Total"], cmap="viridis", alpha=0.6, s=30
)
ax.set_xlabel("Recency (days)")
ax.set_ylabel("Frequency (orders)")
ax.set_zlabel("Monetary ($)")
ax.set_title("RFM 3D Space (color = RFM Total Score)")
plt.colorbar(scatter, label="RFM Total")
save_plot("08_rfm_3d.png")
plt.show()

# %%
# =============================================================================
# 6. SIMPLE FORECASTING — Monthly Revenue (Moving Average + Linear Trend)
# =============================================================================

# Prepare monthly series
ts = monthly.set_index("Order YearMonth")["Revenue"].asfreq("MS")

# 6.1 Moving averages
ts_ma3 = ts.rolling(3).mean()
ts_ma6 = ts.rolling(6).mean()

# 6.2 Simple linear trend (OLS)
from sklearn.linear_model import LinearRegression

X = np.arange(len(ts)).reshape(-1, 1)
y = ts.values.reshape(-1, 1)
model = LinearRegression().fit(X, y)
trend = model.predict(X)

# 6.3 Forecast next 6 months
future_X = np.arange(len(ts), len(ts) + 6).reshape(-1, 1)
forecast = model.predict(future_X)
future_dates = pd.date_range(ts.index[-1] + pd.DateOffset(months=1), periods=6, freq="MS")

# Plot
plt.figure(figsize=(14, 6))
plt.plot(ts.index, ts.values, label="Actual", marker="o")
plt.plot(ts.index, ts_ma3, label="MA(3)", alpha=0.7)
plt.plot(ts.index, ts_ma6, label="MA(6)", alpha=0.7)
plt.plot(ts.index, trend, label=f"Linear Trend (slope={model.coef_[0][0]:.0f}/mo)", linestyle="--", color="red")
plt.plot(future_dates, forecast, label="Forecast (6 mo)", marker="s", color="orange", linestyle=":")
plt.axvline(ts.index[-1], color="gray", linestyle=":", alpha=0.5)
plt.title("Monthly Revenue — Actual, Moving Averages, Trend & Forecast")
plt.ylabel("Revenue ($)")
plt.legend()
plt.tight_layout()
save_plot("09_revenue_forecast.png")
plt.show()

# Forecast table
forecast_df = pd.DataFrame({
    "Month": future_dates.strftime("%Y-%m"),
    "Forecast_Revenue": forecast.flatten().round(2)
})
print("\n=== 6-Month Revenue Forecast ===")
print(forecast_df.to_string(index=False))

# %%
# =============================================================================
# 7. CUSTOMER LIFETIME VALUE (Simple Historical LTV)
# =============================================================================

# LTV = Avg Revenue per Customer per Month * Expected Lifetime (months)
# Using cohort data to estimate lifetime

cohort_ltv = df.groupby(["Customer ID", "CohortMonth"]).agg(
    First_Order=("Order Date", "min"),
    Last_Order=("Order Date", "max"),
    Total_Revenue=("Revenue", "sum"),
    Total_Orders=("Order ID", "nunique"),
    Months_Active=("OrderMonth", "nunique")
).reset_index()

cohort_ltv["Lifetime_Days"] = (cohort_ltv["Last_Order"] - cohort_ltv["First_Order"]).dt.days
cohort_ltv["Lifetime_Months"] = (cohort_ltv["Lifetime_Days"] / 30.44).clip(lower=1)
cohort_ltv["Monthly_Value"] = cohort_ltv["Total_Revenue"] / cohort_ltv["Lifetime_Months"]

# Average LTV by cohort
avg_ltv = cohort_ltv.groupby("CohortMonth").agg(
    Customers=("Customer ID", "count"),
    Avg_Lifetime_Months=("Lifetime_Months", "mean"),
    Avg_Monthly_Value=("Monthly_Value", "mean"),
    Avg_Total_Revenue=("Total_Revenue", "mean")
).reset_index()

avg_ltv["Estimated_LTV"] = avg_ltv["Avg_Monthly_Value"] * avg_ltv["Avg_Lifetime_Months"]

print("\n=== Cohort LTV Estimates ===")
print(avg_ltv.to_string(index=False))

# %%
# =============================================================================
# 8. EXPORT CLEANED DATA & RFM FOR TABLEAU / FURTHER ANALYSIS
# =============================================================================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Cleaned master dataset
df.to_parquet(OUTPUT_DIR / "superstore_cleaned.parquet", index=False)
print(f"✅ Saved cleaned data to {OUTPUT_DIR}/superstore_cleaned.parquet")

# RFM table
rfm.to_csv(OUTPUT_DIR / "rfm_segmentation.csv", index=False)
print(f"✅ Saved RFM segmentation to {OUTPUT_DIR}/rfm_segmentation.csv")

# Customer-level observed CLV and segment summary
customer_value.to_csv(OUTPUT_DIR / "customer_observed_clv.csv", index=False)
clv_by_segment.to_csv(OUTPUT_DIR / "clv_by_rfm_segment.csv", index=False)
dq_checks.to_csv(OUTPUT_DIR / "data_quality_checks.csv", index=False)
print(f"✅ Saved CLV by RFM segment to {OUTPUT_DIR}/clv_by_rfm_segment.csv")
print(f"✅ Saved data-quality checks to {OUTPUT_DIR}/data_quality_checks.csv")

# Cohort retention
retention.reset_index().to_csv(OUTPUT_DIR / "cohort_retention.csv", index=False)
print(f"✅ Saved cohort retention to {OUTPUT_DIR}/cohort_retention.csv")

# Monthly KPIs
monthly.to_csv(OUTPUT_DIR / "monthly_kpis.csv", index=False)
print(f"✅ Saved monthly KPIs to {OUTPUT_DIR}/monthly_kpis.csv")

print("\n🎉 All done! Ready for Tableau / Power BI / further modeling.")

# %%
# =============================================================================
# 9. QUICK INSIGHTS SUMMARY (for README / Presentation)
# =============================================================================

champions = seg_summary[seg_summary["Segment"] == "Champions"]
champions_count = int(champions["Count"].sum())
champions_revenue_share = float(champions["Pct_Revenue"].sum())

subcat_margin = cat_perf[cat_perf["Orders"] >= 10].sort_values("Margin", ascending=False)
best_subcat = subcat_margin.iloc[0]
worst_subcat = subcat_margin.iloc[-1]
category_revenue = cat_perf.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
best_region = region_perf.sort_values("Revenue", ascending=False).iloc[0]

month1_retention = retention[1].mean() if 1 in retention.columns else float("nan")
month3_retention = retention[3].mean() if 3 in retention.columns else float("nan")

insights = f"""
## 📊 Superstore Analysis — Key Insights

**Period:** {df['Order Date'].min().strftime('%b %Y')} – {df['Order Date'].max().strftime('%b %Y')}
**Total Revenue:** ${total_revenue:,.0f} | **Total Profit:** ${total_profit:,.0f} | **Margin:** {total_profit/total_revenue*100:.1f}%
**Customers:** {total_customers:,} | **Orders:** {total_orders:,} | **AOV:** ${avg_order_value:,.0f}

### 🎯 Top Findings
1. **Top Category:** {category_revenue.index[0]} (${category_revenue.iloc[0]:,.0f})
2. **Best Sub-Category Margin (min 10 orders):** {best_subcat['Sub-Category']} ({best_subcat['Margin']*100:.1f}%)
3. **Worst Sub-Category Margin:** {worst_subcat['Sub-Category']} ({worst_subcat['Margin']*100:.1f}%)
4. **Best Region:** {best_region['Region']} (${best_region['Revenue']:,.0f})
5. **RFM Champions:** {champions_count} customers ({champions_revenue_share:.1f}% of revenue)
6. **Retention:** Month-1 avg {month1_retention:.1f}% | Month-3 avg {month3_retention:.1f}%
7. **Forecast:** Next 6 months revenue projected at ${forecast_df['Forecast_Revenue'].sum():,.0f} (linear trend)

### 💡 Recommendations
- Prioritise the loss-making sub-categories for pricing and supplier review.
- Build retention campaigns for **"At Risk"** and **"Potential Loyalists"** segments.
- Protect the **"Champions"** segment with loyalty benefits and early access.
"""

print(insights)

# Save insights to file
with open(OUTPUT_DIR / "key_insights.md", "w") as f:
    f.write(insights)
print(f"\n✅ Insights saved to {OUTPUT_DIR}/key_insights.md")
