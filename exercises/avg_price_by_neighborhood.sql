-- themes: coalesce group_by
-- tables: real_estate_price
-- subject: For each neighborhood (group all the null neighborhoods in a new one: "unknown"), display the real estate average price (named avg_price, ordered by this column).

SELECT
    COALESCE(neighborhood, 'unknown'),
    MEAN(price) AS avg_price
FROM
    real_estate_price
GROUP BY
    neighborhood
ORDER BY
    avg_price
