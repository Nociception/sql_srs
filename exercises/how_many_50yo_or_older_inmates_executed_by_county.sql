-- themes: count where group_by
-- tables: executions
-- subject: In each county, display how many inmates aged 50 years old (or older) were executed.

SELECT
	county,
	COUNT(*)
FROM
	executions
WHERE
	ex_age >= 50
GROUP BY
	county
