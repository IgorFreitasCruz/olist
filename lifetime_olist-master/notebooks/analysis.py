import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.abspath('.')
DATA_DIR = os.path.join( BASE_DIR, 'data' )

df = pd.read_csv( os.path.join( DATA_DIR, 'lifetimes.csv' ) )


cats = ['eletrodomesticos', 'eletrodomesticos_2', 'eletronicos','eletroportateis']

for c in cats:
    df_tmp = df[ df['product_category_name'] == c]
    plt.plot( df_tmp['qtd_dias'], df_tmp['PCT_ACUM'] )


plt.grid(True)
plt.title("Curva acumulada de sobre")
plt.xlabel("Dias para próxima venda")
plt.ylabel("Prob. Acum.")
plt.legend(cats)
plt.show()


df['pct_cum_round'] = df['PCT_ACUM'].round(1)
df[ df['pct_cum_round'] == 0.5 ]