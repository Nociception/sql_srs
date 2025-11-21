-- themes: count group_by order_by
-- tables: executions
-- subject: Display each county (alphabetically ordered) with its total executions amount.

SELECT
  county,
  COUNT(*) AS county_executions
FROM
  executions
GROUP BY
  county
ORDER BY
  county
