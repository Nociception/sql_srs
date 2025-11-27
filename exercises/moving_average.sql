-- themes: over rows_between average
-- tables: sales_2
-- subject: Display all columns from sales_2, plus a 7-day moving average (named moving_average_7_last_days) and a cumulative average of daily sales (named cumulative_average).

SELECT
    *,
    AVG(daily_sales) OVER(
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_average_7_last_days,
    AVG(daily_sales) OVER(
        ORDER BY date
    ) AS cumulative_average,
FROM
    sales_2
