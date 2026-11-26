{% docs gross_revenue %}
**Gross revenue (EUR)** — total amount paid by the customer for an order, VAT included, shipping included, before refunds.
Owner: Head of Sales · Steward: Karim Benali · Status: approved (2026-11-10)
{% enddocs %}

{% docs net_revenue %}
**Net revenue (EUR)** — revenue after refunds and excluding VAT; shipping stays in.
Formula: `(gross_revenue_eur - refunded_eur) / 1.20`
Example: €120 paid incl. VAT, €0 refund → €100 net.
Owner: Paul Girard (Head of Finance) · Steward: Karim Benali · Status: approved (2026-11-25)
Note: Sales commission uses paid − refunds *including* VAT — do not label that as net revenue.
{% enddocs %}

{% docs active_customer %}
**Active customer** — a customer account with at least one non-cancelled order in the last 12 months.
Formula: `last_order_date` within 12 months AND ≥1 order with `status <> cancelled`.
Example: delivered order on 2026-03-01 → active on 2026-11-25.
Owner: Paul Girard (Head of Finance) · Steward: Karim Benali · Status: approved (2026-11-25)
Note: Sales campaigns may filter a *recently active customer* (6 months); that is not the company KPI.
{% enddocs %}

{% docs churned_customer %}
**Churned customer** — a former active customer with no non-cancelled order in the last 12 months.
Formula: previously active AND last non-cancelled `order_date` older than 12 months (or none).
Example: last delivered order 2025-06-01 → churned on 2026-11-25.
Owner: Sara Martin (Head of Sales) · Steward: Karim Benali · Status: approved (2026-11-25)
{% enddocs %}

{% docs customer %}
**Customer** — a person or organisation holding a ShopFast account (one row in the customer dimension).
Formula: one row per `customer_id` in `dim_customers` / `stg_customers`.
Example: `customer_id` 42 with email a@b.com = one customer.
Owner: Sara Martin (Head of Sales) · Steward: Karim Benali · Status: approved (2026-11-25)
{% enddocs %}

{% docs order %}
**Order** — a single purchase transaction placed by a customer.
Formula: one row per `order_id` in `fct_orders` / `stg_orders` (all statuses, including cancelled).
Example: `order_id` 700001 status delivered = one order.
Owner: Sara Martin (Head of Sales) · Steward: Karim Benali · Status: approved (2026-11-25)
{% enddocs %}
