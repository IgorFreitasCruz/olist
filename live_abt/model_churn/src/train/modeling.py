import os
import pandas as pd
from olistlib.db import utils
import argparse
import datetime
from dateutil.relativedelta import relativedelta

parser = argparse.ArgumentParser()
parser.add_argument( '--date_init', '-i', help='Data referencia para inicio da ABT')
parser.add_argument( '--date_end', '-e', help='Data referencia para término da ABT')
parser.add_argument( '--file_type', '-d', help='De onde deseja importar esse arquivo?', choices=['csv','sqlite'] )
args = parser.parse_args()

TRAIN_DIR = os.path.dirname( os.path.abspath( __file__ ) )
SRC_DIR   = os.path.dirname( TRAIN_DIR )
BASE_DIR  = os.path.dirname( SRC_DIR )
DATA_DIR  = os.path.join( BASE_DIR, 'data')

OUT_BASE_DIR = os.path.dirname( os.path.dirname( BASE_DIR ) )
OUT_DATA_DIR = os.path.join( OUT_BASE_DIR, 'upload_olist-master', 'data' )
DB_PATH = os.path.join( OUT_DATA_DIR, 'olist.db')

# Abrindo concexão com o banco de dados...
print('\nAbrindo conexão com banco de dados...')
conn = utils.connect_db( 'sqlite', path=DB_PATH )
print('Pronto.\n')

if args.file_type == 'csv':
    table_name = 'tb_abt_{date_init}_{date_end}.csv'.format( date_init=args.date_init.replace( '-','' ),
                                                             date_end=args.date_end.replace( '-','' ) )
    df = pd.read_csv( os.path.join( DATA_DIR, table_name ) ) 

elif args.file_type == 'sqlite':
    conn = utils.connect_db( 'sqlite', path=DB_PATH )
    table_name = 'tb_abt_{date_init}_{date_end}'.format( date_init=args.date_init.replace( '-','' ),
                                                         date_end=args.date_end.replace( '-','' ) )
    df = pd.read_sql_table( table_name, conn ) 

print( df.head() ) 