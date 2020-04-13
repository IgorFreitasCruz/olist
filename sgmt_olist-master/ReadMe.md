## Olist - Segementos

projeto para realizar segmentação da base de clientes (sellers) da empresa Olist.
As segmentações são geradas a partir de regras de negócio (percentís) de frequência e valor, e recência.

## Clonar

```bash
git clone https://github.com/TeoCalvo/sgmt_olist.git
```

## Uso

Para executar a segmentação para uma base ativa específica basta invocar o scrip make_sgmt.py.
Segue exemplo para a base ativa do dia "2018-06-01"

```bash
python sgmt_olist/src/data_prep/make_sgmt.py --date_end "2018-06-01"
```

Para execução de uma "filme", considerando várias bases ativas de meses diferentes, considere data e inicio e data de término:

```bash
python sgmt_olist/src/data_prep/make_movie.py --first_pic "2017-06-01" --last_pic "2018-06-01"
```

## Tabela com segmentos
A tabela que deve ser consultada que contêm os seguementos é : tb_seller_sgmt