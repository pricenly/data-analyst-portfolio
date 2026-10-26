 # E-Commerce SQL Analytics

 **Portfolio Project 1** - Junior Data Analyst | Daniil Marchenko

 ---

 ## Business Context

 Analyze transactional data from a UK-based online retailer (UCI Online Retail dataset, 2009-2011) to answer:

 1. **Invoice Funnel Proxy** - What share of recorded invoices has positive net revenue and is not cancelled?
 2. **Revenue Reversals** - How much recorded value is reversed by returns/cancellation lines, and which SKUs contribute most?
 3. **Retention** - How well do monthly cohorts retain? (Cohort heatmap)
 4. **RFM Segmentation** - Who are our Champions vs. At-Risk customers?
 5. **LTV by Cohort** - Cumulative revenue per customer over 12 months
 6. **Product Performance** - Top products by revenue & reorder rate
 7. **Geographic Distribution** - Revenue by country

 ---

 ## Dataset

 | Attribute | Value |
 |-----------|-------|
 | **Source** | UCI Machine Learning Repository / Kaggle |
 | **Period** | Dec 2009 - Dec 2011 |
 | **Rows** | ~540k transactions |
 | **Customers** | ~4,300 unique (with ID) |
 | **Countries** | 38 |
 | **Products** | ~3,800 SKUs |

 **Schema:** invoice_no, stock_code, description, quantity, invoice_date, unit_price, customer_id, country

 ---

 ## Tech Stack

 - **PostgreSQL 15+** (CTEs, Window Functions, NTILE, LAG, ROW_NUMBER, RANK)
 - **DBeaver / pgAdmin / psql** for execution
 - **Git** for version control

 ---

 ## Quick Start

 ### 1. Start PostgreSQL (Docker - recommended)
 ```bash
 docker run -d \
   --name pg-retail \
   -e POSTGRES_PASSWORD=postgres \
   -e POSTGRES_DB=retail \
   -p 5432:5432 \
   postgres:15
 ```

 ### 2. Load Data

 **Option A: Python (easiest)**
 ```bash
 pip install pandas openpyxl sqlalchemy psycopg2-binary
 python load_data.py  # edit DATABASE_URL first
 ```

 **Option B: SQL \copy**
 ```bash
 # Download CSV from Kaggle, then in psql:
 \copy online_retail_staging FROM '/path/to/online_retail.csv' CSV HEADER;
 # Then run the CREATE TABLE AS SELECT from load_data.sql
 ```

 ### 3. Run Analysis
 ```bash
 psql -h localhost -U postgres -d retail -f analysis.sql
 ```

 ---

 ## Key Queries in analysis.sql

 | Section | Description | Key Techniques |
 |---------|-------------|----------------|
 | 0 | Data Quality Checks | Null profiling, cancellation rate |
| 1 | Invoice Funnel Proxy | Ordered steps, `LAG`, step drop-off %, baseline retention |
| 1B | Revenue Reversals | Cancellation/return reversal value and share by category |
| 1C | SKU Reversal Hotspots | Ranked SKUs by recorded negative-line value |
 | 2 | Monthly Revenue Trend | DATE_TRUNC, time-series aggregation |
 | 3 | Cohort Retention | CTE + AGE + period_number + self-join |
 | 4 | RFM Segmentation | NTILE(4) quartiles + CASE mapping |
 | 5 | LTV by Cohort | Cumulative SUM() OVER (PARTITION BY ... ORDER BY ...) |
 | 6 | Top Products | Reorder rate calculation |
 | 7 | LTV Prediction | First-3-months vs 12-month ratio |
 | 8 | Geographic Distribution | ARPU by country |
 | 9 | Window Functions Demo | Running totals, RANK/DENSE_RANK per country |

 ---

 ## Sample Outputs (add screenshots after running)

 - Funnel conversion rates table
 - Cohort retention heatmap (export to CSV - Excel conditional formatting)
 - RFM segment distribution (bar chart)
 - LTV curves by cohort (line chart)

 ---

## Funnel Interpretation & Revenue Hotspots

`analysis.sql` reports the invoice count at each proxy step, step-over-step
drop-off rate, and retained share versus all recorded invoices. The source is
transactional: it has no session, cart, or checkout-attempt events. Therefore
these values **must not be presented as website conversion or abandonment rates**.

The revenue-reversal queries identify realized negative line value (returns)
and its distribution by reversal type and SKU. They highlight where recorded
revenue was reversed; they do **not** estimate hypothetical revenue from
abandoned carts or prove preventable loss. Use event-level funnel data and
return reason/cost data for those conclusions.

## Business Insights (populate from query results)

- **Largest proxy step drop-off:** [step] at [X]%
- **Recorded reversal value:** [$X], with [type] contributing [Y]%
- **Top SKU reversal hotspot:** [SKU] at [$X]
 - **Month-1 retention:** Y% average across cohorts
 - **Champions segment:** Z% of customers drive W% of revenue
 - **Top country by ARPU:** [Country] at $XXX
 - **Product reorder leaders:** [SKU] with XX% reorder rate

 ---

 ## File Structure

 ```
 sql-ecomm-funnel/
 в”њв”Ђв”Ђ analysis.sql          # Main analysis (15+ queries)
 в”њв”Ђв”Ђ load_data.sql         # DDL + COPY instructions
 в”њв”Ђв”Ђ load_data.py          # Python loader (alternative)
 в””в”Ђв”Ђ README.md             # This file
 ```

 ---

 ## Related Projects

 - Project 2: Superstore Python EDA - RFM, Cohorts, Forecasting in pandas
 - Project 3: Marketing ROI Dashboard - Tableau visualization

 ---

 *Part of Daniil Marchenko's Data Analyst Portfolio*
