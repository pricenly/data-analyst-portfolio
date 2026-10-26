 -- =============================================================================
 -- LOAD ONLINE RETAIL DATASET (UCI) INTO POSTGRESQL
 -- =============================================================================
 -- Dataset: https://archive.ics.uci.edu/ml/datasets/Online+Retail+II
 -- Or download from: https://www.kaggle.com/datasets/mathchi/online-retail-ii-data-set-from-ml-repository
 -- File: online_retail_II.xlsx (Year 2009-2010) or online_retail.xlsx
 -- =============================================================================
 
 -- 1. Create staging table (matches raw Excel columns)
 CREATE TABLE IF NOT EXISTS online_retail_staging (
     invoice_no    VARCHAR(20),
     stock_code    VARCHAR(20),
     description   VARCHAR(100),
     quantity      INTEGER,
     invoice_date  TIMESTAMP,
     unit_price    NUMERIC(10,2),
     customer_id   VARCHAR(20),
     country       VARCHAR(50)
 );
 
 -- 2. Load data from CSV (adjust path for your system)
 -- Option A: Using \copy (run in psql)
 -- \copy online_retail_staging FROM '/path/to/online_retail.csv' CSV HEADER;
 
 -- Option B: Using COPY (requires superuser / file access on server)
 -- COPY online_retail_staging FROM '/var/lib/postgresql/data/online_retail.csv' CSV HEADER;
 
 -- Option C: Python pandas to_sql (recommended for local dev)
 -- See load_data.py below
 
 -- 3. Create clean analysis table with proper types & constraints
 CREATE TABLE IF NOT EXISTS online_retail AS
 SELECT 
     TRIM(invoice_no) AS invoice_no,
     TRIM(stock_code) AS stock_code,
     TRIM(description) AS description,
     quantity::INTEGER,
     invoice_date::TIMESTAMP,
     unit_price::NUMERIC(10,2),
     NULLIF(TRIM(customer_id), '') AS customer_id,
     TRIM(country) AS country
 FROM online_retail_staging
 WHERE invoice_no IS NOT NULL
   AND stock_code IS NOT NULL
   AND quantity IS NOT NULL
   AND invoice_date IS NOT NULL
   AND unit_price IS NOT NULL;
 
 -- 4. Add indexes for query performance
 CREATE INDEX IF NOT EXISTS idx_online_retail_customer_date 
     ON online_retail (customer_id, invoice_date);
 CREATE INDEX IF NOT EXISTS idx_online_retail_invoice 
     ON online_retail (invoice_no);
 CREATE INDEX IF NOT EXISTS idx_online_retail_date 
     ON online_retail (invoice_date);
 CREATE INDEX IF NOT EXISTS idx_online_retail_country 
     ON online_retail (country);
 
 -- 5. Verify load
 SELECT 
     COUNT(*) AS total_rows,
     COUNT(DISTINCT customer_id) AS unique_customers,
     COUNT(DISTINCT invoice_no) AS unique_invoices,
     MIN(invoice_date) AS min_date,
     MAX(invoice_date) AS max_date,
     ROUND(SUM(quantity * unit_price)::numeric, 2) AS total_revenue
 FROM online_retail
 WHERE quantity > 0 AND invoice_no NOT LIKE 'C%' AND customer_id IS NOT NULL;
 
 -- 6. (Optional) Drop staging table after verification
 -- DROP TABLE online_retail_staging;
 
 -- =============================================================================
 -- ALTERNATIVE: PYTHON LOAD SCRIPT (load_data.py)
 -- =============================================================================
 -- Run: python load_data.py
 -- Requires: pip install pandas openpyxl sqlalchemy psycopg2-binary
 /*
 import pandas as pd
 from sqlalchemy import create_engine
 
 # Connection - update with your credentials
 DATABASE_URL = "postgresql://user:password@localhost:5432/your_db"
 engine = create_engine(DATABASE_URL)
 
 # Read Excel (UCI dataset has two sheets: Year 2009-2010, Year 2010-2011)
 df1 = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2009-2010")
 df2 = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2010-2011")
 df = pd.concat([df1, df2], ignore_index=True)
 
 # Clean column names
 df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
 # Expected: invoice, stockcode, description, quantity, invoicedate, price, customerid, country
 df = df.rename(columns={
     "invoice": "invoice_no",
     "stockcode": "stock_code",
     "invoicedate": "invoice_date",
     "price": "unit_price",
     "customerid": "customer_id"
 })
 
 # Basic cleaning
 df = df.dropna(subset=["invoice_no", "stock_code", "quantity", "invoice_date", "unit_price"])
 df["customer_id"] = df["customer_id"].replace("", pd.NA)
 
 # Write to PostgreSQL
 df.to_sql("online_retail", engine, if_exists="replace", index=False, chunksize=10000)
 print(f"Loaded {len(df)} rows into online_retail")
 */
