-- themes: over rows_between sum
-- tables: sales_2
-- subject: Display all columns from the sales_2 table, plus (in this order) a 7-day moving total of daily_sales (named moving_total_7_last_rows) and a cumulative total of daily_sales (named cumulative_total).

SELECT
    *,
    SUM(daily_sales) OVER(
        ORDER BY
            date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_total_7_last_rows,
    SUM(daily_sales) OVER(
        ORDER BY
            date
    ) AS cumulative_total,
FROM
    sales_2
