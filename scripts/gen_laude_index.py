#!/usr/bin/env python3
"""
Gera a base de referência da skill /laude a partir de match/*.yml.

Saída em skills/laude/references/ (não altera nenhum match/*.yml):
  rotas.md            tabela modalidade | região | seção | índice | nº de entradas | nº de templates
  indices/*.tsv       um índice por (arquivo, banner `# ===`), mais um índice de templates por arquivo
  textos.json         trigger -> replace, todas as entradas
  busca.py            (estático, não gerado) imprime o replace de um ou mais triggers

legado.yml fica de fora: são grafias antigas, com o mesmo texto de um trigger canônico.

Uso:
    python3 scripts/gen_laude_index.py          # regrava a saída
    python3 scripts/gen_laude_index.py --check  # não grava nada; falha se a saída estiver desatualizada

Só stdlib + PyYAML. Saída determinística: mesma entrada, mesmos bytes.

REGRAS DE CLASSIFICAÇÃO (coluna `tipo`), aplicadas nesta ordem
--------------------------------------------------------------
1. template — replace com mais de uma linha e uma destas formas:
     a) 1ª linha em CAIXA ALTA (todas as letras maiúsculas, ao menos 3) seguida de cabeçalho
        de seção em qualquer ponto (Técnica, Método, Metodologia, Análise, Conclusão; com ou
        sem `:`, em Title Case ou CAIXA ALTA);
     b) 1ª linha em CAIXA ALTA seguida de linha em branco, mesmo sem cabeçalho de seção
        (templates de RX: título + corpo);
     c) sem título, mas com ao menos dois cabeçalhos de seção distintos (esqueletos do malu.yml).
   A coluna `titulo` traz a 1ª linha nas formas a/b e fica vazia na forma c.
2. conclusão — trigger `Xc` cujo `X` existe no mesmo arquivo, e o label de `Xc` contém
   "conclus" ou o label de `X` contém "achado descritivo" / "achado geral".
   Só "terminar em c com par" não basta: `hsdc` (crônico), `rmcrc` (com contraste), `retc`
   (cervical). Os `Xc` com `X` no mesmo arquivo que falham nesse teste NÃO são conclusões;
   (templates incluídos) cada índice que contém algum deles abre com uma linha `# ATENÇÃO` que os nomeia.
3. fragmento — replace de uma linha só e: 1ª letra minúscula ("à direita", "lobo inferior
   direito"), ou até 40 caracteres sem `.`, `?` ou `!` final ("Fratura oblíqua", "L4-L5").
4. achado — todo o resto.

Coluna `par`: no achado `X`, o trigger da conclusão `Xc`; na conclusão `Xc`, o trigger `X`.
Coluna `lacunas`: número de caracteres `_` no replace.
Coluna `alternativas`: `sim` se houver `/` entre letras, exceto ALT_EXCLUIDAS (abaixo) e
siglas em CAIXA ALTA de até 4 letras dos dois lados (`DIC/CBR`, `I/II`).

ORGANIZAÇÃO
-----------
- Templates saem dos índices de seção e vão para `<arquivo>__templates.tsv`, um por arquivo.
- Índice acima de LIMITE caracteres é partido na ordem do arquivo em `__1`, `__2`...
- Região: REGIAO_POR_SECAO mapeia cada banner para a taxonomia do CONVENTIONS.md, mais
  Mama, Musculoesquelético (geral) e Técnica. A modalidade vem do arquivo (MODALIDADE),
  e no malu.yml vem do banner (MODALIDADE_MALU).
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
MATCH_DIR = REPO / "match"
OUT = REPO / "skills" / "laude" / "references"
IDX = OUT / "indices"
EXCLUIDOS = {"legado.yml"}
LIMITE = 9000

MODALIDADE = {
    "angio.yml": "TC",
    "geral.yml": "geral",
    "malu.yml": None,  # ver MODALIDADE_MALU
    "mmg.yml": "MMG",
    "rm.yml": "RM",
    "rx.yml": "RX",
    "tc.yml": "TC",
    "tc_abd.yml": "TC",
    "us.yml": "US",
}
MODALIDADE_MALU = {"NÃO-MSK": "US/TC/RM (não MSK)"}
MODALIDADE_MALU_PADRAO = "RM/TC MSK"

CRANIO = "Crânio / Encéfalo / SNC"
FACE = "Face / Pescoço"
COLUNA = "Coluna"
TORAX = "Tórax"
ABDOME = "Abdome / Pelve"
MMSS = "Membros superiores"
MMII = "Membros inferiores"
MSK = "Musculoesquelético (geral)"
VASC = "Vascular"
MAMA = "Mama"
TEMPL = "Templates completos"
TEC = "Técnica"
GERAL = "Gerais / Diversos"

# Região por banner. Arquivos inteiros numa região só ficam em REGIAO_POR_ARQUIVO.
REGIAO_POR_ARQUIVO = {"angio.yml": VASC, "geral.yml": GERAL, "tc_abd.yml": ABDOME, "mmg.yml": MAMA}
REGIAO_POR_SECAO = {
    # rx.yml / tc.yml / rm.yml
    "CRÂNIO / ENCÉFALO / SNC": CRANIO,
    "FACE / ÓRBITAS / SEIOS DA FACE / PESCOÇO / ATM": FACE,
    "COLUNA (CERVICAL, TORÁCICA, LOMBAR, SACROCOCCÍGEA)": COLUNA,
    "COLUNA": COLUNA,
    "TÓRAX (PULMÃO, MEDIASTINO, CORAÇÃO, ARCOS COSTAIS)": TORAX,
    "TÓRAX": TORAX,
    "ABDOME / PELVE": ABDOME,
    "MEMBROS SUPERIORES": MMSS,
    "MEMBROS INFERIORES": MMII,
    "MUSCULOESQUELÉTICO (GERAL)": MSK,
    "VASCULAR": VASC,
    "TEMPLATES COMPLETOS / CABEÇALHOS DE EXAME / ASSINATURAS": TEMPL,
    "GERAIS / DIVERSOS": GERAL,
    "TÉCNICA": TEC,
    # malu.yml
    "OMBRO": MMSS,
    "COTOVELO": MMSS,
    "PUNHO / MÃO / DEDOS": MMSS,
    "QUADRIL / BACIA / SÍNFISE PÚBICA": MMII,
    "COXA / PERNA": MMII,
    "JOELHO": MMII,
    "TORNOZELO / PÉ": MMII,
    "COLUNA CERVICAL": COLUNA,
    "COLUNA TORÁCICA": COLUNA,
    "COLUNA LOMBOSSACRA": COLUNA,
    "SACROILÍACAS / SACROCOCCÍGEA": COLUNA,
    "PLEXOS E DESFILADEIRO TORÁCICO": MSK,
    "TRONCO: ESCÁPULA, PEITORAL, PAREDE ABDOMINAL E ARCOS COSTAIS": MSK,
    "LESÕES ÓSSEAS, TUMORES E OSTEOMIELITE": MSK,
    "MEDIDAS E ÂNGULOS ORTOPÉDICOS": MSK,
    "NÃO-MSK": GERAL,
    "GERAIS / OBSERVAÇÕES": GERAL,
    # us.yml
    "ABDOME TOTAL / SUPERIOR — FÍGADO, VIAS BILIARES, VESÍCULA BILIAR, BAÇO E APÊNDICE": ABDOME,
    "RINS, VIAS URINÁRIAS, BEXIGA E PRÓSTATA": ABDOME,
    "PÉLVICA GINECOLÓGICA E TRANSVAGINAL": ABDOME,
    "OBSTÉTRICA": ABDOME,
    "OBSTÉTRICA — SNC FETAL": ABDOME,
    "OBSTÉTRICA — FACE E PESCOÇO FETAL": ABDOME,
    "OBSTÉTRICA — TÓRAX FETAL": ABDOME,
    "OBSTÉTRICA — PRIMEIRO TRIMESTRE": ABDOME,
    "MAMAS E LINFONODOS AXILARES": MAMA,
    "ALIASES DESCRITIVOS DE MA13–MA86": MAMA,
    "MÚSCULO-ESQUELÉTICO — PARTES MOLES E MÚSCULOS (GERAL)": MSK,
    "MÚSCULO-ESQUELÉTICO — OMBRO": MMSS,
    "MÚSCULO-ESQUELÉTICO — COTOVELO": MMSS,
    "MÚSCULO-ESQUELÉTICO — PUNHO E MÃO": MMSS,
    "MÚSCULO-ESQUELÉTICO — QUADRIL": MMII,
    "MÚSCULO-ESQUELÉTICO — JOELHO": MMII,
    "MÚSCULO-ESQUELÉTICO — TORNOZELO E PÉ": MMII,
    "BOLSA ESCROTAL": ABDOME,
    "PAREDE ABDOMINAL, PARTES MOLES E REGIÃO INGUINAL": ABDOME,
    "TIREOIDE E REGIÃO CERVICAL": FACE,
    "CRÂNIO / TRANSFONTANELA (NEONATAL)": CRANIO,
    "QUADRIL INFANTIL (MÉTODO DE GRAF)": MMII,
    "VASCULAR — DUPLEX SCAN VENOSO DE MEMBROS": VASC,
    "VASCULAR — MAPEAMENTO VENOSO DE MEMBROS INFERIORES": VASC,
    "VASCULAR — DOPPLER ARTERIAL DE MEMBROS SUPERIORES E INFERIORES": VASC,
    "VASCULAR — DOPPLER DE ARTÉRIAS CERVICAIS (CARÓTIDAS E VERTEBRAIS)": VASC,
    "VASCULAR — DOPPLER DO ABDOME SUPERIOR (PORTAL, HEPÁTICO, ESPLÊNICO, MESENTÉRICO)": VASC,
    "VASCULAR — AORTA ABDOMINAL": VASC,
    "FRASES AUXILIARES / CURINGAS (USO TRANSVERSAL)": GERAL,
}

# `/` entre letras que não é escolha do laudador: termo fixo, unidade ou abreviação.
ALT_EXCLUIDAS = {
    "s/c", "c/c", "e/ou",
    "cm/s", "m/s", "ml/min", "ml/s", "mg/dl", "g/dl", "mm/h", "kg/m",
    "inflamatório/infeccioso", "inflamatória/infecciosa",
    "inflamatórios/infecciosos", "inflamatórias/infecciosas",
    "helicoidal/multislice",
    "clínicos/laboratoriais",
    "microangiopatia/gliose", "encefalomalácia/gliose",
    "subacromial/subdeltoidea",
    "atelectasia/consolidação",
    "cabeça/colo",
    "branca/cinzenta",
    "edema/hematoma",
}

SEM_SECAO = "(sem seção)"
BANNER = re.compile(r"^\s*# ={10,}\s*$")
INICIO = re.compile(r'^  - trigger: "')
CABECALHO = re.compile(
    r"^(Técnica|TÉCNICA|Método|MÉTODO|Metodologia|Análise|ANÁLISE|Conclusão|CONCLUSÃO)\s*:?", re.M
)
LETRA = "A-Za-zÀ-ÿ"
BARRA = re.compile(rf"(?<![{LETRA}])([{LETRA}]+)\s*/\s*([{LETRA}]+)(?![{LETRA}])")
ACHADO_DO_PAR = re.compile(r"achado (descritivo|geral)")


def carregar(path):
    """Entradas do arquivo, em ordem, com o banner `# ===` que as precede."""
    texto = path.read_text(encoding="utf-8")
    entradas = yaml.safe_load(texto)["matches"]
    secoes, secao, aberto, esperando = [], SEM_SECAO, False, False
    for linha in texto.split("\n"):
        if BANNER.match(linha):
            aberto = not aberto
            esperando = aberto
            continue
        if esperando and linha.strip().startswith("#"):
            secao = linha.strip().lstrip("#").strip()
            esperando = False
        if INICIO.match(linha):
            if aberto:
                sys.exit(f"{path.name}: trigger dentro de um banner aberto")
            secoes.append(secao)
    if aberto or len(secoes) != len(entradas):
        sys.exit(f"{path.name}: banners desalinhados ({len(secoes)} x {len(entradas)})")
    return [dict(e, secao=s) for e, s in zip(entradas, secoes)]


def caixa_alta(linha):
    letras = [c for c in linha if c.isalpha() and c.lower() != c.upper()]
    return len(letras) >= 3 and all(c.isupper() for c in letras)


def classificar_template(replace):
    """Devolve (é_template, título)."""
    linhas = replace.strip().split("\n")
    if len(linhas) < 2:
        return False, ""
    if caixa_alta(linhas[0]) and (CABECALHO.search(replace) or linhas[1].strip() == ""):
        return True, linhas[0].strip()
    if len({c.lower() for c in CABECALHO.findall(replace)}) >= 2:
        return True, ""
    return False, ""


def fragmento(replace):
    r = replace.strip()
    if "\n" in r:
        return False
    primeira = next((c for c in r if c.isalpha()), "")
    return primeira.islower() or (not re.search(r"[.?!]$", r) and len(r) <= 40)


def alternativas(replace):
    for a, b in BARRA.findall(replace):
        if f"{a}/{b}".lower() in ALT_EXCLUIDAS:
            continue
        if a.isupper() and b.isupper() and len(a) <= 4 and len(b) <= 4:
            continue
        return True
    return False


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def campo(valor, onde):
    if "\t" in valor or "\n" in valor:
        sys.exit(f"tab ou quebra de linha em {onde}: {valor!r}")
    return valor


def modalidade(fname, secao):
    if fname == "malu.yml":
        return MODALIDADE_MALU.get(secao, MODALIDADE_MALU_PADRAO)
    return MODALIDADE[fname]


def regiao(fname, secao):
    if fname in REGIAO_POR_ARQUIVO:
        return REGIAO_POR_ARQUIVO[fname]
    if secao not in REGIAO_POR_SECAO:
        sys.exit(f"{fname}: banner sem região em REGIAO_POR_SECAO: {secao!r}")
    return REGIAO_POR_SECAO[secao]


def classificar(entradas):
    por_trigger = {e["trigger"]: e for e in entradas}
    for e in entradas:
        e["tipo"], e["titulo"], e["par"], e["nao_conclusao"] = "", "", "", False
        tpl, titulo = classificar_template(e["replace"])
        if tpl:
            e["tipo"], e["titulo"] = "template", titulo
            t = e["trigger"]
            e["nao_conclusao"] = t.endswith("c") and t[:-1] in por_trigger
    for e in entradas:
        if e["tipo"]:
            continue
        t = e["trigger"]
        base = por_trigger.get(t[:-1]) if t.endswith("c") else None
        if base is not None:
            if "conclus" in e["label"].lower() or ACHADO_DO_PAR.search(base["label"].lower()):
                e["tipo"], e["par"] = "conclusão", base["trigger"]
                base["par"] = t
                continue
            e["nao_conclusao"] = True
        e["tipo"] = "fragmento" if fragmento(e["replace"]) else "achado"


CABECALHO_TSV = "trigger\tlabel\ttipo\tpar\tlacunas\talternativas\ttitulo"


def linha_tsv(e, fname):
    onde = f"{fname}:{e['trigger']}"
    return "\t".join([
        campo(e["trigger"], onde),
        campo(e["label"], onde),
        e["tipo"],
        e["par"],
        str(e["replace"].count("_")),
        "sim" if alternativas(e["replace"]) else "não",
        campo(e["titulo"], onde),
    ])


def montar_indice(nome, fname, entradas):
    """Devolve [(nome_do_arquivo, conteúdo, nº de linhas)], partido em LIMITE caracteres."""
    def texto(bloco):
        avisos = [e["trigger"] for e in bloco if e["nao_conclusao"]]
        topo = []
        if avisos:
            verbo = "termina" if len(avisos) == 1 else "terminam"
            nao_sao = "NÃO é conclusão" if len(avisos) == 1 else "NÃO são conclusões"
            topo.append(f'# ATENÇÃO: {", ".join(avisos)} {verbo} em "c" mas {nao_sao} (sem par).')
        topo.append(CABECALHO_TSV)
        return "\n".join(topo + [linha_tsv(e, fname) for e in bloco]) + "\n"

    if len(texto(entradas)) <= LIMITE:
        return [(f"{nome}.tsv", texto(entradas), len(entradas))]
    partes, atual = [], []
    for e in entradas:
        if atual and len(texto(atual + [e])) > LIMITE:
            partes.append(atual)
            atual = []
        atual.append(e)
    partes.append(atual)
    return [(f"{nome}__{i}.tsv", texto(p), len(p)) for i, p in enumerate(partes, 1)]


def celula_indice(nome, partes):
    if len(partes) == 1:
        return f"`{nome}`"
    return f"`{nome}__1` a `__{len(partes)}`"


ROTAS_TOPO = """# Rotas da base de referência do /laude

Gerado por `scripts/gen_laude_index.py` a partir de `match/*.yml` (sem `legado.yml`). Não edite à mão.

Ache a linha pela modalidade e pela região, abra o índice em `indices/` (TSV: trigger, label, tipo, par, lacunas, alternativas, titulo) e rode `python3 busca.py <trigger> [...]` para ler o texto, com a conclusão do par logo abaixo. Tipos: template, achado, conclusão, fragmento (regras no topo do gerador). Os templates de cada arquivo ficam em `<arquivo>__templates`; nas linhas de seção, "templates" conta os templates daquele banner que estão lá. "`x__1` a `__3`" é um índice só, partido em até 9.000 caracteres por arquivo; os nomes não levam `.tsv`.

| modalidade | região | seção | índice | entradas | templates |
|---|---|---|---|---|---|
"""


def gerar():
    arquivos = {}
    rotas = []
    textos = {}
    for path in sorted(MATCH_DIR.glob("*.yml")):
        fname = path.name
        if fname in EXCLUIDOS:
            continue
        if fname not in MODALIDADE:
            sys.exit(f"{fname} sem modalidade em MODALIDADE")
        entradas = carregar(path)
        classificar(entradas)
        base = fname[:-4]
        for e in entradas:
            if e["trigger"] in textos:
                sys.exit(f"trigger repetido entre arquivos: {e['trigger']}")
            textos[e["trigger"]] = e["replace"]
        templates = [e for e in entradas if e["tipo"] == "template"]
        secoes = list(dict.fromkeys(e["secao"] for e in entradas))
        for secao in secoes:
            da_secao = [e for e in entradas if e["secao"] == secao]
            n_tpl = sum(1 for e in da_secao if e["tipo"] == "template")
            resto = [e for e in da_secao if e["tipo"] != "template"]
            if not resto:
                continue
            nome = f"{base}__{slug(secao)}"
            partes = montar_indice(nome, fname, resto)
            arquivos.update({n: c for n, c, _ in partes})
            rotas.append((modalidade(fname, secao), regiao(fname, secao), secao,
                          celula_indice(nome, partes), len(resto), n_tpl))
        if templates:
            mod = MODALIDADE_MALU_PADRAO if fname == "malu.yml" else MODALIDADE[fname]
            nome = f"{base}__templates"
            partes = montar_indice(nome, fname, templates)
            arquivos.update({n: c for n, c, _ in partes})
            rotas.append((mod, TEMPL, f"templates de {fname}", celula_indice(nome, partes),
                          len(templates), len(templates)))
    linhas = [f"| {m} | {r} | {s} | {i} | {n} | {t} |" for m, r, s, i, n, t in rotas]
    rotas_md = ROTAS_TOPO + "\n".join(linhas) + "\n"
    textos_json = json.dumps(textos, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    return rotas_md, textos_json, arquivos


def main():
    check = "--check" in sys.argv[1:]
    rotas_md, textos_json, arquivos = gerar()
    esperado = {OUT / "rotas.md": rotas_md, OUT / "textos.json": textos_json}
    esperado.update({IDX / n: c for n, c in arquivos.items()})
    existentes = set(IDX.glob("*.tsv")) if IDX.exists() else set()
    sobrando = sorted(existentes - set(esperado))
    if check:
        ruins = [p for p, c in esperado.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != c]
        if ruins or sobrando:
            for p in ruins:
                print(f"desatualizado: {p.relative_to(REPO)}")
            for p in sobrando:
                print(f"sobrando: {p.relative_to(REPO)}")
            print("rode: python3 scripts/gen_laude_index.py")
            sys.exit(1)
        print(f"OK: {len(arquivos)} índices em dia")
        return
    IDX.mkdir(parents=True, exist_ok=True)
    for p in sobrando:
        p.unlink()
    for p, c in esperado.items():
        p.write_text(c, encoding="utf-8", newline="\n")
    print(f"{len(arquivos)} índices, rotas.md {len(rotas_md)} caracteres")


if __name__ == "__main__":
    main()
