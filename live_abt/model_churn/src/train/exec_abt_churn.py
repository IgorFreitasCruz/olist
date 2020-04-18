import pandas as pd
from olistlib.db import utils
from sklearn import tree
from sklearn import metrics

# Importando a query
query_path = '/Users/igorfreitascruz/Documents/Ciência de dados/olist_project/live_abt/prepara_abt/query.sql'
query = utils.import_query( query_path )

datas = ['2017-01-01',
         '2017-02-01',
         '2017-03-01',
         '2017-04-01',
         '2017-05-01',
         '2017-06-01',
         '2017-07-01',
         '2017-08-01',
         '2017-09-01', 
]

conn = utils.connect_db('sqlite', path = '/Users/igorfreitascruz/Documents/Ciência de dados/olist_project/upload_olist-master/data/olist.db')
dfs = []
for data in datas:
    query_formatada = query.format( date = data )
    df_tmp = pd.read_sql_query( query_formatada, conn )
    dfs.append( df_tmp )

abt = pd.concat( dfs, axis = 0, ignore_index = True )
abt['flag_churn'].mean()

# Definição das variáveis 
target = 'flag_churn'
features = abt.columns[3:-2]

# Definição do classificador e seu ajuste
clf = tree.DecisionTreeClassifier( max_depth=10 )
clf.fit( abt[features], abt[target] )

y_pred = clf.predict( abt[features] )
y_prob = clf.predict_proba( abt[features] )

acc = metrics.accuracy_score( abt[target], y_pred )
auc = metrics.roc_auc_score( abt[target], y_prob[:,1] )

features_importance = pd.Series( clf.feature_importances_, index = features )
features_importance.sort_values( inplace=True ) 
