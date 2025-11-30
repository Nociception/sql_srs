-- themes: lag over partition_by order_by round
-- tables: sensors
-- subject: Display all columns from the sensors table along with the visitors_count from the previous week day in a new column (named previous_week_day). Additionally, calculate the percentage variation between the current visitors_count and the previous week's same day visitors_count in a new column (named percentage_variation), rounded to 2 decimal places. Finally, include a boolean column (named pct_variation_threshold) that indicates whether the percentage variation is less than -30%. Order the results by date.

SELECT
    *,
    LAG(visitors_count) OVER(
        PARTITION BY weekday
    ) AS previous_week_day,
    ROUND(
        (100*(visitors_count - previous_week_day) / previous_week_day),
        2
    ) AS percentage_variation,
    percentage_variation < -30 AS pct_variation_threshold
FROM
    sensors
ORDER BY
    date
