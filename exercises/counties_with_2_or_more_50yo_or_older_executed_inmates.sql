-- themes: count group_by having
-- tables: executions
-- subject: Display counties with 2 or more 50 years old (or older) executed inmates.

SELECT
    county
FROM
    executions
WHERE
    ex_age >= 50
GROUP BY
    county
HAVING
    COUNT(*) > 2
