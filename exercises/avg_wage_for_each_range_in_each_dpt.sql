-- themes: cte case_when group_by count
-- tables: wages
-- subject: There are three wage ranges:\n - 'low': lower than 50000\n - 'medium': between 50000 (included) and 90000 (excluded)\n- 'high': greater (or equal) than 90000\nIn each department, for each range, display (in this order) department, range, the category wage average (results displayed ordered by this column), and how many lines are concerned for the current category.

WITH ranges AS (
    SELECT
        department,
        wage,
        (
            CASE
                WHEN wage < 50000 THEN 'low'
                WHEN wage < 90000 THEN 'medium'
                ELSE 'high'
            END
        ) AS range
    FROM wages
)

SELECT
    department,
    range,
    AVG(wage) AS avg_wage,
    COUNT(*)
FROM
    ranges
GROUP BY
    department,
    range
ORDER BY
    avg_wage
