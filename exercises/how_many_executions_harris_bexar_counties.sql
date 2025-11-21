-- themes: count sum case_when
-- tables: executions
-- subject: Display, in two columns: the number of executions in the counties of Harris and Bexar (in this order)
-- TODO: fix this exercise with future features (text area filler)

SELECT
    SUM(
		CASE
			WHEN county='Harris' THEN 1
        	ELSE 0 
		END
	),
    SUM(
		CASE
			WHEN county='Bexar' THEN 1
        	ELSE 0
		END
	)
FROM executions