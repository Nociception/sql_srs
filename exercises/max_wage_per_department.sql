-- themes: max group_by
-- tables: wages
-- subject: For each department, display the maximum wage (named max_wage_per_department), ordered from greatest to lowest, according to this new column.

SELECT
    department,
    MAX(wage) AS max_wage_per_department
FROM
    wages
GROUP BY
    department
ORDER BY
    max_wage_per_department DESC
