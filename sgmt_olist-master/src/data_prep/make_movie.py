import os
import sys
import subprocess
import datetime
import dateutils
import argparse

DATA_PREP_DIR =os.path.dirname( os.path.abspath(__file__) )
script_path = os.path.join( DATA_PREP_DIR, 'make_sgmt.py')

parser = argparse.ArgumentParser()
parser.add_argument("--first_pic", '-f', help="Data da primeira foto a ser tirada", default='2017-06-01')
parser.add_argument("--last_pic", '-l', help="Data da última foto a ser tirada", default='2018-06-01')
args = parser.parse_args()

actual_date = datetime.datetime.strptime( args.first_pic, "%Y-%m-%d" )
last_date = datetime.datetime.strptime( args.last_pic, "%Y-%m-%d" )

call = 'python {path} -e {date}'

print("\n\n Processando...\n")
while actual_date <= last_date:
    str_date = actual_date.strftime( "%Y-%m-%d" )
    str_call = call.format( path=script_path, date=str_date ).split(" ")

    print( actual_date )
    subprocess.call( str_call )
    actual_date = actual_date + dateutils.relativedelta(months=1)
    print("\n")

print("\n Ok.")