-- themes: where_clause
-- tables: executions
-- subject: Display first_name, last_name and ex_date from all executed inmates aged 25 or less.

SELECT
	first_name,
	last_name,
	ex_age
FROM
	executions
WHERE
	ex_age <= 25
