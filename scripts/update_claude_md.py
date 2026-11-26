#!/usr/bin/env python3
"""
Reescreve os blocos automáticos do CLAUDE.md a partir do repositório.

Só toca no que estiver entre <!-- AUTO:nome --> e <!-- /AUTO:nome -->; o resto do
arquivo sai byte a byte igual. Blocos:

  contagens  tabela por arquivo de match/: entradas, templates, pares x/xc, seções.
             As definições de template e de par são as de scripts/gen_laude_index.py
             (importadas, não copiadas): par = conclusão `Xc` reconhecida como tal;
             seção = banner `# ===` distinto.
  arquivos   lista de match/*.yml. Falha se divergir de ALLOWED_PATHS em web/index.html
             ou de MATCH_FILES em scripts/espanso_to_beeftext.py.
  versao     versão e data da release.

Versão e data:
  --versao vX   usa vX (o workflow de release passa a versão que vai taguear, antes de a
                tag existir). Sem --versao, usa a última tag do git (`git describe`).
  Se o bloco já traz essa versão, a data dele é mantida. Senão, a data é a da tag no git,
  se a tag existir, ou a data de hoje em America/Sao_Paulo. Assim, rodar duas vezes
  seguidas não gera diff, e o --check do build_release.sh passa no mesmo job do release.

Uso:
    python3 scripts/update_claude_md.py [--versao vX]          # regrava o CLAUDE.md
    python3 scripts/update_claude_md.py --check [--versao vX]  # não grava; falha se desatualizado

Só stdlib + PyYAML. Saída determinística.
"""
import argparse
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import gen_laude_index as gli  # noqa: E402
from espanso_to_beeftext import MATCH_FILES  # noqa: E402

CLAUDE_MD = REPO / "CLAUDE.md"
WEB = REPO / "web" / "index.html"
BRT = timezone(timedelta(hours=-3))  # America/Sao_Paulo, sem horário de verão desde 2019
BLOCO = re.compile(r"(<!-- AUTO:(\w+) -->\n)(.*?)(<!-- /AUTO:\2 -->)", re.S)
VERSAO_ATUAL = re.compile(r"^Latest release: `([^`]+)`, (\d{4}-\d{2}-\d{2})\.$", re.M)


def falhar(msg):
    sys.exit(f"update_claude_md: {msg}")


def arquivos_match():
    return sorted(p.name for p in (REPO / "match").glob("*.yml"))


def allowed_paths():
    m = re.search(r"const ALLOWED_PATHS = \[(.*?)\];", WEB.read_text(encoding="utf-8"), re.S)
    if not m:
        falhar("ALLOWED_PATHS não encontrado em web/index.html")
    return re.findall(r"^\s*'match/([^']+)'", m.group(1), re.M)


def bloco_contagens():
    linhas = [
        "| File | Entries | Templates | x/xc pairs | Sections |",
        "|---|--:|--:|--:|--:|",
    ]
    tot = [0, 0, 0, 0]
    for nome in arquivos_match():
        es = gli.carregar(REPO / "match" / nome)
        gli.classificar(es)
        n = [
            len(es),
            sum(e["tipo"] == "template" for e in es),
            sum(e["tipo"] == "conclusão" for e in es),
            len({e["secao"] for e in es} - {gli.SEM_SECAO}),
        ]
        tot = [a + b for a, b in zip(tot, n)]
        linhas.append(f"| `{nome}` | " + " | ".join(str(x) for x in n) + " |")
    linhas.append("| **Total** | " + " | ".join(f"**{x}**" for x in tot[:3]) + " | — |")
    return "\n".join(linhas) + "\n"


def bloco_arquivos():
    disco = arquivos_match()
    web, beef = allowed_paths(), MATCH_FILES
    erros = []
    for rotulo, lista in (("ALLOWED_PATHS (web/index.html)", web),
                          ("MATCH_FILES (scripts/espanso_to_beeftext.py)", beef)):
        if len(lista) != len(set(lista)):
            erros.append(f"{rotulo} tem arquivo repetido")
        faltam, sobram = set(disco) - set(lista), set(lista) - set(disco)
        if faltam:
            erros.append(f"{rotulo} não lista: {', '.join(sorted(faltam))}")
        if sobram:
            erros.append(f"{rotulo} lista arquivo inexistente em match/: {', '.join(sorted(sobram))}")
    if erros:
        falhar("listas de arquivos divergem:\n  " + "\n  ".join(erros))
    return "".join(f"- `match/{n}`\n" for n in disco)


def git(*args):
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def bloco_versao(texto_atual, versao):
    if not versao:
        versao = git("describe", "--tags", "--abbrev=0")
        if not versao:
            falhar("nenhuma tag no git; passe --versao")
    atual = VERSAO_ATUAL.search(texto_atual)
    if atual and atual.group(1) == versao:
        data = atual.group(2)
    else:
        data = git("log", "-1", "--format=%cs", f"refs/tags/{versao}") or \
            datetime.now(BRT).strftime("%Y-%m-%d")
    return f"Latest release: `{versao}`, {data}.\n"


def gerar(texto, versao):
    feitos = set()

    def troca(m):
        nome, atual = m.group(2), m.group(3)
        if nome in feitos:
            falhar(f"bloco AUTO:{nome} repetido")
        feitos.add(nome)
        if nome == "contagens":
            novo = bloco_contagens()
        elif nome == "arquivos":
            novo = bloco_arquivos()
        elif nome == "versao":
            novo = bloco_versao(atual, versao)
        else:
            falhar(f"bloco desconhecido AUTO:{nome}")
        return m.group(1) + novo + m.group(4)

    novo = BLOCO.sub(troca, texto)
    faltam = {"contagens", "arquivos", "versao"} - feitos
    if faltam:
        falhar(f"CLAUDE.md sem bloco(s): {', '.join(sorted(faltam))}")
    return novo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--versao")
    a = ap.parse_args()
    texto = CLAUDE_MD.read_text(encoding="utf-8")
    novo = gerar(texto, a.versao)
    if a.check:
        if novo != texto:
            falhar("CLAUDE.md desatualizado; rode python3 scripts/update_claude_md.py"
                   + (f" --versao {a.versao}" if a.versao else ""))
        print("OK — CLAUDE.md em dia")
        return
    if novo != texto:
        CLAUDE_MD.write_text(novo, encoding="utf-8")
        print("CLAUDE.md atualizado")
    else:
        print("CLAUDE.md já estava em dia")


if __name__ == "__main__":
    main()
