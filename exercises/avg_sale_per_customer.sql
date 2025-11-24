-- themes: average group_by
-- tables: sales
-- subject: For each customer, display her/his sale average (named avg_amout, ordered according this column from greatest to lowest).

SELECT
    customer,
    AVG(amount) AS avg_amount
FROM
    sales
GROUP BY
    customer
ORDER BY
    avg_amount DESC
