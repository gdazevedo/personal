# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 13:14:37 2020

@author: gdaze
"""

#---------------Importando pacotes----------------------------#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as ss
#-------------------------------------------------------------#

#-------------------------------------------------------------#
plt.style.use('seaborn-darkgrid') # pretty matplotlib plots
#-------------------------------------------------------------#

df = pd.read_csv("Dados_COVID_Niteroi.csv", sep = ';', header = 0,
                 names = ['Date', 'Total cases', 'New cases', 'Total deaths', 'New deaths']) #Ler o arquivo .CSV

dias = pd.to_datetime(df['Date']) #Isso é para converter a primeira coluna para o formato de DATAS.

#-------------Algumas contas importantes---------------------------#

Let = df['Total deaths'].iloc[-1] / df['Total cases'].iloc[-1] * 100.0 #Calcula a letalidade da doença na cidade (%);

Pop = 513584 #hab, população estimada de Niterói em 2020

NewCases_100k = df['New cases'].tail(7).sum() / (Pop / 10**5) #Novos casos para cada 100 mil hab (soma dos últimos 7 dias)
NewDeaths_100k = df['New deaths'].tail(7).sum() / (Pop / 10**5) #Novas mortes para cada 100 mil hab (soma dos últimos 7 dias)

#------------------Um pouco de estatística----------------------------#

abril = dias.loc[dias.dt.month == 4] #Pega o mês de abril.
maio = dias.loc[dias.dt.month == 5] #Pega o mês de maio.
junho = dias.loc[dias.dt.month == 6] #Pega o mês de junho

abril_totalcases = df.loc[dias.dt.month == 4, 'Total cases'] #Pega os novos casos do mês de Abril
maio_totalcases = df.loc[dias.dt.month == 5, 'Total cases'] #Pega os novos casos do mês de Maio
junho_totalcases = df.loc[dias.dt.month == 6, 'Total cases'] #Pega os novos casos do mês de Julho

#Conversão dos valores de data para float, importante para a regressão:
    
abril = np.array(abril, dtype = float)
#abril_totalcases = np.array(abril_totalcases, dtype = float)
maio = np.array(maio, dtype = float)
#maio_totalcases = np.array(maio_totalcases, dtype = float)
junho = np.array(junho, dtype = float)
#junho_totalcases = np.array(junho_totalcases, dtype = float)


#Agora, vamos fazer todas as regressões lineares.

slope, intercept, r_value, p_value, std_err = ss.linregress(abril, abril_totalcases) #Para dados de Abril;
slope_2, intercept_2, r_value_2, p_value_2, std_err_2 = ss.linregress(maio, maio_totalcases) #Para dados de Maio;
slope_3, intercept_3, r_value_3, p_value_3, std_err_3 = ss.linregress(junho, junho_totalcases) #Para dados de Junho;

#Construindo o modelo linear para cada mês

y_abril = slope*abril + intercept
y_maio = slope_2 * maio + intercept_2
y_junho = slope_3 * junho + intercept_3

#-----------------Plotando os dados-------------------------------#

# Números totais
plt.figure(0)
plt.plot(dias, df['Total cases'], label = 'Total de casos')
plt.plot(dias, df['Total deaths'], label = 'Total de mortes')
plt.yscale("log")
plt.legend(loc = 'best')
plt.ylabel('Número', fontweight = 'bold', fontsize = 12)
plt.fill_between(dias, 0.7*df['Total cases'], 1.3*df['Total cases'], alpha = 0.4)
plt.fill_between(dias, 0.7*df['Total deaths'], 1.3*df['Total deaths'], alpha = 0.4)
plt.show()

# Novos casos por mês - ajuste linear

plt.figure(1)
plt.plot(abril, abril_totalcases, 'o', markersize = 7, markeredgewidth = 1.5)
plt.plot(abril, y_abril, '--', linewidth = 1.5, label = 'Ajuste linear')
plt.legend(loc = 'best')
plt.title('Casos totais em Niterói' "\n" 'Abril de 2020')
plt.gca().axes.get_xaxis().set_ticklabels([])
plt.text(abril[0], abril_totalcases.iloc[-3], '$R^2$ =  %0.3f' % r_value, fontweight = 'bold')

plt.figure(2)
plt.plot(maio, maio_totalcases, 'o', markersize = 7, markeredgewidth = 1.5)
plt.plot(maio, y_maio, '--', linewidth = 1.5, label = 'Ajuste linear')
plt.legend(loc = 'best')
plt.title('Casos totais em Niterói' "\n" 'Maio de 2020')
plt.gca().axes.get_xaxis().set_ticklabels([])
plt.text(maio[0], maio_totalcases.iloc[-6], '$R^2$ =  %0.3f' % r_value_2, fontweight = 'bold')

plt.figure(3)
plt.plot(junho, junho_totalcases, 'o', markersize = 7, markeredgewidth = 1.5)
plt.plot(junho, y_junho, '--', linewidth = 1.5, label = 'Ajuste linear')
plt.legend(loc = 'best')
plt.title('Casos totais em Niterói' "\n" 'Junho de 2020')
plt.gca().axes.get_xaxis().set_ticklabels([])
plt.text(junho[0], junho_totalcases.iloc[-2], '$R^2$ =  %0.3f' % r_value_3, fontweight = 'bold')

# Números diários

plt.figure(4)
plt.bar(dias, df['New cases'], label = 'Novos casos diários')
plt.bar(dias, df['New deaths'], label = 'Novas mortes diárias')
plt.legend(loc = 'best')
plt.yscale("log")