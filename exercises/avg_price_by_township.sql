-- themes: group_by count cast having
-- tables: nord_pdc_apartments
-- subject: Display, for each Commune, (in this order) all Communes, average apartment price (named vf), how many lines the average has (named nb_lines), each time the vf <= 250000 and nb_lines >= 10.

SELECT
    Commune,
    CAST(MEAN(valeur_fonciere) AS INTEGER) AS vf,
    COUNT(*) AS nb_lines
FROM
    nord_pdc_apartments
GROUP BY
    Commune
HAVING
    nb_lines >= 10
    AND
    vf <= 250000
ORDER BY
    Commune
