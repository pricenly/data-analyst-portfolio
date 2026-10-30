# E-commerce Cohort Retention Analysis

A reproducible demonstration of monthly customer cohort analysis using
synthetic e-commerce transactions. The project generates a transaction CSV,
validates and cleans it, calculates a customer-retention matrix, and saves an
annotated heatmap.

> **Important:** The generated records are synthetic. They illustrate the
> methodology only and must not be represented as actual company results,
> customer behavior, or a measured business impact.

## Business logic

### What is a cohort?

A cohort groups customers by the calendar month of their first observed
purchase. For example, all customers whose first order was in February belong
to the February cohort.

### What is retention?

For each cohort and each month age:

```text
Retention(cohort, month_age)
  = distinct cohort customers with >= 1 order in that month
    / distinct customers in the cohort
    * 100
```

- **Month 0** is the acquisition month and is 100% by definition.
- **Month 1** is the following calendar month; subsequent columns follow the
  same convention.
- A customer is considered active in a month if they placed at least one
  qualifying order during it. Multiple orders in the same month count once.
- Empty matrix cells mean that the cohort had not yet reached that age within
  the available observation period. They are not zero retention.
- The metric uses calendar months, not rolling 30-day windows.

Retention helps answer whether customers return after their first purchase and
how retention patterns differ between acquisition cohorts. It can inform
follow-up questions about onboarding, repeat-purchase campaigns, and changes
in product or acquisition mix. It does not establish why retention changed or
prove that a campaign caused a change.

## Data and quality rules

The generator produces `order_id`, `user_id`, `order_date`, and `revenue`.
The analysis requires `user_id`, `order_date`, and `revenue`.

The analysis script:

1. Validates that required columns exist.
2. Parses order dates and revenue, and reports malformed/missing values.
3. Removes exact duplicate rows, blank user IDs, invalid dates, and rows with
   missing or non-positive revenue.
4. Flags high-revenue IQR outliers for review but retains them. An extreme
   amount can be a genuine order; an IQR rule alone does not prove an error.
5. Saves the quality report so exclusions and flags are visible.

Revenue is only used as a data-quality field here; the retention denominator
and numerator are based on distinct users, not revenue.

## Requirements

- Python 3.10+
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`

Install dependencies:

```bash
python -m pip install pandas numpy matplotlib seaborn
```

## Run

From this project directory:

```bash
# 1. Generate a reproducible 12-month synthetic transaction dataset.
python generate_cohort_data.py

# 2. Calculate retention, write CSV outputs, and save the heatmap.
python cohort_analysis.py
```

Expected files:

```text
transactions.csv             # Synthetic order-level input
retention_matrix.csv         # Cohort-by-month-age percentages
data_quality_report.csv     # Counts of dropped rows and flagged outliers
retention_heatmap.png       # Annotated visual of retention percentages
```

Options:

```bash
python generate_cohort_data.py --months 18 --customers 2500 --seed 7
python cohort_analysis.py --input path/to/transactions.csv --output-dir output
```

The generator defaults to the latest 12 calendar months relative to its run
date. Its fixed default random seed makes generated records reproducible for
the same date and parameters; the date window itself changes over time.

## Results

The current run generated 3,113 transactions from 2025-11-01 to 2026-10-30.
Quality gates passed with 0 rows excluded and 162 high-revenue rows flagged for
review (upper IQR fence: 114.32).

| Cohort | Month 0 | Month 1 | Month 3 | Month 6 |
|---|---|---|---|---|
| 2025-11 | 100.0% | 28.4% | 20.9% | 12.7% |
| 2025-12 | 100.0% | 32.6% | 24.3% | 9.7% |
| 2026-01 | 100.0% | 42.4% | 23.7% | 9.4% |
| 2026-02 | 100.0% | 27.8% | 23.8% | 7.3% |
| 2026-03 | 100.0% | 31.1% | 16.6% | 11.9% |

Month-1 retention varies between 27.8% and 42.4% across cohorts. Because the
data is synthetic, these values describe the generator's decay assumption — they
are not a benchmark for any real business.

![Retention heatmap](retention_heatmap.png)

## Interpretation and limitations

- Synthetic repeat-purchase behavior is simulated and is not calibrated to an
  actual retailer.
- The observation window limits how far recent cohorts can be followed.
- The script assumes positive revenue represents a qualifying purchase; a
  real analysis should define how to handle refunds, cancellations, taxes, and
  currency conversion.
- Retention is descriptive. It does not measure causal impact, profitability,
  or customer lifetime value.
- Cohort analysis can be sensitive to seasonality, acquisition channel, and
  product mix. Segment these dimensions when suitable real data is available.
