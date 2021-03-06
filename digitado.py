!pip install -q streamlit
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


from sklearn.datasets import load_boston
boston = load_boston

data['MEDV'] = boston().target

!pip install https://github.com/pandas-profiling/pandas-profiling/archive/master.zip

from pandas_profiling import ProfileReport
profile = ProfileReport(data, title='Relatório - Pandas Profiling - Marcílio', html={'style':{'full_width':True}})

profile.to_file(output_file="RelatorioMarcilio01.html")

correlacoes = data.corr()

plt.figure(figsize=(16, 6))
sns.heatmap(data=correlacoes, annot=True)

!pip install pyyaml==5.4.1

import plotly.express as px

fig = px.scatter(data, x=data.RM, y=data.MEDV)
fig.show()

fig = px.scatter(data, x=data.LSTAT, y=data.MEDV)
fig.show()

fig = px.scatter(data, x=data.PTRATIO, y=data.MEDV)
fig.show()

import plotly.figure_factory as ff
labels = ['Distribuição da variável RM (número de quartos)']
fig = ff.create_distplot([data.RM], labels, bin_size=.2)
fig.show()

import plotly.express as px
fig = px.box(data, y='RM')
fig.update_layout(width=800, height=800)
fig.show()

import plotly.figure_factory as ff
labels = ['Distribuição da variável MEDV (Preço médio do imóvel)']
fig = ff.create_distplot([data.MEDV], labels, bin_size=.2)
fig.show()

from scipy import stats

stats.skew(data.MEDV)

fig = px.histogram(data, x="MEDV", nbins=50, opacity=0.50)
fig.show()

data.RM = data.RM.astype(int)
data.info()

categorias = []

for i in data.RM.iteritems():
  valor = (i[1])
  if valor <= 4:
    categorias.append('Pequeno')
  elif valor < 7:
    categorias.append('Médio')
  else:
    categorias.append('Grande')

data['categorias'] = categorias

data.categorias.value_counts()

medias_categorias = data.groupby(by='categorias')['MEDV'].mean()

medias_categorias

dic_baseline = {"Grande": medias_categorias[0], "Medio": medias_categorias[1], "Pequeno": medias_categorias[2]}

dic_baseline

def retorna_baseline(n_quartos):
  if n_quartos <= 4:
    return dic_baseline.get('Pequeno')
  elif n_quartos < 7:
    return dic_baseline.get('Medio')
  else:
    return dic_baseline.get('Medio')

retorna_baseline(3)

for i in data.RM.iteritems():
  n_quartos = i[1]
  print('Número de quartos é: {} , Valor médio: {}'.format(n_quartos, retorna_baseline(n_quartos)))

x = data.drop(['RAD', 'TAX', 'MEDV', 'DIS', 'AGE', 'ZN', 'categorias'], axis=1)
y = data['MEDV']

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=5)

predicoes = []
predicoes[:10]

df_results=pd.DataFrame()

df_results['valor_real']=y_test.values

df_results['valor_predito_baseline']=predicoes

#imprimindo as 10 primeiras linhas do df_results
df_results.head(10)

import plotly.graph_objects as go
#Create traces
fig=go.Figure()
#Linha com os dados de teste
fig.add_trace(go.Scatter(x=df_results.index,
                         y=df_results.valor_real,
                          mode="lines+markers",
                         name="Valor Real"))
#Linha com os dados preditos
fig.add_trace(go.Scatter(x=df_results.index,
                         y=df_results.valor_predito_baseline,
                          mode='lines+markers',
                          name='Valor Predito Baseline'))
#Plotaafigura
fig.show()



#calculaamétrica rmse
from sklearn.metrics import mean_squared_error
from math import sqrt

rmse=(np.sqrt(mean_squared_error(y_test,predicoes)))

#imprimeaperformance do modelo
print('Performance do modelo baseline:')
print('\nRMSEé:{}'.format(rmse))

**Machine Learning**

*Algoritmos:*
Regressão Linear;

Algoritmo supervisionado;

utiliza equação linear que usa os valores de entrada para predizer
as saídas.;

Trabalha apenas com dados numéricos.;

Os pesos são atualizados conforme a função que minimiza erros.



#carregaopacote LinearRegression
from sklearn.linear_model import LinearRegression

#criaoobjeto do tipo LinearRegression
lin_model=LinearRegression()

#treina o algoritmo de regressão linear
lin_model.fit(x_train,y_train)

#avaliação do modelo nos dados de teste
y_pred=lin_model.predict (x_test)

#calculaamétrica rmse
rmse = (np.sqrt(mean_squared_error(y_test,y_pred)))

#imprimeaperformance do modelo.
print('Performance do modelo avaliado com os dados de teste:')
print('\nRMSEé:{}'.format(rmse))

#atribui os resultados no dataframe df_results
df_results['valor_predito_reg_linear']=lin_model.predict(x_test)

import plotly.graph_objects as go
#Create traces
fig=go.Figure()
#Linha com os dados de teste
fig.add_trace(go.Scatter(x=df_results.index,
                          y=df_results.valor_real,
                         mode="lines+markers",
                         name='Valor Real'))
#Linha com os dados de baseline
fig.add_trace(go.Scatter(x=df_results.index,
                         y=df_results.valor_predito_baseline,
                         mode='lines+markers',
                         name='Baseline'))
#Linha com os dados preditos pela regressão linear
fig.add_trace(go.Scatter(x=df_results.index,
                          y=df_results.valor_predito_reg_linear,
                          mode='lines',
                          line=dict(color='#FEBFB3'),
                          name='Valor Predito Regressão Linear'))
#Plotaafigura
fig.show()

#importaopacote Decision TreeRegressor
from sklearn.tree import DecisionTreeRegressor

#cria um objeto do tipo DecisionTreeRegressor
regressor=DecisionTreeRegressor()

#treinaoalgoritmo
regressor.fit(x_train, y_train)

#fazendo as previsões
y_pred = regressor.predict(x_test)

#Adicionandoovalor do modelo no dataframe df_results
df_results['valor_predito_arvore'] = y_pred

#visualizaodataframe df_results
df_results.head(10)

import plotly.graph_objects as go
#cria uma figura
fig=go.Figure()
#Linha com os dados de teste
fig.add_trace(go.Scatter(x=df_results.index,
                          y=df_results.valor_real,
                         mode='lines+markers',
                         name='Valor Real'))
#Linha com os dados de teste
fig.add_trace(go.Scatter(x=df_results.index,
                           y=df_results.valor_predito_baseline,
                         mode='lines+markers',
                         name='Valor Predito Baseline'))
#Linha com os dados de teste
fig.add_trace(go.Scatter(x=df_results.index,
                         y=df_results.valor_predito_reg_linear,
                         mode='lines+markers',
                         name='Valor Predito Reg Liner'))
#Linha com os dados preditos
fig.add_trace(go.Scatter(x=df_results.index,
                         y=df_results.valor_predito_arvore,
                         mode="lines+markers",
                         name='Valor Predito Arvore'))
#Plotaafigura
fig.show()

#calculaamétrica rmse
rmse=(np.sqrt(mean_squared_error(y_test,y_pred)))

#imprimeaperformance do modelo
print('Performance do modelo avaliado com os dados de teste:')
print('\nRMSEé:{}'.format(rmse))

#Importaométodo RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor

#criaoobjeto rf_regressor
rf_regressor=RandomForestRegressor()

#treinaoalgoritmo
rf_regressor.fit(x_train,y_train)

#avaliação do modelo nos dados de teste
y_pred=rf_regressor.predict(x_test)

#adiciona os resultados no dataframe df_results
df_results['valor_predito_random_forest']=rf_regressor.predict(x_test)

#calculaamétrica rmse
rmse=(np.sqrt(mean_squared_error(y_test,y_pred)))

#imprimeaperformance do modelo
print('Performance do modelo avaliado com os dados de teste:')
print('\nRMSEé:{}'.format(rmse))

#adiciona os resultados no dataframe df_results
df_results['valor_predito_random_forest']=rf_regressor.predict(x_test)

#calculaamétrica rmse
rmse=(np.sqrt(mean_squared_error(y_test,y_pred)))

#imprimeaperformance do modelo
print('Performance do modelo avaliado com os dados de teste:')
print('\nRMSEé:{}'.format(rmse))

#visualizaodataframe df_results
df_results.head(10)

x['MEDV']=y

x.head
