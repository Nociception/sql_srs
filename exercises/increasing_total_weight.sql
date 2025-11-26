-- themes: over sum
-- tables: furniture
-- subject: Display all columns, plus a new column named increasing_total_weight with, in each row, the total weight of all furniture items with weight less than or equal to the current item's weight.

SELECT 
    *,
    SUM(weight) OVER(
        ORDER BY weight
    ) AS increasing_total_weight
FROM
    furniture
