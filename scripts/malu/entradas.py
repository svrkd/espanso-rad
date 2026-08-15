"""Agrega as tabelas de entrada de cada seção, na ordem em que aparecem no YAML."""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "secoes"))


SECOES = [
    "ombro",
    "cotovelo",
    "punho_mao",
    "quadril",
    "coxa_perna",
    "joelho",
    "tornozelo_pe",
    "cervical",
    "toracolombar",
    "sacro_plexo",
    "diversos",
]

ENTRADAS = []
for nome in SECOES:
    ENTRADAS.extend(importlib.import_module(nome).ENTRADAS)
