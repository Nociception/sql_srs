-- themes: average group_by where cte alias
-- tables: sales
-- subject: For each customer, display customers and their average amount (named avg_amount, ordered from greatest to lowest) if it is greater than the global sales average.

WITH
    avg_per_customer AS (
        SELECT
            customer,
            AVG(amount) AS avg_amout
        FROM
            sales
        GROUP BY
            customer
    )
    ,
    global AS (
        SELECT AVG(amount) AS avg
        FROM
            sales
    )

SELECT
    c.customer,
    c.avg_amout
FROM
    avg_per_customer AS c,
    global AS g
WHERE
    c.avg_amout >= g.avg
ORDER BY
    c.avg_amout DESC,
    customer
