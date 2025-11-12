-- themes: length average composition
-- tables: executions
-- subject: Find the average length (based on character count) of last statements in the dataset (when last_statement exists).

SELECT
    AVG(
        LENGTH(last_statement)
    )
FROM
    executions
