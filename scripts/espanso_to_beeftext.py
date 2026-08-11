#!/usr/bin/env python3
"""
espanso_to_beeftext.py
Converte um ou mais arquivos de matches do Espanso (match/*.yml) para um
comboList.json importável no BeefText (fileFormatVersion 10).

Cada arquivo de entrada vira um grupo do BeefText, nomeado a partir do nome
base do arquivo (ex.: rx.yml -> grupo "rx"). Cada entrada de `matches:` vira
um combo (`keyword` = trigger, `snippet` = replace). Os campos `label` e
`word` do Espanso não têm equivalente no schema do BeefText e são
descartados na conversão.

Uso:
    python3 espanso_to_beeftext.py <arquivo1.yml> [arquivo2.yml ...] [-o saida.json]

A saída padrão é ./comboList.json.
"""

import argparse
import datetime
import json
import os
import sys
import uuid

import yaml


def new_uuid() -> str:
    return f'{{{uuid.uuid4()}}}'


def now_iso() -> str:
    return datetime.datetime.now().isoformat(timespec='milliseconds')


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


def convert(input_paths: list[str], output_path: str) -> None:
    timestamp = now_iso()

    groups = []
    combos = []

    for path in input_paths:
        group_name = os.path.splitext(os.path.basename(path))[0]
        group_uuid = new_uuid()

        groups.append({
            'creationDateTime': timestamp,
            'description': '',
            'enabled': True,
            'modificationDateTime': timestamp,
            'name': group_name,
            'uuid': group_uuid,
        })

        matches = load_matches(path)
        for m in matches:
            combos.append({
                'caseSensitivity': 0,
                'creationDateTime': timestamp,
                'description': '',
                'enabled': True,
                'group': group_uuid,
                'keyword': m['trigger'],
                'matchingMode': 0,
                'modificationDateTime': timestamp,
                'name': '',
                'snippet': m['replace'],
                'uuid': new_uuid(),
            })

        print(f'  {group_name:<20} {len(matches):>4} combos')

    combo_list = {
        'combos': combos,
        'fileFormatVersion': 10,
        'groups': groups,
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combo_list, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print()
    print(f'Total: {len(combos)} combos em {len(groups)} grupo(s).')
    print(f'Saída: {os.path.abspath(output_path)}')


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Converte match/*.yml (Espanso) para comboList.json (BeefText).'
    )
    parser.add_argument('inputs', nargs='+', help='Arquivo(s) .yml de matches do Espanso')
    parser.add_argument(
        '-o', '--output', default='./comboList.json',
        help='Caminho do comboList.json de saída (padrão: ./comboList.json)'
    )
    args = parser.parse_args()

    for path in args.inputs:
        if not os.path.isfile(path):
            print(f'Erro: arquivo não encontrado: {path}', file=sys.stderr)
            sys.exit(1)

    convert(args.inputs, args.output)


if __name__ == '__main__':
    main()
