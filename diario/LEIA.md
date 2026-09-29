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
```

Publicar: escrever o arquivo, `git commit`, `git push`. O site se refaz no
próximo deploy do app. Este arquivo (`LEIA.md`) não entra na página.
