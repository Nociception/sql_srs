-- themes: count
-- tables: executions
-- subject: Find how many executed inmates provide a last_statement (hint: when no last_statement was provided, value is null)

SELECT
	COUNT(last_statement)
FROM
	executions
