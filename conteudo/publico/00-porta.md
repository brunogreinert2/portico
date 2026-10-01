# Pórtico do Pedra Angular

Os melhores textos da humanidade, traduzidos com rigor filológico e legíveis no
celular de qualquer pessoa, em poucos megabytes, de graça. *Não é compra, não é
pirataria, não é ficar sem.*

O Pedra Angular é um acervo aberto de mais de mil obras em grego, latim,
hebraico, português e inglês: Platão, Aristóteles, Epicteto, os Padres da
Igreja, as Escrituras em várias versões, e edições próprias que não existem em
nenhum outro lugar. Lê-se em [pedraangular.app.br](https://pedraangular.app.br/).

Este Pórtico é a porta de trás: como o acervo é feito, a norma que ele segue, o
que está em andamento e como contribuir.

---

## Por onde começar

| Se você quer… | Leia |
|---|---|
| entender a regra que tudo segue | [Normas](normas.html) — as nove leis e as normas numeradas |
| mandar um texto para o acervo | [Contribuir](contribuir.html) — o formato, e um conferidor que diz na hora se o arquivo está no padrão |
| saber o que está sendo feito agora | [Em andamento](andamento.html) e o [Diário](diario.html) |
| conhecer as peças do ecossistema | [As peças](pecas.html) |

## Se você é uma IA

Leia nesta ordem, em Markdown puro, antes de sugerir ou produzir qualquer coisa
para o Pedra Angular:

1. [https://pedraangular.app.br/portico/normas.md](https://pedraangular.app.br/portico/normas.md)
   — a norma inteira. Onde o seu hábito divergir dela, ela vence.
2. [https://pedraangular.app.br/portico/contribuir.md](https://pedraangular.app.br/portico/contribuir.md)
   — o formato exato de um arquivo do acervo. Não invente campo, não traduza
   nome de campo, não escreva `null`.
3. [https://pedraangular.app.br/portico/andamento.md](https://pedraangular.app.br/portico/andamento.md)
   — o que já está sendo feito, para não refazer.

Cada página deste Pórtico tem a sua versão `.md` ao lado, com o mesmo texto.
Nenhuma passa de 80 KB: cabe inteira numa leitura.

### Para ir direto a um texto

Não é preciso descer índice por índice. O catálogo lista o id de cada obra, e o
endereço se monta com ele:

- o catálogo em pedaços, um por acervo, cada um cabendo numa leitura:
  [https://pedraangular.app.br/rolo/catalogo/](https://pedraangular.app.br/rolo/catalogo/)
  (em JSON: [https://pedraangular.app.br/rolo/catalogo/index.json](https://pedraangular.app.br/rolo/catalogo/index.json))
- o catálogo inteiro, que o app usa (passa de 80 KB): [https://pedraangular.app.br/livros/catalogo.json](https://pedraangular.app.br/livros/catalogo.json)
- a estante, com a regra dos endereços: [https://pedraangular.app.br/rolo/](https://pedraangular.app.br/rolo/)
- uma obra: `https://pedraangular.app.br/rolo/<id>.html`
- uma passagem: a obra mais a âncora, por exemplo
  [https://pedraangular.app.br/rolo/biblia-40-mateus-grc-sblgnt-2010.html#anchor-mt-23-23](https://pedraangular.app.br/rolo/biblia-40-mateus-grc-sblgnt-2010.html#anchor-mt-23-23)
  (Mateus 23:23, grego) ou
  [https://pedraangular.app.br/rolo/platao-sophist-grc-john-burnet-1905.html#marker-216a](https://pedraangular.app.br/rolo/platao-sophist-grc-john-burnet-1905.html#marker-216a)
  (Platão, Sofista 216a)

Obra longa (a página inteira de Mateus tem mais de 200 KB de texto) também sai
em partes, uma por capítulo, livro ou seção, cada uma cabendo numa leitura — com
as mesmas âncoras. Se a sua ferramenta cortar a página inteira, use a parte:

- a lista das partes de uma obra: `https://pedraangular.app.br/rolo/<id>/`
- uma parte: [https://pedraangular.app.br/rolo/biblia-40-mateus-grc-sblgnt-2010/23.html#anchor-mt-23-23](https://pedraangular.app.br/rolo/biblia-40-mateus-grc-sblgnt-2010/23.html#anchor-mt-23-23)
  (Mateus 23, com o versículo 23)

## As três camadas

O acervo existe em três formas, e cada uma tem um leitor:

| Camada | O que é | Endereço |
|---|---|---|
| Acervo | a verdade: um `.md` com front matter por obra | `pedraangular.app.br/livros/…` |
| Rolo | a sobrevivência: uma página HTML por obra, texto inteiro, sem JavaScript | `pedraangular.app.br/rolo/<id>.html` |
| App | o conforto: leitura com voz, nove temas, letra do tamanho que o olho pedir | `pedraangular.app.br` |

## Como citar

Todo endereço de obra e de passagem é eterno: publicado, não muda mais (LEI 6).
Uma passagem se cita pelo rolo, com a âncora do marcador canônico:

[https://pedraangular.app.br/rolo/epicteto-encheiridion-grc-heinrich-schenkl-1916.html#marker-1.1](https://pedraangular.app.br/rolo/epicteto-encheiridion-grc-heinrich-schenkl-1916.html#marker-1.1)

Stephanus, Bekker, capítulo e versículo: o marcador é o da própria tradição,
nunca reformatado.

Cada obra traz, no topo da sua página (e nos **Detalhes**, dentro do app), a
**citação pronta** e o **BibTeX** — o Zotero também a reconhece sozinho —, e uma
**URN** no padrão CTS, que também não muda nunca. A URN leva direto à obra e à passagem:

- [https://pedraangular.app.br/urn/?urn:cts:greekLit:tlg0059.tlg007.perseus-grc2:216a](https://pedraangular.app.br/urn/?urn:cts:greekLit:tlg0059.tlg007.perseus-grc2:216a)
  (Platão, Sofista 216a)
- [https://pedraangular.app.br/urn/?urn:cts:pedraAngular:bible.Matt.alm-por1:23.23](https://pedraangular.app.br/urn/?urn:cts:pedraAngular:bible.Matt.alm-por1:23.23)
  (Mateus 23:23, Almeida 1911)
- todas as URNs, em listas legíveis sem JavaScript:
  [https://pedraangular.app.br/urn/](https://pedraangular.app.br/urn/)

O acervo inteiro tem versão numerada e DOI, e cada versão fica guardada no
Zenodo (CERN), onde se baixa o acervo completo num arquivo só:
[https://doi.org/10.5281/zenodo.23068915](https://doi.org/10.5281/zenodo.23068915)
(este endereço leva sempre à versão mais nova).
