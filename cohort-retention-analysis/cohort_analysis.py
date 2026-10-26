"""Clean e-commerce transactions and calculate monthly customer retention."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Works in headless environments and CI.

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


REQUIRED_COLUMNS = {"user_id", "order_date", "revenue"}


def load_and_clean_data(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load a CSV, report data-quality issues, and return valid transactions.

    Exact duplicate records and rows missing required values are removed.
    Invalid dates and non-positive/non-numeric revenue are also excluded.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Input CSV not found: {path}. Generate it with generate_cohort_data.py first."
        )
    if not path.is_file():
        raise ValueError(f"Input path is not a file: {path}")

    raw = pd.read_csv(path)
    missing_columns = REQUIRED_COLUMNS - set(raw.columns)
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {sorted(missing_columns)}")

    data = raw.copy()
    data["user_id"] = data["user_id"].astype("string").str.strip()
    data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce", utc=True).dt.tz_convert(None)
    data["revenue"] = pd.to_numeric(data["revenue"], errors="coerce")

    checks: list[tuple[str, int, str]] = [
        ("Input rows", len(raw), "Rows read from CSV"),
        ("Exact duplicate rows", int(data.duplicated().sum()), "Exact duplicates removed"),
        ("Missing/blank user_id", int(data["user_id"].isna().sum() + data["user_id"].eq("").sum()), "Rows removed"),
        ("Invalid or missing order_date", int(data["order_date"].isna().sum()), "Rows removed"),
        ("Invalid or missing revenue", int(data["revenue"].isna().sum()), "Rows removed"),
        ("Non-positive revenue", int(data["revenue"].le(0).sum()), "Rows removed; assumes revenue is a positive purchase amount"),
    ]

    # Flag extreme values for review, but retain valid positive orders. Large
    # purchases can be legitimate; an IQR flag alone is not proof of bad data.
    valid_revenue = data.loc[data["revenue"].gt(0), "revenue"]
    if not valid_revenue.empty:
        q1, q3 = valid_revenue.quantile([0.25, 0.75])
        upper_fence = q3 + 1.5 * (q3 - q1)
        high_revenue_count = int(data["revenue"].gt(upper_fence).sum())
    else:
        upper_fence = float("nan")
        high_revenue_count = 0
    checks.append((
        "High-revenue IQR flags",
        high_revenue_count,
        f"Retained for review (upper fence: {upper_fence:.2f})",
    ))

    duplicate_mask = data.duplicated(keep="first")
    valid_mask = (
        data["user_id"].notna()
        & data["user_id"].ne("")
        & data["order_date"].notna()
        & data["revenue"].notna()
        & data["revenue"].gt(0)
    )
    cleaned = data.loc[~duplicate_mask & valid_mask].copy()
    cleaned["order_date"] = cleaned["order_date"].dt.normalize()

    if cleaned.empty:
        raise ValueError("No valid transaction rows remain after data-quality filtering.")

    report = pd.DataFrame(checks, columns=["check", "rows_or_flags", "handling"])
    report.loc[len(report)] = [
        "Rows retained",
        len(cleaned),
        f"{len(raw) - len(cleaned):,} rows excluded in total",
    ]
    return cleaned, report


def calculate_retention(transactions: pd.DataFrame) -> pd.DataFrame:
    """Return a cohort-by-age retention matrix in percent.

    A customer is active in a month if they have at least one valid transaction
    in that calendar month. Month 0 is the acquisition month and equals 100%.
    """
    data = transactions.copy()
    data["order_month"] = data["order_date"].dt.to_period("M")

    first_purchase = data.groupby("user_id")["order_month"].min().rename("cohort_month")
    data = data.join(first_purchase, on="user_id")
    data["cohort_age"] = (
        (data["order_month"].dt.year - data["cohort_month"].dt.year) * 12
        + data["order_month"].dt.month
        - data["cohort_month"].dt.month
    )

    cohort_sizes = first_purchase.groupby(first_purchase).size().sort_index()
    active_users = (
        data.groupby(["cohort_month", "cohort_age"])["user_id"]
        .nunique()
        .unstack("cohort_age")
        .sort_index()
    )
    retention = active_users.div(cohort_sizes, axis=0).mul(100)
    retention = retention.reindex(columns=range(int(data["cohort_age"].max()) + 1))
    retention.index = retention.index.astype(str)
    retention.columns.name = "Months Since First Purchase"
    retention.index.name = "Cohort Month"
    return retention.round(1)


def save_heatmap(retention: pd.DataFrame, output_path: Path) -> None:
    """Render and save the cohort retention matrix as an annotated heatmap."""
    if retention.empty:
        raise ValueError("Retention matrix is empty; cannot create a heatmap.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    values = retention.to_numpy(dtype=float)
    mask = pd.isna(values)
    height = max(5.0, min(0.55 * len(retention) + 2.0, 16.0))
    width = max(9.0, min(0.65 * retention.shape[1] + 4.0, 18.0))

    fig, ax = plt.subplots(figsize=(width, height))
    sns.heatmap(
        retention,
        mask=mask,
        annot=True,
        fmt=".0f",
        cmap="YlGnBu",
        vmin=0,
        vmax=100,
        linewidths=0.5,
        linecolor="white",
        cbar_kws={"label": "Returning customers (%)"},
        ax=ax,
    )
    ax.set_title("Monthly Customer Retention by Acquisition Cohort", pad=14, weight="bold")
    ax.set_xlabel("Months Since First Purchase")
    ax.set_ylabel("Acquisition Cohort")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=project_dir / "transactions.csv",
        help="Path to transaction CSV (default: project directory/transactions.csv)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=project_dir,
        help="Directory for retention outputs (default: project directory)",
    )
    args = parser.parse_args()

    transactions, quality_report = load_and_clean_data(args.input)
    retention = calculate_retention(transactions)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    matrix_path = args.output_dir / "retention_matrix.csv"
    report_path = args.output_dir / "data_quality_report.csv"
    heatmap_path = args.output_dir / "retention_heatmap.png"

    retention.to_csv(matrix_path)
    quality_report.to_csv(report_path, index=False)
    save_heatmap(retention, heatmap_path)

    print("\nData-quality report:")
    print(quality_report.to_string(index=False))
    print(f"\nRetention matrix: {matrix_path}")
    print(f"Heatmap:          {heatmap_path}")


if __name__ == "__main__":
    main()
