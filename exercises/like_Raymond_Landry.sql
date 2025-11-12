-- themes: where like
-- tables: executions
-- subject: Display first_name, last_name and ex_number of Raymond Landry. Use LIKE clause to find him, as his name might have been written in a slightly different way. (The solution query is one possibility, not the only one.)

SELECT
	first_name,
	last_name,
	ex_number
FROM
	executions
WHERE
	first_name LIKE '%aym%'
    AND last_name LIKE '%andr%'
