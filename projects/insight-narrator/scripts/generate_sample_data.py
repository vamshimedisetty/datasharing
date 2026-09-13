"""
Generates a small synthetic dataset shaped exactly like the real Olist
Brazilian E-Commerce dataset (same file names and columns), so the pipeline
is runnable end-to-end without waiting on a Kaggle download.

This is fixture data for demoing/testing the pipeline -- swap in the real
CSVs from https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce into
data/raw/ for a real analysis.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(7)

OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "sample"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CATEGORIES = ["electronics", "housewares", "sports_leisure", "beauty_health", "toys"]
STATES = ["SP", "RJ", "MG", "RS", "PR"]

N_WEEKS = 10
START = datetime(2017, 9, 4)  # a Monday

customers, orders, order_items, payments, reviews, products, sellers = (
    [], [], [], [], [], [], []
)

N_PRODUCTS = 20
N_SELLERS = 6
for i in range(N_PRODUCTS):
    products.append({
        "product_id": f"prod_{i:03d}",
        "product_category_name": random.choice(CATEGORIES),
    })
for i in range(N_SELLERS):
    sellers.append({
        "seller_id": f"seller_{i:02d}",
        "seller_zip_code_prefix": 10000 + i,
        "seller_city": "sao paulo",
        "seller_state": "SP",
    })

order_seq = 0
customer_seq = 0

for week in range(N_WEEKS):
    week_start = START + timedelta(weeks=week)

    # baseline order volume grows slightly week over week
    base_orders = 22 + week * 2

    # inject two deliberate anomalies for the narrator to catch:
    # - week 6: a demand spike (flash sale)
    # - week 8: a delivery-quality problem (logistics issue)
    if week == 6:
        base_orders = int(base_orders * 2.2)
    n_orders_this_week = base_orders + random.randint(-3, 3)

    for _ in range(n_orders_this_week):
        order_seq += 1
        customer_seq += 1
        order_id = f"order_{order_seq:05d}"
        customer_id = f"cust_{customer_seq:05d}"

        purchase_dt = week_start + timedelta(
            days=random.randint(0, 6),
            hours=random.randint(8, 21),
        )

        # delivery behavior
        normal_delivery_days = random.randint(4, 9)
        estimated_days = 12
        if week == 8:
            # logistics issue: deliveries run much later this week
            delivery_days = normal_delivery_days + random.randint(8, 16)
        else:
            delivery_days = normal_delivery_days

        delivered_dt = purchase_dt + timedelta(days=delivery_days)
        estimated_dt = purchase_dt + timedelta(days=estimated_days)

        customers.append({
            "customer_id": customer_id,
            "customer_unique_id": customer_id,
            "customer_zip_code_prefix": 20000 + (customer_seq % 500),
            "customer_city": "rio de janeiro",
            "customer_state": random.choice(STATES),
        })

        orders.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_status": "delivered",
            "order_purchase_timestamp": purchase_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "order_approved_at": (purchase_dt + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "order_delivered_carrier_date": (purchase_dt + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "order_delivered_customer_date": delivered_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "order_estimated_delivery_date": estimated_dt.strftime("%Y-%m-%d %H:%M:%S"),
        })

        n_items = random.choice([1, 1, 1, 2, 2, 3])
        for item_no in range(1, n_items + 1):
            price = round(random.uniform(25, 320), 2)
            order_items.append({
                "order_id": order_id,
                "order_item_id": item_no,
                "product_id": random.choice(products)["product_id"],
                "seller_id": random.choice(sellers)["seller_id"],
                "shipping_limit_date": (purchase_dt + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
                "price": price,
                "freight_value": round(price * random.uniform(0.05, 0.15), 2),
            })

        order_total = sum(
            it["price"] + it["freight_value"]
            for it in order_items if it["order_id"] == order_id
        )
        payments.append({
            "order_id": order_id,
            "payment_sequential": 1,
            "payment_type": random.choice(["credit_card", "credit_card", "boleto", "voucher"]),
            "payment_installments": random.choice([1, 1, 2, 3, 6]),
            "payment_value": round(order_total, 2),
        })

        # review score drops during the week-8 logistics problem
        if week == 8:
            score = random.choices([1, 2, 3, 4, 5], weights=[30, 30, 20, 10, 10])[0]
        else:
            score = random.choices([1, 2, 3, 4, 5], weights=[3, 5, 12, 30, 50])[0]
        reviews.append({
            "review_id": f"rev_{order_seq:05d}",
            "order_id": order_id,
            "review_score": score,
            "review_creation_date": (delivered_dt + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
        })


def write_csv(filename, rows, fieldnames):
    path = OUT_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows):>5} rows -> {path}")


write_csv("olist_customers_dataset.csv", customers,
          ["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"])
write_csv("olist_orders_dataset.csv", orders,
          ["order_id", "customer_id", "order_status", "order_purchase_timestamp", "order_approved_at",
           "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"])
write_csv("olist_order_items_dataset.csv", order_items,
          ["order_id", "order_item_id", "product_id", "seller_id", "shipping_limit_date", "price", "freight_value"])
write_csv("olist_order_payments_dataset.csv", payments,
          ["order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"])
write_csv("olist_order_reviews_dataset.csv", reviews,
          ["review_id", "order_id", "review_score", "review_creation_date"])
write_csv("olist_products_dataset.csv", products, ["product_id", "product_category_name"])
write_csv("olist_sellers_dataset.csv", sellers, ["seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"])

print(f"\nSample data spans {N_WEEKS} weeks starting {START.date()}.")
print("Deliberate anomalies: week 6 = demand spike, week 8 = late-delivery/review-score drop.")
