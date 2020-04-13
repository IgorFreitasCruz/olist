# Olist - Tempo para revenda (nível categoria)

Projeto para prever tempo até a próxima revenda em nível de categoria para os sellers.

### Objetivo

Uma das principais aplciações deste tipo de modelo é detectar o melhor momento para realizar comunicações direcionadas (campanhas de CRM) em nível do indivíduo.

## Clonar

```bash
git clone https://github.com/TeoCalvo/lifetime_olist.git
```

## Uso

### Ajuste do modelo

Para ajustar o modelo, é necessário invocar o script de ajuste, passando os argumentos de data final de transações e janela de tempo (em meses) desejada para observar os tempos de revenda.

```bash
python lifetime_olist/src/data_prep/train/lifetime.py --date_end "2018-06-07" --delta 24
```

O resultado do ajuste (modelo propriamente dito) se encontra em uma tabela no banco de dados: tb_model_lifetime

### Escorando base

Para realizar o escore dos indivíduos (sellers) é necessário executar o script de escore, passando a última data de transação e a janela de tempo (em meses) para serem consideradas:

```bash
python lifetime_olist/src/data_prep/predict/make_score.py --date_end "2018-06-07" --delta 24
```

O resultado da escoragem é salvo na tabela 'tb_score_lifetime', contendo todos os indivíduos escorado e a data referente ao escore.