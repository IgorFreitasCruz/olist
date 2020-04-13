import os
import sqlalchemy
import argparse
import pandas as pd
import datetime
import dateutils
from olistlib.db import utils

# Os endereços de nosso projeto e sub pastas
DATA_PREP_DIR = os.path.dirname( os.path.abspath(__file__) ) # Diretório de data prep
SRC_DIR = os.path.dirname( DATA_PREP_DIR ) # Diretório de código
BASE_DIR = os.path.dirname( SRC_DIR ) # Diretório raiz do projeto
DATA_DIR = os.path.join( BASE_DIR, 'data' ) # Diretório de dados
DB_PATH = os.path.join( os.path.dirname( BASE_DIR ), 'upload_olist', 'data', 'olist.db')

# Parser de data apra fazer a foto
parser = argparse.ArgumentParser()
parser.add_argument( '--date_end', '-e', help='Data de fim da extração', default='2018-06-01' )
parser.add_argument("--database", help='Nome do bando de dados', choices=['sqlite', 'sql'], default='sqlite')
args = parser.parse_args()

date_end = args.date_end
date_init = datetime.datetime.strptime( args.date_end, "%Y-%m-%d" ) - dateutils.relativedelta(years=1)
date_init = date_init.strftime( "%Y-%m-%d" )

# Importa a query
query = utils.import_query(os.path.join(DATA_PREP_DIR, 'segmentos.sql') )
query = query.format( date_init=date_init, date_end=date_end )

if args.database == 'sqlite':
    query = query.replace('olist.', '')
    table_name = 'tb_seller_sgmt'

elif args.database == 'sql':
    table_name = 'olist.tb_seller_sgmt'

# Abrindo conexão com banco...
conn = utils.connect_db(args.database, path=DB_PATH  )

try:
    create_query = f'''CREATE TABLE {table_name} AS\n{query};'''
    utils.execute_many_sql( create_query, conn )

except:
    insert_query = f'''DELETE FROM {table_name} WHERE DT_SGMT = '{date_end}';
    INSERT INTO {table_name} {query};'''
    utils.execute_many_sql( insert_query, conn, verbose=True)