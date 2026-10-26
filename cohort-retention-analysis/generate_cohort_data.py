"""Generate a reproducible synthetic e-commerce transaction dataset.

The data is synthetic and is intended for demonstrating cohort retention
analysis. It must not be presented as real company or customer performance.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def generate_transactions(
    *,
    months: int = 12,
    customers: int = 1_500,
    seed: int = 42,
    as_of: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """Return synthetic order-level transactions over the latest `months`.

    Users are acquired throughout the period. The chance of repeat purchases
    decreases with time since acquisition, and order revenue is right-skewed.
    """
    if months < 1:
        raise ValueError("months must be at least 1")
    if customers < 1:
        raise ValueError("customers must be at least 1")

    rng = np.random.default_rng(seed)
    end_date = pd.Timestamp(as_of).normalize() if as_of is not None else pd.Timestamp.today().normalize()
    # Start at the first day of the month `months - 1` months before end_date.
    start_date = (end_date.to_period("M") - (months - 1)).start_time
    month_starts = pd.date_range(start=start_date, end=end_date, freq="MS")
    if month_starts.empty:
        month_starts = pd.DatetimeIndex([start_date])

    # Spread new customer acquisition across the observation months.
    acquisition_weights = np.linspace(1.25, 0.8, len(month_starts))
    acquisition_weights /= acquisition_weights.sum()
    cohort_sizes = rng.multinomial(customers, acquisition_weights)
    rows: list[dict[str, object]] = []
    order_counter = 1

    for cohort_idx, (cohort_month, cohort_size) in enumerate(zip(month_starts, cohort_sizes)):
        for customer_number in range(int(cohort_size)):
            user_id = f"U{cohort_idx + 1:02d}{customer_number + 1:05d}"
            last_day = min((cohort_month + pd.offsets.MonthEnd(0)).normalize(), end_date)
            available_days = max(1, (last_day - cohort_month).days + 1)
            first_order_date = cohort_month + pd.Timedelta(
                days=int(rng.integers(0, available_days))
            )
            rows.append({
                "order_id": f"O{order_counter:08d}",
                "user_id": user_id,
                "order_date": first_order_date,
                "revenue": round(float(rng.lognormal(mean=3.7, sigma=0.65)), 2),
            })
            order_counter += 1

            # Repeat opportunities are limited to observed months after signup.
            months_observed = max(
                0,
                (end_date.to_period("M") - first_order_date.to_period("M")).n,
            )
            for month_age in range(1, months_observed + 1):
                # Gradually declining monthly repeat probability, with a floor.
                repeat_probability = max(0.07, 0.32 * np.exp(-0.22 * (month_age - 1)))
                if rng.random() < repeat_probability:
                    order_month = first_order_date.to_period("M") + month_age
                    month_start = order_month.start_time
                    month_end = min(order_month.end_time.normalize(), end_date)
                    max_day = max(1, (month_end - month_start).days + 1)
                    order_date = month_start + pd.Timedelta(days=int(rng.integers(0, max_day)))
                    rows.append({
                        "order_id": f"O{order_counter:08d}",
                        "user_id": user_id,
                        "order_date": order_date,
                        "revenue": round(float(rng.lognormal(mean=3.7, sigma=0.65)), 2),
                    })
                    order_counter += 1

    result = pd.DataFrame(rows, columns=["order_id", "user_id", "order_date", "revenue"])
    return result.sort_values(["order_date", "user_id", "order_id"]).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--months", type=int, default=12, help="Observation window in months (default: 12)")
    parser.add_argument("--customers", type=int, default=1500, help="Number of acquired customers (default: 1500)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible output")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "transactions.csv",
        help="CSV output path (default: project directory/transactions.csv)",
    )
    args = parser.parse_args()

    transactions = generate_transactions(
        months=args.months,
        customers=args.customers,
        seed=args.seed,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    transactions.to_csv(args.output, index=False, date_format="%Y-%m-%d")
    print(
        f"Saved {len(transactions):,} synthetic transactions from "
        f"{transactions['order_date'].min():%Y-%m-%d} to "
        f"{transactions['order_date'].max():%Y-%m-%d} at {args.output}"
    )


if __name__ == "__main__":
    main()
