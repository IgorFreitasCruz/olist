DELETE FROM tb_score_lifetime
WHERE dt_score = '{date}';

INSERT INTO tb_score_lifetime
{query} ;