<!--
Versão pública das peças: é a fonte de pecas.html e pecas.md do Pórtico.
A régua técnica é o NORMAS.md na raiz deste repositório; o mapa de trabalho
das ferramentas (com pastas e READMEs) é o conteudo/01-pecas.md, que fica só
na página privada. Este comentário não é publicado: o gerar.py o tira antes
de gerar as páginas.
-->
# As peças

Um texto chega ao Pedra Angular como um PDF ou como uma página escaneada, e sai pronto para ser lido: na tela, em voz alta ou no papel. Entre uma ponta e outra há algumas ferramentas, cada uma com uma tarefa só.

```
PDF ou página escaneada
          ↓
   conversão e revisão
          ↓
   o acervo: um arquivo de texto por obra
          ↓
app de leitura · página simples · acesso por IA · livro impresso
```

## Entrada: do papel ao texto

**Conversão.** O PDF digital é transformado em texto. A página escaneada passa por reconhecimento de caracteres (OCR), que lê a imagem e devolve o texto.

**Revisão.** Nenhum texto convertido entra direto no acervo. Antes passa por uma bancada de correção, onde se conserta o que a máquina leu errado.

## O acervo

Cada obra é um arquivo de texto simples, com uma ficha no topo: título, autor, edição de origem, licença. Esse arquivo é a versão de referência. Tudo o que você vê no site é gerado a partir dele, e nada o altera por fora.

**Traduções próprias.** Do grego para o português, sempre direto do grego, nunca passando pelo inglês. São feitas com auxílio de IA, com as escolhas de vocabulário registradas e as passagens duvidosas assinaladas. Começaram pelos diálogos de Platão: *Górgias*, *Teeteto*, *Sofista*.

## Saída: onde o texto encontra o leitor

**App de leitura** ([pedraangular.app.br](https://pedraangular.app.br/)). A leitura confortável: voz, nove temas, letra do tamanho que for preciso. Depois de aberto, funciona sem internet.

**Rolo.** Uma página simples por obra, com o texto inteiro, que abre em qualquer aparelho, mesmo antigo, sem precisar de nada instalado. É também o endereço que se usa para citar.

**Acesso por IA.** Um conector público que deixa um assistente de IA buscar no acervo e ler o trecho exato, em vez de citar de memória.

**Livro impresso.** Uma oficina projeta a edição física (formato, papel, encadernação) e um diagramador leva o texto ao arquivo de impressão. Em construção.

**Historinhas** ([historinhas.app.br](https://historinhas.app.br/)). Histórias bilíngues para crianças, num app à parte.

## O que mantém tudo coerente

**As [Normas](normas.html).** As regras que todas as peças seguem.

**Medição de cor.** Cada combinação de cor é medida antes de ser usada, inclusive como a enxergam pessoas com daltonismo.

**Este Pórtico.** Gerado automaticamente a partir dos arquivos do projeto, para nunca dizer algo diferente deles.
