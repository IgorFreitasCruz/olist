DROP TABLE IF EXISTS PRE_ABT_{stage}_CHURN;
CREATE TABLE PRE_ABT_{stage}_CHURN as

        SELECT t1.seller_id,
                MAX( t1.dt_venda ) as dt_ultima_venda,

                /* Totais */
                SUM( ROUND( t1.price ) ) as receita_total,
                COUNT( DISTINCT t1.order_id) as qtde_venda,
                COUNT( t1.product_id ) as qtde_itens_total,
                COUNT( DISTINCT t1.product_id ) as qtde_itens_distintos_total,
                SUM( t1.freight_value ) as frete_total,

                /* Medias por pedido (venda) */
                ROUND( SUM( t1.price ) / COUNT( DISTINCT t1.order_id) ) as receita_por_venda,
                COUNT( t1.product_id ) / COUNT( DISTINCT t1.order_id) as qtde_itens_por_venda,
                ROUND( SUM( t1.freight_value ) / COUNT( DISTINCT t1.order_id) ) as frete_por_venda,
                SUM( t1.freight_value ) / COUNT( t1.product_id ) as frete_por_item,

                ROUND( COUNT( DISTINCT strftime( '%m', dt_venda) ) / 6., 2 ) as proporcao_ativacao


                
        FROM (
                SELECT t1.order_id, 
                        t1.order_purchase_timestamp as dt_venda,
                        CASE WHEN t1.order_delivered_customer_date > t1.order_estimated_delivery_date THEN 1 ELSE 0 END as FLAG_ATRASO,
                        T2.product_id,
                        t2.seller_id,
                        t2.price,
                        t2.freight_value,
                        t3.seller_state,
                        t4.product_category_name

                FROM tb_orders as t1 -- Table de pedidos 

                LEFT JOIN tb_order_items as t2 -- Tabela de pedidos/items
                ON t1.order_id = t2.order_id

                LEFT JOIN tb_sellers as t3 -- Tabela de vendedores
                ON t2.seller_id = t3.seller_id

                LEFT JOIN tb_products as t4 -- Tabela de produtos
                ON t2.product_id = t4.product_id

                WHERE t1.order_purchase_timestamp < '{date}' 
                AND t1.order_purchase_timestamp >= date( '{date}', '-6 month' ) 
                AND t1.order_status = 'delivered'
        ) as t1

        GROUP BY T1.seller_id

        HAVING MAX( t1.dt_venda ) >= date( '{date}', '-3 month' ) 
;

