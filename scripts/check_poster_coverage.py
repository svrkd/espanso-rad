#!/usr/bin/env python3
"""
Lint somente-leitura de deriva entre match/us.yml e docs/poster/poster_data.py.

Não corrige nada, só reporta. Sai com código 1 se houver problema.

Regras:
  - ERRO: trigger presente em poster_data.py que não existe em match/us.yml
          (referência quebrada — o pôster está mentindo).
  - ERRO: trigger presente em match/us.yml que não está no pôster e não casa
          nenhuma regra de EXCLUSOES (match novo sem decisão editorial).

Uso:
    python3 scripts/check_poster_coverage.py
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
US_YML = REPO / "match" / "us.yml"
POSTER_DIR = REPO / "docs" / "poster"

sys.path.insert(0, str(POSTER_DIR))
from poster_data import EXCLUSOES, todos_os_triggers  # noqa: E402


def triggers_em_us_yml():
    text = US_YML.read_text(encoding="utf-8")
    lines = text.split("\n")
    starts = [i for i, l in enumerate(lines) if re.match(r'^  - trigger: "', l)]
    triggers = []
    for i in starts:
        m = re.match(r'^  - trigger: "((?:[^"\\]|\\.)*)"', lines[i])
        triggers.append(m.group(1))
    return triggers


def excluido(trigger, regras):
    return any(re.search(pat, trigger) for pat, _motivo in regras)


def main():
    us_triggers = triggers_em_us_yml()
    us_set = set(us_triggers)
    poster_triggers = todos_os_triggers()

    problems = []

    quebrados = sorted(poster_triggers - us_set)
    for t in quebrados:
        problems.append(f"referência quebrada: {t!r} está em poster_data.py mas não existe em match/us.yml")

    nao_classificados = sorted(
        t for t in us_triggers
        if t not in poster_triggers and not excluido(t, EXCLUSOES)
    )
    for t in nao_classificados:
        problems.append(f"não classificado: {t!r} existe em match/us.yml, não está no pôster e não casa nenhuma EXCLUSOES")

    if not problems:
        print(
            f"OK — {len(us_triggers)} triggers em match/us.yml, "
            f"{len(poster_triggers)} cobertos pelo pôster, "
            f"0 não-classificados, 0 referências quebradas."
        )
        return 0

    print(f"{len(problems)} problema(s) encontrado(s):\n")
    for p in problems:
        print(" -", p)
    return 1


if __name__ == "__main__":
    sys.exit(main())
