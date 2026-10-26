 # Marketing ROI Dashboard - Tableau Public
 
 **Portfolio Project 3** - Junior Data Analyst | Daniil Marchenko
 
 ---
 
 ## Business Context
 
 Executive-facing dashboard for a D2C e-commerce brand to answer:
 
 1. **Channel Performance** - Spend vs Revenue, ROAS, CAC by channel/week
 2. **CAC Payback Period** - Months to recover acquisition cost per channel
 3. **Attribution Waterfall** - First-touch vs Last-touch vs Data-driven
 4. **Scenario Planning** - What if we increase TikTok spend by 20%?
 5. **Cohort LTV:CAC** - Lifetime value to acquisition cost by acquisition month
 
 ---
 
 ## Data Sources (Simulated / Public)
 
 | Source | Description | Refresh |
 |--------|-------------|---------|
 | marketing_spend.csv | Daily spend by channel (Meta, Google, TikTok, Email, Affiliate) | Daily |
 | attributed_revenue.csv | Orders with UTM-attributed channel, revenue, customer_id | Daily |
 | customers.csv | Customer cohort, first_order_date, lifetime_revenue | Daily |
 
 Note: For portfolio, use the exported CSVs from Project 2 (superstore-analytics/output/)
 or generate synthetic data via generate_data.py (see below).
 
 ---
 
 ## Dashboard Structure (Tableau Public)
 
 ### Page 1: Executive Overview
 - **KPI Cards:** Total Spend, Total Revenue, Blended ROAS, Blended CAC, Payback (mo)
 - **Trend:** Weekly Spend vs Revenue (dual axis)
 - **Channel Mix:** Stacked bar (spend % by channel over time)
 
 ### Page 2: Channel Deep-Dive
 - **Scatter:** CAC vs LTV by channel (quadrant: Stars, Dogs, Questions, Cash Cows)
 - **Table:** Channel | Spend | Revenue | ROAS | CAC | Orders | Payback Mo
 - **Parameter:** Select channel -> filters all charts
 
 ### Page 3: Cohort Analysis
 - **Heatmap:** Acquisition Month x Months Since First Order | Retention %
 - **Line:** Cumulative LTV by Cohort (Month 0-12)
 - **Bar:** LTV:CAC Ratio by Cohort (target > 3x)
 
 ### Page 4: Scenario Simulator
 - **Parameter:** Channel selector + % Spend Change slider (-50% to +100%)
 - **Calculated Field:** Projected Revenue = Current Revenue * (1 + %Change * Elasticity)
 - **KPI:** Projected ROAS, Projected Payback, Incremental Profit
 - **Assumption:** Elasticity per channel (Meta 0.8, Google 0.9, TikTok 1.2, Email 0.5)
 
 ---
 
 ## Key Tableau Techniques Demonstrated
 
 | Technique | Where Used |
 |-----------|------------|
 | **Level of Detail (LOD)** | {FIXED [Customer ID]: MIN([Order Date])} for cohort assignment |
 | **Table Calculations** | RUNNING_SUM, LOOKUP, WINDOW_AVG for payback & retention |
 | **Parameters** | Channel filter, Spend change %, Date range |
 | **Calculated Fields** | ROAS, CAC, Payback, LTV:CAC, Elasticity projection |
 | **Sets** | Top N channels, High-value customers |
 | **Dashboard Actions** | Filter across sheets, URL action to Google Ads |
 | **Tooltips** | Custom viz in tooltip (sparkline per channel) |
 
 ---
 
 ## Quick Start
 
 ### 1. Generate Sample Data (if you don't have real data)
 ```bash
 cd tableau-marketing-roi
 python generate_data.py
 # Creates: marketing_spend.csv, attributed_revenue.csv, customers.csv
 ```
 
 ### 2. Open in Tableau
 - **Tableau Desktop:** Open marketing_roi.twbx
 - **Tableau Public:** Download .twbx -> Open in Public -> Publish
 
 ### 3. Connect Your Data
 - Replace CSV connections with your database (PostgreSQL, BigQuery, Snowflake)
 - Update calculated fields if column names differ
 
 ---
 
 ## File Structure
 
 ```
 tableau-marketing-roi/
 ├── marketing_roi.twbx           # Packaged workbook (Tableau)
 ├── marketing_roi.twb            # XML workbook (editable in text editor)
 ├── data/
 │   ├── marketing_spend.csv
 │   ├── attributed_revenue.csv
 │   └── customers.csv
 ├── generate_data.py             # Synthetic data generator
 ├── calculated_fields.md         # All calculated field definitions
 └── README.md                    # This file
 ```
 
 ---
 
 ## Calculated Fields Reference (calculated_fields.md)
 
 Key fields to recreate:
 
 ```
 // Blended ROAS
 SUM([Revenue]) / SUM([Spend])
 
 // Blended CAC
 SUM([Spend]) / COUNTD([Customer ID])
 
 // Payback Months
 // Running sum of profit per cohort / CAC
 RUNNING_SUM(SUM([Profit])) / [CAC]
 
 // Cohort Month (LOD)
 {FIXED [Customer ID]: DATETRUNC('month', MIN([Order Date]))}
 
 // Months Since First Order
 DATEDIFF('month', [Cohort Month], DATETRUNC('month', [Order Date]))
 
 // Retention % (Table Calc)
 COUNTD([Customer ID]) / LOOKUP(COUNTD([Customer ID]), FIRST())
 
 // Scenario Projected Revenue
 [Revenue] * (1 + [Spend Change %] * [Channel Elasticity])
 ```
 
 ---
 
 ## Screenshots for Portfolio
 
 Add these after building:
 1. Executive Overview (full dashboard)
 2. Channel Deep-Dive with parameter selected
 3. Cohort Retention Heatmap
 4. Scenario Simulator with slider at +30%
 
 ---
 
 ## Publish to Tableau Public
 
 1. Open .twbx in Tableau Desktop (free trial) or Tableau Public Web Authoring
 2. Server -> Tableau Public -> Save to Tableau Public
 3. Title: "Marketing ROI Dashboard - D2C E-commerce"
 4. Description: Link to this repo + methodology
 5. Set to Public -> Copy embed code / URL for LinkedIn/Resume
 
 ---
 
 ## Related Projects
 
 - Project 1: E-Commerce SQL Analytics - Cohort retention & LTV in SQL
 - Project 2: Superstore Python EDA - RFM, forecasting, data prep
 
 ---
 
 *Part of Daniil Marchenko's Data Analyst Portfolio*
