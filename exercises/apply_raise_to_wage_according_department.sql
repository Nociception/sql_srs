-- themes: case_when
-- tables: wages
-- subject: apply the following raises by displaying (in this order) name (ordered according this column), wage(raised then) and department, depending on the department:\n- +10% for SALES\n- 5% for HR\n- 3% for IT\n- 0% for the CEO

SELECT
    name,
    department,
    CASE
        WHEN department = 'IT' THEN CAST(wage * 1.03 AS DECIMAL(10,2))
        WHEN department = 'SALES' THEN CAST(wage * 1.1 AS DECIMAL(10,2))
        WHEN department = 'HR' THEN CAST(wage * 1.05 AS DECIMAL(10,2))
        ELSE CAST(wage AS DECIMAL(10,2))
    END AS wage_raised
FROM wages