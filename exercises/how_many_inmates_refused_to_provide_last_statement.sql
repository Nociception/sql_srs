-- themes: count sum case_when where
-- tables: executions
-- subject: Display the number of inmates who refused to give any last_statement. Get the same result with 4 different ways: with a WHERE, a COUNT, a SUM, two COUNT
-- TODO: fix this exercise with future features (text area filler)

SELECT
	COUNT(*)
FROM
	executions
WHERE
	last_statement IS null