#!/usr/bin/env python3
"""
Imprime o texto (replace) de um ou mais triggers, com o par de conclusão logo abaixo.

Uso:
    python3 busca.py <trigger> [<trigger> ...]

Lê textos.json e a coluna `par` de indices/*.tsv, nesta mesma pasta. Só stdlib.
Trigger inexistente: erro em stderr e saída 1 (os demais são impressos assim mesmo).
"""
import json
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def carregar():
    textos = json.loads((AQUI / "textos.json").read_text(encoding="utf-8"))
    pares, tipos = {}, {}
    for tsv in sorted((AQUI / "indices").glob("*.tsv")):
        cab = None
        for linha in tsv.read_text(encoding="utf-8").splitlines():
            if not linha or linha.startswith("#"):
                continue
            campos = linha.split("\t")
            if cab is None:
                cab = campos
                continue
            reg = dict(zip(cab, campos))
            tipos[reg["trigger"]] = reg["tipo"]
            if reg["par"]:
                pares[reg["trigger"]] = reg["par"]
    return textos, pares, tipos


def main():
    triggers = sys.argv[1:]
    if not triggers:
        sys.exit("uso: python3 busca.py <trigger> [<trigger> ...]")
    textos, pares, tipos = carregar()
    faltando = []
    for t in triggers:
        if t not in textos:
            faltando.append(t)
            continue
        print(f"=== {t} ({tipos.get(t, '?')}) ===")
        print(textos[t].rstrip("\n"))
        par = pares.get(t)
        if par and tipos.get(t) != "conclusão":
            print(f"--- conclusão: {par} ---")
            print(textos[par].rstrip("\n"))
        print()
    for t in faltando:
        print(f"ERRO: trigger inexistente: {t}", file=sys.stderr)
    if faltando:
        sys.exit(1)


if __name__ == "__main__":
    main()
