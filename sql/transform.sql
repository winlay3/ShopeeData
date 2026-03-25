CREATE TABLE mart_orders_enriched AS
SELECT 
    o.order_id,
    o.order_date,
    o.customer_id,
    o.total_amount,
    oi.order_item_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.unit_price_after_discount,
    oi.line_total,
    oi.discount_percent,
    oi.item_status,
    p.product_name,
    p.category,
    p.seller_id
FROM raw_orders o
JOIN raw_order_items oi ON o.order_id = oi.order_id
JOIN raw_products p     ON oi.product_id = p.product_id;