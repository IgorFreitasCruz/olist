import os
import pandas as pd
from olistlib.db import utils
import argparse
import datetime
import dateutils

parser = argparse.ArgumentParser()
parser.add_argument("--date_end", help='Data de fim para contabilizar as compras no modelo', default="2018-07-01")
parser.add_argument("--delta", help='Quantos meses deve ser considerado na análise', default=12, type=int)
parser.add_argument("--backup", '-b', help='Deseja salvar um backup do score', action='store_true')
args = parser.parse_args()

# Folders do projeto
PREDICT_DIR = os.path.dirname( os.path.abspath(__file__) )
DATA_PREP_DIR = os.path.dirname( PREDICT_DIR )
SRC_DIR = os.path.dirname( DATA_PREP_DIR )
BASE_DIR = os.path.dirname( SRC_DIR )
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join( os.path.dirname( BASE_DIR ), 'upload_olist', 'data', 'olist.db' )

# Buscando data de incio da extração
date_init = datetime.datetime.strptime(args.date_end, "%Y-%m-%d") - dateutils.relativedelta(months=args.delta)
date_init = date_init.strftime( "%Y-%m-%d" )

# Abrindo conexão com o banco
con  = utils.connect_db('sqlite', path=DB_PATH)

# Importando query
query = utils.import_query( os.path.join(PREDICT_DIR, 'make_score.sql' ) )
query = query.format( date_init=date_init, date_end=args.date_end )

try:
    print("\n\n Criando tabela...")
    create = utils.import_query( os.path.join( PREDICT_DIR, 'create.sql' ) )
    create = create.format( query=query )
    utils.execute_many_sql( create, con, verbose=True )
    print(" Ok.")
except:
    print("\n\n Inserindo dados na tabela...")    
    insert = utils.import_query( os.path.join( PREDICT_DIR, 'insert.sql' ) )
    insert = insert.format( query=query, date=args.date_end )
    utils.execute_many_sql( insert, con, verbose=True )
    print(" Ok.")