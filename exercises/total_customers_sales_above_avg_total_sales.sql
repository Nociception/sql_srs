-- themes: cte group_by where alias
-- tables: sales
-- subject: Display, in this order, customer and their total sales (named total_amount_per_customer, ordered according to this column, from greatest to lowest), only if this total is greater than the total amount average per customer.

WITH
    total_per_customer AS (
        SELECT
            customer,
            SUM(amount) AS total_amount_per_customer
        FROM
            sales
        GROUP BY
            customer
    )
    ,
    total_mean_sales_per_customer AS(
        SELECT
            AVG(c.total_amount_per_customer) AS mean
        FROM
            total_per_customer AS c
    )

SELECT
    c.customer,
    c.total_amount_per_customer
FROM
    total_per_customer AS c,
    total_mean_sales_per_customer AS m
WHERE
    c.total_amount_per_customer > m.mean
ORDER BY
    c.total_amount_per_customer DESC
