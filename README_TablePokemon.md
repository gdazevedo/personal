# Pegando tabelas de sites

Esse pequeno código (explicações no arquivo) serve para raspar uma tabela de um site e formatá-la para uma melhor visualização de dados, utilizado como única biblioteca o **Pandas**

```python
import pandas as pd
```

Agora, vamos criar um objeto que leia as tabelas contidas num determinado site (no nosso caso, do site [IGN](https://www.ign.com/wikis/pokemon-sword-shield/List_of_Pokemon_(Pokedex)):

```python
pokemon = pd.read_html("http://www.ign.com/wikis/pokemon-sword-shield/List_of_Pokemon_(Pokedex)")
```
Ao ler a tabela, o **pandas** a coloca como um único objeto (*tuple*) dentro de uma lista. Precisamos fazer essa separação. Nesse caso específico, a URL que investigamos nos dá apenas uma única tabela, então nós desejamos o índice 0 da lista `pokemon`:

```python
tabela_pokemon = pokemon[0]
```
