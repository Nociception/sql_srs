-- themes: group_by count
-- tables: nord_pdc_apartments
-- subject: Display how many apartment are within each Commune ("township" in french), ordered by Commune.

SELECT
    Commune,
    COUNT(*)
FROM
    nord_pdc_apartments
GROUP BY
    Commune
ORDER BY
    Commune
