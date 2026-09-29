# Contribuir com um texto

Qualquer pessoa pode preparar um texto para o Pedra Angular: uma edição de
domínio público, uma transcrição, uma tradução própria. O que o acervo pede é
um formato só, igual para todas as obras, para que cada uma seja legível por
gente e por máquina daqui a cem anos.

Esta página é a norma do formato, resumida. A norma completa é o esquema
[frontmatter.schema.json](frontmatter.schema.json); as regras do texto estão
em [Normas](normas.html), capítulo 3.

## Confira o seu arquivo aqui

Arraste o `.md` para a caixa abaixo, escolha o arquivo, ou cole o texto. O
conferidor usa exatamente a mesma regra do portão que guarda o acervo: o que
sair daqui com ✓ entra sem ser barrado. O arquivo é lido no seu próprio
aparelho e não é enviado a lugar nenhum.

## O arquivo

Um `.md` em UTF-8 com duas partes: o front matter (os dados da obra, entre
duas linhas `---`) e o texto.

### Front matter

Campos e valores em inglês. Exemplo:

```yaml
---
id: platao-sophist-grc-john-burnet-1905
type: primary_text
title: Σοφιστής
author: Plato
language: grc
base_edition: "Burnet, Oxford: Clarendon Press, 1905"
publication_year: 1905
tags: [platonism, dialogue]
status: draft
project: pedra_angular
urn_work: urn:cts:greekLit:tlg0059.tlg007
urn: urn:cts:greekLit:tlg0059.tlg007.perseus-grc2
license: CC-BY-SA-4.0
source: "Plato. Sophist. Ed. John Burnet. Oxford: Clarendon Press, 1905. Perseus Digital Library."
---
```

| Campo | O que vai |
|---|---|
| `id` | autor-obra-idioma-editor-ano, em minúsculas, sem acento, com hífen. Publicado, nunca muda |
| `type` | `primary_text`, `translation`, `interlinear` ou `commentary` |
| `title` | o título na língua do texto |
| `author` | o autor da obra, não o tradutor |
| `translator` | lista de tradutores, só em tradução: `[Nome Sobrenome]` |
| `language` | `grc`, `lat`, `heb`, `por`, `eng`, `ara`, `rus`, `fra`, `deu`, `spa`, `ita`. Bilíngue: `[por, grc]` |
| `base_edition` | a edição de base, numa linha |
| `tags` | etiquetas em inglês, com hífen: `[stoicism, ethics]` |
| `status` | `draft`. Só uma pessoa marca `reviewed`, depois de conferir contra a fonte |
| `project` | sempre `pedra_angular` |
| `urn_work`, `urn` | a URN CTS da obra e da edição, quando a obra está no catálogo TLG, PHI ou Perseus |
| `license` | `public-domain`, `CC-BY-SA-4.0`, `CC-BY-SA-3.0`, `CC-BY-4.0` ou `CC0-1.0` |
| `source` | de onde veio o texto, numa linha |
| `pa_exclusive` | `true` se o texto só existe no Pedra Angular |

Três regras que valem para todo campo:

- **Campo desconhecido fica de fora.** Apague a linha. Nunca escreva `null`,
  nunca deixe `""`.
- **Só o que está na fonte.** Não invente nem deduza data, editor ou tradutor.
- **Nada de campo novo.** Um campo que não está na tabela barra o arquivo.

### Texto

Só esta sintaxe, e nada além:

- `#`, `##`, `###`… para títulos, sem limite de profundidade;
- parágrafo: linhas de texto, separadas por uma linha em branco;
- marcador canônico entre colchetes, um por ponto: `[216a]`, `[1094a1]`,
  `[1.1]` — nunca `[216] [216a]` no mesmo lugar;
- âncora no fim da linha: `texto ^gn-1-1`;
- etiqueta de idioma no fim da linha, quando a detecção não basta: `^por`,
  `^grc`, `^eng`, `^lat`, `^heb`, `^rus`;
- nota: `[^1]` no texto e `[^1]: texto da nota` no fim do arquivo. Nota do
  editor ou do tradutor nunca fica colada no texto corrido;
- verso ou poema: dentro de um bloco ` ```verso ` … ` ``` `, onde cada linha
  fica uma linha;
- interlinear: dentro de ` ```interlinear ` … ` ``` `;
- imagem: `{{img:id}}` sozinha na linha.

**Não entra no texto:** `>` de citação, `[[wikilink]]`, `![imagem](…)`,
tabela, `==realce==`, tag ou comentário HTML/XML, e a palavra `null`.

## Licença

Só entra texto que pode circular livremente: domínio público ou licença aberta
(Creative Commons). Tradução ou transcrição sua entra com a licença que você
escolher entre as da lista, e com o seu nome como tradutor. Se o texto foi
cedido por outra pessoa, guarde a cessão por escrito.

## Se você está pedindo a uma IA para preparar o texto

Mande o endereço desta página junto com o pedido:
`https://pedraangular.app.br/portico/contribuir.md`. É o que impede cada
conversa de inventar um formato próprio — foi assim que o acervo chegou a ter
três.
