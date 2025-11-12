-- themes: count percentage nested_query group_by order_by
-- tables: executions
-- subject: Display the percentage of executions from each county, from greatest to lowest.

SELECT
    county,
    (
        100.0
        *
        COUNT(*)
    )
    /
    (
        SELECT
            COUNT(*)
        FROM
            executions
    ) AS percentage
FROM
    executions
GROUP BY
    county
ORDER BY
    percentage DESC
