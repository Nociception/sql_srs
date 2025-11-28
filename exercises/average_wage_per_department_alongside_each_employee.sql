-- themes: average over partition_by order_by
-- tables: wages
-- subject: For each employee, display all columns from the wages table, plus the average wage in their department (named mean_dpt_wage). Order the results by department, then by mean_dpt_wage from greatest to lowest, and finally by employee name.

SELECT
    *,
    AVG(wage) OVER(PARTITION BY department) AS mean_dpt_wage
FROM
    wages
ORDER BY
    department,
    mean_dpt_wage DESC,
    name
