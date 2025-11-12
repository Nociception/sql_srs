-- themes: where like
-- tables: executions
-- subject: Display the Napoleon Beazley's last_statement.

SELECT
    last_statement
FROM
	executions
WHERE
	first_name LIKE '%apole%'
    AND last_name LIKE '%eazl%'
