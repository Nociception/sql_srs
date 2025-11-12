-- themes: count
-- tables: executions
-- subject: Find how many executions the dataset contains. Rely on this hypothesis : for an execution, there is at least one column not null.

SELECT
	COUNT(*)
FROM
	executions
