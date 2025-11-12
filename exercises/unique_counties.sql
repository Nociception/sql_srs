-- themes: distinct
-- tables: executions
-- subject: List all the counties in the dataset without duplication.

SELECT
	DISTINCT county
FROM
	executions
