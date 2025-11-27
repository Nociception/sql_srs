-- themes: over rows_between preceding
-- tables: sensors
-- subject: Display all columns from sensors, plus a moving average of visitors_count for the last 7 days including the current day.

SELECT
    *,
    AVG(visitors_count) OVER(
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_average_last_7_days
FROM
    sensors
