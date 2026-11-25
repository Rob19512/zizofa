"""CTP 2 - Exercise 3: expectation suite for ShopFast orders (GX Core 1.x).
Run from the CTP 2 folder:  python gx_orders.py

Business choices (why each rule):
- status: only canonical lowercase values — SHIPPED/Delivered/canceled are data bugs
- channel: web / mobile_app / marketplace (what the data actually uses)
- shipping_country: ISO-2 ShopFast markets FR/DE/ES/BE
- total_amount_eur: > 0 and <= 1500 (history max ~1400; negatives/zeros are errors)
"""
from datetime import date

import pandas as pd
import great_expectations as gx

KIT = "../datagov/shopfast-kit/data/"
orders = pd.read_csv(KIT + "orders.csv", dtype=str)
customers = pd.read_csv(KIT + "customers.csv", dtype=str)
orders["total_amount_eur"] = pd.to_numeric(orders["total_amount_eur"], errors="coerce")
orders["order_date_dt"] = pd.to_datetime(orders["order_date"], format="%Y-%m-%d", errors="coerce")

context = gx.get_context(mode="file")
source = context.data_sources.add_or_update_pandas("shopfast")
asset = source.add_dataframe_asset(name="orders")
batch_def = asset.add_batch_definition_whole_dataframe("all_orders")

suite = context.suites.add_or_update(gx.ExpectationSuite(name="orders_suite"))
E = gx.expectations
for e in [
    # 1 table size
    E.ExpectTableRowCountToBeBetween(min_value=1000, max_value=100000),
    # 2–3 identity
    E.ExpectColumnValuesToNotBeNull(column="order_id"),
    E.ExpectColumnValuesToBeUnique(column="order_id"),
    # TODO 1–2 customer FK
    E.ExpectColumnValuesToNotBeNull(column="customer_id"),
    E.ExpectColumnValuesToBeInSet(
        column="customer_id",
        value_set=set(customers["customer_id"].dropna().astype(str)),
    ),
    # TODO 3–4 dates
    E.ExpectColumnValuesToNotBeNull(column="order_date"),
    E.ExpectColumnValuesToMatchRegex(column="order_date", regex=r"^\d{4}-\d{2}-\d{2}$"),
    E.ExpectColumnValuesToBeBetween(
        column="order_date_dt",
        min_value=pd.Timestamp("2020-01-01"),
        max_value=pd.Timestamp(date.today()),
    ),
    # TODO 5 status
    E.ExpectColumnValuesToBeInSet(
        column="status",
        value_set=["pending", "shipped", "delivered", "cancelled", "returned"],
    ),
    # TODO 6 channel + shipping_country
    E.ExpectColumnValuesToBeInSet(
        column="channel",
        value_set=["web", "mobile_app", "marketplace"],
    ),
    E.ExpectColumnValuesToBeInSet(
        column="shipping_country",
        value_set=["FR", "DE", "ES", "BE"],
    ),
    # TODO 7 amount
    E.ExpectColumnValuesToBeBetween(column="total_amount_eur", min_value=0.01, max_value=1500),
]:
    suite.add_expectation(e)
suite.save()

vd = context.validation_definitions.add_or_update(
    gx.ValidationDefinition(name="orders_validation", data=batch_def, suite=suite)
)
checkpoint = context.checkpoints.add_or_update(
    gx.Checkpoint(
        name="orders_checkpoint",
        validation_definitions=[vd],
        actions=[gx.checkpoint.UpdateDataDocsAction(name="docs")],
    )
)
result = checkpoint.run(batch_parameters={"dataframe": orders})

print("\nSuite passed:", result.success)
n_exp = 0
for vr in result.run_results.values():
    for r in vr.results:
        n_exp += 1
        cfg = r.expectation_config
        print(
            f"{'PASS' if r.success else 'FAIL'}  {cfg.type:<45} "
            f"{cfg.kwargs.get('column', ''):<18} unexpected={r.result.get('unexpected_count', '-')}"
        )
print(f"\nExpectations run: {n_exp}")
print("Open the report: gx/uncommitted/data_docs/local_site/index.html")
