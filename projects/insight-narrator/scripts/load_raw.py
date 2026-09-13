"""
Loads Olist-shaped CSVs into a local DuckDB warehouse under the `raw` schema.

Looks in data/raw/ first (the real Kaggle download); falls back to
data/sample/ (synthetic fixture data) so the pipeline runs out of the box.
"""

import sys
from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
SAMPLE_DIR = PROJECT_ROOT / "data" / "sample"
WAREHOUSE_PATH = PROJECT_ROOT / "warehouse" / "insight_narrator.duckdb"

TABLES = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
}


def pick_source_dir() -> Path:
    if RAW_DIR.exists() and any(RAW_DIR.glob("*.csv")):
        print(f"Using real dataset from {RAW_DIR}")
        return RAW_DIR
    if SAMPLE_DIR.exists() and any(SAMPLE_DIR.glob("*.csv")):
        print(f"No files in data/raw/ -- using synthetic sample data from {SAMPLE_DIR}")
        print("(run `python scripts/generate_sample_data.py` first if this folder is empty too)")
        return SAMPLE_DIR
    print("No data found in data/raw/ or data/sample/.")
    print("Either download the real dataset from")
    print("  https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce")
    print("into data/raw/, or run: python scripts/generate_sample_data.py")
    sys.exit(1)


def main():
    source_dir = pick_source_dir()
    WAREHOUSE_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(WAREHOUSE_PATH))
    con.execute("create schema if not exists raw")

    for table, filename in TABLES.items():
        csv_path = source_dir / filename
        if not csv_path.exists():
            print(f"  skip {table}: {csv_path.name} not found")
            continue
        con.execute(f"""
            create or replace table raw.{table} as
            select * from read_csv_auto('{csv_path.as_posix()}', header=True)
        """)
        count = con.execute(f"select count(*) from raw.{table}").fetchone()[0]
        print(f"  loaded raw.{table:<16} {count:>6} rows")

    con.close()
    print(f"\nWarehouse ready at {WAREHOUSE_PATH}")


if __name__ == "__main__":
    main()
