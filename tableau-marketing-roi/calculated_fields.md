# Tableau Calculated Fields Reference

Copy these into Tableau Desktop / Public (Analysis → Create Calculated Field).

Column names below are the **Tableau field names after mapping** the generated
CSVs (`attribution_channel` → `Channel`, `order_date` → `Order Date`,
`customer_id` → `Customer ID`). The full mapping is in
[`README.md`](./README.md#field-mapping).

---

## KPI Fields

### Total Spend
```
SUM([Spend])
```

### Total Revenue
```
SUM([Revenue])
```

### Blended ROAS
```
SUM([Revenue]) / SUM([Spend])
```

### Blended CAC
```
SUM([Spend]) / COUNTD([Customer ID])
```

### Blended Payback (Months)
```
// Approximate: cumulative profit per cohort / CAC
// Requires cohort context - see Cohort Payback below
SUM([Profit]) / [Blended CAC]
```

---

## Cohort Fields (Customer Level)

### Cohort Month (LOD - Fixed)
```
{FIXED [Customer ID]: DATETRUNC('month', MIN([Order Date]))}
```

### Months Since First Order
```
DATEDIFF('month', [Cohort Month], DATETRUNC('month', [Order Date]))
```

### Cohort Size (LOD)
```
{FIXED [Cohort Month]: COUNTD([Customer ID])}
```

### Customers Active in Period (Table Calc)
```
// Place on Text/Label, Compute Using: Months Since First Order
COUNTD([Customer ID])
```

### Retention % (Table Calc)
```
// Compute Using: Months Since First Order
COUNTD([Customer ID]) / LOOKUP(COUNTD([Customer ID]), FIRST())
```

### Cumulative Revenue per Customer (Table Calc)
```
// Compute Using: Months Since First Order
RUNNING_SUM(SUM([Revenue])) / ATTR([Cohort Size])
```

---

## Channel Performance Fields

### ROAS by Channel
```
{FIXED [Channel]: SUM([Revenue])} / {FIXED [Channel]: SUM([Spend])}
```

### CAC by Channel
```
{FIXED [Channel]: SUM([Spend])} / {FIXED [Channel]: COUNTD([Customer ID])}
```

### Payback Months by Channel
```
// Running sum of profit per channel cohort / CAC
// Requires Channel + Cohort Month in view
RUNNING_SUM(SUM([Profit])) / {FIXED [Channel], [Cohort Month]: SUM([Spend]) / COUNTD([Customer ID])}
```

---

## Scenario Simulator Fields (Parameters Required)

### Parameter: [Spend Change %]
- Data Type: Float
- Current Value: 0
- Display: Slider (-0.5 to 1.0, step 0.05)

### Parameter: [Selected Channel]
- Data Type: String
- List: Meta, Google, TikTok, Email, Affiliate, Organic

### Channel Elasticity (Calculated Field)
```
CASE [Channel]
    WHEN 'Meta' THEN 0.8
    WHEN 'Google' THEN 0.9
    WHEN 'TikTok' THEN 1.2
    WHEN 'Email' THEN 0.5
    WHEN 'Affiliate' THEN 0.7
    WHEN 'Organic' THEN 0.3
    ELSE 0.8
END
```

### Projected Spend
```
CASE 
    WHEN [Channel] = [Selected Channel] THEN [Spend] * (1 + [Spend Change %])
    ELSE [Spend]
END
```

### Projected Revenue
```
CASE 
    WHEN [Channel] = [Selected Channel] 
    THEN [Revenue] * (1 + [Spend Change %] * [Channel Elasticity])
    ELSE [Revenue]
END
```

### Projected ROAS
```
SUM([Projected Revenue]) / SUM([Projected Spend])
```

### Projected Payback
```
SUM([Projected Spend]) / COUNTD([Customer ID]) / 
(SUM([Projected Revenue]) - SUM([Projected Spend])) * 30
// Simplified: assumes monthly profit = revenue - spend
```

### Incremental Profit
```
(SUM([Projected Revenue]) - SUM([Projected Spend])) - (SUM([Revenue]) - SUM([Spend]))
```

---

## LTV:CAC Ratio Fields

### LTV per Cohort (12-month)
```
// Compute Using: Months Since First Order
RUNNING_SUM(SUM([Revenue])) / ATTR({FIXED [Cohort Month]: COUNTD([Customer ID])})
```

### CAC per Cohort
```
{FIXED [Cohort Month]: SUM([Spend])} / {FIXED [Cohort Month]: COUNTD([Customer ID])}
```

### LTV:CAC Ratio
```
[LTV per Cohort (Month 12)] / [CAC per Cohort]
```

---

## Formatting Helpers

### Currency (K/M)
```
IF ABS(SUM([Revenue])) >= 1000000 
THEN "$" + STR(ROUND(SUM([Revenue])/1000000, 1)) + "M"
ELSEIF ABS(SUM([Revenue])) >= 1000
THEN "$" + STR(ROUND(SUM([Revenue])/1000, 1)) + "K"
ELSE "$" + STR(ROUND(SUM([Revenue]), 0))
END
```

### Percentage with 1 Decimal
```
STR(ROUND([Retention %] * 100, 1)) + "%"
```

### Payback Label
```
IF [Payback Months] <= 0 THEN "Immediate"
ELSEIF [Payback Months] > 24 THEN "24+ mo"
ELSE STR(ROUND([Payback Months], 1)) + " mo"
END
```

---

## Dashboard Actions Setup

1. **Filter Action**: Click Channel bar -> Filter Channel Deep-Dive sheets
   - Source: Executive Overview (Channel Mix bar)
   - Target: Channel Deep-Dive (all sheets)
   - Run on: Select
   - Clear: Show all values

2. **Highlight Action**: Hover Cohort cell -> Highlight same cohort in LTV curve
   - Source: Cohort Retention Heatmap
   - Target: Cohort LTV Line Chart
   - Run on: Hover

3. **URL Action**: Click Channel name -> Open Google Ads / Meta Ads Manager
   - Source: Channel Deep-Dive table
   - URL: `https://ads.google.com/aw/campaigns` (or parameterized)
   - Run on: Menu -> "Open in Ads Manager"

---

## Data Source Joins (Logical Layer)

```
marketing_spend (daily, channel)
    |
    |-- 1:M -- attributed_revenue (daily, channel, customer_id)
    |                    |
    |                    |-- M:1 -- customers (customer_id)
    |
    (Blend on: Date + Channel)
```

**Recommended**: Use Relationships (noodles) in Tableau 2020.2+
- `marketing_spend` <-> `attributed_revenue` on `date` + `channel`
- `attributed_revenue` <-> `customers` on `customer_id`

---

## Performance Tips

- **Extract** data (.hyper) for Public publishing
- **Aggregate** to weekly/monthly in Custom SQL if daily too granular
- **Hide** unused fields in Data Source tab
- **Materialize** LODs as extracts where possible
- **Limit** dashboard to 10-15 worksheets max
