-- themes: over sum count avg alias
-- tables: sales_2
-- subject: Display all columns, plus a new column named total_weight with, in each row, the total weight of all furniture items. Order the results by category and item.

SELECT
    *,
    SUM(daily_sales) OVER(ORDER BY date) AS running_total,
    COUNT(daily_sales) OVER(ORDER BY date) AS running_count,
    AVG(daily_sales) OVER(ORDER BY date) AS running_mean
FROM
    sales_2
