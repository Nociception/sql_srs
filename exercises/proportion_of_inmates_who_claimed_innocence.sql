-- themes: sum case_when decimal_division proportion
-- tables: executions
-- subject: Find the proportion of inmates with claims of innocence in their last statements.

SELECT
	(
	  1.0
	  *
	  SUM(
		CASE
			WHEN last_statement LIKE '%innocent%' THEN 1
			ELSE 0
		END
	  )
	)
	/
	COUNT(
	  *
	)
	AS
		proportion_of_inmates_who_claim_innocence
FROM
	executions