-- themes: sum group_by
-- tables: orders_customers
-- subject: For each customer, display the total amount of their orders, ordered by this total.

SELECT
    customer,
    SUM(amount) AS amount_by_customer
FROM
    orders_customers
GROUP BY
    customer
ORDER BY
    amount_by_customer
