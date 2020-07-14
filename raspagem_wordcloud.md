# Raspagem de tweets e word clouds

Esse tutorial tem por objetivo fazer o processo de raspagem de tweets e criar um word cloud com as palavras mais utilizadas. Como exemplo, vamos usar a minha conta pessoal (**@gdiasz**).

Agradecimento especial à [Judyte Prestes](https://github.com/juditecypreste/O_tutorial_mais_facil_do_mundo_para_raspar_tweets#twint-conhe%C3%A7a-seu-novo-amor) que disponibilizou o tutorial para a raspagem! :blush:

## Raspagem dos tweets ##

Neste tutorial nós vamos usar o Twint, uma ferramenta que não utiliza a API e não necessita que o usuário tenha conta no Twitter. Para conhecer mais, acesse o repositório [aqui](https://github.com/twintproject/twint/).

Vamo começar instalando o Twint. No prompt de comando, escreva o comando:

```
pip3 install twint
```

Agora, vamos buscar os tweets da minha conta. A sintaxe geral é muito simples, e no repositório da ferramenta existem outros comandos para aperfeiçoar o código para melhorar o processo de raspagem.

```
twint -u @username -o file.csv --csv -ho
```

Vamos destrinchar esse código: @username é o nome do usuário que você quer raspar os tweets (no caso, é o meu: @gdiasaz); `file.csv` é o nome do arquivo de destino que você enviará os tweets (chamaremos no nosso caso de `tweets_gustavo.csv`) e o `-ho` é o *hide output*, que evita mostrar o processo de raspagem na tela do terminal e ignora alguns erros possíveis. Portanto, nosso código ficará:

```
twint -u @gdiasaz -o tweets_gustavo.csv --csv -ho
```

Prontinho! Agora é esperar o processo acabar (pode demorar dependendo de quantos tweets tem na sua conta) e abrir o arquivo gerado no diretório (o mesmo que você executou o terminal).

## Gerar o word cloud ##

*Word clouds* são aquelas formas de visualização de dados que contém *strings* (palavras). As palavras mais mencionadas aparecem em evidência, enquanto palavras menos mencionadas ficam mais 'escondidas'. É uma boa maneira de sabermos quais os assuntos/tópicos determinada conta no TT aborda. Para gerarmos uma cloud word com os tweets da minha conta, faremos o seguinte:

### Primeiro passo: importar os pacotes utilizados ###

Vamos usar 4 pacotes nesse processo:

* **Matplotlib.pyplot** para printar o gráfico;
* **Pandas** para ler o arquivo .csv e trabalhar melhor com o dataframe;
* **wordcloud** para gerar o gráfico na forma de *word cloud*;
* **npltk** para trabalhar com dados não-numéricos;

```python
import matplotlib.pyplot as plt
import pandas as pd
import wordcloud
import nltk
```

### Segundo passo: definindo as *stopwords* ###

*Stopwords* são palavras que não são interessantes de serem contabilizadas nesse processo, como verbos conjugados, preposições, artigos definidos e indefinidos, alguns advérbios etc. Por isso, o pacote `nltk` tem uma lista dessas *stopwords* disponível em sua base de dados, em vários idiomas. Usaremos a lista do português e adicionaremos algumas palavras à ela:

```python
nltk.download('stopwords')

stopwords = nltk.corpus.stopwords.words('portuguese')

stopwords.extend(("twitter", "pic", "bit", "ly", "http", "https", "vc", "qnd",
                  "pq", "nada", "nd", "dá", "após", "aqui", "pra", "aí", "tudo", 
                  "desde", "tá", "ta", "sim", "não", "n", "nao", "outro", "vai",
                  "diz", "faz", "vcs", "bem", "mal", "pro", "ser", "fazer", "ainda",
                  "sobre", "gente", "mto", "mt", "falar", "smp", "sempre", "agora", "pode", "fala", "lá"))
```

Você pode adicionar mais palavras caso sinta que o word cloud gerado contempla outras palavras não interessantes, ok?

### Terceiro passo: ler os dados e ajeitá-los ###

```python
df = pd.read_csv("tweets_gustavo.csv", sep = ',', header = 0, 
                 error_bad_lines = 0, encoding = 'utf-8')
```
Atenção nesse processo de leitura: o aquivo `.csv` gerado é separado por **vírgulas**, então não esqueça de mencionar isso. Use, também, o `erros_bad_lines = 0` para que o programa desconsidere erros de linhas não preenchidas. Por fim, `enconding = utf-8` garante que seus dados serão lidos na codificação que contempla acentos da língua portuguesa.

Não preciso nem dizer que o arquivo `tweets_gustavo.csv` precisa estar na mesma pasta onde está sendo rodado esse programa, né?

Você irá gerar um DataFrame (`df`) com 35 colunas. Uma delas é a coluna *tweet*, onde está o tweet em si. É possível que algumas palavras estejam com letra maiúscula no tweet (isso é particularmente verdade pro meu perfil, eu sempre tuíto com maiúsculas). Para evitar problema de compatibilidade, vamos deixar tudo minúsculo?

```python
df['tweet'] = df['tweet'].str.lower() #Coloca tudo em minúsculo
tweets = df['tweet'].to_string() #Cria um objeto tipo *string* contendo somente a coluna dos tweets. Isso é importante no processo de geração do *word cloud*.
```

### Quarto passo: gerando o *word cloud* ###

Agora vamos gerar o *word cloud*. É muito simples:

```python
wc = WordCloud(stopwords = stopwords, background_color = "white").generate(tweets)
```

Recomendo que você leia a documentação do WordCloud para mais comandos. 

### Quinto passo: mostrando a imagem ###

Agora, uma sequência de comandos para mostrar a imagem gerada:

```python
plt.imshow(wc, interpolation = 'bilinear') #interpolation gera figuras mais 'suaves'
plt.axis('off') #Tira os eixos
plt.tight_layout() #Deixa o layout mais 'apertadinho'
plt.savefig('wc_gus.png', format = 'png', dpi = 600) #Salva a figura gerada
```
