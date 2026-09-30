#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador do Portico do Pedra Angular.

Uma verdade so: este script NAO guarda conteudo. Ele le os arquivos que ja
sao a verdade do ecossistema e monta a pagina a partir deles.

  NORMAS.md ......................... aba "Normas"
  oficina/Catalogo_Formatos_...md ... aba "Formatos fisicos"
  conteudo/00-portico.md ............ aba "Portico"
  conteudo/01-pecas.md .............. aba "As pecas"
  app-leitura/src/styles.css ........ os nove temas, lidos token a token
  app-leitura/public/fonts/ ......... as fontes embutidas (LEI 3)

Editou a norma? Rode de novo. A pagina se refaz.

    python gerar.py               -> index.html          (fontes em fonts/)
    python gerar.py --embutir     -> index_embutido.html (fontes em data:)

O primeiro e o arquivo para publicar num servidor: HTML + pasta fonts/ ao
lado, nada de rede em runtime. O segundo e um arquivo unico, para mandar por
anexo ou publicar como artefato.

Sem dependencia nenhuma: so a biblioteca padrao do Python 3.8+.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import os
import shutil
import subprocess
import sys
import unicodedata
from datetime import date, datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent

# --------------------------------------------------------------------------
# Onde moram as fontes de verdade. A primeira que existir ganha.
# --------------------------------------------------------------------------

CANDIDATOS_APP_LEITURA = [
    AQUI.parent / "app-leitura",                                  # C:\Claude\app-leitura (junction)
    Path.home() / "Claude" / "Projects" / "Projeto Pedra Angular" / "app-leitura",
    Path("C:/Users/bruno/Claude/Projects/Projeto Pedra Angular/app-leitura"),
    Path.home() / "mnt" / "Projeto Pedra Angular" / "app-leitura",  # VM do Cowork
]

CANDIDATOS_NORMAS = [
    AQUI / "NORMAS.md",                                           # casa desde 2026-09-29: o repositorio portico
    AQUI.parent / "NORMAS.md",
    Path("C:/Claude/NORMAS.md"),
    Path.home() / "mnt" / "Claude" / "NORMAS.md",
]

CANDIDATOS_CATALOGO = [
    AQUI.parent / "oficina" / "Catalogo_Formatos_Encadernacao.md",
    Path("C:/Claude/oficina/Catalogo_Formatos_Encadernacao.md"),
    Path.home() / "mnt" / "Claude" / "oficina" / "Catalogo_Formatos_Encadernacao.md",
]


CANDIDATOS_ANDAMENTO = [
    AQUI.parent / "andamento",
    Path("C:/Claude/andamento"),
    Path.home() / "mnt" / "Claude" / "andamento",
]


def primeiro_que_existe(candidatos, oquee):
    for c in candidatos:
        try:
            if c.exists():
                return c
        except OSError:
            continue
    print(f"ERRO: nao achei {oquee}. Procurei em:", file=sys.stderr)
    for c in candidatos:
        print(f"  - {c}", file=sys.stderr)
    sys.exit(1)


# --------------------------------------------------------------------------
# Markdown -> HTML. Minimo e proposital: cobre exatamente o que os documentos
# do ecossistema usam, e nada mais. Sem dependencia, sem surpresa.
# --------------------------------------------------------------------------

RE_CODIGO_INLINE = re.compile(r"`([^`]+)`")
# O negrito nao comeca por asterisco nem espaco: `(*****)` fica literal.
# Mesma regra do Gerador e do rolo.
RE_FORTE = re.compile(r"\*\*(?=[^*\s])(.+?)\*\*", re.S)
RE_ENFASE = re.compile(r"(?<![\*\w])\*([^\*\n]+?)\*(?!\*)")
RE_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"[^\w\s-]", "", t.lower())
    t = re.sub(r"[\s_-]+", "-", t).strip("-")
    return t or "secao"


def inline(texto: str) -> str:
    """Escapa e depois aplica a formatacao de linha. O codigo inline vira um
    marcador antes da enfase, para que ** dentro de `codigo` fique literal."""
    guardados: list[str] = []

    def guardar(m):
        guardados.append(html.escape(m.group(1)))
        return f"\x00{len(guardados) - 1}\x00"

    texto = RE_CODIGO_INLINE.sub(guardar, texto)
    texto = html.escape(texto)
    texto = RE_LINK.sub(r'<a href="\2">\1</a>', texto)
    texto = RE_FORTE.sub(r"<strong>\1</strong>", texto)
    texto = RE_ENFASE.sub(r"<em>\1</em>", texto)

    def devolver(m):
        return f"<code>{guardados[int(m.group(1))]}</code>"

    return re.sub(r"\x00(\d+)\x00", devolver, texto)


def tirar_front_matter(texto: str) -> str:
    if texto.startswith("---"):
        fim = texto.find("\n---", 3)
        if fim != -1:
            return texto[texto.find("\n", fim + 1) + 1:]
    return texto


# --------------------------------------------------------------------------
# Em andamento: uma ficha por frente em andamento/*.md (formato no LEIA.md de
# la). Aqui so se le, valida e ordena; o texto e das fichas.
# --------------------------------------------------------------------------

ESTADOS = ["esperando Bruno", "em curso", "na fila", "parado", "concluído"]
CAMPOS_OBRIGATORIOS = ["frente", "estado", "onde", "proximo", "tocado_em"]


def ler_ficha(caminho: Path) -> dict:
    texto = caminho.read_text(encoding="utf-8").replace("\r\n", "\n")
    campos: dict = {}
    if texto.startswith("---"):
        fim = texto.find("\n---", 3)
        if fim != -1:
            for linha in texto[3:fim].split("\n"):
                if ":" in linha:
                    chave, valor = linha.split(":", 1)
                    campos[chave.strip()] = valor.strip()
    campos["corpo"] = tirar_front_matter(texto).strip()

    erros = [f"falta o campo '{c}'" for c in CAMPOS_OBRIGATORIOS if not campos.get(c)]
    if campos.get("public", "false") not in ("true", "false"):
        erros.append("public tem de ser true ou false")
    if campos.get("public") == "true" and re.search(r"[A-Za-z]:\\|\\\\", campos.get("public_note", "")):
        erros.append("public_note tem caminho de disco: o site público não mostra caminhos")
    if campos.get("estado") and campos["estado"] not in ESTADOS:
        erros.append(f"estado '{campos['estado']}' fora da lista: {', '.join(ESTADOS)}")
    if campos.get("tocado_em"):
        try:
            campos["tocado"] = date.fromisoformat(campos["tocado_em"])
        except ValueError:
            erros.append(f"tocado_em '{campos['tocado_em']}' nao e AAAA-MM-DD")
    if erros:
        print(f"ERRO na ficha {caminho}:", file=sys.stderr)
        for e in erros:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    return campos


def andamento_md(pasta: Path, hoje: date) -> str:
    """Monta o Markdown da aba a partir das fichas: grupos na ordem de
    ESTADOS e, dentro de cada grupo, a mais esquecida primeiro."""
    fichas = [ler_ficha(p) for p in sorted(pasta.glob("*.md"))
              if not p.name.startswith("_") and p.name != "LEIA.md"]

    def dias(f):
        return (hoje - f["tocado"]).days

    def quando(f):
        d = dias(f)
        if d <= 0:
            return "hoje"
        if d == 1:
            return "ontem"
        return f"há {d} dias"

    contagem = ", ".join(
        f"{sum(1 for f in fichas if f['estado'] == e)} {e}"
        for e in ESTADOS if any(f["estado"] == e for f in fichas)
    )
    partes = [
        "# Em andamento",
        "",
        f"{len(fichas)} frentes: {contagem}. Os dias são contados até "
        f"{hoje.isoformat()}, quando esta página foi gerada. Dentro de cada "
        "grupo, a frente parada há mais tempo vem primeiro.",
        "",
        "Cada frente é uma ficha em `C:\\Claude\\andamento\\`. Toda sessão que "
        "mexe numa frente termina atualizando a ficha dela; o formato está no "
        "`LEIA.md` da pasta.",
    ]
    for estado in ESTADOS:
        grupo = sorted((f for f in fichas if f["estado"] == estado),
                       key=dias, reverse=True)
        if not grupo:
            continue
        partes += ["", f"## {estado[0].upper() + estado[1:]}"]
        for f in grupo:
            partes += ["", f"### {f['frente']}", "",
                       f"- **Próximo:** {f['proximo']}",
                       f"- **Onde:** {f['onde']}"]
            if f.get("espera"):
                partes.append(f"- **Espera:** {f['espera']}")
            if f.get("retomar"):
                partes.append(f"- **Para retomar, ler:** `{f['retomar']}`")
            partes.append(f"- **Última vez:** {f['tocado_em']} ({quando(f)})")
            if f["corpo"]:
                partes += ["", f["corpo"]]
    return "\n".join(partes) + "\n"


def md_para_html(texto: str, nivel_base: int = 2):
    """Devolve (html, sumario) — sumario e uma lista de (nivel, id, titulo)."""
    texto = tirar_front_matter(texto).replace("\r\n", "\n")
    linhas = texto.split("\n")
    saida: list[str] = []
    sumario: list[tuple[int, str, str]] = []
    ids_usados: set[str] = set()

    i = 0
    n = len(linhas)

    def id_unico(base: str) -> str:
        s = base
        k = 2
        while s in ids_usados:
            s = f"{base}-{k}"
            k += 1
        ids_usados.add(s)
        return s

    while i < n:
        linha = linhas[i]
        crua = linha.rstrip()

        # -- bloco de codigo ------------------------------------------------
        if crua.startswith("```"):
            lingua = crua[3:].strip()
            corpo = []
            i += 1
            while i < n and not linhas[i].startswith("```"):
                corpo.append(linhas[i])
                i += 1
            i += 1
            cls = f' class="lang-{html.escape(lingua)}"' if lingua else ""
            saida.append(
                f'<pre class="bloco-codigo"><code{cls}>'
                + html.escape("\n".join(corpo))
                + "</code></pre>"
            )
            continue

        # -- linha em branco ------------------------------------------------
        if not crua.strip():
            i += 1
            continue

        # -- regua ----------------------------------------------------------
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", crua.strip()):
            saida.append('<hr class="regua">')
            i += 1
            continue

        # -- titulo ---------------------------------------------------------
        m = re.match(r"^(#{1,6})\s+(.*)$", crua)
        if m:
            nivel = len(m.group(1))
            titulo = m.group(2).strip()
            tag = min(6, nivel_base + nivel - 1)
            ident = id_unico(slug(titulo))
            saida.append(f'<h{tag} id="{ident}">{inline(titulo)}</h{tag}>')
            if nivel <= 2:
                sumario.append((nivel, ident, re.sub(r"[`*]", "", titulo)))
            i += 1
            continue

        # -- tabela ---------------------------------------------------------
        if crua.lstrip().startswith("|") and i + 1 < n and re.match(
            r"^\s*\|[\s:\-|]+\|\s*$", linhas[i + 1]
        ):
            def celulas(l: str):
                l = l.strip()
                if l.startswith("|"):
                    l = l[1:]
                if l.endswith("|"):
                    l = l[:-1]
                return [c.strip() for c in l.split("|")]

            cabecalho = celulas(crua)
            i += 2
            corpo = []
            while i < n and linhas[i].strip().startswith("|"):
                corpo.append(celulas(linhas[i]))
                i += 1
            partes = ['<div class="rolagem-tabela"><table>', "<thead><tr>"]
            partes += [f"<th>{inline(c)}</th>" for c in cabecalho]
            partes.append("</tr></thead><tbody>")
            for fila in corpo:
                partes.append("<tr>")
                partes += [f"<td>{inline(c)}</td>" for c in fila]
                partes.append("</tr>")
            partes.append("</tbody></table></div>")
            saida.append("".join(partes))
            continue

        # -- citacao --------------------------------------------------------
        if crua.lstrip().startswith(">"):
            corpo = []
            while i < n and (linhas[i].lstrip().startswith(">") or linhas[i].strip()):
                if not linhas[i].lstrip().startswith(">"):
                    break
                corpo.append(re.sub(r"^\s*>\s?", "", linhas[i]))
                i += 1
            interno, _ = md_para_html("\n".join(corpo), nivel_base)
            saida.append(f"<blockquote>{interno}</blockquote>")
            continue

        # -- listas ---------------------------------------------------------
        m = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", linha)
        if m:
            ordenada = not m.group(2) in ("-", "*", "+")
            itens: list[str] = []
            recuo_base = len(m.group(1))
            while i < n:
                mm = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.*)$", linhas[i])
                if mm and len(mm.group(1)) == recuo_base:
                    bloco = [mm.group(3)]
                    i += 1
                    while i < n:
                        seg = linhas[i]
                        if not seg.strip():
                            # so continua a lista se a proxima linha ainda for do item
                            if i + 1 < n and linhas[i + 1].startswith(" " * (recuo_base + 2)):
                                bloco.append("")
                                i += 1
                                continue
                            break
                        if re.match(r"^(\s*)([-*+]|\d+\.)\s+", seg) and \
                           len(seg) - len(seg.lstrip()) <= recuo_base:
                            break
                        bloco.append(seg[recuo_base:] if len(seg) > recuo_base else seg.strip())
                        i += 1
                    texto_item = "\n".join(bloco).strip("\n")
                    if "\n\n" in texto_item or re.search(r"^\s*([-*+]|\d+\.)\s", texto_item, re.M):
                        interno, _ = md_para_html(texto_item, nivel_base)
                        itens.append(f"<li>{interno}</li>")
                    else:
                        itens.append(f"<li>{inline(' '.join(texto_item.split(chr(10))))}</li>")
                else:
                    break
            tag = "ol" if ordenada else "ul"
            saida.append(f"<{tag}>{''.join(itens)}</{tag}>")
            continue

        # -- paragrafo ------------------------------------------------------
        bloco = []
        while i < n and linhas[i].strip() and not re.match(
            r"^\s*(#{1,6}\s|```|\||>|[-*+]\s|\d+\.\s|-{3,}$)", linhas[i]
        ):
            bloco.append(linhas[i].strip())
            i += 1
        if bloco:
            saida.append(f"<p>{inline(' '.join(bloco))}</p>")
        else:
            i += 1

    return "\n".join(saida), sumario


# --------------------------------------------------------------------------
# Os nove temas, lidos do styles.css do app-leitura. Nunca redigitados.
# --------------------------------------------------------------------------

# O tema que mora no :root do styles.css do app (la ele e a AUSENCIA de
# atributo). Era o sepia ate 2026-09-25; hoje e o claro, e o escuro entra pelo
# sistema enquanto ninguem escolheu. Uma linha so, como o TEMA_PADRAO do app.
TEMA_PADRAO = "claro"

TEMAS = [
    ("claro", "Preto sobre branco", "padrão; à noite segue o aparelho"),
    ("escuro", "Branco sobre preto", None),
    ("sepia", "Sépia", "leitura longa"),
    ("amarelo", "Amarelo sobre preto", None),
    ("verde", "Verde sobre preto", None),
    ("azul-noite", "Azul-noite", "protanomalia"),
    ("azul-petroleo", "Azul-petróleo", None),
    ("pergaminho", "Pergaminho", None),
    ("amarelo-azul", "Amarelo sobre azul", None),
]

TOKENS_QUE_IMPORTAM = re.compile(
    r"^\s*(--color-[\w-]+|--hl-[\w-]+|--shadow-color|--ui-foco|color-scheme)\s*:\s*([^;]+);"
)


def extrair_bloco(css: str, seletor: str) -> str:
    idx = css.find(seletor)
    if idx == -1:
        return ""
    ini = css.find("{", idx)
    fim = css.find("}", ini)
    return css[ini + 1:fim]


def declaracoes(bloco: str) -> list[str]:
    fora = []
    for linha in bloco.split("\n"):
        m = TOKENS_QUE_IMPORTAM.match(linha)
        if m:
            fora.append(f"  {m.group(1)}: {m.group(2).strip()};")
    return fora


def css_dos_temas(styles: str) -> str:
    partes = ["/* Os nove temas, lidos de app-leitura/src/styles.css. Nao editar aqui. */"]
    base = declaracoes(extrair_bloco(styles, ":root {"))
    if not base:
        print(f"AVISO: nao consegui ler o tema {TEMA_PADRAO} (:root) do styles.css",
              file=sys.stderr)
    partes.append(f":root,\n[data-theme='{TEMA_PADRAO}'] {{\n" + "\n".join(base) + "\n}")
    for chave, _, _ in TEMAS:
        if chave == TEMA_PADRAO:
            continue
        bloco = extrair_bloco(styles, f"[data-theme='{chave}'] {{")
        decls = declaracoes(bloco)
        if not decls:
            print(f"AVISO: tema '{chave}' nao encontrado no styles.css", file=sys.stderr)
            continue
        # 'dark' e o nome que o visor do claude.ai escreve na raiz (artefato);
        # pinta certo mesmo antes do script traduzir para 'escuro'.
        seletor = f"[data-theme='{chave}']" + (",\n[data-theme='dark']" if chave == "escuro" else "")
        partes.append(seletor + " {\n" + "\n".join(decls) + "\n}")
    # O pergaminho tem manchas: e regra de body, nao token.
    manchas = extrair_bloco(styles, "[data-theme='pergaminho'] body {")
    if manchas.strip():
        partes.append("[data-theme='pergaminho'] body {" + manchas + "}")
    return "\n\n".join(partes)


# --------------------------------------------------------------------------
# Fontes. LEI 3: nenhuma vem da rede.
# --------------------------------------------------------------------------

FONTES = [
    ("Cardo", "normal", 400, "cardo-regular.woff2"),
    ("Cardo", "italic", 400, "cardo-italic.woff2"),
    ("Cardo", "normal", 700, "cardo-bold.woff2"),
    ("Atkinson Hyperlegible", "normal", 400, "atkinson-hyperlegible-400.woff2"),
    ("Atkinson Hyperlegible", "italic", 400, "atkinson-hyperlegible-400i.woff2"),
    ("Atkinson Hyperlegible", "normal", 700, "atkinson-hyperlegible-700.woff2"),
    ("Atkinson Hyperlegible", "italic", 700, "atkinson-hyperlegible-700i.woff2"),
    ("OpenDyslexic", "normal", 400, "opendyslexic-400.woff"),
    ("OpenDyslexic", "normal", 700, "opendyslexic-700.woff"),
    ("OpenDyslexic", "italic", 400, "opendyslexic-400i.woff"),
    ("Marca Angular", "normal", 400, "marca-angular.woff2"),
]
# A guarnicao (N73) so entra na versao de pasta: 500 KB que o navegador so
# baixa se um caractere realmente precisar dela. Em data: URI ela viria sempre.
GUARNICAO = [
    ("DejaVu Guarnicao", "normal", 400, "dejavu-sans.woff2"),
    ("DejaVu Guarnicao", "normal", 700, "dejavu-sans-bold.woff2"),
]

LICENCAS = [
    "Cardo-OFL.txt",
    "Atkinson-OFL.txt",
    "OpenDyslexic-OFL.txt",
    "DejaVu-LICENSE.txt",
    "MarcaAngular-GFSDidot-OFL.txt",
]


def css_das_fontes(pasta_fontes: Path, embutir: bool, prefixo: str = "fonts/") -> str:
    regras = []
    lista = FONTES if embutir else FONTES + GUARNICAO
    for familia, estilo, peso, arquivo in lista:
        caminho = pasta_fontes / arquivo
        if not caminho.exists():
            print(f"AVISO: fonte ausente, pulando: {arquivo}", file=sys.stderr)
            continue
        formato = "woff2" if arquivo.endswith(".woff2") else "woff"
        if embutir:
            dados = base64.b64encode(caminho.read_bytes()).decode("ascii")
            src = f"url('data:font/{formato};base64,{dados}') format('{formato}')"
        else:
            src = f"url('{prefixo}{arquivo}') format('{formato}')"
        exibicao = "block" if familia == "Marca Angular" else "swap"
        regras.append(
            f"@font-face{{font-family:'{familia}';font-style:{estilo};"
            f"font-weight:{peso};font-display:{exibicao};src:{src};}}"
        )
    return "\n".join(regras)


def copiar_fontes(pasta_fontes: Path, destino: Path) -> int:
    destino.mkdir(parents=True, exist_ok=True)
    copiadas = 0
    for _, _, _, arquivo in FONTES + GUARNICAO:
        origem = pasta_fontes / arquivo
        if origem.exists():
            shutil.copy2(origem, destino / arquivo)
            copiadas += 1
    for lic in LICENCAS:
        origem = pasta_fontes / lic
        if origem.exists():
            shutil.copy2(origem, destino / lic)
    return copiadas


# --------------------------------------------------------------------------
# A pagina
# --------------------------------------------------------------------------

ESTILO = r"""
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0;
  background:var(--color-bg);
  color:var(--color-text);
  font-family:var(--fonte-leitura);
  font-size:var(--corpo);
  line-height:var(--entrelinha);
  padding-top:var(--altura-barra);
}
:root{
  --corpo:18px;
  --entrelinha:1.7;
  --fonte-leitura:'Cardo','DejaVu Guarnicao',serif;
  --fonte-ui:'Atkinson Hyperlegible','DejaVu Guarnicao',system-ui,sans-serif;
  --fonte-mono:ui-monospace,'DejaVu Guarnicao','Consolas',monospace;
  --altura-barra:7.5rem;
  --esp:1rem;
}
[data-fonte='atkinson']{--fonte-leitura:'Atkinson Hyperlegible','DejaVu Guarnicao',sans-serif}
[data-fonte='opendyslexic']{--fonte-leitura:'OpenDyslexic','DejaVu Guarnicao',sans-serif}
@media (min-width:64rem){:root{--altura-barra:4.5rem}}

/* ===== Barra Angular — LEI 8. Φ na ponta esquerda, Ξ na ponta direita,
   A− e A+ entre os dois. O que e especifico desta pagina (as abas) vem na
   fila seguinte, nunca no lugar deles. ===== */
.barra-angular{
  position:fixed;inset:0 0 auto 0;z-index:50;
  /* No celular, como artefato do claude.ai, a pagina vai ate a borda e a
     barra do app fica por cima dela: barra fixa em top:0 some ali atras. A
     area protegida do topo entra como recuo (zero fora do celular). A altura
     medida pelo script ja a inclui, entao o texto desce junto. */
  padding-top:env(safe-area-inset-top,0px);
  background:var(--color-surface);
  border-bottom:2px solid var(--color-borda-ui);
  box-shadow:0 1px 8px var(--shadow-color);
}
.fila{display:flex;align-items:center;gap:.4rem;
  padding:.4rem max(.75rem,env(safe-area-inset-left)) .4rem .75rem;
  max-width:78rem;margin:0 auto}
.fila--angular{border-bottom:1px solid var(--color-border)}
.espaco{flex:1 1 auto}
.ui-botao-barra{
  min-width:2.75rem;min-height:2.75rem;
  padding:.25rem .5rem;
  border:2px solid currentColor;border-radius:.35rem;
  background:none;color:var(--color-accent);
  font-family:var(--fonte-ui);font-size:1.05rem;font-weight:700;line-height:1;
  cursor:pointer;display:inline-flex;align-items:center;justify-content:center;
  gap:.35rem;
}
.ui-botao-barra--grego{font-family:'Marca Angular','Cardo',serif;font-weight:400;
  font-size:1.75rem}
.ui-botao-barra[aria-expanded='true']{background:var(--color-accent);color:var(--color-bg)}
.ui-botao-barra .rotulo{font-size:.8rem;font-weight:400;letter-spacing:.02em}
@media (max-width:34rem){.ui-botao-barra .rotulo{display:none}}

/* Abas — a fila especifica desta superficie */
.fila--abas{overflow-x:auto;gap:.3rem;padding-top:.3rem;padding-bottom:.3rem;
  scrollbar-width:thin}
.aba-botao{
  min-height:2.75rem;padding:.3rem .8rem;white-space:nowrap;
  border:2px solid transparent;border-radius:.35rem;
  background:none;color:var(--color-text);
  font-family:var(--fonte-ui);font-size:.95rem;cursor:pointer;
}
.aba-botao[aria-selected='true']{
  border-color:var(--color-accent);color:var(--color-accent);font-weight:700;
}
/* No site publico cada secao e uma pagina: o link e a aba, e funciona sem JS */
.aba-link{display:inline-flex;align-items:center;min-height:2.75rem;
  padding:.3rem .8rem;white-space:nowrap;border:2px solid transparent;
  border-radius:.35rem;color:var(--color-text);text-decoration:none;
  font-family:var(--fonte-ui);font-size:.95rem}
.aba-link[aria-current='page']{border-color:var(--color-accent);
  color:var(--color-accent);font-weight:700}

/* ===== Corpo ===== */
main{max-width:74ch;margin:0 auto;padding:2.5rem max(1rem,env(safe-area-inset-left)) 6rem 1rem}
.aba[hidden]{display:none}
h1,h2,h3,h4{font-family:var(--fonte-leitura);line-height:1.2;text-wrap:balance;
  margin:2.2rem 0 .6rem}
h1{font-size:2.1em;margin-top:0}
h2{font-size:1.55em;padding-bottom:.3rem;border-bottom:2px solid var(--color-accent)}
h3{font-size:1.2em}
h4{font-size:1.05em;color:var(--color-muted)}
p,ul,ol,blockquote,pre,.rolagem-tabela{margin:0 0 1.1rem}
li{margin:0 0 .4rem}
a{color:var(--color-accent);text-underline-offset:.2em}
a:hover{text-decoration-thickness:2px}
strong{font-weight:700}
code{font-family:var(--fonte-mono);font-size:.88em;
  background:var(--color-surface);border:1px solid var(--color-border);
  padding:.06em .3em;border-radius:.2rem;word-break:break-word}
.bloco-codigo{background:var(--color-surface);border:1px solid var(--color-border);
  border-left:3px solid var(--color-accent);border-radius:.2rem;
  padding:.9rem 1rem;overflow-x:auto}
.bloco-codigo code{background:none;border:0;padding:0;font-size:.82em;line-height:1.5}
blockquote{border-left:3px solid var(--color-accent);
  padding:.2rem 0 .2rem 1rem;color:var(--color-muted);font-style:italic}
blockquote p:last-child{margin-bottom:0}
hr.regua{border:0;border-top:1px solid var(--color-border);margin:2.4rem 0}
.rolagem-tabela{overflow-x:auto;border:1px solid var(--color-border);border-radius:.2rem}
table{border-collapse:collapse;width:100%;font-size:.9em;
  font-variant-numeric:tabular-nums}
th,td{padding:.5rem .7rem;text-align:left;border-bottom:1px solid var(--color-border);
  vertical-align:top}
th{background:var(--color-surface);font-weight:700;white-space:nowrap}
tbody tr:last-child td{border-bottom:0}

/* ===== Cabecalho de aba ===== */
.chapeu{font-family:var(--fonte-ui);font-size:.72em;letter-spacing:.14em;
  text-transform:uppercase;color:var(--color-muted);margin:0 0 .4rem}
.fonte-da-aba{font-family:var(--fonte-ui);font-size:.78em;color:var(--color-muted);
  border-top:1px solid var(--color-border);
  padding:.8rem 0 0;margin:3rem 0 0}
.fonte-da-aba code{background:none;border:0;padding:0}
/* Em andamento: caminho de pasta nao tem espaco para quebrar no celular */
#aba-andamento li,#aba-andamento p{overflow-wrap:anywhere}

/* ===== Paineis Φ e Ξ ===== */
dialog.painel{
  border:2px solid var(--color-borda-ui);border-radius:.4rem;padding:0;
  background:var(--color-surface);color:var(--color-text);
  max-width:min(32rem,92vw);width:100%;max-height:82vh;
  font-family:var(--fonte-ui);
}
dialog.painel::backdrop{background:rgb(0 0 0 / .55)}
.painel-topo{display:flex;align-items:center;justify-content:space-between;
  gap:1rem;padding:.8rem 1rem;border-bottom:1px solid var(--color-border);
  position:sticky;top:0;background:var(--color-surface)}
.painel-topo h2{margin:0;font-size:1.15rem;border:0;padding:0;
  font-family:var(--fonte-ui)}
.painel-corpo{padding:.8rem 1rem 1.2rem;overflow-y:auto}
.painel-lista{list-style:none;margin:0;padding:0;display:grid;gap:.15rem}
.painel-lista a,.painel-lista button{
  display:block;width:100%;text-align:left;
  padding:.6rem .7rem;min-height:2.75rem;
  border:1px solid transparent;border-radius:.25rem;
  background:none;color:var(--color-text);font:inherit;cursor:pointer;
  text-decoration:none;
}
.painel-lista a:hover,.painel-lista button:hover{
  border-color:var(--color-border);background:var(--color-bg)}
.painel-lista .n2{padding-left:1.8rem;font-size:.92em;color:var(--color-muted)}
.painel-grupo{margin:0 0 1.1rem}
.painel-grupo>h3{margin:0 0 .35rem;font-size:.72rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--color-muted);font-family:var(--fonte-ui)}
.opcoes{display:grid;gap:.35rem}
@media (min-width:30rem){.opcoes--tema{grid-template-columns:1fr 1fr}}
.opcao{display:flex;align-items:center;gap:.6rem;min-height:2.75rem;
  padding:.4rem .6rem;border:2px solid var(--color-border);border-radius:.25rem;
  background:none;color:var(--color-text);font:inherit;cursor:pointer;text-align:left}
.opcao[aria-pressed='true']{border-color:var(--color-accent);
  box-shadow:inset 0 0 0 1px var(--color-accent)}
.amostra{width:2.2rem;height:2.2rem;flex:none;border-radius:.15rem;
  border:1px solid var(--color-borda-ui);
  display:flex;align-items:center;justify-content:center;
  font-family:'Marca Angular','Cardo',serif;font-size:1.1rem}
.opcao-texto{display:flex;flex-direction:column;line-height:1.25}
.opcao-dica{font-size:.75em;color:var(--color-muted)}

/* ===== Piso de acessibilidade — Capitulo 7 ===== */
:where(a,button,summary,[tabindex]):focus-visible{
  outline:3px solid var(--ui-foco,var(--color-accent));
  outline-offset:2px;border-radius:.2rem}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;
  scroll-behavior:auto!important}}
html{scroll-behavior:smooth;scroll-padding-top:calc(var(--altura-barra) + 1rem)}
.pular{position:absolute;left:-9999px;top:0}
.pular:focus{left:.5rem;top:.5rem;z-index:100;padding:.6rem .9rem;
  background:var(--color-accent);color:var(--color-bg);border-radius:.25rem}

/* ===== Sem JavaScript: tudo aberto, tudo legivel — LEI 1 e LEI 2 ===== */
.so-com-js{display:none}
html.js .so-com-js{display:revert}
html.js .fila--abas .aba-botao{display:inline-block}
.aviso-sem-js{border:2px dashed var(--color-border);border-radius:.25rem;
  padding:.7rem .9rem;margin:0 0 2rem;color:var(--color-muted);
  font-family:var(--fonte-ui);font-size:.85em}
html.js .aviso-sem-js{display:none}

.colofao{margin-top:4rem;padding-top:1.4rem;border-top:1px solid var(--color-border);
  text-align:center;color:var(--color-muted)}
.colofao .selo{font-family:'Cardo',serif;font-size:1.15em}
.colofao .miudo{font-family:var(--fonte-ui);font-size:.75em;margin-top:.4rem}
"""

SCRIPT = r"""
(function(){
  'use strict';
  document.documentElement.classList.add('js');

  var GUARDA = 'portico:';
  function ler(k, padrao){ try { var v = localStorage.getItem(GUARDA+k); return v===null?padrao:v; } catch(e){ return padrao; } }
  function gravar(k, v){ try { localStorage.setItem(GUARDA+k, v); } catch(e){} }

  var raiz = document.documentElement;

  /* A barra e fixa e cresce com a letra (A+ tambem aumenta os botoes dela).
     Medir e melhor que adivinhar: um valor chutado esconde o topo do texto
     justamente em quem mais aumentou a letra. */
  var barra = document.querySelector('.barra-angular');
  function medirBarra(){
    if (!barra) return;
    raiz.style.setProperty('--altura-barra', barra.offsetHeight + 'px');
  }
  window.addEventListener('resize', medirBarra);

  /* ---- tema ---- */
  /* Como no app (ThemeDialog.tsx): enquanto ninguem escolheu, segue o sistema,
     claro ou escuro, e essa leitura NAO grava. A escolha grava, e a partir
     dela anoitecer nao muda mais a pagina. */
  function mostrarTema(t){ raiz.setAttribute('data-theme', t);
    document.querySelectorAll('[data-escolha-tema]').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.escolhaTema === t)); }); }
  function porTema(t){ mostrarTema(t); gravar('tema', t); }
  var escuroMQ = null;
  try { escuroMQ = window.matchMedia('(prefers-color-scheme: dark)'); } catch(e){}
  function temaDoSistema(){ return escuroMQ && escuroMQ.matches ? 'escuro' : 'claro'; }
  mostrarTema(ler('tema', null) || temaDoSistema());
  if (escuroMQ && escuroMQ.addEventListener) escuroMQ.addEventListener('change', function(){
    if (ler('tema', null) === null) mostrarTema(temaDoSistema()); });
  /* Publicado como artefato, o visor do claude.ai escreve data-theme="dark"
     ou "light" na raiz, o mesmo atributo daqui. Vale como a voz do sistema:
     sem escolha gravada, vira escuro/claro; com escolha, a escolha fica. */
  try { new MutationObserver(function(){
    var v = raiz.getAttribute('data-theme');
    if (v !== 'dark' && v !== 'light') return;
    mostrarTema(ler('tema', null) || (v === 'dark' ? 'escuro' : 'claro'));
  }).observe(raiz, {attributes: true, attributeFilter: ['data-theme']}); } catch(e){}

  /* ---- fonte de leitura ---- */
  function porFonte(f){ raiz.setAttribute('data-fonte', f); gravar('fonte', f);
    document.querySelectorAll('[data-escolha-fonte]').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.escolhaFonte === f)); }); }
  porFonte(ler('fonte','cardo'));

  /* ---- corpo do texto: A− e A+ (N60) ---- */
  var MIN = 12, MAX = 256, PASSO = 1.125;
  function padrao(){ try { return window.matchMedia('(min-width:64rem)').matches ? 21 : 18; } catch(e){ return 18; } }
  var px = parseInt(ler('corpo', String(padrao())), 10);
  if (!isFinite(px)) px = padrao();
  function porCorpo(v){
    px = Math.min(MAX, Math.max(MIN, Math.round(v)));
    raiz.style.setProperty('--corpo', px + 'px');
    gravar('corpo', String(px));
    var r = document.getElementById('leitor-corpo');
    if (r) r.textContent = px + ' pixels';
    medirBarra();
  }
  porCorpo(px);
  document.getElementById('btn-menos').addEventListener('click', function(){ porCorpo(px/PASSO); });
  document.getElementById('btn-mais').addEventListener('click', function(){ porCorpo(px*PASSO); });

  /* ---- abas ---- */
  var abas = Array.prototype.slice.call(document.querySelectorAll('.aba'));
  var botoes = Array.prototype.slice.call(document.querySelectorAll('.aba-botao'));
  function abrirAba(id, rolar){
    abas.forEach(function(s){ s.hidden = (s.id !== id); });
    botoes.forEach(function(b){ b.setAttribute('aria-selected', String(b.dataset.aba === id)); });
    gravar('aba', id);
    montarSumario();
    if (rolar) window.scrollTo({top:0, behavior:'auto'});
    try { history.replaceState(null,'','#'+id); } catch(e){}
  }
  botoes.forEach(function(b){
    b.addEventListener('click', function(){ abrirAba(b.dataset.aba, true); });
    b.addEventListener('keydown', function(e){
      var i = botoes.indexOf(b), j = -1;
      if (e.key === 'ArrowRight') j = (i+1) % botoes.length;
      if (e.key === 'ArrowLeft') j = (i-1+botoes.length) % botoes.length;
      if (j >= 0){ e.preventDefault(); botoes[j].focus(); abrirAba(botoes[j].dataset.aba, true); }
    });
  });

  /* ---- Ξ: o sumario do que esta na tela ---- */
  function montarSumario(){
    var atual = abas.filter(function(s){ return !s.hidden; })[0];
    var alvo = document.getElementById('lista-sumario');
    alvo.innerHTML = '';
    if (!atual) return;
    var tits = atual.querySelectorAll('h2[id], h3[id]');
    if (!tits.length){
      var vazio = document.createElement('li');
      vazio.className = 'n2';
      vazio.textContent = 'Esta aba não tem seções.';
      alvo.appendChild(vazio);
      return;
    }
    Array.prototype.forEach.call(tits, function(h){
      var li = document.createElement('li');
      if (h.tagName === 'H3') li.className = 'n2';
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent;
      a.addEventListener('click', function(){ fechar(dlgSumario); });
      li.appendChild(a);
      alvo.appendChild(li);
    });
  }

  /* ---- paineis ---- */
  var dlgIndice = document.getElementById('painel-indice');
  var dlgSumario = document.getElementById('painel-sumario');
  var dlgAparencia = document.getElementById('painel-aparencia');
  function abrir(d, botao){
    if (typeof d.showModal === 'function') d.showModal(); else d.setAttribute('open','');
    if (botao) botao.setAttribute('aria-expanded','true');
    d._botao = botao;
  }
  function fechar(d){
    if (typeof d.close === 'function') d.close(); else d.removeAttribute('open');
  }
  [dlgIndice, dlgSumario, dlgAparencia].forEach(function(d){
    d.addEventListener('close', function(){
      if (d._botao){ d._botao.setAttribute('aria-expanded','false'); d._botao.focus(); }
    });
    d.addEventListener('click', function(e){ if (e.target === d) fechar(d); });
    d.querySelector('[data-fechar]').addEventListener('click', function(){ fechar(d); });
  });
  document.getElementById('btn-phi').addEventListener('click', function(){ abrir(dlgIndice, this); });
  document.getElementById('btn-xi').addEventListener('click', function(){ montarSumario(); abrir(dlgSumario, this); });
  document.getElementById('btn-aparencia').addEventListener('click', function(){ abrir(dlgAparencia, this); });

  document.querySelectorAll('[data-escolha-tema]').forEach(function(b){
    b.addEventListener('click', function(){ porTema(b.dataset.escolhaTema); }); });
  document.querySelectorAll('[data-escolha-fonte]').forEach(function(b){
    b.addEventListener('click', function(){ porFonte(b.dataset.escolhaFonte); }); });

  /* Φ leva a qualquer ponto de qualquer aba */
  document.querySelectorAll('#lista-indice a').forEach(function(a){
    a.addEventListener('click', function(e){
      if (!a.dataset.aba) return;            /* outra pagina do site publico */
      e.preventDefault();
      var alvo = a.getAttribute('href').slice(1);
      abrirAba(a.dataset.aba, false);
      fechar(dlgIndice);
      var el = document.getElementById(alvo);
      if (el) el.scrollIntoView();
      else window.scrollTo({top:0});
    });
  });

  /* ---- primeira tela ---- */
  var inicial = (location.hash || '').slice(1);
  if (!document.getElementById(inicial) || inicial.indexOf('aba-') !== 0) inicial = ler('aba', abas[0].id);
  if (!document.getElementById(inicial)) inicial = abas[0].id;
  abrirAba(inicial, false);
})();
"""


NUMERAIS = {3: "três", 4: "quatro", 5: "cinco", 6: "seis", 7: "sete"}


def montar(abas, temas_css, fontes_css, embutido: bool, fragmento: bool = False,
           publico: dict | None = None) -> str:
    """publico=None: a pagina privada de abas (index.html / artefato).
    publico={...}: UMA pagina do site publico /portico/, com as outras como
    links. Chaves: todas (as abas de todas as paginas, cada uma com
    'arquivo'), titulo, descricao, url, md (versao .md ao lado, opcional)."""
    hoje = date.today().isoformat()

    if publico:
        botoes_aba = "".join(
            f'<a class="aba-link" href="{t["arquivo"]}"'
            + (' aria-current="page"' if t["id"] == abas[0]["id"] else "")
            + f'>{html.escape(t["nome"])}</a>'
            for t in publico["todas"]
        )
    else:
        botoes_aba = "".join(
            f'<button class="aba-botao" type="button" role="tab" '
            f'data-aba="{a["id"]}" aria-selected="false" '
            f'aria-controls="{a["id"]}">{html.escape(a["nome"])}</button>'
            for a in abas
        )

    secoes = []
    for a in abas:
        fonte = ""
        if a.get("fonte"):
            fonte = (
                f'<p class="fonte-da-aba">Esta aba é gerada de '
                f'<code>{html.escape(a["fonte"])}</code>. Para mudar o que está '
                f"escrito aqui, edite esse arquivo e rode <code>gerar.py</code> "
                f"de novo — a página não é uma segunda verdade.</p>"
            )
        secoes.append(
            f'<section class="aba" id="{a["id"]}" role="tabpanel" '
            f'aria-label="{html.escape(a["nome"])}">\n'
            f'<p class="chapeu">{html.escape(a["chapeu"])}</p>\n'
            f"{a['html']}\n{fonte}\n</section>"
        )

    itens_indice = []
    for a in (publico["todas"] if publico else abas):
        # no site publico so os links da propria pagina levam data-aba;
        # os das outras paginas navegam de verdade
        aqui = not publico or a["id"] == abas[0]["id"]
        pre = "" if aqui else a["arquivo"]
        dados = f' data-aba="{a["id"]}"' if aqui else ""
        itens_indice.append(
            f'<li class="painel-grupo"><h3>{html.escape(a["nome"])}</h3><ul class="painel-lista">'
        )
        itens_indice.append(
            f'<li><a href="{pre}#{a["id"]}"{dados}>'
            + ("Abrir a página" if publico else "Abrir a aba") + "</a></li>"
        )
        for nivel, ident, titulo in a["sumario"]:
            if nivel > 2:
                continue
            cls = ' class="n2"' if nivel == 2 else ""
            itens_indice.append(
                f'<li{cls}><a href="{pre}#{ident}"{dados}>{html.escape(titulo)}</a></li>'
            )
        itens_indice.append("</ul></li>")

    opcoes_tema = "".join(
        f'<button class="opcao" type="button" data-escolha-tema="{chave}" aria-pressed="false">'
        f'<span class="amostra" data-theme="{chave}" '
        f'style="background:var(--color-bg);color:var(--color-accent)" aria-hidden="true">Φ</span>'
        f'<span class="opcao-texto"><span>{html.escape(nome)}</span>'
        + (f'<span class="opcao-dica">{html.escape(dica)}</span>' if dica else "")
        + "</span></button>"
        for chave, nome, dica in TEMAS
    )

    opcoes_fonte = "".join(
        f'<button class="opcao" type="button" data-escolha-fonte="{chave}" aria-pressed="false">'
        f'<span class="amostra" style="font-family:{familia}" aria-hidden="true">Aa</span>'
        f'<span class="opcao-texto"><span>{html.escape(nome)}</span>'
        f'<span class="opcao-dica">{html.escape(dica)}</span></span></button>'
        for chave, nome, dica, familia in [
            ("cardo", "Serifada (padrão)", "Cardo — latim, grego politônico e hebraico no mesmo desenho.", "'Cardo',serif"),
            ("atkinson", "Atkinson Hyperlegible", "Traço uniforme e letras bem diferentes entre si.", "'Atkinson Hyperlegible',sans-serif"),
            ("opendyslexic", "OpenDyslexic", "Base das letras mais pesada, contra a troca de b/d e p/q.", "'OpenDyslexic',sans-serif"),
        ]
    )

    nota_fontes = (
        "fontes embutidas no próprio arquivo"
        if embutido
        else "fontes na pasta <code>fonts/</code> ao lado"
    )

    if publico:
        aviso_sem_js = ""
        md = publico.get("md")
        colofao = (f"Gerado em {publico.get('carimbo') or hoje} pelo <code>gerar.py</code> do repositório "
                   '<a href="https://github.com/brunogreinert2/portico">portico</a>'
                   + (f' · o mesmo texto em Markdown: <a href="{md}">{md}</a>' if md else "")
                   + " · zero rede em runtime (LEI 3)")
        script = '<script src="portico.js"></script>'
        cabeca = (f"<title>{html.escape(publico['titulo'])}</title>\n"
                  '<link rel="stylesheet" href="portico.css">')
    else:
        aviso_sem_js = (
            '  <p class="aviso-sem-js">Sem JavaScript, esta página mostra tudo de uma vez —\n'
            f'     as {NUMERAIS.get(len(abas), len(abas))} seções, na ordem. É de propósito: '
            'LEI 1 e LEI 2. As abas, os\n'
            '     nove temas e o A+ são conforto, não condição de leitura.</p>')
        colofao = (f"Pórtico gerado em {hoje} · {nota_fontes} · zero rede em\n"
                   "    runtime (LEI 3) · gerado por <code>gerar.py</code> a partir dos arquivos do\n"
                   "    ecossistema")
        script = f"<script>\n{SCRIPT}\n</script>"
        cabeca = f"""<title>Pórtico do Pedra Angular</title>
<style>
{fontes_css}

{temas_css}
{ESTILO}
</style>"""

    corpo = f"""<a class="pular" href="#conteudo">Pular para o conteúdo</a>

<header class="barra-angular">
  <div class="fila fila--angular">
    <button id="btn-phi" class="ui-botao-barra ui-botao-barra--grego so-com-js"
            type="button" aria-label="Abrir o índice do Pórtico"
            aria-haspopup="dialog" aria-expanded="false">Φ</button>
    <span class="espaco"></span>
    <button id="btn-menos" class="ui-botao-barra so-com-js" type="button"
            aria-label="Diminuir letra">A&minus;</button>
    <button id="btn-mais" class="ui-botao-barra so-com-js" type="button"
            aria-label="Aumentar letra">A+</button>
    <button id="btn-aparencia" class="ui-botao-barra so-com-js" type="button"
            aria-label="Abrir tema e fonte" aria-haspopup="dialog" aria-expanded="false">
      <span aria-hidden="true">◐</span><span class="rotulo">Tema</span></button>
    <span class="espaco"></span>
    <button id="btn-xi" class="ui-botao-barra ui-botao-barra--grego so-com-js"
            type="button" aria-label="Abrir sumário"
            aria-haspopup="dialog" aria-expanded="false">Ξ</button>
  </div>
  <nav class="fila fila--abas" {'aria-label="Páginas do Pórtico"' if publico else 'role="tablist" aria-label="Seções do Pórtico"'}>
    {botoes_aba}
  </nav>
</header>

<main id="conteudo">
{aviso_sem_js}

{chr(10).join(secoes)}

  <p class="colofao"><span class="selo">Ὁ Διαφορεύς παρῆν</span><br>
    <span class="miudo">{colofao}</span></p>
</main>

<dialog class="painel" id="painel-indice" aria-labelledby="tit-indice">
  <div class="painel-topo"><h2 id="tit-indice">Índice do Pórtico</h2>
    <button class="ui-botao-barra" type="button" data-fechar aria-label="Fechar">✕</button></div>
  <div class="painel-corpo"><ul class="painel-lista" id="lista-indice">
    {''.join(itens_indice)}
  </ul></div>
</dialog>

<dialog class="painel" id="painel-sumario" aria-labelledby="tit-sumario">
  <div class="painel-topo"><h2 id="tit-sumario">Sumário desta seção</h2>
    <button class="ui-botao-barra" type="button" data-fechar aria-label="Fechar">✕</button></div>
  <div class="painel-corpo"><ul class="painel-lista" id="lista-sumario"></ul></div>
</dialog>

<dialog class="painel" id="painel-aparencia" aria-labelledby="tit-aparencia">
  <div class="painel-topo"><h2 id="tit-aparencia">Tema e fonte</h2>
    <button class="ui-botao-barra" type="button" data-fechar aria-label="Fechar">✕</button></div>
  <div class="painel-corpo">
    <div class="painel-grupo"><h3>Tema</h3>
      <div class="opcoes opcoes--tema">{opcoes_tema}</div></div>
    <div class="painel-grupo"><h3>Fonte de leitura</h3>
      <div class="opcoes">{opcoes_fonte}</div></div>
    <div class="painel-grupo"><h3>Corpo do texto</h3>
      <p class="opcao-dica" style="margin:0">Agora em <span id="leitor-corpo">18 pixels</span>.
         Use A&minus; e A+ na barra, a qualquer momento.</p></div>
  </div>
</dialog>

{script}"""

    if publico:
        extra = ""
        if publico.get("md"):
            extra += f'<link rel="alternate" type="text/markdown" href="{publico["md"]}">\n'
        extra += ('<link rel="alternate" type="application/atom+xml" '
                  'title="Diário do Pedra Angular" href="feed.xml">\n')
        return (
            f'<!DOCTYPE html>\n<html lang="pt-BR" data-theme="{TEMA_PADRAO}" data-fonte="cardo">\n'
            '<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f'<meta name="description" content="{html.escape(publico["descricao"], quote=True)}">\n'
            f'<link rel="canonical" href="{publico["url"]}">\n'
            '<link rel="icon" href="icone/icone-32.png" sizes="32x32" type="image/png">\n'
            + extra + cabeca
            + "\n</head>\n<body>\n" + corpo + "\n</body>\n</html>\n"
        )

    if fragmento:
        # Para artefato: o esqueleto (<!doctype>, <html>, <head>, <body>) e posto
        # por quem publica. O data-theme entra pelo script, no primeiro quadro.
        return cabeca + "\n" + corpo + "\n"

    return (
        f'<!DOCTYPE html>\n<html lang="pt-BR" data-theme="{TEMA_PADRAO}" data-fonte="cardo">\n'
        '<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        # Ícone oficial da peça (origem: C:\Claude\icones) e manifesto — só na
        # página inteira. No artefato quem publica põe o próprio ícone, e o
        # caminho relativo icone/ nem existe lá. O manifesto só vale servido
        # (abrir_portico.bat); por duplo clique o navegador o ignora.
        '<link rel="icon" href="icone/icone.svg" type="image/svg+xml">\n'
        '<link rel="icon" href="icone/icone-32.png" sizes="32x32" type="image/png">\n'
        '<link rel="manifest" href="manifest.json">\n'
        '<meta name="description" content="A porta de entrada do ecossistema '
        'Pedra Angular: o que existe, o que cada peça faz, a norma que tudo '
        'obedece e os formatos do livro físico.">\n'
        + cabeca
        + "\n</head>\n<body>\n"
        + corpo
        + "\n</body>\n</html>\n"
    )


# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# O site publico: pedraangular.app.br/portico/
#
# Uma pagina por secao, cada uma com a versao .md ao lado e nenhuma acima de
# ~80 KB: uma IA que recebe o link le a pagina inteira (a pagina de 232 KB do
# rolo chegou cortada e fez uma IA concluir que o Plutarco grego nao existia).
# O que e privado — caminhos do disco, fichas nao marcadas public — nao sai.
# --------------------------------------------------------------------------

SITE = "https://pedraangular.app.br/portico/"
ANDAMENTO_PUBLICO = AQUI / "andamento_publico.json"
LIMITE_PAGINA = 80 * 1024


def exportar_andamento_publico(pasta: Path) -> int:
    """Grava andamento_publico.json so com as fichas public: true e so com os
    campos da lista branca. E a fronteira: o que nao esta aqui nao vai ao site."""
    fichas = [ler_ficha(p) for p in sorted(pasta.glob("*.md"))
              if not p.name.startswith("_") and p.name != "LEIA.md"]
    publicas = [
        {"frente": f["frente"], "estado": f["estado"], "tocado_em": f["tocado_em"],
         **({"nota": f["public_note"]} if f.get("public_note") else {})}
        for f in fichas if f.get("public") == "true"
    ]
    dados = {"_gerado_por": "portico/gerar.py, das fichas locais marcadas public — nao editar",
             "fichas": publicas}
    novo = json.dumps(dados, ensure_ascii=False, indent=1) + "\n"
    if not ANDAMENTO_PUBLICO.exists() or ANDAMENTO_PUBLICO.read_text(encoding="utf-8") != novo:
        ANDAMENTO_PUBLICO.write_text(novo, encoding="utf-8")
    return len(publicas)


def andamento_publico_md(hoje: date) -> str:
    fichas = []
    if ANDAMENTO_PUBLICO.exists():
        fichas = json.loads(ANDAMENTO_PUBLICO.read_text(encoding="utf-8"))["fichas"]
    partes = ["# Em andamento", "",
              "O que está sendo feito no Pedra Angular agora. O registro do que já "
              "foi feito está no [Diário](diario.html).", ""]
    for estado in ESTADOS:
        grupo = sorted((f for f in fichas if f["estado"] == estado),
                       key=lambda f: f["tocado_em"])
        if not grupo:
            continue
        partes += [f"## {estado[0].upper() + estado[1:]}", ""]
        for f in grupo:
            partes += [f"### {f['frente']}", ""]
            if f.get("nota"):
                partes += [f["nota"], ""]
            # so a data: "ontem" numa pagina estatica congela (teste de 2026-09-29)
            partes += [f"*Última vez: {f['tocado_em']}.*", ""]
    if not fichas:
        partes.append("Nada publicado aqui ainda.")
    return "\n".join(partes) + "\n"


def entradas_do_diario(pasta: Path) -> list[dict]:
    entradas = []
    for p in sorted(pasta.glob("*.md"), reverse=True):
        m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)\.md$", p.name)
        if not m:
            continue
        texto = p.read_text(encoding="utf-8").replace("\r\n", "\n")
        titulo = re.search(r"^title:\s*(.+)$", texto, re.M)
        titulo = titulo.group(1).strip().strip('"') if titulo else m.group(2).replace("-", " ")
        entradas.append({"data": m.group(1), "slug": m.group(2), "titulo": titulo,
                         "corpo": tirar_front_matter(texto).strip()})
    return entradas


def diario_md(entradas: list[dict]) -> str:
    partes = ["# Diário", "",
              "O que foi feito, e por quê. A entrada mais nova vem primeiro. Para "
              "acompanhar sem voltar aqui: o [feed](feed.xml).", ""]
    for e in entradas:
        partes += [f"## {e['data']} · {e['titulo']}", "", e["corpo"], ""]
    if not entradas:
        partes.append("Nenhuma entrada ainda.")
    return "\n".join(partes) + "\n"


def feed_atom(entradas: list[dict], sumario_por_titulo: dict) -> str:
    agora = (entradas[0]["data"] if entradas else date.today().isoformat()) + "T00:00:00Z"
    itens = []
    for e in entradas:
        ancora = sumario_por_titulo.get(f"{e['data']} · {e['titulo']}", "")
        corpo_html, _ = md_para_html(e["corpo"], nivel_base=3)
        itens.append(
            "<entry>"
            f"<id>tag:pedraangular.app.br,{e['data']}:portico/diario/{html.escape(e['slug'])}</id>"
            f"<title>{html.escape(e['titulo'])}</title>"
            f"<updated>{e['data']}T00:00:00Z</updated>"
            f'<link href="{SITE}diario.html#{ancora}"/>'
            f'<content type="html">{html.escape(corpo_html)}</content>'
            "</entry>"
        )
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">'
        "<title>Diário do Pedra Angular</title>"
        f'<link href="{SITE}diario.html"/><link rel="self" href="{SITE}feed.xml"/>'
        f"<id>{SITE}diario.html</id><updated>{agora}</updated>"
        "<author><name>Διαφορεύς</name></author>"
        + "".join(itens) + "</feed>\n"
    )


def sem_caminhos(texto: str) -> str:
    """As pecas, sem os caminhos do disco: `C:\\...` some, com o separador."""
    texto = re.sub(r"\s*·\s*`[A-Za-z]:\\[^`]*`", "", texto)
    return re.sub(r"`[A-Za-z]:\\[^`]*`\s*·?\s*", "", texto)


CSS_CONFERIDOR = r"""
/* ===== Conferidor (contribuir.html) ===== */
.conf{margin:1.5rem 0 2.5rem;font-family:var(--fonte-ui)}
.conf-zona{border:2px dashed var(--color-borda-ui);border-radius:.4rem;padding:1.2rem;
  display:flex;flex-direction:column;gap:.8rem;align-items:flex-start}
.conf-zona.conf-sobre{border-style:solid;border-color:var(--color-accent)}
.conf-zona p{margin:0}
.conf input[type=file]{font:inherit;color:var(--color-text);max-width:100%}
.conf label{display:block;font-weight:700;margin:1.2rem 0 .4rem}
.conf textarea{width:100%;font-family:var(--fonte-mono);font-size:.9em;
  color:var(--color-text);background:var(--color-surface);
  border:2px solid var(--color-borda-ui);border-radius:.35rem;padding:.6rem}
.conf-botao{min-height:2.75rem;padding:.4rem 1rem;margin-top:.6rem;font:inherit;font-weight:700;
  color:var(--color-text);background:var(--color-surface);cursor:pointer;
  border:2px solid var(--color-accent);border-radius:.35rem}
.conf-bloco{margin-top:1.4rem;padding:1rem 1.2rem;border:2px solid var(--color-borda-ui);
  border-radius:.4rem}
.conf-bloco.conf-aprovado{border-color:var(--color-accent)}
.conf-bloco h3{margin:0 0 .3rem;font-size:1.05rem;overflow-wrap:anywhere}
.conf-veredito{margin:0 0 .6rem}
.conf-lista{margin:0;padding-left:1.1rem}
.conf-lista li{margin:.8rem 0}
.conf-ex{display:block;margin:.3rem 0;white-space:pre-wrap;overflow-wrap:anywhere}
.conf-mais{display:block;color:var(--color-muted)}
.conf-dica{margin:.3rem 0 0}
"""

HTML_CONFERIDOR = """
<div id="conferidor" class="conf" hidden>
  <div id="conf-zona" class="conf-zona">
    <p>Arraste o arquivo <code>.md</code> para esta caixa, ou escolha no aparelho:</p>
    <input id="conf-arquivo" type="file" multiple
           accept=".md,.markdown,.txt,text/markdown,text/plain"
           aria-label="Escolher arquivo .md para conferir">
  </div>
  <label for="conf-texto">Ou cole o texto inteiro, com o front matter:</label>
  <textarea id="conf-texto" rows="8" spellcheck="false"></textarea>
  <button id="conf-colado" type="button" class="conf-botao">Conferir o texto colado</button>
  <div id="conf-resultado" aria-live="polite"></div>
</div>
<p class="so-sem-js-conf">O conferidor precisa de JavaScript. Sem ele, confira
  pela tabela abaixo, ou rode <code>conferir.py</code> do repositório
  <a href="https://github.com/brunogreinert2/app-leitura">app-leitura</a>.</p>
"""


def _commit(pasta: Path) -> str:
    try:
        r = subprocess.run(["git", "-C", str(pasta), "rev-parse", "HEAD"],
                           capture_output=True, text=True, timeout=10)
        return r.stdout.strip()[:8] if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def carimbo_dos_commits(app: Path) -> str:
    """Data e hora UTC da geracao e o commit dos dois repositorios. Uma IA le
    copia em cache sem saber; foi o carimbo do rolo que mostrou a um Claude,
    em 2026-09-29, que ele estava lendo a versao velha."""
    agora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    portico = _commit(AQUI)
    leitura = os.environ.get("GITHUB_SHA", "")[:8] or _commit(app)
    partes = [agora]
    if portico:
        partes.append(f"portico {portico}")
    if leitura:
        partes.append(f"app-leitura {leitura}")
    return ", ".join(partes)


def gerar_publico(saida: Path, app: Path, normas: Path):
    hoje = date.today()
    saida.mkdir(parents=True, exist_ok=True)
    acervo = app / "scripts" / "acervo"

    # a norma do conferidor: o esquema e as regras do proprio validador
    sys.path.insert(0, str(acervo))
    import validar_corpus  # noqa: E402
    shutil.copy2(acervo / "frontmatter.schema.json", saida / "frontmatter.schema.json")
    (saida / "regras.json").write_text(
        json.dumps(validar_corpus.exportar_regras(), ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    shutil.copy2(AQUI / "conferidor.js", saida / "conferidor.js")

    carimbo = carimbo_dos_commits(app)
    publico = AQUI / "conteudo" / "publico"
    entradas = entradas_do_diario(AQUI / "diario")
    paginas = [
        ("aba-porta", "Pórtico", "o que é isto", "index", (publico / "00-porta.md").read_text(encoding="utf-8"),
         "A porta de trás do Pedra Angular: como o acervo é feito, a norma que ele segue e como contribuir."),
        ("aba-nota", "Nota editorial", "o que o acervo faz com os textos", "nota-editorial",
         (publico / "nota-editorial.md").read_text(encoding="utf-8"),
         "O que o Pedra Angular normaliza e o que preserva nos textos, de onde eles vêm e como citá-los."),
        ("aba-andamento", "Em andamento", "o que está sendo feito", "andamento", andamento_publico_md(hoje),
         "O que está sendo feito no Pedra Angular agora."),
        ("aba-diario", "Diário", "o que foi feito, e por quê", "diario", diario_md(entradas),
         "Diário de bordo do Pedra Angular: o que entrou no acervo e por quê."),
        ("aba-contribuir", "Contribuir", "como mandar um texto", "contribuir",
         (publico / "contribuir.md").read_text(encoding="utf-8"),
         "O formato de um arquivo do acervo do Pedra Angular, e um conferidor que diz na hora se ele está no padrão."),
        ("aba-normas", "Normas", "o que toda coisa nova obedece", "normas", normas.read_text(encoding="utf-8"),
         "As oito leis e as normas numeradas do ecossistema Pedra Angular."),
        ("aba-pecas", "As peças", "o que existe e o que cada uma faz", "pecas",
         sem_caminhos((AQUI / "conteudo" / "01-pecas.md").read_text(encoding="utf-8")),
         "As peças do ecossistema Pedra Angular e o percurso de um texto, do bruto ao leitor."),
    ]

    todas = []
    for ident, nome, chapeu, base, md, desc in paginas:
        corpo, sumario = md_para_html(md, nivel_base=1)
        if ident == "aba-contribuir":
            # o conferidor entra logo depois da secao que o anuncia
            marca = '<h2 id="o-arquivo">'
            assert marca in corpo, "contribuir.md mudou: ajustar onde entra o conferidor"
            corpo = corpo.replace(marca, HTML_CONFERIDOR + marca, 1)
        todas.append({"id": ident, "nome": nome, "chapeu": chapeu, "html": corpo,
                      "sumario": sumario, "arquivo": "index.html" if base == "index" else f"{base}.html",
                      "base": base, "md": md, "desc": desc})

    temas_css = css_dos_temas((app / "src" / "styles.css").read_text(encoding="utf-8", errors="replace"))
    fontes_css = css_das_fontes(app / "public" / "fonts", False, prefixo="/fonts/")
    estilo = (fontes_css + "\n" + temas_css + "\n" + ESTILO + CSS_CONFERIDOR
              + "\nhtml:not(.js) .so-sem-js-conf{display:block}\n.so-sem-js-conf{display:none}\n")
    (saida / "portico.css").write_text("/* gerado por portico/gerar.py — nao editar */\n" + estilo, encoding="utf-8")
    (saida / "portico.js").write_text("/* gerado por portico/gerar.py — nao editar */\n" + SCRIPT, encoding="utf-8")

    grandes = []
    for a in todas:
        (saida / f"{a['base']}.md").write_text(a["md"], encoding="utf-8")
        pagina = montar([a], "", "", False, publico={
            "todas": todas, "titulo": f"{a['nome']} · Pórtico do Pedra Angular" if a["base"] != "index"
            else "Pórtico do Pedra Angular",
            "descricao": a["desc"], "url": SITE + ("" if a["base"] == "index" else a["arquivo"]),
            "md": f"{a['base']}.md", "carimbo": carimbo})
        if a["base"] == "contribuir":
            pagina = pagina.replace("</body>", '<script src="conferidor.js"></script>\n</body>', 1)
        (saida / a["arquivo"]).write_text(pagina, encoding="utf-8")
        # O que corta a leitura de uma IA e o TEXTO que ela extrai (as tags
        # somem antes), entao a medida e o texto visivel, sem script nem estilo.
        texto = re.sub(r"<(script|style)\b.*?</\1>|<[^>]+>", " ", pagina, flags=re.S)
        texto = html.unescape(re.sub(r"\s+", " ", texto))
        a["tam_texto"] = len(texto.encode("utf-8"))
        if a["tam_texto"] > LIMITE_PAGINA:
            grandes.append(f"{a['arquivo']} ({a['tam_texto'] // 1024} KB de texto)")

    diario = next(a for a in todas if a["base"] == "diario")
    (saida / "feed.xml").write_text(
        feed_atom(entradas, {t: i for _, i, t in diario["sumario"]}), encoding="utf-8")
    if (AQUI / "icone").exists():
        shutil.copytree(AQUI / "icone", saida / "icone", dirs_exist_ok=True)

    print(f"site público: {len(todas)} páginas em {saida}")
    for a in todas:
        print(f"  {a['arquivo']:18} {(saida / a['arquivo']).stat().st_size // 1024:4} KB de HTML · "
              f"{a['tam_texto'] // 1024:3} KB de texto")
    if grandes:
        print("ERRO: página com mais de 80 KB de texto (uma IA leria cortada): " + ", ".join(grandes), file=sys.stderr)
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="Gera o Pórtico do Pedra Angular.")
    ap.add_argument("--embutir", action="store_true",
                    help="embute as fontes em data: URI e gera um arquivo unico")
    ap.add_argument("--fragmento", action="store_true",
                    help="sem <!doctype>/<html>/<head>/<body> — para publicar como artefato")
    ap.add_argument("--saida", default=None, help="nome do arquivo de saida")
    ap.add_argument("--app-leitura", default=None, help="caminho da pasta app-leitura")
    ap.add_argument("--publico", default=None, metavar="PASTA",
                    help="gera o site publico /portico/ (varias paginas) nesta pasta")
    args = ap.parse_args()

    app = Path(args.app_leitura) if args.app_leitura else \
        primeiro_que_existe(CANDIDATOS_APP_LEITURA, "a pasta app-leitura")
    normas = primeiro_que_existe(CANDIDATOS_NORMAS, "o NORMAS.md")

    if args.publico:
        # No deploy nao ha C:\Claude\andamento: o site le o andamento_publico.json
        # que a geracao local exportou e o git levou.
        gerar_publico(Path(args.publico), app, normas)
        return
    catalogo = primeiro_que_existe(CANDIDATOS_CATALOGO,
                                   "o Catalogo_Formatos_Encadernacao.md")
    styles = app / "src" / "styles.css"
    pasta_fontes = app / "public" / "fonts"

    for p, oquee in [(styles, "styles.css"), (pasta_fontes, "public/fonts")]:
        if not p.exists():
            print(f"ERRO: nao achei {oquee} em {p}", file=sys.stderr)
            sys.exit(1)

    conteudo = AQUI / "conteudo"
    fontes_abas = [
        ("aba-portico", "Pórtico", "o que é isto", conteudo / "00-portico.md",
         "conteudo/00-portico.md"),
        ("aba-pecas", "As peças", "o que existe e o que cada uma faz",
         conteudo / "01-pecas.md", "conteudo/01-pecas.md"),
        ("aba-normas", "Normas", "o que toda coisa nova obedece", normas,
         "NORMAS.md"),
        ("aba-formatos", "Formatos físicos", "do A4 ao códice", catalogo,
         "oficina/Catalogo_Formatos_Encadernacao.md"),
    ]

    abas = []
    for ident, nome, chapeu, caminho, rotulo in fontes_abas:
        if not caminho.exists():
            print(f"ERRO: nao achei {caminho}", file=sys.stderr)
            sys.exit(1)
        corpo, sumario = md_para_html(caminho.read_text(encoding="utf-8"), nivel_base=1)
        abas.append({"id": ident, "nome": nome, "chapeu": chapeu,
                     "html": corpo, "sumario": sumario, "fonte": rotulo})

    # Em andamento: logo depois do Portico, porque e o que muda toda semana.
    andamento = primeiro_que_existe(CANDIDATOS_ANDAMENTO, "a pasta andamento/")
    corpo, sumario = md_para_html(andamento_md(andamento, date.today()), nivel_base=1)
    abas.insert(1, {"id": "aba-andamento", "nome": "Em andamento",
                    "chapeu": "o que está em curso e onde parou",
                    "html": corpo, "sumario": sumario,
                    "fonte": "andamento/*.md"})
    n_publicas = exportar_andamento_publico(andamento)
    print(f"andamento_publico.json: {n_publicas} ficha(s) marcada(s) public: true")

    temas_css = css_dos_temas(styles.read_text(encoding="utf-8", errors="replace"))
    fontes_css = css_das_fontes(pasta_fontes, args.embutir)

    if not args.embutir:
        n = copiar_fontes(pasta_fontes, AQUI / "fonts")
        print(f"fontes copiadas para fonts/: {n}")

    padrao_saida = "index.html"
    if args.fragmento:
        padrao_saida = "portico_artefato.html"
    elif args.embutir:
        padrao_saida = "index_embutido.html"
    saida = AQUI / (args.saida or padrao_saida)
    saida.write_text(
        montar(abas, temas_css, fontes_css, args.embutir, args.fragmento),
        encoding="utf-8",
    )
    print(f"gerado: {saida}  ({saida.stat().st_size/1024:.0f} KB)")
    print(f"  normas:   {normas}")
    print(f"  catalogo: {catalogo}")
    print(f"  temas:    {styles}")


if __name__ == "__main__":
    main()
