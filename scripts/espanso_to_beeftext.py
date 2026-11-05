#!/usr/bin/env python3
"""
espanso_to_beeftext.py
Converte arquivos de matches do Espanso (match/*.yml) para um comboList.json
importável no BeefText (fileFormatVersion 10).

Cada arquivo de entrada vira um grupo do BeefText, nomeado a partir do nome
base do arquivo (ex.: rx.yml -> grupo "rx"). Cada entrada de `matches:` vira
um combo (`keyword` = trigger, `snippet` = replace). Os campos `label` e
`word` do Espanso não têm equivalente no schema do BeefText e são
descartados na conversão.

A saída é determinística: os UUIDs são derivados (uuid5) do nome do grupo e
do trigger, e as datas são uma constante. Assim o mesmo match/*.yml gera
sempre o mesmo arquivo byte a byte, o que permite versionar
beeftext/comboList.json e checar se ele está em dia com --check. Como o UUID
de cada combo depende só de grupo + trigger, ele também fica estável entre
releases.

Uso:
    python3 espanso_to_beeftext.py              # regenera beeftext/comboList.json
    python3 espanso_to_beeftext.py --check      # falha se beeftext/comboList.json estiver desatualizado
    python3 espanso_to_beeftext.py a.yml b.yml -o saida.json

Sem arquivos de entrada, usa MATCH_FILES (todos os match/*.yml, na ordem dos
grupos) e grava em beeftext/comboList.json. Essa é a única lista de arquivos
do BeefText: scripts/build_release.sh não mantém outra.
"""

import argparse
import json
import os
import sys
import uuid

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ordem dos grupos no comboList. Ao criar ou renomear um match/*.yml, atualizar
# aqui (e em ALLOWED_PATHS de web/index.html); a checagem abaixo aborta se
# algum arquivo de match/ ficar de fora.
MATCH_FILES = [
    'geral.yml', 'us.yml', 'tc.yml', 'tc_abd.yml', 'angio.yml', 'rx.yml',
    'rm.yml', 'mmg.yml', 'malu.yml', 'legado.yml',
]

DEFAULT_OUTPUT = os.path.join(REPO_ROOT, 'beeftext', 'comboList.json')

# Namespace fixo para os UUIDs derivados. Não mudar: mudaria todos os UUIDs.
UUID_NS = uuid.UUID('6f1c2a8e-3b7d-5e94-a0c1-7d2e9b4f8a35')

# Data fixa de criação/modificação. O BeefText só a exibe; uma data real
# tornaria o arquivo diferente a cada geração.
TIMESTAMP = '2026-01-01T00:00:00.000'


def stable_uuid(name: str) -> str:
    return f'{{{uuid.uuid5(UUID_NS, name)}}}'


def load_matches(path: str) -> list[dict]:
    with open(path, encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if not data or 'matches' not in data:
        raise ValueError(f"{path}: chave 'matches:' não encontrada")

    matches = data['matches']
    for i, m in enumerate(matches):
        if 'trigger' not in m or 'replace' not in m:
            raise ValueError(
                f"{path}: entrada {i} sem 'trigger' ou 'replace'"
            )
    return matches


def build(input_paths: list[str], verbose: bool = True) -> str:
    groups = []
    combos = []
    seen = set()

    for path in input_paths:
        group_name = os.path.splitext(os.path.basename(path))[0]
        group_uuid = stable_uuid(f'group:{group_name}')

        groups.append({
            'creationDateTime': TIMESTAMP,
            'description': '',
            'enabled': True,
            'modificationDateTime': TIMESTAMP,
            'name': group_name,
            'uuid': group_uuid,
        })

        matches = load_matches(path)
        for m in matches:
            key = f'combo:{group_name}:{m["trigger"]}'
            n = 1
            while key in seen:  # trigger repetido no mesmo arquivo (check_matches.py já acusa)
                n += 1
                key = f'combo:{group_name}:{m["trigger"]}#{n}'
            seen.add(key)
            combos.append({
                'caseSensitivity': 0,
                'creationDateTime': TIMESTAMP,
                'description': '',
                'enabled': True,
                'group': group_uuid,
                'keyword': m['trigger'],
                'matchingMode': 0,
                'modificationDateTime': TIMESTAMP,
                'name': '',
                'snippet': m['replace'],
                'uuid': stable_uuid(key),
            })

        if verbose:
            print(f'  {group_name:<20} {len(matches):>4} combos')

    if verbose:
        print(f'Total: {len(combos)} combos em {len(groups)} grupo(s).')

    combo_list = {
        'combos': combos,
        'fileFormatVersion': 10,
        'groups': groups,
    }
    return json.dumps(combo_list, ensure_ascii=False, indent=2) + '\n'


def default_inputs() -> list[str]:
    match_dir = os.path.join(REPO_ROOT, 'match')
    on_disk = {f for f in os.listdir(match_dir) if f.endswith('.yml')}
    missing = on_disk - set(MATCH_FILES)
    stale = set(MATCH_FILES) - on_disk
    if missing or stale:
        if missing:
            print(f'Erro: fora de MATCH_FILES: {", ".join(sorted(missing))}', file=sys.stderr)
        if stale:
            print(f'Erro: em MATCH_FILES mas ausente de match/: {", ".join(sorted(stale))}', file=sys.stderr)
        sys.exit(1)
    return [os.path.join(match_dir, f) for f in MATCH_FILES]


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Converte match/*.yml (Espanso) para comboList.json (BeefText).'
    )
    parser.add_argument('inputs', nargs='*',
                        help='Arquivo(s) .yml de matches (padrão: todos de match/, na ordem de MATCH_FILES)')
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT,
                        help='Caminho do comboList.json (padrão: beeftext/comboList.json)')
    parser.add_argument('--check', action='store_true',
                        help='Não grava; sai com erro se o arquivo de saída diferir do gerado')
    args = parser.parse_args()

    for path in args.inputs:
        if not os.path.isfile(path):
            print(f'Erro: arquivo não encontrado: {path}', file=sys.stderr)
            sys.exit(1)

    inputs = args.inputs or default_inputs()
    content = build(inputs, verbose=not args.check)

    if args.check:
        try:
            with open(args.output, encoding='utf-8') as f:
                current = f.read()
        except FileNotFoundError:
            current = None
        if current != content:
            rel = os.path.relpath(args.output, REPO_ROOT)
            print(f'ERRO: {rel} desatualizado em relação a match/*.yml. '
                  f'Rode: python3 scripts/espanso_to_beeftext.py', file=sys.stderr)
            sys.exit(1)
        print('OK')
        return

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Saída: {os.path.abspath(args.output)}')


if __name__ == '__main__':
    main()
