# Impact: payments.amount switch to cents
If `amount` moves from euros to cents, `stg_payments` then `fct_orders` (gross/refunded/net) and `dim_customers.lifetime_net_revenue_eur` inflate ~100× — Sales dashboard + Finance monthly report show wrong revenue; churn model features drift.
Warn owners: Paul Girard (payments/`stg_payments`, Finance report), Sara Martin (`fct_orders`, Sales dashboard), Karim Benali (`dim_customers`, churn model).
Add a dbt test that `stg_payments.amount` stays in a plausible euro range (e.g. 0–10_000) and document unit = euros in YAML/dictionary.
Change must be approved by Paul Girard (Head of Finance) before merge; update `stg_payments.amount` description and any ÷100 transform in the same PR.
