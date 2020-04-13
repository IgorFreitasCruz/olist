import os
import pandas as pd
from olistlib.db import utils
import argparse
import datetime
import dateutils

parser = argparse.ArgumentParser()
parser.add_argument("--date_end", help='Data de fim para contabilizar as compras no modelo', default="2018-06-01")
parser.add_argument("--delta", help='Quantos meses deve ser considerado na análise', default=18, type=int)
parser.add_argument("--backup", '-b', help='Deseja salvar um backup do modelo', action='store_true')
args = parser.parse_args()

# Folders do projeto
TRAIN_DIR = os.path.dirname( os.path.abspath(__file__) )
DATA_PREP_DIR = os.path.dirname( TRAIN_DIR )
SRC_DIR = os.path.dirname( DATA_PREP_DIR )
BASE_DIR = os.path.dirname( SRC_DIR )
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join( os.path.dirname( BASE_DIR ), 'upload_olist', 'data', 'olist.db' )

# Buscando data de incio da extração
date_init = datetime.datetime.strptime(args.date_end, "%Y-%m-%d") - dateutils.relativedelta(months=args.delta)
date_init = date_init.strftime( "%Y-%m-%d" )

# Abrindo conexão com o banco
con  = utils.connect_db('sqlite', path=DB_PATH) # Abre a conexao com o banco....

# Calculo da quantidade maxima de dias para revenda
days_between = datetime.datetime.strptime( args.date_end, "%Y-%m-%d" ) - datetime.datetime.strptime( date_init, "%Y-%m-%d" )
days_between = days_between.days

print("\n\n Criando tabela axuliar...")
# identificação de todas possíveis categorias
categories_query = utils.import_query( os.path.join(TRAIN_DIR, 'categories.sql') )
categories = pd.read_sql_query( categories_query, con )['categories'].tolist()

# criação de tabela com info de dia a dia por catetoria
df_days = pd.DataFrame()
for c in categories:
    df_tmp = pd.DataFrame( {"days": list(range(1, days_between+1)),
                            'category': [c] * days_between  } )
    df_days = df_days.append( df_tmp, ignore_index=True )
df_days.to_sql( 'tb_days_between', con, if_exists='replace', index=False )
print("Ok.")

# Query de modelagem
print("\n\n Executando o ETL...")
query = utils.import_query( os.path.join(TRAIN_DIR, 'lifetime.sql') ) # Importa a nossa query
query = query.format( date_init = date_init, date_end = args.date_end )
utils.execute_many_sql( query, con, verbose=True )
print("\n Ok.")

if args.backup:
    file_name = 'lifetime_{date_init}_{date_end}.csv'.format( date_init=date_init.replace("-",""),
                                                              date_end=args.date_end.replace("-","") )
    df = pd.read_sql_table( 'tb_model_lifetime', con ) # Executa a query dentro do banco
    df.to_csv( os.path.join(DATA_DIR, file_name), sep=",", index=False) # Salvando em um csv...