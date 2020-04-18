import os
import pandas as pd
import shutil
from olistlib.db import utils
import argparse

import datetime
from dateutil.relativedelta import relativedelta
from sklearn import tree

parser = argparse.ArgumentParser()
parser.add_argument( '--date', '-d', help='Data referencia para inicio da ABT')
parser.add_argument( '--export', '-e', help='Tipo de exportação', choices=[ 'csv', 'sqlite'] )
args = parser.parse_args()

PREDICT_DIR = os.path.dirname( os.path.abspath( __file__ ) )
SRC_DIR   = os.path.dirname( PREDICT_DIR )

TRAIN_DIR = os.path.join( SRC_DIR, 'train' )

BASE_DIR  = os.path.dirname( SRC_DIR )
DATA_DIR  = os.path.join( BASE_DIR, 'data')
MODELS_DIR  = os.path.join( BASE_DIR, 'models')

OUT_BASE_DIR = os.path.dirname( os.path.dirname( BASE_DIR ) )
OUT_DATA_DIR = os.path.join( OUT_BASE_DIR, 'upload_olist-master', 'data' )
DB_PATH = os.path.join( OUT_DATA_DIR, 'olist.db')

shutil.copyfile( os.path.join( TRAIN_DIR, 'etl.sql' ), os.path.join( PREDICT_DIR, 'etl.sql' ) )
query = utils.import_query( os.path.join( PREDICT_DIR, 'etl.sql' ) )

print('\nImportando modelo...')
model = pd.read_pickle( os.path.join( MODELS_DIR, 'models.pkl' ) )
print('Pronto.')

print('\nAbrindo conexão...')
conn = utils.connect_db( 'sqlite', path=DB_PATH )
print('Pronto.')

print('\nFazendo ETL...')
query = query.format( date=args.date,
                      stage='PREDICT' )
utils.execute_many_sql( query, conn )
df = pd.read_sql_table( 'PRE_ABT_PREDICT_CHURN', conn )
print('Pronto.')

print('\nRealizando predições...')
df['churn_prob'] = model['models'].predict_proba( df[ model['features'] ] )[:,1]
print('Pronto.')

print('\nSalvando base escora...')
table = df[['churn_prob','seller_id']]
if args.export == 'sqlite':
    table.to_sql( 'tb_churn_score', conn)

elif args.export == 'csv':
    table.to_csv( os.path.join( DATA_DIR, 'tb_churn_score.csv' ), index=False)
print('Pronto\n')
