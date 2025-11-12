-- themes: count group_by
-- tables: executions
-- subject: Display how many executions happend in each county

SELECT
  county,
  COUNT(*) AS county_executions
FROM
    executions
GROUP BY
    county
