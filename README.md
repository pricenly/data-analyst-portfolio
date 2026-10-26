 # Daniil Marchenko | Junior Data Analyst Portfolio
 
 📍 **Kyiv, Ukraine (GMT+2)** • 🇬🇧 **English B2** (Upper-Intermediate)  
 🎓 **B.Sc. Digital Economics (2nd Year)**  
 🔗 [LinkedIn Profile](https://www.linkedin.com/in/daniil-marchenko-7660203b6/) • 🐙 [GitHub Profile](https://github.com/pricenly) • 📧 [Email Me](mailto:daniil.marchenko@example.com)
 
 ---
 
 ## 🎯 Executive Summary
 
 Aspiring **Junior Data Analyst / Analytics Intern** with a solid educational background in quantitative economics, econometrics, and business modeling. Experienced in hands-on commercial funnels, conversion optimization, and automated reporting.
 
 This repository contains **3 production-grade portfolio projects** demonstrating end-to-end proficiency across modern data analytics workflows:
 1. **Database querying & transformation** via Advanced SQL (`PostgreSQL`).
 2. **Exploratory Data Analysis, Cohort Retention & RFM Segmentation** via `Python` (`pandas`, `seaborn`).
 3. **Business Intelligence, Executive Reporting & What-If Simulations** via `Tableau`.
 
 ---
 
 ## 🛠 Tech Stack & Core Competencies
 
 | Category | Technologies & Methodologies |
 | :--- | :--- |
 | **SQL & Databases** | PostgreSQL, CTEs, Window Functions (`NTILE`, `LAG`, `RANK`, `FIRST_VALUE`), Multi-table Joins, Aggregations, Indexing |
 | **Python Stack** | `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn` (linear trends), Jupyter Lab |
 | **BI & Data Viz** | Tableau Public / Desktop (LOD Expressions `{FIXED}`, Table Calcs, Parameters, Interactive Dashboards) |
 | **Analytical Frameworks** | Cohort Retention Analysis, RFM Segmentation, E-commerce Funnel Conversion, Customer Lifetime Value (LTV), Unit Economics (CAC/LTV, ROAS) |
 | **Tools & Best Practices** | Git, GitHub, VS Code, DBeaver, Clean Code, Reproducible Pipelines |
 
 ---
 
 ## 📂 Featured Portfolio Projects
 
 ### 🛒 [1. E-Commerce SQL Analytics](./sql-ecomm-funnel)
 > **Tech Stack:** PostgreSQL 15+, Complex CTEs, Window Functions, DBeaver  
 > **Dataset:** Online Retail II (~540K transaction records)
 
 * **Sales Funnel Analysis:** Structured multi-step conversion funnel (`Cart -> Checkout -> Paid`) using `FIRST_VALUE()` and `LAG()` to identify drop-off bottlenecks.
 * **Monthly Cohort Retention Matrix:** Calculated customer acquisition cohorts and tracked month-over-month retention using `AGE()` and interval metrics.
 * **Quartile-based RFM Segmentation:** Segmented the user base into actionable groups (*Champions*, *Loyal*, *At Risk*, *Lost*) using `NTILE(4)`.
 * **Cumulative LTV:** Computed 12-month forward cumulative revenue per cohort to evaluate customer value dynamics.
 
 📁 **Key Files:** [`sql-ecomm-funnel/analysis.sql`](./sql-ecomm-funnel/analysis.sql) • [`sql-ecomm-funnel/README.md`](./sql-ecomm-funnel/README.md)
 
 ---
 
 ### 📊 [2. Superstore Exploratory Analysis & Forecasting](./superstore-analytics)
 > **Tech Stack:** Python 3.11, pandas, seaborn, matplotlib, scikit-learn  
 > **Dataset:** Kaggle Sample Superstore (~10K records)
 
 * **Data Cleansing & Integrity:** Automated missing value imputation, duplicate removal, and outlier detection using Interquartile Range (IQR).
 * **Exploratory Data Analysis:** Evaluated profitability margins across product sub-categories, customer segments, and states.
 * **Cohort Retention Heatmap:** Visualized retention rates over a 12-month window with annotated heatmaps.
 * **RFM Behavioral Clustering:** Implemented quartile scoring and built a 3D feature space (Recency vs. Frequency vs. Monetary).
 * **Revenue Forecasting:** Applied moving averages (`MA-3`, `MA-6`) and linear trend extrapolation for upcoming quarters.
 
 📁 **Key Files:** [`superstore-analytics/eda_notebook.py`](./superstore-analytics/eda_notebook.py) • [`superstore-analytics/requirements.txt`](./superstore-analytics/requirements.txt)
 
 ---
 
 ### 📈 [3. Marketing ROI & Attribution Dashboard](./tableau-marketing-roi)
 > **Tech Stack:** Tableau Public / Desktop, Level of Detail (LOD) Calculations, Synthetic Data Generation  
 > **Domain:** D2C E-Commerce & Performance Marketing
 
 * **Executive Overview:** High-level scorecard monitoring blended CAC, ROAS, Spend, and Revenue velocity across paid channels (Meta, Google, TikTok, Email).
 * **LOD Expressions:** Engineered `{FIXED [Customer ID] : MIN([Order Date])}` calculations to dynamically evaluate cohort lifetime values.
 * **Scenario Simulator:** Designed interactive what-if parameters to model revenue elasticity when reallocating paid ad spend.
 * **Calculated Fields Architecture:** Documented all production calculations (payback period, blended metrics, retention lookup).
 
 📁 **Key Files:** [`tableau-marketing-roi/calculated_fields.md`](./tableau-marketing-roi/calculated_fields.md) • [`tableau-marketing-roi/generate_data.py`](./tableau-marketing-roi/generate_data.py)
 
 ---
 
 ## 📁 Repository Structure
 
 ```text
 .
 ├── .gitignore                          # Root ignore file (excludes data dumps, venv, temporary files)
 ├── README.md                           # Main portfolio landing page
 ├── deploy_instructions.md              # Git setup & deployment cheat-sheet
 ├── linkedin_profile.md                 # Profile copy, Headline, About & Launch Post
 │
 ├── sql-ecomm-funnel/                   # Project 1: SQL queries & schema setup
 │   ├── analysis.sql
 │   ├── load_data.sql
 │   └── README.md
 │
 ├── superstore-analytics/               # Project 2: Python scripts & dependencies
 │   ├── eda_notebook.py
 │   ├── requirements.txt
 │   └── README.md
 │
 └── tableau-marketing-roi/              # Project 3: BI logic & synthetic data pipeline
     ├── generate_data.py
     ├── calculated_fields.md
     └── README.md
 ```
 
 ---
 
 ## 📬 Contact & Availability
 
 * **Role Target:** Junior Data Analyst / Analytics Intern / Business Analyst Trainee
 * **Availability:** Full-Time / Part-Time (Flexible for academic obligations)
 * **Location:** Kyiv, Ukraine (Open to Remote / Hybrid / Relocation)
 * **LinkedIn:** [daniil-marchenko](https://www.linkedin.com/in/daniil-marchenko-7660203b6/)
 * **GitHub:** [@pricenly](https://github.com/pricenly)
