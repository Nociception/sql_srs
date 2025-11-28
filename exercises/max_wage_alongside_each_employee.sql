-- themes: max over partition_by order_by
-- tables: wages
-- subject: For each employee, display all columns from the wages table, plus the maximum wage in their department (named max_dpt_wage). Order the results by department, then by max_dpt_wage from greatest to lowest, and finally by employee name.

SELECT
    *,
    MAX(wage) OVER(PARTITION BY department) AS max_dpt_wage
FROM
    wages
ORDER BY
    department,
    max_dpt_wage DESC,
    name
