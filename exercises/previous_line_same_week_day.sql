-- themes: lag over partition_by order_by
-- tables: sensors
-- subject: Display the date, visitors_count, and the previous visitors_count for the same weekday in a new column (named last_same_day_visitors_count). Order the results by date.

SELECT
    date,
    visitors_count,
    LAG(visitors_count) OVER(
        PARTITION BY weekday 
        ORDER BY date
    ) AS last_same_day_visitors_count,
FROM
    sensors
ORDER BY
    date
