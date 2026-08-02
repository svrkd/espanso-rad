#!/usr/bin/env python3
"""Gera docs/cheatsheet-us.md — índice exaustivo trigger -> label de match/us.yml.

Diferente de docs/poster/poster_data.py (curado, com pareamento achado/
conclusão, colapso de escadas e verificação de deriva em
scripts/check_poster_coverage.py), este cheatsheet não tem trabalho
editorial: é um dump direto, na ordem em que os triggers aparecem no
arquivo, agrupado pelos banners de seção (`# === ... ===`). Por isso nunca
defasa — regenere sempre que match/us.yml mudar, não edite o .md à mão.

Uso:
    python3 scripts/gen_cheatsheet.py
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
US_YML = REPO / "match" / "us.yml"
OUT = REPO / "docs" / "cheatsheet-us.md"

BANNER = re.compile(r'^  # =+$')


def main():
    lines = US_YML.read_text(encoding="utf-8").split("\n")

    sections = []  # [(titulo, [(trigger, label), ...]), ...]
    current_title = None
    current_entries = []

    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if BANNER.match(line) and i + 1 < n and lines[i + 1].strip().startswith("#"):
            titulo = lines[i + 1].strip().lstrip("#").strip()
            if current_title is not None and current_entries:
                sections.append((current_title, current_entries))
            current_title = titulo
            current_entries = []
            i += 3  # banner, título, banner
            continue

        m = re.match(r'^  - trigger: "((?:[^"\\]|\\.)*)"', line)
        if m:
            trigger = m.group(1)
            label = None
            j = i + 1
            while j < n and not re.match(r'^  - trigger: "', lines[j]):
                lm = re.match(r'^    label:\s*(.*)$', lines[j])
                if lm:
                    label = lm.group(1).strip()
                    if label.startswith('"') and label.endswith('"'):
                        label = label[1:-1]
                    break
                j += 1
            current_entries.append((trigger, label or ""))
        i += 1

    if current_title is not None and current_entries:
        sections.append((current_title, current_entries))

    out_lines = [
        "# Cheat-sheet — Ultrassonografia (match/us.yml)",
        "",
        "Índice **exaustivo** trigger → label de `match/us.yml`, gerado automaticamente — "
        "não é curado e não colapsa pares achado/conclusão nem variantes D/E. Para a "
        "referência de parede curada e resumida (uso na sala de exame), ver "
        "`docs/poster-us.pdf` / `docs/poster/poster_data.py`.",
        "",
        "Gerado por `scripts/gen_cheatsheet.py` a partir dos campos `trigger`/`label`. "
        "Não edite este arquivo à mão — as mudanças seriam perdidas na próxima geração; "
        "edite `match/us.yml` e rode o script de novo.",
        "",
    ]
    for titulo, entries in sections:
        out_lines.append(f"## {titulo.title() if titulo.isupper() else titulo}")
        out_lines.append("")
        out_lines.append("| Trigger | Label |")
        out_lines.append("|---|---|")
        for trigger, label in entries:
            trigger_cell = trigger.replace("|", "\\|")
            label_cell = label.replace("|", "\\|")
            out_lines.append(f"| {trigger_cell} | {label_cell} |")
        out_lines.append("")

    OUT.write_text("\n".join(out_lines).rstrip("\n") + "\n", encoding="utf-8")
    total = sum(len(entries) for _, entries in sections)
    print(f"gerado: {OUT} ({total} triggers, {len(sections)} seções)")


if __name__ == "__main__":
    sys.exit(main())
