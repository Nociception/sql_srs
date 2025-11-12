-- themes: group_by count
-- tables: executions
-- subject: In each county, display how many inmates provided a last_statement, and how many did not.

SELECT
  last_statement IS NOT null AS has_last_statement,
  county,
  COUNT(*)
FROM
	executions
GROUP BY
	county,
	has_last_statement
