#!/usr/bin/env python3
"""
beeftext_to_espanso.py
Converte uma lista de combos exportada do BeefText (JSON v10) para arquivos
de matches do Espanso, um por grupo, com word: true em cada match.

Uso:
    python3 beeftext_to_espanso.py <comboList.json> [diretório_de_saída]

O diretório de saída padrão é ./espanso_matches/ (criado automaticamente).
Combos desativados no BeefText são ignorados.
"""

import json
import os
import re
import sys


# ---------------------------------------------------------------------------
# Serialização YAML manual
# PyYAML por padrão serializa strings multiline como double-quoted com \n,
# o que é válido mas pouco legível. Usamos bloco literal (|) para manter
# a estrutura visual dos templates de laudo.
# ---------------------------------------------------------------------------

# Conjunto de valores que o YAML interpreta como booleanos/nulos sem aspas
_YAML_RESERVED = frozenset(
    ['true', 'false', 'null', 'yes', 'no', 'on', 'off', '~']
)

# Caracteres que forçam quoting em scalares YAML plain
_YAML_LEADING_SPECIAL = set(':{}[]|>&*!,%@`"\'-#?')


def _needs_double_quotes(s: str) -> bool:
    """Determina se um scalar single-line precisa de aspas duplas."""
    if not s:
        return True
    if s[0] in _YAML_LEADING_SPECIAL:
        return True
    if s[-1] in (' ', '\t'):
        return True
    if s.lower() in _YAML_RESERVED:
        return True
    # Dois-pontos seguido de espaço dentro da string quebra o parser
    if ': ' in s or s.endswith(':'):
        return True
    return False


def _double_quote(s: str) -> str:
    """Envolve a string em aspas duplas com escapes mínimos."""
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    # Espanso interpreta \n dentro de replace como newline real,
    # mas aqui não há newlines (single-line path).
    return f'"{s}"'


def yaml_replace_value(snippet: str, content_indent: int) -> str:
    """
    Serializa o valor do campo 'replace' como scalar YAML.

    Strings multiline -> bloco literal (|, |-, ou |+).
    Strings single-line -> plain ou double-quoted.

    content_indent: número de espaços de indentação do conteúdo do bloco.

    Chomping:
      '|-'  strip: remove todos os \n finais
      '|'   clip:  preserva exatamente um \n final
      '|+'  keep:  preserva todos os \n finais (incluindo linhas em branco)
    """
    if '\n' not in snippet:
        if _needs_double_quotes(snippet):
            return _double_quote(snippet)
        return snippet

    pad = ' ' * content_indent
    lines = snippet.split('\n')

    # Contar quantos \n há no final do snippet
    trailing_nl = len(snippet) - len(snippet.rstrip('\n'))

    if trailing_nl == 0:
        block_header = '|-'
        # Nenhum ajuste nas lines (split não gerou trailing empty string)
    elif trailing_nl == 1:
        block_header = '|'
        # split('\n') gera um '' extra no final que o clip já compensa;
        # removemos para não criar uma linha em branco redundante no bloco.
        lines = lines[:-1]
    else:
        # >= 2 trailing \n: usar keep para preservar todos
        block_header = '|+'
        # split('\n') gera um '' extra no final (artefato do split);
        # removemos apenas esse, mantendo os '' que representam linhas em branco reais.
        lines = lines[:-1]

    body_lines = []
    for line in lines:
        if line == '':
            # Linha verdadeiramente vazia: sem padding (YAML aceita e preserva)
            body_lines.append('')
        else:
            # Inclui linhas que contêm apenas espaços: pad + line preserva
            # o espaço original após o parser remover o indent do bloco.
            body_lines.append(pad + line)

    body = '\n'.join(body_lines)
    return f'{block_header}\n{body}'


# ---------------------------------------------------------------------------
# Conversão principal
# ---------------------------------------------------------------------------

def sanitize_filename(name: str) -> str:
    """Normaliza um nome de grupo para nome de arquivo YAML seguro."""
    name = name.lower().strip()
    name = re.sub(r'[^a-z0-9]', '_', name)
    name = re.sub(r'_+', '_', name).strip('_')
    return f'{name}.yml'


def convert(input_path: str, output_dir: str) -> None:
    with open(input_path, encoding='utf-8') as f:
        data = json.load(f)

    groups: dict[str, str] = {g['uuid']: g['name'] for g in data['groups']}
    combos: list[dict] = data['combos']

    # Separar por grupo, preservando a ordem original de cada grupo
    by_group: dict[str, list[dict]] = {}
    skipped = 0
    for combo in combos:
        if not combo.get('enabled', True):
            skipped += 1
            continue
        gid = combo.get('group', '')
        gname = groups.get(gid, 'ungrouped')
        by_group.setdefault(gname, []).append(combo)

    os.makedirs(output_dir, exist_ok=True)

    total_matches = 0
    files_written = []

    for gname in sorted(by_group.keys()):
        group_combos = by_group[gname]
        filename = sanitize_filename(gname)
        filepath = os.path.join(output_dir, filename)

        # 'replace:' fica a 4 espaços; conteúdo do bloco literal a 6
        REPLACE_INDENT = 6

        lines = ['matches:']
        for combo in group_combos:
            trigger = combo['keyword']
            snippet = combo['snippet']

            replace_val = yaml_replace_value(snippet, content_indent=REPLACE_INDENT)

            lines.append(f'  - trigger: "{trigger}"')
            lines.append(f'    replace: {replace_val}')
            lines.append(f'    word: true')
            lines.append('')  # linha em branco entre matches para legibilidade

        # Remover última linha em branco e adicionar newline final de arquivo
        content = '\n'.join(lines).rstrip('\n') + '\n'

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        total_matches += len(group_combos)
        files_written.append((filename, len(group_combos)))
        print(f'  {filename:<30} {len(group_combos):>4} matches')

    print()
    print(f'Total: {total_matches} matches em {len(files_written)} arquivo(s)', end='')
    if skipped:
        print(f', {skipped} combo(s) desativado(s) ignorado(s)', end='')
    print('.')
    print(f'Saída: {os.path.abspath(output_dir)}/')


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './espanso_matches'

    if not os.path.isfile(input_path):
        print(f'Erro: arquivo não encontrado: {input_path}', file=sys.stderr)
        sys.exit(1)

    convert(input_path, output_dir)
