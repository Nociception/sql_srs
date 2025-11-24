-- themes: full_join
-- tables: customers products store_products stores
-- subject: Display all the columns of all the tables in one, starting from customers, ordered by customer_id.

SELECT
    *
FROM
    customers
FULL JOIN
    stores USING (customer_id)
FULL JOIN
    store_products USING (store_id)
FULL JOIN
    products USING(product_id)
ORDER BY
    customer_id
