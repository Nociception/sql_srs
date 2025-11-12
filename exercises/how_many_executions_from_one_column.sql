-- themes: count
-- tables: executions
-- subject: Find how many executions the dataset contains. Rely on one column you are confident it does not contain any null.

SELECT
	COUNT(ex_number)
FROM
	executions
