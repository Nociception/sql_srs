-- themes: alias self_join where group_by order_by cte
-- tables: meetings
-- subject: For each colleague, diplay the average meeting where Benjamin is; order by meeting_duration (from greatest to lowest), colleague.

WITH benjamin_meetings AS (
    SELECT
        l.meeting_id,
        r.person_name AS colleague,
        l.duration_minutes
    FROM
        meetings AS l
        INNER JOIN meetings AS r ON l.meeting_id = r.meeting_id
    WHERE
        l.person_name = 'Benjamin'
        AND
        r.person_name != 'Benjamin'
)

SELECT
    bm.colleague,
    AVG(bm.duration_minutes) AS avg_meeting_duration
FROM
    benjamin_meetings AS bm
GROUP BY
    bm.colleague
ORDER BY
    avg_meeting_duration DESC
