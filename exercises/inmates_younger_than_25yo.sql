-- themes: where
-- tables: executions
-- subject: Display, (in this order) first_name, last_name and ex_age from all executed inmates aged 25 or less. Sort the lines according the last_name alphabetical order.

SELECT
	first_name,
	last_name,
	ex_age
FROM
	executions
WHERE
	ex_age <= 25
ORDER BY
	last_name
