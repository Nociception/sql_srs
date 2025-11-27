-- themes: over rows_between preceding following
-- tables: sales_2
-- subject: Display all columns from sales_2, plus a moving average of daily sales, considering the five days before and the two days after each date.

SELECT
    *,
    AVG(daily_sales) OVER(
        ORDER BY date
        ROWS BETWEEN 5 PRECEDING AND 2 FOLLOWING
    ) AS moving_average
FROM sales_2
