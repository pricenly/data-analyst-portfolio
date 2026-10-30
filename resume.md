# DANIIL MARCHENKO

**Junior Data Analyst / Analytics Intern**
Kyiv, Ukraine · +380 67 110 9366 · beshary47@gmail.com
[LinkedIn](https://www.linkedin.com/in/daniil-marchenko-7660203b6/) · [GitHub](https://github.com/pricenly/data-analyst-portfolio) · English B2

---

## SUMMARY

Second-year Digital Economics student moving into data analytics. I build small,
reproducible analyses end to end: clean the data, document every exclusion,
answer one business question, and state what the data cannot support. Four
public projects cover SQL, Python EDA, cohort retention and a Tableau dashboard
specification. Looking for a Junior Data Analyst or internship role (remote,
hybrid or Kyiv office).

---

## TECHNICAL SKILLS

- **SQL (PostgreSQL):** CTEs, window functions (`LAG`, `FIRST_VALUE`, `NTILE`,
  `RANK`), cohort retention, RFM segmentation, joins, aggregation, indexes.
- **Python:** pandas, numpy, matplotlib, seaborn, scikit-learn (linear
  regression); data validation, CLI scripts, reproducible pipelines.
- **BI:** Tableau calculated fields, LOD expressions, table calculations and
  parameter-driven scenarios (dashboard design); Excel (pivot tables, XLOOKUP).
- **Methods:** cohort retention, RFM segmentation, funnel analysis, unit
  economics (CAC, LTV, ROAS), data-quality checks, IQR outlier handling.
- **Tools:** Git / GitHub, VS Code, DBeaver, Jupyter Lab.

---

## PROJECTS

**Superstore EDA, RFM Segmentation & Forecasting** — Python, pandas, seaborn
[github.com/pricenly/data-analyst-portfolio](https://github.com/pricenly/data-analyst-portfolio/tree/main/superstore-analytics)
- Cleaned 10,800 raw rows: removed the empty Returns block and 504 exact
  duplicates, logged each exclusion, and flagged IQR outliers instead of
  deleting them.
- Analysed $2.30M revenue and $286K profit across 793 customers; identified
  Tables as the loss-making sub-category (−8.6% margin) against Labels (44.4%).
- Scored customers with quartile RFM: Champions are 22% of customers but 35% of
  revenue.
- Built a 6-month baseline forecast (MA-3/MA-6 + linear trend, ≈$433K) and
  documented why it is a baseline, not a seasonal model.

**E-Commerce SQL Analytics** — PostgreSQL, CTEs, window functions
- Wrote 9 query sections: data-quality checks, invoice-quality funnel proxy,
  revenue reversals by type and SKU, monthly trends, cohort retention, RFM,
  cumulative LTV, product reorder rates and country ARPU.
- Documented that the dataset contains no cart or session events, so the output
  is explicitly not presented as website conversion.

**Cohort Retention Pipeline** — Python, pandas, matplotlib (synthetic data)
- Built a reproducible generator plus a validation pipeline: required columns,
  date parsing, duplicates, blank users, non-positive revenue, IQR flags.
- Produced a month-0…month-11 retention matrix and annotated heatmap, and
  separated "not yet observable" cells from true 0% retention.

**Marketing ROI Dashboard Specification** — Tableau, LOD, parameters
- Designed a four-page dashboard (executive overview, channel deep-dive, cohort
  view, spend scenario) with a full calculated-field library.
- Built a seeded data generator for spend, attributed orders and customer
  lifetime revenue; documented that elasticity inputs are assumptions.

---

## EXPERIENCE

**Customer Retention & Sales Analytics Specialist** — Digital / e-commerce agency (remote)
*2023 – Present*
- Tracked conversion and repeat-purchase metrics for high-ticket accounts and
  reported drop-off points to account managers.
- A/B tested outreach scripts and messaging, feeding results back into the next
  campaign cycle.
- Automated weekly reporting in Google Sheets, removing 4+ hours of manual work
  per week.

**Founder / Commercial Operations** — D2C streetwear project (Kyiv)
*2021 – 2023*
- Modelled unit economics (CAC, gross margin, AOV) in Excel to set pricing and
  negotiate supply costs.
- Analysed repeat-purchase behaviour and customer feedback to adjust the
  product range.

---

## EDUCATION

**B.Sc. in Digital Economics** — National University of Kyiv-Mohyla Academy
*2023 – 2027 (expected), 2nd year*
Coursework: statistics, econometrics, micro- and macroeconomics, business
modelling, data-driven decision making.

---

## LANGUAGES

Ukrainian — native · Russian — native · English — B2 (upper-intermediate)
