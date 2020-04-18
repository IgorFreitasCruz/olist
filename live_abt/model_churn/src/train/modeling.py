import os
import pandas as pd
from olistlib.db import utils
import argparse
import datetime
from dateutil.relativedelta import relativedelta
from sklearn import tree

parser = argparse.ArgumentParser()
parser.add_argument( '--date_init', '-i', help='Data referencia para inicio da ABT')
parser.add_argument( '--date_end', '-e', help='Data referencia para término da ABT')
parser.add_argument( '--file_type', '-d', help='De onde deseja importar esse arquivo?', choices=['csv','sqlite'] )
args = parser.parse_args()

TRAIN_DIR = os.path.dirname( os.path.abspath( __file__ ) )
SRC_DIR   = os.path.dirname( TRAIN_DIR )
BASE_DIR  = os.path.dirname( SRC_DIR )
DATA_DIR  = os.path.join( BASE_DIR, 'data')
MODELS_DIR  = os.path.join( BASE_DIR, 'models')

OUT_BASE_DIR = os.path.dirname( os.path.dirname( BASE_DIR ) )
OUT_DATA_DIR = os.path.join( OUT_BASE_DIR, 'upload_olist-master', 'data' )
DB_PATH = os.path.join( OUT_DATA_DIR, 'olist.db')

# Abrindo concexão com o banco de dados...
print('\nAbrindo conexão com banco de dados...')
conn = utils.connect_db( 'sqlite', path=DB_PATH )
print('Pronto.\n')

print('Extraindo a base de dados...')
if args.file_type == 'csv':
    table_name = 'tb_abt_{date_init}_{date_end}.csv'.format( date_init=args.date_init.replace( '-','' ),
                                                             date_end=args.date_end.replace( '-','' ) )
    df = pd.read_csv( os.path.join( DATA_DIR, table_name ) ) 

elif args.file_type == 'sqlite':
    conn = utils.connect_db( 'sqlite', path=DB_PATH )
    table_name = 'tb_abt_{date_init}_{date_end}'.format( date_init=args.date_init.replace( '-','' ),
                                                         date_end=args.date_end.replace( '-','' ) )
    df = pd.read_sql_table( table_name, conn ) 
print('Pronto.\n')

print('Ajustando modelo...')
features = df.columns[3:-2]
target = 'flag_churn'

X = df[features]
y = df[target] 

clf = tree.DecisionTreeClassifier(max_depth=8)
clf.fit( X,y )
print('Pronto.\n')

print('Salvando o modelo...')
model = pd.Series( [features, clf ], index=['features','models'] )
model.to_pickle( os.path.join( MODELS_DIR, 'models.pkl' ) )
print('Pronto.\n')