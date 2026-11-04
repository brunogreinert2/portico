"""Confere os posts do Diário antes de o site se refazer (2026-11-04).

Roda no workflow publicar.yml, a cada push no portico, e aqui na máquina:
    python conferir_diario.py
Erro (o post não entraria, ou entraria quebrado) para o workflow, e o site
continua como estava. Aviso (falta o título, a assinatura) só aparece.
"""
from __future__ import annotations

import datetime
import os
import re
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent / "diario"
ASSINATURA = "> Ὁ Διαφορεύς παρῆν"
NOME = re.compile(r"(\d{4}-\d{2}-\d{2})-[a-z0-9-]+\.md$")
NO_GITHUB = bool(os.environ.get("GITHUB_ACTIONS"))


def dizer(tipo: str, arq: Path, msg: str) -> None:
    rel = arq.relative_to(PASTA.parent).as_posix()
    if NO_GITHUB:
        print(f"::{tipo} file={rel}::{msg}")
    else:
        print(f"{'ERRO' if tipo == 'error' else 'aviso'} {rel}: {msg}")


def main() -> int:
    erros = 0
    posts = 0
    for arq in sorted(PASTA.iterdir()):
        if arq.name == "LEIA.md" or arq.is_dir():
            continue
        if arq.suffix.lower() != ".md":
            dizer("warning", arq, "não é .md: não entra no Diário")
            continue
        m = NOME.match(arq.name)
        if not m:
            dizer("error", arq, "o nome tem de ser AAAA-MM-DD-assunto.md, minúsculas, sem acento nem "
                                "espaço (ex.: 2026-11-04-homero-e-hesiodo.md); assim o post ficaria de fora")
            erros += 1
            continue
        try:
            datetime.date.fromisoformat(m.group(1))
        except ValueError:
            dizer("error", arq, f"a data {m.group(1)} não existe")
            erros += 1
            continue
        try:
            texto = arq.read_bytes().decode("utf-8").replace("\r\n", "\n")
        except UnicodeDecodeError:
            dizer("error", arq, "o arquivo não está em UTF-8 (os acentos e o grego sairiam estragados)")
            erros += 1
            continue
        posts += 1
        corpo = texto
        if texto.startswith("---\n"):
            fim = texto.find("\n---", 4)
            if fim < 0:
                dizer("error", arq, "o cabeçalho abre com --- e não fecha com outro ---")
                erros += 1
                continue
            if not re.search(r"^title:\s*\S", texto[:fim], re.M):
                dizer("warning", arq, "sem title: no cabeçalho; o título sai do nome do arquivo")
            corpo = texto[fim + 4:]
        else:
            dizer("warning", arq, "sem cabeçalho (--- title: ... ---); o título sai do nome do arquivo")
        linhas = [l.strip() for l in corpo.strip().split("\n") if l.strip()]
        if not linhas:
            dizer("error", arq, "o post está vazio")
            erros += 1
            continue
        if linhas[-1] != ASSINATURA:
            dizer("warning", arq, f"a última linha não é a assinatura «{ASSINATURA}»")
    print(f"{posts} post(s) conferido(s), {erros} erro(s)")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
