# Olist - Upload Data

Projeto para fazer upload dos arquivo csv para um banco de dados relacional.
Primeiro é necessário baixar os arquivos do Kaggle: https://www.kaggle.com/olistbr/brazilian-ecommerce

Também é necessário extrair os documentos do arquivo .zip

## Clonar
Para clonar o repositório basta seguir o comando:

```bash
git clone https://github.com/TeoCalvo/upload_olist.git
```

## Uso

```bash
python upload_data/src/upload_data.py
```

Após o comando acima, seus dados estarão contidos no banco de dados SQLite, encontrado em upload_data/data/olist.db