 -- =============================================================================
 -- E-COMMERCE SQL ANALYTICS вЂ” Online Retail Dataset (UCI)
 -- Author: Daniil Marchenko | Junior Data Analyst Portfolio
 -- Database: PostgreSQL 15+
 -- =============================================================================

 -- -----------------------------------------------------------------------------
 -- SCHEMA REFERENCE (after loading data via load_data.sql)
 -- -----------------------------------------------------------------------------
 -- Table: online_retail
 -- Columns:
 --   invoice_no   VARCHAR(20)   -- 'C' prefix indicates cancellation
 --   stock_code   VARCHAR(20)
 --   description  VARCHAR(100)
 --   quantity     INTEGER       -- negative = return
 --   invoice_date TIMESTAMP
 --   unit_price   NUMERIC(10,2)
 --   customer_id  VARCHAR(20)   -- NULL for guest checkouts
 --   country      VARCHAR(50)
 -- -----------------------------------------------------------------------------

 -- =============================================================================
 -- 0. DATA QUALITY CHECKS
 -- =============================================================================

 -- 0.1 Row count & null profile
 SELECT
     COUNT(*) AS total_rows,
     COUNT(customer_id) AS rows_with_customer,
     COUNT(*) - COUNT(customer_id) AS guest_rows,
     MIN(invoice_date) AS min_date,
     MAX(invoice_date) AS max_date
 FROM online_retail;

 -- 0.2 Cancellation rate (invoices starting with 'C')
 SELECT
     ROUND(100.0 * COUNT(*) FILTER (WHERE invoice_no LIKE 'C%') / COUNT(*), 2) AS cancel_rate_pct
 FROM online_retail;

 -- 0.3 Negative quantities (returns) вЂ” should match cancellations
 SELECT COUNT(*) AS negative_qty_rows
 FROM online_retail
 WHERE quantity < 0;


 -- =============================================================================
 -- 1. TRANSACTION FUNNEL PROXY & DROP-OFF
 -- =============================================================================
 -- This dataset contains completed/recorded transactions, not web sessions,
 -- carts, or checkout attempts. Therefore this is an invoice-quality proxy,
 -- NOT a behavioral session funnel. Do not interpret the proxy as website
 -- conversion without event-level data.

 WITH invoice_agg AS (
     SELECT
         invoice_no,
         MAX(invoice_date)::date AS invoice_date,
         SUM(quantity * unit_price) AS invoice_revenue,
         COUNT(DISTINCT stock_code) AS line_items,
         MAX(customer_id) AS customer_id,
         MAX(country) AS country,
         BOOL_OR(invoice_no LIKE 'C%') AS is_cancelled
     FROM online_retail
     GROUP BY invoice_no
 ),
 funnel_steps AS (
     SELECT 1 AS step_order, 'Recorded invoices' AS step, COUNT(*)::bigint AS invoice_count
     FROM invoice_agg
     UNION ALL
     SELECT 2, 'Invoices with positive net revenue', COUNT(*)::bigint
     FROM invoice_agg WHERE invoice_revenue > 0
     UNION ALL
     SELECT 3, 'Positive-revenue, non-cancelled invoices', COUNT(*)::bigint
     FROM invoice_agg WHERE invoice_revenue > 0 AND NOT is_cancelled
 ),
 measured_steps AS (
     SELECT
         step_order,
         step,
         invoice_count,
         LAG(invoice_count) OVER (ORDER BY step_order) AS previous_step_count,
         FIRST_VALUE(invoice_count) OVER (ORDER BY step_order) AS baseline_count
     FROM funnel_steps
 )
 SELECT
     step_order,
     step,
     invoice_count,
     previous_step_count - invoice_count AS invoices_dropped_at_step,
     ROUND(100.0 * (previous_step_count - invoice_count)
           / NULLIF(previous_step_count, 0), 2) AS step_drop_off_rate_pct,
     ROUND(100.0 * invoice_count / NULLIF(baseline_count, 0), 2) AS retained_vs_baseline_pct
 FROM measured_steps
 ORDER BY step_order;


 -- =============================================================================
 -- 1B. REVENUE REVERSALS: CANCELLATIONS / RETURNS (NON-OVERLAPPING ROW BASIS)
 -- =============================================================================
 -- The file does not contain abandoned carts or unrealized demand, so revenue
 -- "lost" at web-funnel steps cannot be measured. This query quantifies recorded
 -- negative line value as a proxy for reversals, split by cancellation invoice
 -- vs. other negative-quantity return lines to highlight where realized revenue
 -- was reversed. Amounts are absolute values and categories are disjoint.
 WITH reversal_lines AS (
     SELECT
         CASE WHEN invoice_no LIKE 'C%' THEN 'Cancellation invoice'
              ELSE 'Return / negative-quantity line' END AS reversal_type,
         ABS(quantity * unit_price) AS reversed_revenue,
         invoice_no,
         stock_code
     FROM online_retail
     WHERE quantity < 0
 )
 SELECT
     reversal_type,
     COUNT(*) AS reversal_line_count,
     COUNT(DISTINCT invoice_no) AS affected_invoices,
     ROUND(SUM(reversed_revenue)::numeric, 2) AS reversed_revenue,
     ROUND(100.0 * SUM(reversed_revenue)
           / NULLIF(SUM(SUM(reversed_revenue)) OVER (), 0), 2) AS share_of_reversals_pct
 FROM reversal_lines
 GROUP BY reversal_type
 ORDER BY reversed_revenue DESC;

 -- 1C. Largest product areas by recorded reversal value (prioritization).
 SELECT
     stock_code,
     MAX(description) AS description,
     COUNT(*) AS reversal_line_count,
     ROUND(SUM(ABS(quantity * unit_price))::numeric, 2) AS reversed_revenue
 FROM online_retail
 WHERE quantity < 0
 GROUP BY stock_code
 ORDER BY reversed_revenue DESC
 LIMIT 10;


 -- =============================================================================
 -- 2. MONTHLY REVENUE & ORDERS TREND
 -- =============================================================================
 SELECT
     DATE_TRUNC('month', invoice_date)::date AS month,
     COUNT(DISTINCT invoice_no) AS orders,
     ROUND(SUM(quantity * unit_price)::numeric, 2) AS revenue,
     ROUND(SUM(quantity * unit_price)::numeric / NULLIF(COUNT(DISTINCT invoice_no), 0), 2) AS aov
 FROM online_retail
 WHERE quantity > 0 AND invoice_no NOT LIKE 'C%' AND customer_id IS NOT NULL
 GROUP BY 1
 ORDER BY 1;


 -- =============================================================================
 -- 3. COHORT ANALYSIS вЂ” MONTHLY RETENTION HEATMAP
 -- =============================================================================
 -- Cohort = customer's first purchase month
 -- Period = months since first purchase (0 = cohort month)
 -- =============================================================================

 WITH first_orders AS (
     SELECT
         customer_id,
         DATE_TRUNC('month', MIN(invoice_date))::date AS cohort_month
     FROM online_retail
     WHERE quantity > 0 AND invoice_no NOT LIKE 'C%' AND customer_id IS NOT NULL
     GROUP BY customer_id
 ),
 customer_orders AS (
     SELECT
         o.customer_id,
         DATE_TRUNC('month', o.invoice_date)::date AS order_month,
         f.cohort_month
     FROM online_retail o
     JOIN first_orders f ON o.customer_id = f.customer_id
     WHERE o.quantity > 0 AND o.invoice_no NOT LIKE 'C%'
 ),
 cohort_activity AS (
     SELECT
         cohort_month,
         order_month,
         COUNT(DISTINCT customer_id) AS active_customers,
         EXTRACT(YEAR FROM AGE(order_month, cohort_month)) * 12 +
         EXTRACT(MONTH FROM AGE(order_month, cohort_month)) AS period_number
     FROM customer_orders
     GROUP BY cohort_month, order_month
 ),
 cohort_sizes AS (
     SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_size
     FROM first_orders
     GROUP BY cohort_month
 )
 SELECT
     ca.cohort_month,
     cs.cohort_size,
     ca.period_number,
     ca.active_customers,
     ROUND(100.0 * ca.active_customers / cs.cohort_size, 1) AS retention_pct
 FROM cohort_activity ca
 JOIN cohort_sizes cs ON ca.cohort_month = cs.cohort_month
 WHERE ca.period_number <= 12  -- first 12 months
 ORDER BY ca.cohort_month, ca.period_number;


 -- =============================================================================
 -- 4. RFM SEGMENTATION (Recency, Frequency, Monetary)
 -- =============================================================================
 -- Uses NTILE(4) for quartile-based scoring в†’ 4x4x4 = 64 segments в†’ mapped to 5 labels
 -- =============================================================================

 WITH customer_metrics AS (
     SELECT
         customer_id,
         MAX(invoice_date) AS last_purchase_date,
         COUNT(DISTINCT invoice_no) AS frequency,
         SUM(quantity * unit_price) AS monetary
     FROM online_retail
     WHERE quantity > 0 AND invoice_no NOT LIKE 'C%' AND customer_id IS NOT NULL
     GROUP BY customer_id
 ),
 rfm_scores AS (
     SELECT
         customer_id,
         -- Recency: days since last purchase (lower = better)
         (SELECT MAX(invoice_date) FROM online_retail) - last_purchase_date AS recency_days,
         frequency,
         monetary,
         NTILE(4) OVER (ORDER BY (SELECT MAX(invoice_date) FROM online_retail) - last_purchase_date DESC) AS r_score,  -- 4=best (most recent)
         NTILE(4) OVER (ORDER BY frequency) AS f_score,
         NTILE(4) OVER (ORDER BY monetary) AS m_score
     FROM customer_metrics
 ),
 rfm_labeled AS (
     SELECT
         customer_id,
         recency_days,
         frequency,
         monetary,
         r_score, f_score, m_score,
         (r_score + f_score + m_score) AS rfm_total,
         CASE
             WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Champions'
             WHEN r_score >= 3 AND f_score >= 2 THEN 'Loyal Customers'
             WHEN r_score >= 3 AND f_score = 1 THEN 'New Customers'
             WHEN r_score = 2 AND f_score >= 2 THEN 'Potential Loyalists'
             WHEN r_score = 1 AND f_score >= 3 THEN 'At Risk'
             WHEN r_score = 1 AND f_score = 1 THEN 'Lost'
             ELSE 'Others'
         END AS segment
     FROM rfm_scores
 )
 SELECT
     segment,
     COUNT(*) AS customer_count,
     ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_customers,
     ROUND(AVG(recency_days), 1) AS avg_recency_days,
     ROUND(AVG(frequency), 1) AS avg_frequency,
     ROUND(AVG(monetary), 2) AS avg_monetary
 FROM rfm_labeled
 GROUP BY segment
 ORDER BY
     CASE segment
         WHEN 'Champions' THEN 1
         WHEN 'Loyal Customers' THEN 2
         WHEN 'Potential Loyalists' THEN 3
         WHEN 'New Customers' THEN 4
         WHEN 'At Risk' THEN 5
         WHEN 'Others' THEN 6
         WHEN 'Lost' THEN 7
     END;


 -- =============================================================================
 -- 5. LTV BY COHORT (Cumulative Revenue per Customer)
 -- =============================================================================
 WITH first_orders AS (
     SELECT
         customer_id,
         DATE_TRUNC('month', MIN(invoice_date))::date AS cohort_month
     FROM online_retail
     WHERE quantity > 0 AND invoice_no NOT LIKE 'C%' AND customer_id IS NOT NULL
     GROUP BY customer_id
 ),
 customer_revenue AS (
     SELECT
         o.customer_id,
         f.cohort_month,
         DATE_TRUNC('month', o.invoice_date)::date AS revenue_month,
         SUM(o.quantity * o.unit_price) AS monthly_revenue
     FROM online_retail o
     JOIN first_orders f ON o.customer_id = f.customer_id
     WHERE o.quantity > 0 AND o.invoice_no NOT LIKE 'C%'
     GROUP BY o.customer_id, f.cohort_month, DATE_TRUNC('month', o.invoice_date)
 ),
 cohort_ltv AS (
     SELECT
         cohort_month,
         revenue_month,
         EXTRACT(YEAR FROM AGE(revenue_month, cohort_month)) * 12 +
         EXTRACT(MONTH FROM AGE(revenue_month, cohort_month)) AS period_number,
         SUM(monthly_revenue) / COUNT(DISTINCT customer_id) AS avg_revenue_per_customer
     FROM customer_revenue
     GROUP BY cohort_month, revenue_month
 )
 SELECT
     cohort_month,
     period_number,
     ROUND(avg_revenue_per_customer, 2) AS avg_cumulative_revenue_per_customer,
     ROUND(SUM(avg_revenue_per_customer) OVER (PARTITION BY cohort_month ORDER BY period_number), 2) AS cumulative_ltv
 FROM cohort_ltv
 WHERE period_number <= 12
 ORDER BY cohort_month, period_number;


 -- =============================================================================
 -- 6. TOP PRODUCTS BY REVENUE & REORDER RATE
 -- =============================================================================
 WITH product_stats AS (
     SELECT
         stock_code,
         MAX(description) AS description,
         SUM(quantity) AS total_units_sold,
         ROUND(SUM(quantity * unit_price)::numeric, 2) AS total_revenue,
         COUNT(DISTINCT invoice_no) AS order_count,
         COUNT(DISTINCT customer_id) AS unique_customers,
         ROUND(COUNT(DISTINCT customer_id)::numeric / NULLIF(COUNT(DISTINCT invoice_no), 0), 3) AS reorder_rate
     FROM online_retail
     WHERE quantity > 0 AND invoice_no NOT LIKE 'C%'
     GROUP BY stock_code
 )
 SELECT
     stock_code,
     description,
     total_units_sold,
     total_revenue,
     order_count,
     unique_customers,
     reorder_rate
 FROM product_stats
 ORDER BY total_revenue DESC
 LIMIT 20;


 -- =============================================================================
 -- 7. CUSTOMER LIFETIME VALUE PREDICTION (Simple Linear Model via SQL)
 -- =============================================================================
 -- Predicts 12-month LTV based on first 3 months of data
 -- =============================================================================
 WITH first_orders AS (
     SELECT
         customer_id,
         DATE_TRUNC('month', MIN(invoice_date))::date AS cohort_month
     FROM online_retail
     WHERE quantity > 0 AND invoice_no NOT LIKE 'C%' AND customer_id IS NOT NULL
     GROUP BY customer_id
 ),
 early_revenue AS (
     SELECT
         o.customer_id,
         f.cohort_month,
         SUM(CASE
             WHEN o.invoice_date <= f.cohort_month + INTERVAL '3 months'
             THEN o.quantity * o.unit_price ELSE 0 END) AS revenue_first_3m,
         SUM(o.quantity * o.unit_price) AS revenue_total
     FROM online_retail o
     JOIN first_orders f ON o.customer_id = f.customer_id
     WHERE o.quantity > 0 AND o.invoice_no NOT LIKE 'C%'
       AND o.invoice_date <= f.cohort_month + INTERVAL '12 months'
     GROUP BY o.customer_id, f.cohort_month
 )
 SELECT
     cohort_month,
     COUNT(*) AS customers,
     ROUND(AVG(revenue_first_3m), 2) AS avg_revenue_3m,
     ROUND(AVG(revenue_total), 2) AS avg_ltv_12m,
     ROUND(AVG(revenue_total) / NULLIF(AVG(revenue_first_3m), 0), 2) AS ltv_to_3m_ratio
 FROM early_revenue
 GROUP BY cohort_month
 ORDER BY cohort_month;


 -- =============================================================================
 -- 8. GEOGRAPHIC DISTRIBUTION (Revenue by Country)
 -- =============================================================================
 SELECT
     country,
     COUNT(DISTINCT customer_id) AS customers,
     COUNT(DISTINCT invoice_no) AS orders,
     ROUND(SUM(quantity * unit_price)::numeric, 2) AS revenue,
     ROUND(SUM(quantity * unit_price)::numeric / NULLIF(COUNT(DISTINCT customer_id), 0), 2) AS arpu
 FROM online_retail
 WHERE quantity > 0 AND invoice_no NOT LIKE 'C%' AND customer_id IS NOT NULL
 GROUP BY country
 ORDER BY revenue DESC;


 -- =============================================================================
 -- 9. WINDOW FUNCTIONS DEMO вЂ” Running Totals & Rankings
 -- =============================================================================
 -- 9.1 Running revenue per customer over time
 SELECT
     customer_id,
     invoice_date::date,
     SUM(quantity * unit_price) OVER (PARTITION BY customer_id ORDER BY invoice_date
         ROWS UNBOUNDED PRECEDING) AS running_revenue,
     ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY invoice_date) AS purchase_number
 FROM online_retail
 WHERE quantity > 0 AND invoice_no NOT LIKE 'C%' AND customer_id IS NOT NULL
 ORDER BY customer_id, invoice_date;

 -- 9.2 Top customer per country by revenue (RANK vs DENSE_RANK)
 WITH country_customer_rev AS (
     SELECT
         country,
         customer_id,
         SUM(quantity * unit_price) AS total_revenue
     FROM online_retail
     WHERE quantity > 0 AND invoice_no NOT LIKE 'C%' AND customer_id IS NOT NULL
     GROUP BY country, customer_id
 ),
 ranked_customers AS (
     SELECT
         country,
         customer_id,
         total_revenue,
         RANK() OVER (PARTITION BY country ORDER BY total_revenue DESC) AS rnk,
         DENSE_RANK() OVER (PARTITION BY country ORDER BY total_revenue DESC) AS dense_rnk
     FROM country_customer_rev
 )
 SELECT
     country,
     customer_id,
     total_revenue,
     rnk,
     dense_rnk
 FROM ranked_customers
 WHERE rnk <= 3
 ORDER BY country, total_revenue DESC;


 -- =============================================================================
 -- END OF ANALYSIS
 -- =============================================================================
