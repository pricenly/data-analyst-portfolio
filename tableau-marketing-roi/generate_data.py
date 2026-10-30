# Synthetic Marketing Data Generator for Tableau Dashboard
# Run: python generate_data.py
# Outputs: data/marketing_spend.csv, data/attributed_revenue.csv, data/customers.csv

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

np.random.seed(42)

OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True)

# Configuration
CHANNELS = ["Meta", "Google", "TikTok", "Email", "Affiliate", "Organic"]
CHANNEL_ELASTICITY = {"Meta": 0.8, "Google": 0.9, "TikTok": 1.2, "Email": 0.5, "Affiliate": 0.7, "Organic": 0.3}
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)
NUM_CUSTOMERS = 5000

# 1. Generate marketing_spend.csv (daily spend by channel)
date_range = pd.date_range(START_DATE, END_DATE, freq="D")
spend_rows = []

for channel in CHANNELS:
    # Base daily spend with trend + seasonality + noise
    base_spend = {"Meta": 2000, "Google": 1500, "TikTok": 800, "Email": 200, "Affiliate": 300, "Organic": 0}[channel]
    
    for i, date in enumerate(date_range):
        # Weekly seasonality (higher on weekdays)
        weekday_mult = 1.2 if date.weekday() < 5 else 0.7
        # Monthly trend (growing)
        month_mult = 1 + (i / len(date_range)) * 0.5
        # Random noise
        noise = np.random.lognormal(0, 0.15)
        
        daily_spend = max(0, base_spend * weekday_mult * month_mult * noise)
        
        spend_rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "channel": channel,
            "spend": round(daily_spend, 2),
            "impressions": int(daily_spend * np.random.uniform(50, 200)),
            "clicks": int(daily_spend * np.random.uniform(2, 10))
        })

spend_df = pd.DataFrame(spend_rows)
spend_df.to_csv(OUTPUT_DIR / "marketing_spend.csv", index=False)
print(f"Generated marketing_spend.csv: {len(spend_df)} rows")

# 2. Generate customers.csv (customer cohorts)
customer_rows = []
for cust_id in range(1, NUM_CUSTOMERS + 1):
    # Acquisition date (weighted toward recent)
    days_range = (END_DATE - START_DATE).days
    acq_offset = int(np.random.beta(2, 5) * days_range)  # more recent
    first_order_date = START_DATE + timedelta(days=acq_offset)
    
    # Channel attribution (weighted by spend)
    channel_weights = [spend_df[spend_df["channel"]==c]["spend"].sum() for c in CHANNELS]
    channel_weights = np.array(channel_weights) / sum(channel_weights)
    acq_channel = np.random.choice(CHANNELS, p=channel_weights)
    
    # Customer lifetime value (depends on channel + random)
    base_ltv = {"Meta": 180, "Google": 220, "TikTok": 150, "Email": 300, "Affiliate": 120, "Organic": 250}[acq_channel]
    lifetime_revenue = max(0, np.random.normal(base_ltv, base_ltv * 0.4))
    
    # Number of orders
    num_orders = max(1, int(np.random.poisson(lifetime_revenue / 50)))
    
    customer_rows.append({
        "customer_id": f"CUST{cust_id:06d}",
        "first_order_date": first_order_date.strftime("%Y-%m-%d"),
        "acquisition_channel": acq_channel,
        "lifetime_revenue": round(lifetime_revenue, 2),
        "total_orders": num_orders,
        "is_active": np.random.random() > 0.3  # 70% still active
    })

customers_df = pd.DataFrame(customer_rows)
customers_df.to_csv(OUTPUT_DIR / "customers.csv", index=False)
print(f"Generated customers.csv: {len(customers_df)} rows")

# 3. Generate attributed_revenue.csv (orders with channel attribution)
order_rows = []
order_id = 1

for _, cust in customers_df.iterrows():
    cust_id = cust["customer_id"]
    first_date = datetime.strptime(cust["first_order_date"], "%Y-%m-%d")
    acq_channel = cust["acquisition_channel"]
    num_orders = cust["total_orders"]
    total_rev = cust["lifetime_revenue"]
    
    # Distribute revenue across orders (Pareto: first order larger)
    if num_orders == 1:
        order_revenues = [total_rev]
    else:
        weights = np.random.dirichlet([2] + [1]*(num_orders-1))
        order_revenues = (weights * total_rev).round(2)
    
    for j, rev in enumerate(order_revenues):
        # Order date: first order = acquisition date, subsequent spaced out
        if j == 0:
            order_date = first_date
        else:
            # Gap between orders: 10-90 days
            gap = np.random.randint(10, 90)
            order_date = first_date + timedelta(days=gap*j)
        
        # Attribution: first order = acquisition channel, repeat orders = mix
        if j == 0:
            attrib_channel = acq_channel
        else:
            # Repeat orders: 60% same channel, 20% email, 20% organic
            attrib_channel = np.random.choice(
                [acq_channel, "Email", "Organic"], 
                p=[0.6, 0.2, 0.2]
            )
        
        # Profit margin ~30%
        profit = round(rev * np.random.uniform(0.25, 0.35), 2)
        
        order_rows.append({
            "order_id": f"ORD{order_id:08d}",
            "customer_id": cust_id,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "attribution_channel": attrib_channel,
            "revenue": rev,
            "profit": profit,
            "is_first_order": j == 0
        })
        order_id += 1

orders_df = pd.DataFrame(order_rows)
orders_df.to_csv(OUTPUT_DIR / "attributed_revenue.csv", index=False)
print(f"Generated attributed_revenue.csv: {len(orders_df)} rows")

print("\nDone! Files in ./data/:")
for f in OUTPUT_DIR.glob("*.csv"):
    print(f"  {f.name} ({f.stat().st_size/1024:.1f} KB)")
