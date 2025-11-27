-- themes: over rows_between preceding
-- tables: sensors
-- subject: Display all columns from the sensors table, plus a 7-last days moving visitors sum, a 7-last days moving rows count, a 7-last days moving average calculated with the two new preceding columns, and a 7-last days moving average calculated with the AVG() window function. Compare the two moving averages to check they are equal.

SELECT
    *,
    SUM(visitors_count) OVER(
        ORDER BY DATE 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS seven_days_running_total,
    COUNT(*) OVER(
        ORDER BY DATE 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS seven_days_moving_count,
    seven_days_running_total / seven_days_moving_count AS check,
    AVG(visitors_count) OVER(
        ORDER BY DATE 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS seven_days_moving_average
FROM
    sensors
