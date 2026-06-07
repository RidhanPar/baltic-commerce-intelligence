"""Generate deterministic, realistic Baltic commerce data for portfolio analysis."""

from __future__ import annotations

import argparse
import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

MARKETS = {
    "LV": {"weight": 0.48, "conversion": 0.01, "delivery": 4.1},
    "LT": {"weight": 0.32, "conversion": -0.01, "delivery": 4.8},
    "EE": {"weight": 0.20, "conversion": 0.00, "delivery": 5.4},
}
CHANNELS = {
    "Paid Search": {"weight": 0.27, "base_cac": 18.0, "intent": 0.07},
    "Paid Social": {"weight": 0.25, "base_cac": 23.0, "intent": -0.04},
    "Organic Search": {"weight": 0.20, "base_cac": 5.0, "intent": 0.05},
    "CRM": {"weight": 0.16, "base_cac": 4.0, "intent": 0.08},
    "Affiliate": {"weight": 0.12, "base_cac": 15.0, "intent": -0.01},
}
CATEGORIES = {
    "Electronics": {"weight": 0.20, "price": 105, "margin": 0.30, "refund": 0.09},
    "Home": {"weight": 0.25, "price": 62, "margin": 0.43, "refund": 0.05},
    "Beauty": {"weight": 0.22, "price": 38, "margin": 0.56, "refund": 0.03},
    "Sports": {"weight": 0.18, "price": 71, "margin": 0.40, "refund": 0.06},
    "Pet Care": {"weight": 0.15, "price": 34, "margin": 0.48, "refund": 0.02},
}
CARRIERS = {
    "BalticPost": {"weight": 0.44, "cost_factor": 0.95, "base_late": 0.08},
    "FastShip": {"weight": 0.34, "cost_factor": 1.15, "base_late": 0.04},
    "EconomyBox": {"weight": 0.22, "cost_factor": 0.82, "base_late": 0.12},
}


def weighted_choice(rng: random.Random, mapping: dict[str, dict]) -> str:
    names = list(mapping)
    return rng.choices(names, weights=[mapping[name]["weight"] for name in names], k=1)[0]


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def generate(output_dir: Path, seed: int = 42, prospect_count: int = 6000) -> None:
    rng = random.Random(seed)
    start = date(2025, 1, 1)
    prospects: list[dict] = []
    customers: list[dict] = []
    orders: list[dict] = []
    marketing: list[dict] = []
    deliveries: list[dict] = []
    experiments: list[dict] = []

    for prospect_num in range(1, prospect_count + 1):
        prospect_id = f"P{prospect_num:05d}"
        market = weighted_choice(rng, MARKETS)
        channel = weighted_choice(rng, CHANNELS)
        category_interest = weighted_choice(rng, CATEGORIES)
        assignment_date = start + timedelta(days=rng.randint(0, 300))
        treatment = "treatment" if rng.random() < 0.5 else "control"
        device = rng.choices(["mobile", "desktop"], weights=[0.64, 0.36], k=1)[0]
        engagement = clamp(rng.betavariate(2.3, 3.2), 0.02, 0.98)

        conversion_probability = (
            0.27
            + CHANNELS[channel]["intent"]
            + MARKETS[market]["conversion"]
            + (engagement - 0.45) * 0.24
            + (0.025 if treatment == "treatment" else 0)
            - (0.025 if device == "mobile" else 0)
            + rng.gauss(0, 0.025)
        )
        converted = rng.random() < clamp(conversion_probability, 0.08, 0.68)
        prospects.append(
            {
                "prospect_id": prospect_id,
                "market": market,
                "acquisition_channel": channel,
                "category_interest": category_interest,
                "device_type": device,
                "engagement_score": round(engagement, 4),
                "assignment_date": assignment_date.isoformat(),
                "converted": int(converted),
            }
        )
        experiments.append(
            {
                "prospect_id": prospect_id,
                "experiment_id": "free_shipping_threshold",
                "treatment": treatment,
                "assignment_date": assignment_date.isoformat(),
            }
        )
        if not converted:
            continue

        customer_id = f"C{len(customers) + 1:05d}"
        repeat_propensity = clamp(0.45 + engagement * 0.8 + rng.gauss(0, 0.25), 0.12, 1.55)
        customer_orders = max(1, min(7, 1 + int(rng.expovariate(1 / repeat_propensity))))
        customers.append(
            {
                "customer_id": customer_id,
                "prospect_id": prospect_id,
                "market": market,
                "acquisition_channel": channel,
                "acquisition_date": assignment_date.isoformat(),
            }
        )

        acquisition_cost = max(
            1.0,
            CHANNELS[channel]["base_cac"]
            * (1 + 0.15 * math.sin(assignment_date.timetuple().tm_yday / 30))
            * rng.uniform(0.82, 1.22),
        )
        for purchase_num in range(1, customer_orders + 1):
            order_id = f"O{len(orders) + 1:06d}"
            category = category_interest if rng.random() < 0.48 else weighted_choice(rng, CATEGORIES)
            carrier = weighted_choice(rng, CARRIERS)
            order_date = assignment_date + timedelta(days=(purchase_num - 1) * rng.randint(18, 48))
            if order_date > date(2025, 12, 31):
                break

            cfg = CATEGORIES[category]
            market_price_factor = {"LV": 1.00, "LT": 0.96, "EE": 1.08}[market]
            gross = round(max(12, rng.gauss(cfg["price"] * market_price_factor, cfg["price"] * 0.34)), 2)
            treatment_discount = 0.07 if treatment == "treatment" and gross >= 55 else 0
            discount_rate = max(treatment_discount, rng.choices([0, 0.05, 0.10], weights=[0.60, 0.25, 0.15], k=1)[0])
            discount = round(gross * discount_rate, 2)
            refund_probability = cfg["refund"] + (0.025 if device == "mobile" else 0) + (0.015 if channel == "Paid Social" else 0)
            refund = round(gross * rng.uniform(0.65, 1.0), 2) if rng.random() < refund_probability else 0
            product_cost = round(gross * (1 - cfg["margin"] + rng.uniform(-0.025, 0.025)), 2)
            delivery_cost = round(MARKETS[market]["delivery"] * CARRIERS[carrier]["cost_factor"] + rng.uniform(-0.5, 1.0), 2)
            payment_cost = round(gross * 0.018 + 0.20, 2)
            fulfillment_cost = round(2.10 + rng.uniform(-0.2, 0.7), 2)
            marketing_cost = round(acquisition_cost if purchase_num == 1 else acquisition_cost * 0.03, 2)
            net_revenue = round(gross - discount - refund, 2)
            contribution = round(net_revenue - product_cost - delivery_cost - payment_cost - fulfillment_cost - marketing_cost, 2)
            status = "completed" if refund < gross else "refunded"
            orders.append(
                {
                    "order_id": order_id,
                    "customer_id": customer_id,
                    "prospect_id": prospect_id,
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
            route_risk = (0.035 if market == "EE" else 0) + (0.025 if category == "Electronics" else 0)
            seasonal_risk = 0.05 if order_date.month in [11, 12] else 0
            late_probability = clamp(CARRIERS[carrier]["base_late"] + route_risk + seasonal_risk + rng.gauss(0, 0.02), 0.01, 0.35)
            late = rng.random() < late_probability
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
                        "spend": round(cfg["base_cac"] * rng.randint(25, 70), 2),
                    }
                )

    write_csv(output_dir / "prospects.csv", prospects)
    write_csv(output_dir / "customers.csv", customers)
    write_csv(output_dir / "orders.csv", orders)
    write_csv(output_dir / "marketing_spend.csv", marketing)
    write_csv(output_dir / "deliveries.csv", deliveries)
    write_csv(output_dir / "experiment_assignments.csv", experiments)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--prospects", type=int, default=6000)
    args = parser.parse_args()
    generate(args.output_dir, args.seed, args.prospects)
