-- themes: cross_join
-- tables: beverages food_items
-- subject: Give all possible lines combinations between beverages and food_items tables.

SELECT
    *
FROM
    beverages
CROSS JOIN
    food_items
