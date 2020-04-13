import os
import pandas as pd
import sqlalchemy
import argparse

from olistlib.db import utils

parser = argparse.ArgumentParser()
parser.add_argument("--database", help='Nome do bando de dados', choices=['sqlite', 'sql'], default='sqlite')
args = parser.parse_args()

# Os endereços de nosso projeto e sub pastas
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
DATA_DIR = os.path.join( BASE_DIR, 'data' )

# Encontrando os arquivos de dados
files_names = [ i for i in os.listdir( DATA_DIR ) if i.endswith('.csv') ]

# Abrindo conexão com banco...
connection = utils.connect_db(args.database, os.path.join( BASE_DIR, '.env' ), path=os.path.join(DATA_DIR, 'olist.db') )

# Para cada arquivo é realizado uma inserção no banco
for i in files_names:
    print(i)
    df_tmp = pd.read_csv( os.path.join( DATA_DIR, i )  )
    table_name = "tb_" + i.strip(".csv").replace("olist_", "").replace("_dataset", "")
    if args.database == 'sqlite':
        df_tmp.to_sql( table_name,
                        connection,
                        if_exists='replace',
                        index=False )
    
    elif args.database == 'sql':
        df_tmp.to_sql( table_name,
                        connection,
                        schema='olist',
                        if_exists='replace',
                        index=False )