"""Generate a deterministic Baltic e-commerce dataset for portfolio analysis."""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

MARKETS = {
    "LV": {"weight": 0.48, "delivery": 4.1},
    "LT": {"weight": 0.32, "delivery": 4.8},
    "EE": {"weight": 0.20, "delivery": 5.4},
}
CHANNELS = {
    "Paid Search": {"weight": 0.27, "cac": 18.0, "quality": 1.10},
    "Paid Social": {"weight": 0.25, "cac": 25.0, "quality": 0.78},
    "Organic Search": {"weight": 0.20, "cac": 4.0, "quality": 1.18},
    "CRM": {"weight": 0.16, "cac": 3.0, "quality": 1.35},
    "Affiliate": {"weight": 0.12, "cac": 15.0, "quality": 0.88},
}
CATEGORIES = {
    "Electronics": {"weight": 0.20, "price": 105, "margin": 0.30, "refund": 0.09},
    "Home": {"weight": 0.25, "price": 62, "margin": 0.43, "refund": 0.05},
    "Beauty": {"weight": 0.22, "price": 38, "margin": 0.56, "refund": 0.03},
    "Sports": {"weight": 0.18, "price": 71, "margin": 0.40, "refund": 0.06},
    "Pet Care": {"weight": 0.15, "price": 34, "margin": 0.48, "refund": 0.02},
}
CARRIERS = {
    "BalticPost": {"weight": 0.44, "cost_factor": 0.95, "late_rate": 0.08},
    "FastShip": {"weight": 0.34, "cost_factor": 1.15, "late_rate": 0.04},
    "EconomyBox": {"weight": 0.22, "cost_factor": 0.82, "late_rate": 0.18},
}


def weighted_choice(rng: random.Random, mapping: dict[str, dict]) -> str:
    names = list(mapping)
    return rng.choices(names, weights=[mapping[name]["weight"] for name in names], k=1)[0]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def generate(output_dir: Path, seed: int = 42, customer_count: int = 2400) -> None:
    rng = random.Random(seed)
    start = date(2025, 1, 1)
    customers: list[dict] = []
    orders: list[dict] = []
    marketing: list[dict] = []
    deliveries: list[dict] = []
    experiments: list[dict] = []

    for customer_num in range(1, customer_count + 1):
        customer_id = f"C{customer_num:05d}"
        market = weighted_choice(rng, MARKETS)
        channel = weighted_choice(rng, CHANNELS)
        acquisition_date = start + timedelta(days=rng.randint(0, 300))
        quality = CHANNELS[channel]["quality"]
        customer_orders = max(1, min(7, int(rng.expovariate(1 / quality)) + 1))
        customers.append(
            {
                "customer_id": customer_id,
                "market": market,
                "acquisition_channel": channel,
                "acquisition_date": acquisition_date.isoformat(),
            }
        )

        treatment = "treatment" if rng.random() < 0.5 else "control"
        experiments.append(
            {
                "customer_id": customer_id,
                "experiment_id": "free_shipping_threshold",
                "treatment": treatment,
                "assignment_date": acquisition_date.isoformat(),
            }
        )

        for purchase_num in range(1, customer_orders + 1):
            order_id = f"O{len(orders) + 1:06d}"
            category = weighted_choice(rng, CATEGORIES)
            carrier = weighted_choice(rng, CARRIERS)
            order_date = acquisition_date + timedelta(days=(purchase_num - 1) * rng.randint(18, 48))
            if order_date > date(2025, 12, 31):
                break

            category_cfg = CATEGORIES[category]
            gross = round(max(12, rng.gauss(category_cfg["price"], category_cfg["price"] * 0.35)), 2)
            discount_rate = 0.10 if treatment == "treatment" and gross >= 55 else rng.choice([0, 0, 0.05, 0.10])
            discount = round(gross * discount_rate, 2)
            refund = round(gross * rng.uniform(0.65, 1.0), 2) if rng.random() < category_cfg["refund"] else 0
            product_cost = round(gross * (1 - category_cfg["margin"]), 2)
            delivery_cost = round(
                MARKETS[market]["delivery"] * CARRIERS[carrier]["cost_factor"] + rng.uniform(-0.5, 1.0), 2
            )
            payment_cost = round(gross * 0.018 + 0.20, 2)
            fulfillment_cost = round(2.10 + rng.uniform(-0.2, 0.7), 2)
            marketing_cost = round(CHANNELS[channel]["cac"] / max(1, customer_orders), 2)
            net_revenue = round(gross - discount - refund, 2)
            contribution = round(
                net_revenue - product_cost - delivery_cost - payment_cost - fulfillment_cost - marketing_cost, 2
            )
            status = "completed" if refund < gross else "refunded"
            orders.append(
                {
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "order_date": order_date.isoformat(),
                    "market": market,
                    "acquisition_channel": channel,
                    "category": category,
                    "order_status": status,
                    "gross_revenue": gross,
                    "discount_amount": discount,
                    "refund_amount": refund,
                    "product_cost": product_cost,
                    "delivery_cost": delivery_cost,
                    "payment_cost": payment_cost,
                    "fulfillment_cost": fulfillment_cost,
                    "attributed_marketing_cost": marketing_cost,
                    "net_revenue": net_revenue,
                    "contribution_margin": contribution,
                }
            )

            promised = order_date + timedelta(days=3)
            late = rng.random() < CARRIERS[carrier]["late_rate"]
            delivered = promised + timedelta(days=rng.randint(1, 4) if late else rng.randint(-1, 0))
            deliveries.append(
                {
                    "order_id": order_id,
                    "carrier": carrier,
                    "promised_date": promised.isoformat(),
                    "delivered_date": delivered.isoformat(),
                    "on_time": int(delivered <= promised),
                    "delivery_cost": delivery_cost,
                }
            )

    for month in range(1, 13):
        for market in MARKETS:
            for channel, cfg in CHANNELS.items():
                marketing.append(
                    {
                        "month": date(2025, month, 1).isoformat(),
                        "market": market,
                        "channel": channel,
                        "spend": round(cfg["cac"] * rng.randint(25, 70), 2),
                    }
                )

    write_csv(output_dir / "customers.csv", customers)
    write_csv(output_dir / "orders.csv", orders)
    write_csv(output_dir / "marketing_spend.csv", marketing)
    write_csv(output_dir / "deliveries.csv", deliveries)
    write_csv(output_dir / "experiment_assignments.csv", experiments)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--customers", type=int, default=2400)
    args = parser.parse_args()
    generate(args.output_dir, args.seed, args.customers)

