SELECT T1.*,
        T2.pct_acum,
        '{date_end}' AS dt_score
FROM (

    SELECT t2.seller_id,
        t3.product_category_name,
        MAX(order_approved_at) AS last_sale,
        MIN( CAST( julianday( '{date_end}' ) -julianday( DATE(t1.order_approved_at) ) AS INT) ) as days

    FROM tb_orders as t1

    LEFT JOIN tb_order_items as t2
    ON T1.order_id = T2.order_id

    LEFT JOIN tb_products as t3
    ON t2.product_id = t3.product_id

    WHERE t1.order_approved_at >= '{date_init}'
    AND t1.order_approved_at < '{date_end}'
    AND t3.product_category_name IS NOT NULL

    GROUP BY t2.seller_id, t3.product_category_name

    ORDER BY t2.seller_id, t1.order_approved_at
) AS T1

LEFT JOIN tb_model_lifetime AS T2
ON T1.product_category_name = T2.category AND T1.days = T2.days

ORDER BY T1.product_category_name, T2.pct_acum