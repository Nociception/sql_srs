-- themes: count where
-- tables: executions
-- subject: Display how many inmates were over the age of 50 at execution time.

SELECT
	COUNT(*)
FROM
	executions
WHERE
	ex_age > 50