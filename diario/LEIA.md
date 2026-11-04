# Diário de bordo — uma entrada por arquivo

O commit humano do Pedra Angular: o que foi feito e por quê, em palavras de
gente. O `gerar.py --publico` monta a página `/portico/diario.html` e o feed
`/portico/feed.xml` a partir destes arquivos, a entrada mais nova primeiro.

Nome do arquivo: `AAAA-MM-DD-assunto.md` — a data vem do nome.

```markdown
---
title: Chegaram os três tomos do Manual do Cidadão
---
Texto livre, em Markdown simples (parágrafos, **negrito**, *itálico*, links).

> Ὁ Διαφορεύς παρῆν
```

**Toda entrada termina com a assinatura**, na última linha, com o `>` na frente:
`> Ὁ Διαφορεύς παρῆν`. O Diário tem a voz de quem ajudou a escrever, mas a
assinatura é do Διαφορεύς — no Pórtico, ela importa mais do que qualquer outra
coisa (decisão dele, 2026-10-13).

Publicar: escrever o arquivo e salvar no GitHub (commit e push daqui, ou
direto no site: github.com/brunogreinert2/portico → pasta `diario` → «Add
file» → «Create new file», e «Commit changes»). O workflow `publicar.yml`
confere o post (`conferir_diario.py`) e manda o site se refazer: em 3 a 4
minutos está no ar. Post com erro (nome fora do padrão, data que não existe,
arquivo vazio) não sobe, e o site continua como estava; o erro aparece em
Actions, no GitHub do portico. Este arquivo (`LEIA.md`) não entra na página.
