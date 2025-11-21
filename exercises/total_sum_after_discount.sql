-- themes: count case_when
-- tables: orders
-- subject: Calculate the total orders amount after applying discount.

SELECT
	SUM (
		CASE
			WHEN discount_code LIKE '%10%' THEN price_per_unit * 0.9 * quantity
			WHEN discount_code LIKE '%20%' THEN price_per_unit * 0.8 * quantity
			ELSE price_per_unit * 1.0 * quantity
		END
	) AS sum_after_discount
FROM orders