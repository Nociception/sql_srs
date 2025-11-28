-- themes: lag over limit
-- tables: sensors
-- subject: Display the date, visitors_count, and the previous day's visitors_count in a new column (named previous_visitors_count) for the first 8 days.

SELECT
    date,
    visitors_count,
    LAG(visitors_count) OVER() AS previous_visitors_count
FROM
    sensors
ORDER BY
    date
LIMIT
    8
