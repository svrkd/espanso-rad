#!/usr/bin/env python3
"""
Lint somente-leitura para match/*.yml — verifica a convenção descrita em
CONVENTIONS.md. Não corrige nada, só reporta.

Uso:
    python3 scripts/check_matches.py
"""
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MATCH_DIR = REPO / "match"
SECTIONED_FILES = {"rx.yml", "tc.yml", "us.yml"}
LEGADO_FILE = "legado.yml"


def parse_entries(path):
    """Retorna lista de (trigger, has_label, has_word, key_order, line_no)."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    starts = [i for i, l in enumerate(lines) if re.match(r'^  - trigger: "', l)]
    starts.append(len(lines))
    entries = []
    for k in range(len(starts) - 1):
        block = lines[starts[k]:starts[k + 1]]
        while block and block[-1].strip() == "":
            block.pop()
        m = re.match(r'^  - trigger: "((?:[^"\\]|\\.)*)"', block[0])
        trigger = m.group(1)
        keys = []
        for line in block:
            if line.startswith("    label:"):
                keys.append("label")
            elif line.startswith("    replace:"):
                keys.append("replace")
            elif line.strip() == "word: true":
                keys.append("word")
        entries.append({
            "trigger": trigger,
            "has_label": "label" in keys,
            "has_word": "word" in keys,
            "key_order": keys,
            "line_no": starts[k] + 1,
        })
    return entries


def is_ascii_lower(trigger):
    return bool(re.fullmatch(r"[a-z0-9]+", trigger))


def main():
    files = sorted(MATCH_DIR.glob("*.yml"))
    all_entries = {}  # trigger -> list of (filename, line_no)
    problems = []

    for path in files:
        fname = path.name
        entries = parse_entries(path)

        seen_in_file = {}
        for e in entries:
            t = e["trigger"]
            seen_in_file.setdefault(t, []).append(e["line_no"])
            all_entries.setdefault(t, []).append((fname, e["line_no"]))

            if not e["has_word"]:
                problems.append(f"{fname}:{e['line_no']}: trigger {t!r} sem `word: true`")
            if not e["has_label"]:
                problems.append(f"{fname}:{e['line_no']}: trigger {t!r} sem `label`")

            expected = ["label", "replace", "word"] if e["has_label"] else ["replace", "word"]
            if e["key_order"] != expected:
                problems.append(
                    f"{fname}:{e['line_no']}: trigger {t!r} fora da ordem canônica "
                    f"(encontrado {e['key_order']}, esperado {expected})"
                )

            if fname != LEGADO_FILE and not is_ascii_lower(t):
                problems.append(
                    f"{fname}:{e['line_no']}: trigger {t!r} fora do charset [a-z0-9] "
                    f"fora de match/{LEGADO_FILE}"
                )

        dups = {t: lines for t, lines in seen_in_file.items() if len(lines) > 1}
        for t, lines in dups.items():
            problems.append(f"{fname}: trigger {t!r} duplicado dentro do arquivo (linhas {lines})")

    cross_dups = {t: locs for t, locs in all_entries.items() if len(set(f for f, _ in locs)) > 1}
    for t, locs in cross_dups.items():
        loc_str = ", ".join(f"{f}:{n}" for f, n in locs)
        problems.append(f"trigger {t!r} duplicado entre arquivos ({loc_str})")

    if not problems:
        print(f"OK — {sum(len(parse_entries(p)) for p in files)} entradas em {len(files)} arquivos, nenhum problema encontrado.")
        return 0

    print(f"{len(problems)} problema(s) encontrado(s):\n")
    for p in problems:
        print(" -", p)
    return 1


if __name__ == "__main__":
    sys.exit(main())
