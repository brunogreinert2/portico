# As peças

Um texto entra bruto — PDF nativo ou página escaneada — e sai lido. Este é o
percurso, e toda peça do ecossistema ocupa um ponto dele.

```
PDF nativo  →  Conversor  ─┐
                           ├→  Corretor  →  corpus .md  ─┬→  App-Leitura     pedraangular.app.br
PNG / scan  →  OCR        ─┘                             ├→  App-Infantil    historinhas.app.br
                                                         ├→  Rolo · MCP      acervo estático, leitura por IA
                                                         └→  Oficina → Gerador   livro físico
```

O que cada uma faz, e onde mora. O detalhe de operação está no `README.md` de
cada pasta — é lá que se lê antes de mexer, não aqui.

---

## Entrada — do bruto ao corpus

**Conversor** · `C:\Claude\conversor`

PDF nascido digital vira `.md`, agrupando por fonte, corpo e margem, com você
nomeando cada estilo. Marca-texto na saída.

**OCR** · `C:\Projetos\OFICINA\ocr_png_to_md.js` · olmOCR-2 via LM Studio

Página escaneada vira `.md`, com a marcação canônica de margem pedida no
prompt em vez de adivinhada.

**Agrupador de páginas** · `C:\Projetos\OFICINA\12_agrupar_paginas_md.js`

Junta as páginas soltas do OCR num arquivo por obra.

**Corretor** · `C:\Claude\corretor`

Bancada de revisão do `.md` cru: apontar e dizer, marca-texto, buscar e trocar,
registro, desfazer, front matter, perfil por obra que refaz o resultado do zero.

---

## Corpus — guardar e deixar ler

**Rolo** · `C:\Claude\Rolo_HTML\gerador_rolo.py` · `pedraangular.app.br/rolo/`

Gera a camada 2 em HTML puro, sem JavaScript. É o que faz o acervo abrir em
qualquer aparelho e sobreviver a qualquer framework. Desde 2026-08-08 é também
a implementação de referência da Barra Angular.

**Servidor MCP** · `C:\Claude\pedra_mcp` · `servidor.py` · `servidor_remoto.py`

Conector público: qualquer IA busca no corpus, lista filhos, lê trecho exato e
atualiza catálogo e obra.

**Tradução em lote** · `C:\Projetos\OFICINA\traduzir_lote.py`

Grego → português sempre direto do grego, nunca por intermediário em inglês.
Batch API, `lexico_decisoes.yaml` para as decisões de tradução, sinalização
obrigatória de incerteza. Começou pelos diálogos platônicos: Górgias, Teeteto,
Sofista.

**Acervo Diaphoreus** · `C:\Projetos\Diaphoreus\ACERVO`

Latim e grego, de Abelardo a Boécio, 41 autores. Chegou por outro caminho e
ainda não passa pelo Conversor nem pelo Corretor.

---

## Saída — onde o texto encontra o leitor

**App-Leitura** · `C:\Users\bruno\Claude\Projects\Projeto Pedra Angular`

O acervo adulto na tela. Nove temas, TTS, i18n em três camadas, editor
embutido, fontes embarcadas.

**App-Infantil** · `C:\Claude\app-infantil`

As historinhas bilíngues, insígnias fixas, um megabyte no total.

**Oficina** · `C:\Claude\oficina`

Projeta o livro físico: capa, mancha, folhas, materiais, especificação de
produção. Nasceu conforme às normas em 2026-08-09 e é hoje a referência de
implementação da LEI 8 aplicada a uma ferramenta. O `Catalogo_Formatos_Encadernacao.md`
dela é a aba **Formatos físicos** desta página.

**Gerador** · `C:\Claude\gerador`

Bancada de diagramação: leva o corpus ao PDF no leiaute que a Oficina projetou
e deixa mexer no resultado — evitar quebra desnecessária, mover coisa de lugar,
acrescentar imagem. Não é invólucro de pandoc. Hoje a pasta guarda a proposta;
os nove perfis de pandoc atendem enquanto isso, entre eles `abnt`, `academico`
e os cadernos de astigmatismo, baixa visão, dislexia e presbiopia.

---

## Régua — o que impede cada peça de inventar a sua verdade

**NORMAS.md** · `C:\Claude\NORMAS.md`

Oito leis e N1–N79 em treze capítulos. Onde o código diverge da norma, o código
está errado. Está inteiro na aba **Normas**.

**Laboratório de Cores** · `C:\Claude\laboratorio` · `medir_contraste.py`

Mede cada par sob visão normal e as três dicromacias. Substitui o chute, não o
olho.

**Pórtico** · `C:\Claude\portico`

Esta página. Gerada dos arquivos acima, nunca digitada por cima deles.
