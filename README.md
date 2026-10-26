 # Daniil Marchenko | Junior Data Analyst Portfolio

 рџ“Ќ **Kyiv, Ukraine (GMT+2)** вЂў рџ‡¬рџ‡§ **English B2** (Upper-Intermediate)
 рџЋ“ **B.Sc. Digital Economics (2nd Year)**
 рџ”— [LinkedIn Profile](https://www.linkedin.com/in/daniil-marchenko-7660203b6/) вЂў рџђ™ [GitHub Profile](https://github.com/pricenly) вЂў рџ“§ [Email Me](mailto:daniil.marchenko@example.com)

 ---

 ## рџЋЇ Executive Summary

 Aspiring **Junior Data Analyst / Analytics Intern** with a solid educational background in quantitative economics, econometrics, and business modeling. Experienced in hands-on commercial funnels, conversion optimization, and automated reporting.

This repository contains **three portfolio projects** covering modern data analytics workflows:
 1. **Database querying & transformation** via Advanced SQL (`PostgreSQL`).
 2. **Exploratory Data Analysis, Cohort Retention & RFM Segmentation** via `Python` (`pandas`, `seaborn`).
 3. **Business Intelligence, Executive Reporting & What-If Simulations** via `Tableau`.

 ---

 ## рџ›  Tech Stack & Core Competencies

 | Category | Technologies & Methodologies |
 | :--- | :--- |
 | **SQL & Databases** | PostgreSQL, CTEs, Window Functions (`NTILE`, `LAG`, `RANK`, `FIRST_VALUE`), Multi-table Joins, Aggregations, Indexing |
 | **Python Stack** | `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn` (linear trends), Jupyter Lab |
 | **BI & Data Viz** | Tableau Public / Desktop (LOD Expressions `{FIXED}`, Table Calcs, Parameters, Interactive Dashboards) |
 | **Analytical Frameworks** | Cohort Retention Analysis, RFM Segmentation, E-commerce Funnel Conversion, Customer Lifetime Value (LTV), Unit Economics (CAC/LTV, ROAS) |
 | **Tools & Best Practices** | Git, GitHub, VS Code, DBeaver, Clean Code, Reproducible Pipelines |

 ---

 ## рџ“‚ Featured Portfolio Projects

 ### рџ›’ [1. E-Commerce SQL Analytics](./sql-ecomm-funnel)
 > **Tech Stack:** PostgreSQL 15+, Complex CTEs, Window Functions, DBeaver
 > **Dataset:** Online Retail II (~540K transaction records)

 * **Sales Funnel Analysis:** Structured multi-step conversion funnel (`Cart -> Checkout -> Paid`) using `FIRST_VALUE()` and `LAG()` to identify drop-off bottlenecks.
 * **Monthly Cohort Retention Matrix:** Calculated customer acquisition cohorts and tracked month-over-month retention using `AGE()` and interval metrics.
 * **Quartile-based RFM Segmentation:** Segmented the user base into actionable groups (*Champions*, *Loyal*, *At Risk*, *Lost*) using `NTILE(4)`.
 * **Cumulative LTV:** Computed 12-month forward cumulative revenue per cohort to evaluate customer value dynamics.

 рџ“Ѓ **Key Files:** [`sql-ecomm-funnel/analysis.sql`](./sql-ecomm-funnel/analysis.sql) вЂў [`sql-ecomm-funnel/README.md`](./sql-ecomm-funnel/README.md)

 ---

 ### рџ“Љ [2. Superstore Exploratory Analysis & Forecasting](./superstore-analytics)
 > **Tech Stack:** Python 3.11, pandas, seaborn, matplotlib, scikit-learn
 > **Dataset:** Kaggle Sample Superstore (~10K records)

 * **Data Cleansing & Integrity:** Automated missing value imputation, duplicate removal, and outlier detection using Interquartile Range (IQR).
 * **Exploratory Data Analysis:** Evaluated profitability margins across product sub-categories, customer segments, and states.
 * **Cohort Retention Heatmap:** Visualized retention rates over a 12-month window with annotated heatmaps.
 * **RFM Behavioral Clustering:** Implemented quartile scoring and built a 3D feature space (Recency vs. Frequency vs. Monetary).
 * **Revenue Forecasting:** Applied moving averages (`MA-3`, `MA-6`) and linear trend extrapolation for upcoming quarters.

 рџ“Ѓ **Key Files:** [`superstore-analytics/eda_notebook.py`](./superstore-analytics/eda_notebook.py) вЂў [`superstore-analytics/requirements.txt`](./superstore-analytics/requirements.txt)

 ---

 ### рџ“€ [3. Marketing ROI & Attribution Dashboard](./tableau-marketing-roi)
 > **Tech Stack:** Tableau Public / Desktop, Level of Detail (LOD) Calculations, Synthetic Data Generation
 > **Domain:** D2C E-Commerce & Performance Marketing

 * **Executive Overview:** High-level scorecard monitoring blended CAC, ROAS, Spend, and Revenue velocity across paid channels (Meta, Google, TikTok, Email).
 * **LOD Expressions:** Engineered `{FIXED [Customer ID] : MIN([Order Date])}` calculations to dynamically evaluate cohort lifetime values.
 * **Scenario Simulator:** Designed interactive what-if parameters to model revenue elasticity when reallocating paid ad spend.
 * **Calculated Fields Architecture:** Documented all production calculations (payback period, blended metrics, retention lookup).

 рџ“Ѓ **Key Files:** [`tableau-marketing-roi/calculated_fields.md`](./tableau-marketing-roi/calculated_fields.md) вЂў [`tableau-marketing-roi/generate_data.py`](./tableau-marketing-roi/generate_data.py)

 ---

## Business Impact & Key Metrics

The analyses are designed to turn raw data into prioritizable business questions. Dataset-specific results should be filled in after running the projects; no outcome percentages are claimed here before execution.

| Project | Business value | Key metrics surfaced |
| :--- | :--- | :--- |
| **E-Commerce SQL** | Locate invoice-quality drop-offs and prioritize recorded return/reversal hotspots for investigation. The source is transactional, so the invoice funnel is explicitly a proxyвЂ”not website-session conversion. | Step drop-off rate; retained invoices vs. baseline; reversed revenue and reversal share; top 10 SKUs by negative-line value; cohort retention; 12-month cumulative revenue per customer. |
| **Superstore Python** | Identify customer groups and product/geography areas for retention, pricing, and profitability follow-up. | Observed historical gross revenue per RFM customer (labeled observed CLV, not a forecast); revenue share by segment; customer count; order frequency; profit margin; cohort retention; data-quality issue counts; six-month linear-trend projection. |
| **Marketing ROI / Tableau** | Provide a reproducible way to compare channels and explore spend-change scenarios using generated sample data. | Spend, attributed revenue, ROAS, CAC, profit, cohort LTV:CAC and scenario-projected revenue. **These are synthetic-data demonstrations, not real campaign results; the Tableau workbook/dashboard still needs to be built and published.** |

### Results reporting

After executing the SQL queries and Python analysis, replace the result placeholders in the project READMEs with outputs from the actual datasets (including dataset period, currency, filters, and definitions). For the Tableau demo, label generated figures as synthetic. Do not describe these metrics as realized business impact or causal uplift without validated production data and an appropriate experiment.

---

 ## рџ“Ѓ Repository Structure

 ```text
 .
 в”њв”Ђв”Ђ .gitignore                          # Root ignore file (excludes data dumps, venv, temporary files)
 в”њв”Ђв”Ђ README.md                           # Main portfolio landing page
 в”њв”Ђв”Ђ deploy_instructions.md              # Git setup & deployment cheat-sheet
 в”њв”Ђв”Ђ linkedin_profile.md                 # Profile copy, Headline, About & Launch Post
 в”‚
 в”њв”Ђв”Ђ sql-ecomm-funnel/                   # Project 1: SQL queries & schema setup
 в”‚   в”њв”Ђв”Ђ analysis.sql
 в”‚   в”њв”Ђв”Ђ load_data.sql
 в”‚   в””в”Ђв”Ђ README.md
 в”‚
 в”њв”Ђв”Ђ superstore-analytics/               # Project 2: Python scripts & dependencies
 в”‚   в”њв”Ђв”Ђ eda_notebook.py
 в”‚   в”њв”Ђв”Ђ requirements.txt
 в”‚   в””в”Ђв”Ђ README.md
 в”‚
 в””в”Ђв”Ђ tableau-marketing-roi/              # Project 3: BI logic & synthetic data pipeline
     в”њв”Ђв”Ђ generate_data.py
     в”њв”Ђв”Ђ calculated_fields.md
     в””в”Ђв”Ђ README.md
 ```

 ---

 ## рџ“¬ Contact & Availability

 * **Role Target:** Junior Data Analyst / Analytics Intern / Business Analyst Trainee
 * **Availability:** Full-Time / Part-Time (Flexible for academic obligations)
 * **Location:** Kyiv, Ukraine (Open to Remote / Hybrid / Relocation)
 * **LinkedIn:** [daniil-marchenko](https://www.linkedin.com/in/daniil-marchenko-7660203b6/)
 * **GitHub:** [@pricenly](https://github.com/pricenly)
