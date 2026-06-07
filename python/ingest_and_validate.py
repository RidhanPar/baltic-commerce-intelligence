"""Validate a source extract before loading it into the analytics warehouse."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "order_id",
    "customer_id",
    "order_date",
    "market",
    "gross_revenue",
    "discount_amount",
    "refund_amount",
    "product_cost",
    "delivery_cost",
}


def validate_orders(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        errors.append(f"Missing required columns: {sorted(missing)}")
        return errors

    if df["order_id"].duplicated().any():
        errors.append("order_id contains duplicates")
    if df[["order_id", "customer_id", "order_date"]].isna().any().any():
        errors.append("Critical identifiers or dates contain nulls")
    if (df["gross_revenue"] < 0).any():
        errors.append("gross_revenue contains negative values")
    if (~df["market"].isin(["LV", "LT", "EE"])).any():
        errors.append("market contains unsupported values")
    return errors


def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["order_date"] = pd.to_datetime(result["order_date"], errors="raise")
    result["net_revenue"] = (
        result["gross_revenue"]
        - result["discount_amount"]
        - result["refund_amount"]
    )
    result["contribution_margin"] = (
        result["net_revenue"] - result["product_cost"] - result["delivery_cost"]
    )
    return result


def main(source: Path, output: Path) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    orders = pd.read_csv(source)
    errors = validate_orders(orders)
    if errors:
        raise ValueError("; ".join(errors))

    transformed = transform_orders(orders)
    output.parent.mkdir(parents=True, exist_ok=True)
    transformed.to_parquet(output, index=False)
    logging.info("Validated and wrote %s rows to %s", len(transformed), output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    main(args.source, args.output)

