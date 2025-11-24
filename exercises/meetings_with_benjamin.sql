-- themes: alias self_join where order_by
-- tables: meetings
-- subject: Display all the lines concerning meetings where Benjamin was, but not the lines where his name appears. Columns are shown in this order: meeting_id, colleague, duration_minutes. Order: duration_minutes (greatest to lowest), meeting_id, colleague.

SELECT
    l.meeting_id,
    r.person_name AS colleague,
    l.duration_minutes
FROM
    meetings l
    INNER JOIN
        meetings r
        ON l.meeting_id = r.meeting_id
WHERE
    l.person_name = 'Benjamin'
    AND
    r.person_name != 'Benjamin'
ORDER BY
    l.duration_minutes DESC,
    l.meeting_id,
    colleague
