#!/usr/bin/env python3
"""
Converte o arquivo HTML de exportação do Texter para YAML compatível com Espanso.

Uso:
    python texter_to_espanso.py <arquivo.html> [saida.yml]

Se o arquivo de saída não for especificado, grava em 'texter_matches.yml'.
"""

import sys
import re
from pathlib import Path

# Mapa de substituições para caracteres cp1252 comuns que latin-1 decodifica
# como controles C1 inválidos em YAML.
CP1252_FIXES = {
    "\x80": "€", "\x82": "‚", "\x83": "ƒ", "\x84": "„", "\x85": "…",
    "\x86": "†", "\x87": "‡", "\x88": "ˆ", "\x89": "‰", "\x8a": "Š",
    "\x8b": "‹", "\x8c": "Œ", "\x8e": "Ž", "\x91": "\u2018", "\x92": "\u2019",
    "\x93": "\u201c", "\x94": "\u201d", "\x95": "•", "\x96": "\u2013",
    "\x97": "\u2014", "\x98": "˜", "\x99": "™", "\x9a": "š", "\x9b": "›",
    "\x9c": "œ", "\x9e": "ž", "\x9f": "Ÿ",
}


def fix_c1(text: str) -> str:
    """Substitui controles C1 (U+0080-U+009F) pelos equivalentes cp1252."""
    for char, replacement in CP1252_FIXES.items():
        text = text.replace(char, replacement)
    # Remove qualquer C1 residual sem mapeamento
    text = re.sub(r'[\x80-\x9f]', '', text)
    return text


def sanitize(text: str) -> str:
    """
    Remove/normaliza caracteres inválidos em YAML:
    - CRLF e CR solitário -> LF
    - Controles C0 (< 0x20) exceto TAB e LF
    - Controles C1 (0x80-0x9F): substitui pelos equivalentes cp1252
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    text = fix_c1(text)
    return text


def extract_matches(html: str) -> list[dict]:
    block_re = re.compile(
        r'<div class="row\d+">\s*'
        r'<span class="hotstring">(.*?)</span>'
        r'<span class="replacement">(.*?)</span>',
        re.DOTALL
    )
    matches = []
    for m in block_re.finditer(html):
        trigger = m.group(1).strip()
        replacement = m.group(2)
        if trigger:
            matches.append({"trigger": trigger, "replacement": replacement})
    return matches


def clean_replacement(text: str) -> str:
    text = sanitize(text)
    lines = [l.rstrip() for l in text.split("\n")]
    return "\n".join(lines).strip()


def escape_yaml_scalar(value: str) -> str:
    if "\n" in value:
        lines = value.split("\n")
        indented = "\n".join("      " + line for line in lines)
        return "|\n" + indented
    needs_quotes = any(c in value for c in ':{}[]|>&*!,%@`"\'\\#?') \
                   or value.startswith(" ") or value.endswith(" ")
    if needs_quotes:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


def build_yaml(matches: list) -> str:
    lines = ["matches:"]
    for m in matches:
        trigger = sanitize(m["trigger"].strip())
        replacement = clean_replacement(m["replacement"])
        yaml_value = escape_yaml_scalar(replacement)
        lines.append("")
        lines.append(f'  - trigger: "{trigger}"')
        lines.append(f"    replace: {yaml_value}")
    lines.append("")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("texter_matches.yml")

    for encoding in ("utf-8", "latin-1", "cp1252"):
        try:
            html = input_path.read_text(encoding=encoding)
            break
        except (UnicodeDecodeError, LookupError):
            continue
    else:
        print("Erro: não foi possível decodificar o arquivo.")
        sys.exit(1)

    matches = extract_matches(html)
    if not matches:
        print("Nenhum match encontrado.")
        sys.exit(1)

    yaml_content = build_yaml(matches)
    output_path.write_text(yaml_content, encoding="utf-8")

    # Verificação pós-geração
    content_bytes = output_path.read_bytes()
    text = content_bytes.decode("utf-8")
    bad = [i for i, c in enumerate(text) if ord(c) < 0x09 or (0x0a < ord(c) < 0x0d) or (0x0d < ord(c) < 0x20) or (0x80 <= ord(c) <= 0x9f)]
    if bad:
        print(f"AVISO: {len(bad)} caracteres inválidos residuais encontrados nas posições: {bad[:10]}")
    else:
        print(f"{len(matches)} matches convertidos → {output_path} (sem caracteres inválidos)")


if __name__ == "__main__":
    main()
