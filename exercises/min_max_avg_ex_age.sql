-- themes: min max avg agregate_functions
-- tables: executions
-- subject: Display the minimum, maximum and average age of inmates at the time of execution.

SELECT
	MIN(ex_age),
	MAX(ex_age),
	AVG(ex_age)
FROM
	executions
