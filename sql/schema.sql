CREATE TABLE IF NOT EXISTS raw_orders (
    order_id          INTEGER PRIMARY KEY,
    order_date        DATE,
    customer_id       VARCHAR(20),
    order_day         DATE,
    year_month        VARCHAR(7),
    subtotal_amount   NUMERIC(12,2),
    shipping_fee_total NUMERIC(10,2),
    commission_total  NUMERIC(10,2),
    maintenance_total NUMERIC(10,2),
    total_amount      NUMERIC(12,2),
    campaign_id       VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS raw_order_items (
    order_item_id           INTEGER PRIMARY KEY,
    order_id                INTEGER,
    product_id              VARCHAR(20),
    quantity                INTEGER,
    unit_price              NUMERIC(12,2),
    unit_price_after_discount NUMERIC(12,2),
    line_total              NUMERIC(12,2),
    discount_percent        NUMERIC(5,2),
    commission_amount       NUMERIC(10,2),
    maintenance_amount      NUMERIC(10,2),
    shipping_fee_item       NUMERIC(10,2),
    estimated_delivery_start DATE,
    estimated_delivery_end  TIMESTAMP,
    item_status             VARCHAR(20),
    is_campaign             BOOLEAN,
    product_campaign_id     VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS raw_products (
    product_id        VARCHAR(20) PRIMARY KEY,
    seller_id         VARCHAR(20),
    category          VARCHAR(50),
    product_name      VARCHAR(100),
    maintenance_rate  NUMERIC(5,4),
    commission_rate   NUMERIC(5,4),
    weight            NUMERIC(8,2),
    created_at        DATE
);