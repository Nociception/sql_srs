-- themes: max over partition_by order_by cte where
-- tables: wages
-- subject: For each employee who does not have the maximum wage in their department, display all columns from the wages table. Order the results by the maximum wage in their department from greatest to lowest, and then by wage from greatest to lowest. The idea is to show the second highest wage per department.

WITH at_max_dpt_wage AS(
    SELECT
        *,
        MAX(wage) OVER(PARTITION BY department) AS max_dpt_wage,
        wage = max_dpt_wage AS leader_dpt_wage
    FROM
        wages
)

SELECT
    *
FROM
    at_max_dpt_wage
WHERE
    leader_dpt_wage = false
ORDER BY
    max_dpt_wage DESC,
    wage DESC
