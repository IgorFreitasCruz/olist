
/* Criação de tabela com a informação nivel usuário para qtde de dias para revenda */
DROP TABLE IF EXISTS tb_category_day_b_day;
CREATE TABLE tb_category_day_b_day AS

        SELECT T1.days,
        T1.category,
                COUNT( DISTINCT T2.seller_id ) AS qtd_sellers

        FROM tb_days_between AS T1

        LEFT JOIN (
                SELECT * 

                FROM (
                        SELECT *,
                                julianday(DATE(order_approved_at)) - julianday(DATE(last_sale)) AS qtd_dias,
                                ROW_NUMBER() OVER ( PARTITION BY seller_id,product_category_name  ORDER BY RANDOM() ) AS RANDOM
                        FROM (

                        SELECT T2.seller_id,
                                T3.product_category_name,
                                T1.order_approved_at,
                                LAG( T1.order_approved_at ) OVER ( PARTITION BY T2.seller_id, T3.product_category_name ORDER BY T1.order_approved_at) AS last_sale

                        FROM tb_orders AS T1

                        LEFT JOIN tb_order_items as T2
                        ON T1.order_id = T2.order_id

                        LEFT JOIN tb_products AS T3
                        ON T2.product_id = T3.product_id

                        WHERE T2.seller_id IS NOT NULL
                        AND T3.product_category_name IS NOT NULL
                        AND T1.order_approved_at >= '{date_init}' AND T1.order_approved_at <= '{date_end}' 

                        ORDER BY T2.seller_id, T1.order_approved_at

                        ) AS T1

                        WHERE T1.last_sale IS NOT NULL
                        AND julianday(DATE(order_approved_at)) - julianday(DATE(last_sale)) >= 1

                )
                WHERE RANDOM = 1 OR RANDOM IS NULL
        ) AS T2

        ON T1.category = T2.product_category_name
        AND T1.days = T2.qtd_dias


        GROUP BY T1.category, T1.days
        ORDER BY T1.category, T1.days
;

/* Ajuste do modelo propriamente dito com a porcentagem acumulada */
DROP TABLE IF EXISTS tb_model_lifetime;
CREATE TABLE tb_model_lifetime AS
    SELECT T1.category,
            T1.days,
            T1.qtde_acum / T2.total_sellers as pct_acum

    FROM (
        SELECT T1.category,
                T1.days,
                T1.qtd_sellers,
                SUM( CAST(T2.qtd_sellers AS FLOAT) ) as qtde_acum

        FROM tb_category_day_b_day AS T1

        INNER JOIN tb_category_day_b_day AS T2
        ON T1.category = T2.category AND T1.days >= T2.days

        GROUP BY T1.category, T1.days, T1.qtd_sellers
    ) AS T1

    LEFT JOIN (
        SELECT category,
                SUM( qtd_sellers ) AS total_sellers

        FROM tb_category_day_b_day
        GROUP BY category
    ) AS T2
    ON T1.category = T2.category

;

/* Dropa tabela descenecessária */
DROP TABLE IF EXISTS tb_category_day_b_day;
