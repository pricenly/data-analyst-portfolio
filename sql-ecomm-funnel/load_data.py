"""Load the UCI Online Retail II dataset into PostgreSQL.

The script reads the raw Excel workbook (both yearly sheets) or a CSV export,
normalises the column names and loads the rows into the ``online_retail_staging``
table. Run ``load_data.sql`` afterwards to build the typed ``online_retail``
table and its indexes.

Example
-------
    python load_data.py --file online_retail_II.xlsx \
        --database-url postgresql+psycopg2://postgres:postgres@localhost:5432/retail
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

STAGING_COLUMNS = [
    "invoice_no",
    "stock_code",
    "description",
    "quantity",
    "invoice_date",
    "unit_price",
    "customer_id",
    "country",
]

COLUMN_ALIASES = {
    "invoice": "invoice_no",
    "invoiceno": "invoice_no",
    "stockcode": "stock_code",
    "description": "description",
    "quantity": "quantity",
    "invoicedate": "invoice_date",
    "price": "unit_price",
    "unitprice": "unit_price",
    "customerid": "customer_id",
    "country": "country",
}


def read_source(path: Path) -> pd.DataFrame:
    """Return the raw transaction rows from an Excel workbook or a CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    if path.suffix.lower() in {".xlsx", ".xls"}:
        sheets = pd.read_excel(path, sheet_name=None)
        frames = [frame for frame in sheets.values() if not frame.empty]
        if not frames:
            raise ValueError(f"No non-empty sheets found in {path}")
        return pd.concat(frames, ignore_index=True)

    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin1")


def _header_key(column: str) -> str:
    """Reduce a vendor header to lower-case alphanumerics (handles BOM, spaces, punctuation)."""
    return "".join(character for character in column.lower() if character.isalnum())


def normalise(df: pd.DataFrame) -> pd.DataFrame:
    """Map vendor column names onto the staging schema and clean the values."""
    renamed = {
        column: COLUMN_ALIASES[key]
        for column in df.columns
        if (key := _header_key(column)) in COLUMN_ALIASES
    }
    df = df.rename(columns=renamed)

    missing = [column for column in STAGING_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Source is missing required columns: {missing}")

    df = df[STAGING_COLUMNS].copy()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["customer_id"] = df["customer_id"].astype("string").str.strip()
    df["customer_id"] = df["customer_id"].replace({"": pd.NA, "nan": pd.NA})

    before = len(df)
    df = df.dropna(subset=["invoice_no", "stock_code", "quantity", "invoice_date", "unit_price"])
    print(f"Dropped {before - len(df):,} incomplete rows, keeping {len(df):,}")
    return df.reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", required=True, type=Path, help="Path to the raw dataset")
    parser.add_argument(
        "--database-url",
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/retail",
        help="SQLAlchemy connection string",
    )
    parser.add_argument("--table", default="online_retail_staging", help="Target staging table")
    args = parser.parse_args()

    try:
        from sqlalchemy import create_engine
    except ImportError as exc:  # pragma: no cover - dependency hint
        raise SystemExit(
            "SQLAlchemy is required. Install it with: "
            "pip install pandas openpyxl sqlalchemy psycopg2-binary"
        ) from exc

    df = normalise(read_source(args.file))

    engine = create_engine(args.database_url)
    df.to_sql(args.table, engine, if_exists="replace", index=False, chunksize=10_000)
    print(f"Loaded {len(df):,} rows into {args.table}")
    print("Next: run load_data.sql to create and index the online_retail table.")


if __name__ == "__main__":
    main()
