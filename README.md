# Fishviewer by Caio Felipe Mendes de Sousa
### Produzido  com intuito de:

- Criar base RDF a partir dos dados fornecidos pela [Google](https://www.google.com/search?q= ) e pela Rest API da [Fishbase](https://fishbaseapi.readme.io/docs) para posteriormente listar espécies com imagens, além de apresentar sua família;


### Como a base foi produzida:
- Para isso os dados fornecidos pela   [Fishbase](https://fishbaseapi.readme.io/docs) foram separados em dois vocabulários. Um com os dados de cada espécie de peixe, e um relacional criado em cima do gênero do peixe, relacionando diferente espécies.
Além de ter sido criado um termo com o endereço da imagem da espécie, a partir de uma busca ao [Google](https://www.google.com/search?q= ), o qual está aninhado à espécie em questão.


### Vocabulários criados:
- fishing;
- sf;
- img;

### Fim
