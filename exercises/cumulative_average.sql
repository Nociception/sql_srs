-- themes: over sum
-- tables: furniture
-- subject: Display all columns, plus a new column named cumulative_average with, in each (item ordered) row, the cumulative average weight.

SELECT
    *,
    AVG(weight) OVER(ORDER BY item) AS cumulative_average,
FROM
    furniture
