-- themes: over sum
-- tables: furniture
-- subject: Display all columns, plus a new column named total_weight with, in each row, the total weight of all furniture items. Order the results by category and item.

SELECT
    *,
    SUM(weight) OVER() AS total_weight
FROM
    furniture
ORDER BY
    category,
    item
