SELECT '{date}' as dt_referencia,
        T1.*,
        COALESCE( T2.qtde_venda, 0 ) as qtde_venda_futura,
        CASE WHEN COALESCE( T2.qtde_venda, 0) = 0 THEN 1 ELSE 0 END as flag_churn

FROM PRE_ABT_TRAIN_CHURN as T1

-- CRIANDO A VARIÁVEL RESPOSTA
LEFT JOIN (
        SELECT t2.seller_id,
                COUNT( DISTINCT t1.order_id ) as qtde_venda
                
        FROM tb_orders as t1

        LEFT JOIN tb_order_items as t2
        ON t1.order_id = t2.order_id

        WHERE t1.order_purchase_timestamp >= '{date}' 
        AND t1.order_purchase_timestamp < date( '{date}', '+3 month' )

        GROUP BY t2.seller_id
) as T2
ON T1.seller_id = T2.seller_id