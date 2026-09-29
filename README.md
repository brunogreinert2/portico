# Pórtico do Pedra Angular

A porta de entrada do ecossistema, em uma página HTML autocontida: o que
existe, o que cada peça faz, a norma que tudo obedece, e os formatos do livro
físico.

## O princípio

**Esta pasta não guarda conteúdo.** O `gerar.py` lê os arquivos que já são a
verdade do ecossistema e monta a página a partir deles:

| Aba | Vem de |
|---|---|
| Pórtico | `conteudo/00-portico.md` |
| Em andamento | `../andamento/*.md` — uma ficha por frente, formato no `LEIA.md` de lá |
| As peças | `conteudo/01-pecas.md` |
| Normas | `NORMAS.md` — mora aqui desde 2026-09-29 (em `C:\Claude\NORMAS.md` ficou só uma placa) |
| Formatos físicos | `../oficina/Catalogo_Formatos_Encadernacao.md` |
| Os nove temas | `app-leitura/src/styles.css`, token a token |
| As fontes | `app-leitura/public/fonts/` |

Editou a norma? Rode de novo. A página se refaz. **Nunca edite o `index.html`
à mão** — ele é derivado, e a próxima geração o sobrescreve.

## Uso

```
python gerar.py                 # index.html + fonts/  → para publicar
python gerar.py --embutir       # index_embutido.html  → arquivo único
```

Sem dependência nenhuma: biblioteca padrão do Python 3.8+.

Se o `app-leitura` não estiver onde o script procura:

```
python gerar.py --app-leitura "C:\Users\bruno\Claude\Projects\Projeto Pedra Angular\app-leitura"
```

## O que a página cumpre

- **LEI 1 e LEI 2** — todo o texto das abas está no `<body>`, como HTML
  real. Sem JavaScript a página mostra tudo de uma vez, na ordem; as abas são
  conforto, não condição de leitura. Um extrator de HTML lê a página inteira.
- **LEI 3** — zero rede em runtime. As fontes vêm da pasta `fonts/` ao lado
  (ou embutidas em `data:` URI). Nenhum CDN, nenhuma fonte remota.
- **LEI 4 e LEI 5** — os nove temas do app, A− / A+ de 12 a 256 px, foco de
  teclado visível, alvo de toque de 2,75 rem, `prefers-reduced-motion`
  respeitado.
- **LEI 8** — a Barra Angular: Φ · A− · A+ · Ξ, nesta ordem, na primeira fila,
  desde a primeira tela. Φ abre o índice do Pórtico inteiro; Ξ abre o sumário
  da aba aberta. As abas são a fila seguinte, nunca no lugar deles.
- **Capítulo 11** — o que o leitor escolhe (tema, fonte, corpo) fica no
  `localStorage` do próprio navegador dele. Nada sai da máquina.

## Publicar

`index.html` mais a pasta `fonts/` ao lado. Nada mais. Serve em qualquer
hospedagem estática, subdomínio ou pendrive.

## Versão completa, privada (artefato no claude.ai)

`python gerar.py --fragmento --embutir` gera o `portico_artefato.html`: todas
as fichas, com os caminhos do disco. É publicado como artefato privado no
claude.ai; o endereço está na memória do Claude Code e no
`C:\Claude\Saneamento\CONTINUAR_AQUI.md`. Republicar sempre passando esse
endereço como `url`, senão nasce um artefato novo e o link do celular fica velho.

## O site público: pedraangular.app.br/portico/

Desde 2026-09-29 este repositório também gera um site público, montado no
deploy do app-leitura (que clona este repositório):

```
python gerar.py --publico <pasta> --app-leitura <app-leitura>
```

Seis páginas — Pórtico, Em andamento, Diário, Contribuir, Normas, As peças —,
cada uma com a versão `.md` ao lado e nenhuma acima de 80 KB de texto: quem
manda o link a uma IA sabe que ela lê a página inteira. Mais `feed.xml` (o
diário em Atom) e o conferidor (`conferidor.js`), que executa o esquema e as
regras do portão do acervo no navegador.

**O que é público e o que não é.** O artefato privado continua completo. O
site público só leva:

- as fichas de `C:\Claude\andamento` marcadas `public: true`, e delas só nome,
  estado, data e `public_note` — via `andamento_publico.json`, que a geração
  local reescreve e o git traz para cá;
- o diário (`diario/`), escrito para ser lido;
- `conteudo/publico/` (a porta e o contribuir), o `NORMAS.md` e as peças sem os
  caminhos do disco.

**O conferidor tem de concordar com o portão.** Depois de mexer em
`conferidor.js`, no esquema ou nas regras:

```
node teste_conferidor.mjs <esquema> <regras.json> <pasta do corpus> <validacao.csv>
```

O `validacao.csv` sai do `validar_corpus.py` do app-leitura, na mesma pasta.
Em 2026-09-29: 1.109 de 1.109 arquivos com o mesmo veredito.
