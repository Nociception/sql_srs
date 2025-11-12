-- themes: nested_query where
-- tables: executions
-- subject: Find the first and last name of the inmate with the longest last statement (by character count).

SELECT
    first_name,
    last_name
FROM
    executions
WHERE
    LENGTH(last_statement)
    =
    (
        SELECT
            MAX(LENGTH(last_statement))
        FROM
            executions
    )
