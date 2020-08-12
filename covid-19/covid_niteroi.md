***
# Covid-19 em Niterói (RJ)
***

O código a seguir foi desenvolvido para fazer uma análise dos dados sobre a Covid-19 em Niterói, disponibilizados pela Prefeitura diariamente em sua página no [Twitter](https://twitter.com/saudeniteroi?s=20). 
Para isso, todos os dados foram pegos da página da Secretaria de Saúde do município e colocados no arquivo `Dados_Covid_Niteroi.csv`, também disponível nesse repositório.
O único trabalho aqui é atualizar esse arquivo .csv diariamente, a partir dos dados divulgados pela prefeitura.

## Primeiro passo: chamando os pacotes

Vamos utilizar nesse código 4 pacotes:

* **Pandas**, um pacote para lidar com estrutura de dados em tabelas;
* **Numpy**, um pacote para operações matemáticas;
* **Seaborn**, um pacote com vários códigos HTML para cores diversas;
* **Matplotlib.pyplot**, pacote mais utilizado para gerar gráficos;
* **Matplotlib.dates**, para formatação das datas nos gráficos.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
```

## Segundo passo: lendo o arquivo csv

A leitura do arquivo será feita pelo pacote **Pandas**, utilizando a função `read_csv`. Atente para o separador utilizado no arquivo .csv (`sep = ';'`), para o argumento `header = 0`, que diz que a primeira linha de cada coluna é o cabeçalho, 
e para os nomes das colunas dados. Caso você opte por usar outra base de dados (de outra cidade) ou atualizar o arquivo com mais colunas, deverá colocar mais uma entrada no vetor `names`.

```python
df = pd.read_csv("Dados_COVID_Niteroi.csv", sep = ';', header = 0,
                 names = ['Date', 'Total cases', 'New cases', 'Total deaths', 'New deaths'])
```
Vamos, agora, criar um vetor `dias` que receberá os dados da primeira coluna do `df` (dataframe), *convertendo-os* para o formato de data. Isso é importante pois não iremos conseguir manipular esses dados da maneira tradicional, 
uma vez que o Pandas lê naturalmente como números inteiros (*integers*). Para isso, usaremos o comando `pd.to_datetime`:

```python
dias = pd.to_datetime(df['Date'])
```
## Terceiro passo: cálculos

Agora é o momento de fazermos alguns cálculos. Vamos por partes:

* Cálculo da taxa de letalidade da Covid-19 em Niterói

Esse cálculo é feito através da razão entre o número total de mortes atribuídas à COVID-19 e o número total de infectados. Como nossa planilha de dados é atualizada diariamente com o número total de casos na cidade, então basta pegarmos 
o *último* dado da coluna `Total cases` e o último dado da coluna `Total deaths`. Acessamos o último dado (posição -1) da respectiva coluna do DataFrame `df` utilizando o comando `.iloc[-1]`. Multiplicamos o resultado por 100.0 para obtermos 
o valor em porcentagem:

```python
Letalidade = df['Total deaths'].iloc[-1] / df['Total cases'].iloc[-1] * 100.0
```
Caso você deseje rodar esse código em alguma IDLE do Python, como Spyder, a variável `Letalidade` será armazenada e você pode acessá-la sem a necessidade de imprimir seu valor.
No entanto, se você estiver rodando no terminal do Windows, caso queira visualizar o valor da letalidade, pode mandar imprimí-lo da seguinte maneira:

```python
print('A taxa de letalidade é: %0.2f' % Letalidade,'%')
```

* Cálculo da média móvel de novos casos e novas mortes (7 dias)

Esse cálculo é feito a partir da *média* dos novos casos dos últimos 7 dias. Ou seja, a partir do sétimo dia de casos registrados, teremos atualização nesses valores. Podemos fazer da seguinte maneira: vamos criar uma nova coluna ao nosso DataFrame (`df`),
e vamos chamá-la de `New cases_MA`. Essa coluna será criada quando mandamos o programa ir "rolando" (descendo) na coluna dos novos casos diários do nosso DataFrame (`New cases`) e calculando a média (`mean()`) dos sete valores anteriores. É de se esperar então que
as seis primeiras linhas dessa coluna não tenham valor algum (pois não há sete valores antes delas), sendo o primeiro valor calculado registrado na sétima linha apenas. Para fazer essa "descida" na coluna, usamos o comando `rolling(window = 7)`, onde window = 7 indica o número de valores que vamos pegar
para calcular a média. Podemos estender o raciocínio para as novas mortes diárias também. O comando fica:

```python
df['NewCases_MA'] = df['New cases'].rolling(window = 7).mean()
df['NewDeaths_MA'] = df['New deaths'].rolling(window = 7).mean()
```

## Quarto passo: plotando os gráficos

Vamos plotar alguns gráficos agora para melhor visualizar nossos dados. Para questões de melhor entendimento da situação atual da pandemia, é interessante plotar as curvas de *novos casos* e *novas mortes* diárias, para que seja possível analisar aspectos de estabilidade, crescimento ou redução dos valores.
A sequência de comandos a seguir é utilizada. Vamos explicar alguns comandos?

* `plt.bar` plota gráficos de **barras**, sendo o primeiro argumento o eixo X (`dias`) e o segundo o eixo Y (novos casos ou novas mortes);
* `label` dá um nome à curva que (ou barras) que você está plotando;
* `plt.plot` plota gráfico de **linhas**, usando a mesma ordem de argumentos do `plt.bar`;
* `cores` e `colors` serão vetores contendo código de cores importados de paletas de cores próprias do Python;
* `lw` é a espessura da linha (line width);
* `plt.legend` é a legenda do gráfico, onde `loc = 'best'` manda o programa posicioná-la no melhor lugar no gráfico, `fontsize = 7` seta o tamanho da fonte para 7 e `frameon = False` tira a borda da caixa de texto;
* `ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))` formata as datas para o formato dia/mês;
* `plt.yscale` muda a escala do eixo Y (no nosso caso, para "log");
* `plt.ylabel` coloca um título para o eixo Y;
* `plt.xticks(rotation=70)` seta uma pequena rotação ao texto do eixo X, para "caber tudo";
* `plt.savefig('Niteroi_diario_MA.png', format = 'png', dpi = 300)` salva a figura gerada, com formato `png` e resolução `dpi = 300`.

```python
colors = sns.color_palette("pastel")
cores = cores = sns.color_palette("dark")

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.bar(dias, df['New cases'], label = 'Novos casos diários', color = colors[0])
plt.bar(dias, df['New deaths'], label = 'Novas mortes diárias', color = colors[1])
plt.plot(dias, df['NewCases_MA'], color = cores[0], lw = 2.0, label = 'Novos casos (média móvel)')
plt.plot(dias, df['NewDeaths_MA'], color = cores[1], lw = 2.0, label = 'Novas mortes (média móvel)')
plt.legend(loc = 'best', fontsize = 7, frameon = False)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
plt.ylabel('Número de casos', fontweight = 'bold')
plt.yscale("log")
plt.xticks(rotation=70)
plt.savefig('Niteroi_diario_MA.png', format = 'png', dpi = 300)
```

O resultado final deve ser algo mais ou menos assim:
![NiteroiCovid](
