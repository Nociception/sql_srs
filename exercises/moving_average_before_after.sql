-- themes: over rows_between preceding following
-- tables: sales_2
-- subject: Display all columns from sales_2, plus a moving total and moving average of daily sales, considering the day before and the day after each date.

SELECT
    *,
    SUM(daily_sales) OVER(
        ORDER BY date 
        ROWS BETWEEN 1 PRECEDING and 1 FOLLOWING
    ) AS moving_total,
        AVG(daily_sales) OVER(
        ORDER BY date 
        ROWS BETWEEN 1 PRECEDING and 1 FOLLOWING
    ) AS moving_average,
FROM sales_2
