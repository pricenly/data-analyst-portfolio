# Superstore Sales Analysis — Python EDA, RFM & Forecasting

**Portfolio project** · Daniil Marchenko · Junior Data Analyst

A full exploratory analysis of the public Kaggle **Sample Superstore** dataset
(10,800 raw rows, 2015–2018) in a single reproducible script.

---

## Business questions

1. Where does revenue and profit actually come from — category, geography, segment?
2. Which customers carry the business, and which are about to churn?
3. How well do monthly acquisition cohorts retain?
4. What is a defensible baseline for the next 6 months?

---

## Dataset

| Attribute | Value |
|---|---|
| Source | [Kaggle — Sample Superstore](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) |
| File | `data/SampleSuperstore.csv` (bundled, 2.3 MB) |
| Period | 2015-01-03 → 2018-12-30 |
| Raw rows / columns | 10,800 / 21 |
| Analysis rows | 9,994 after removing the empty Returns block and 504 exact duplicates |

The bundled CSV is the widely redistributed public sample. It is used here for
practice and comparison, not as a client deliverable.

---

## Stack

- Python 3.10+, pandas, numpy
- matplotlib, seaborn
- scikit-learn (`LinearRegression` for the trend baseline)
- pyarrow (Parquet export)

Install:

```bash
pip install -r requirements.txt
```

---

## Run

```bash
python eda_notebook.py
```

The script resolves paths relative to itself, so it can be started from any
working directory. Outputs:

```text
images/                       9 publication-ready charts (150 dpi)
output/superstore_cleaned.parquet
output/rfm_segmentation.csv
output/customer_observed_clv.csv
output/clv_by_rfm_segment.csv
output/cohort_retention.csv
output/monthly_kpis.csv
output/data_quality_checks.csv
output/key_insights.md
```

`eda_notebook.py` uses Jupytext `# %%` cell markers, so it also opens as a
notebook:

```bash
jupytext --to notebook eda_notebook.py
```

---

## What the analysis does

| Section | Work |
|---|---|
| 0 | Setup, paths, figure export helper |
| 1 | Load the CSV with parsed dates |
| 2 | Data quality: missing identity rows, duplicates, date order, negative sales, quantity, discount range, IQR outliers; `Postal Code` normalised to one dtype |
| 3 | EDA: monthly revenue / profit / orders / margin, category and sub-category, states, regions, segment, ship mode, correlations |
| 4 | Monthly cohort retention matrix and heatmap |
| 5 | Quartile RFM, 7 segments, observed historical revenue per customer, 3D RFM view |
| 6 | MA(3), MA(6), linear trend and a 6-month projection |
| 7 | Cohort lifetime value (descriptive, not predictive) |
| 8 | Export cleaned data and tables |
| 9 | Auto-generated `key_insights.md` |

---

## Results (actual run)

| Metric | Value |
|---|---|
| Revenue | $2,297,201 |
| Profit / margin | $286,397 / 12.5% |
| Customers / orders / AOV | 793 / 5,009 / $459 |
| Top category | Technology — $836,154 |
| Best sub-category margin (≥10 orders) | Labels — 44.4% |
| Worst sub-category margin | Tables — −8.6% |
| Best region | West — $725,458 (14.9% margin) |
| RFM Champions | 176 customers, 35.0% of revenue |
| Month-1 / month-3 retention | 12.1% / 15.0% avg |
| 6-month linear forecast | $433,275 |

---

## Charts

| File | Content |
|---|---|
| `01_monthly_trends.png` | Revenue, profit, orders and margin by month |
| `02_category_performance.png` | Top sub-categories by revenue, margin by sub-category |
| `03_regional_performance.png` | Top 20 states by revenue and profit |
| `04_segment_and_ship_mode.png` | Segment revenue/margin, ship-mode volume and lead time |
| `05_correlation_matrix.png` | Correlation between sales, quantity, discount, profit, ship days |
| `06_cohort_retention.png` | Monthly cohort retention heatmap |
| `07_rfm_segments.png` | Customers and revenue per RFM segment |
| `08_rfm_3d.png` | Recency × frequency × monetary scatter |
| `09_revenue_forecast.png` | Actual, MA(3), MA(6), trend and 6-month projection |

---

## Limitations

- "CLV" in this project is **observed historical revenue per customer**, not a
  prediction of future value.
- The linear trend ignores seasonality; it is a baseline, not a forecast model.
- Retention is low because Superstore is a retail catalogue, not a subscription
  product. The number is descriptive.
- Profit figures come from the dataset; no cost model was reconstructed.

---

*Part of [Daniil Marchenko's data analyst portfolio](../README.md).*
