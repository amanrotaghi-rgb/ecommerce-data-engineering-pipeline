-- 1. Calculate total revenue
SELECT
    SUM(quantity * price) AS total_revenue
FROM orders;

-- 2. Calculate revenue by product category
SELECT
    category,
    SUM(quantity * price) AS total_revenue,
    SUM(quantity) AS total_units_sold
FROM orders
GROUP BY category
ORDER BY total_revenue DESC;

-- 3. Find the top 10 products by units sold
SELECT
    product,
    SUM(quantity) AS total_units_sold,
    SUM(quantity * price) AS total_revenue
FROM orders
GROUP BY product
ORDER BY total_units_sold DESC
LIMIT 10;

-- 4. Calculate monthly revenue
SELECT
    DATE_TRUNC('month', order_date)::DATE AS sales_month,
    SUM(quantity * price) AS total_revenue,
    COUNT(*) AS total_order_rows
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY sales_month;

-- 5. Find the top 10 customers by calculated revenue
SELECT
    customer_id,
    COUNT(*) AS order_rows,
    SUM(quantity) AS total_units,
    SUM(quantity * price) AS total_revenue
FROM orders
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10;

-- 6. Summarize data quality issues
SELECT
    COUNT(*) AS total_rows,

    COUNT(*) FILTER (
        WHERE customer_id IS NULL
    ) AS missing_customer_id,

    COUNT(*) FILTER (
        WHERE product IS NULL
    ) AS missing_product,

    COUNT(*) FILTER (
        WHERE quantity IS NULL OR quantity <= 0
    ) AS invalid_quantity,

    COUNT(*) FILTER (
        WHERE quantity IS NOT NULL
          AND quantity <> TRUNC(quantity)
    ) AS fractional_quantity,

    COUNT(*) FILTER (
        WHERE price IS NULL OR price < 0
    ) AS invalid_price,

    COUNT(*) FILTER (
        WHERE order_date > CURRENT_DATE
    ) AS future_dated_rows,

    COUNT(*) FILTER (
        WHERE order_date < DATE '2020-01-01'
    ) AS unusually_old_dates

FROM orders;