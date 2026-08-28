#!/usr/bin/env python3
"""Gera o pôster de parede (HTML com CSS de impressão) a partir de docs/poster/poster_data.py.

Saída: docs/poster-us.html — sem dependência externa. A conversão para PDF
(docs/poster-us.pdf) usa weasyprint e é feita por quem chama este script
(ver scripts/build_release.sh), não aqui.

Calibração de fonte: `html { font-size: 11.8px }` é o piso de legibilidade a
1-2 m de distância (regra validada no design original). NÃO reduza abaixo
disso para forçar o conteúdo a caber numa página só. Se o conteúdo do pôster
crescer (nova seção, mais itens de escada), é aceitável — e esperado — que
ele passe a ocupar 2 ou mais páginas A4 paisagem; o layout em colunas do
CSS já flui para páginas adicionais sem nenhuma mudança de código. Cortar
conteúdo ou espremer fonte para caber numa página é sempre pior do que
imprimir duas.
"""
import html
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "docs" / "poster"))
from poster_data import BLOCOS, MODELOS, CURINGAS  # noqa: E402


def esc(s):
    return html.escape(s)


# Um sufixo só pode ser exibido solto ("usinguinald/e") se o leitor não
# conseguir confundi-lo com um trigger inteiro. Dois ou menos caracteres é o
# limite: cobre os pares D/E e as escadas numéricas, e barra sufixo que forma
# palavra. Sem esse limite, `["ut5", "ut8", "utbicorno"]` saía como
# "ut5/8/bicorno" — indistinguível de "ut7/bicorno", que na linha logo acima
# são dois triggers inteiros e não prefixo + sufixo.
SUFIXO_MAX = 2

# Geometria da calha do índice.
#
# 13.5mm não cabe o trigger mais largo que a coluna exibe por extenso
# ("utbicorno", 9 caracteres, ~63px contra ~51px de calha). Isso NÃO corta nem
# faz o texto invadir a coluna vizinha: `.pfx` é item flex sem `min-width: 0`,
# então `min-width: auto` faz a caixa crescer até o min-content, e o efeito é
# local — só aquela linha fica com a calha ~3mm mais larga e o corpo começando
# mais à direita que as demais.
#
# Alargar a calha para uniformizar sai caro e foi medido: a 17mm o corpo perde
# 3.5mm em TODAS as linhas, e como os itens de escada são `white-space: nowrap`,
# duas linhas que cabiam passam a ultrapassar o filete da coluna ("não
# caracterizado no presente estudo…" e "síndrome intersticial, perfil B'…"),
# enquanto o transbordo pré-existente da escada `tx` piora de 26px para 39px,
# entrando na coluna vizinha. Uma linha desalinhada custa menos que três linhas
# invadindo colunas, então a calha fica estreita de propósito.
#
# O recuo das notas é derivado daqui, nunca digitado: quando este valor mudou
# e o recuo ficou para trás, as duas notas do pôster desalinharam 3.5mm do
# texto que anotam.
CALHA_MM = 13.5
GAP_MM = 1.4
RECUO_NOTA_MM = round(CALHA_MM + GAP_MM, 2)


def compacta(triggers):
    """Deriva uma exibição compacta de uma lista de triggers para a coluna
    de índice, sem que a compactação vire a fonte da verdade: os triggers
    reais continuam explícitos em poster_data.py, isto é só apresentação."""
    triggers = list(triggers)
    if len(triggers) == 1:
        return triggers[0]
    prefix = triggers[0]
    for t in triggers[1:]:
        while prefix and not t.startswith(prefix):
            prefix = prefix[:-1]
    if prefix and all(0 < len(t) - len(prefix) <= SUFIXO_MAX for t in triggers):
        sufixos = [t[len(prefix):] for t in triggers]
        return f"{prefix}{'/'.join(sufixos)}"
    return "/".join(triggers)


def render_escada_itens(itens):
    partes = []
    for item in itens:
        sufixo, rotulo = item[0], item[1]
        partes.append(f'<span class="it"><b>{esc(sufixo)}</b>&#8202;{esc(rotulo)}</span>')
    return " ".join(partes)


def render_linha(linha):
    tipo = linha[0]

    if tipo == "nota":
        _, texto = linha
        return f'<div class="nota">{esc(texto)}</div>'

    if tipo == "escada":
        _, prefixo, orgao, itens = linha
        escada_html = f'<div class="escada">{render_escada_itens(itens)}</div>' if itens else ""
        return (
            '<div class="linha">'
            f'<div class="pfx">{esc(prefixo)}</div>'
            f'<div class="corpo"><div class="org">{esc(orgao)}</div>{escada_html}</div>'
            "</div>"
        )

    if tipo == "triggers":
        _, triggers, orgao, rotulo = linha
        pfx = compacta(triggers)
        return (
            '<div class="linha">'
            f'<div class="pfx">{esc(pfx)}</div>'
            f'<div class="corpo"><div class="org">{esc(orgao)}</div>'
            f'<div class="escada"><span class="it">{esc(rotulo)}</span></div></div>'
            "</div>"
        )

    raise ValueError(f"tipo de linha desconhecido: {tipo!r}")


blocos_html = []
for titulo, linhas in BLOCOS:
    corpo = "".join(render_linha(l) for l in linhas)
    blocos_html.append(f'<section class="bloco"><h2>{esc(titulo)}</h2>{corpo}</section>')

modelos_html = " ".join(
    f'<span class="mod"><b>{esc(compacta(triggers))}</b>&#8202;{esc(desc)}</span>'
    for triggers, desc in MODELOS
)
curingas_html = " ".join(
    f'<span class="mod"><b>{esc(compacta(triggers))}</b>&#8202;{esc(desc)}</span>'
    for triggers, desc in CURINGAS
)

DOC = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>US — referência de triggers</title>
<style>
@page {{ size: A4 landscape; margin: 7mm 8mm; }}
* {{ box-sizing: border-box; }}
html {{ font-size: 11.8px; }}
body {{
  margin: 0;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  color: #000; background: #fff;
  -webkit-font-smoothing: antialiased;
}}

/* ---------- cabeçalho: a gramática. É a única coisa que se decora. ---------- */
.topo {{
  display: flex; align-items: baseline; gap: 6mm;
  border-bottom: 1.6pt solid #000; padding-bottom: 1.6mm; margin-bottom: 2.6mm;
}}
.titulo {{ font-size: 2.05rem; font-weight: 800; letter-spacing: -.02em; line-height: 1; }}
.titulo em {{ font-style: normal; font-weight: 300; }}
.regras {{ display: flex; gap: 4.5mm; font-size: .96rem; line-height: 1.25; }}
.regra b {{ font-family: "SF Mono", "DejaVu Sans Mono", monospace; font-weight: 700; }}
.regra span {{ color: #444; }}

/* ---------- corpo em colunas — flui para páginas extras se precisar ---------- */
.grade {{ column-count: 3; column-gap: 5mm; column-rule: .4pt solid #bbb; }}
.bloco {{ break-inside: avoid-column; margin-bottom: 2.4mm; }}
h2 {{
  font-size: .82rem; font-weight: 800; letter-spacing: .1em;
  margin: 0 0 .9mm; padding-bottom: .5mm; border-bottom: .7pt solid #000;
}}

/* a linha: prefixo pendurado numa calha à esquerda = índice para o olho */
.linha {{ display: flex; gap: {GAP_MM}mm; margin-bottom: .85mm; break-inside: avoid; }}
.pfx {{
  flex: 0 0 {CALHA_MM}mm; text-align: right;
  font-family: "SF Mono", "DejaVu Sans Mono", monospace;
  font-size: 1.02rem; font-weight: 700; line-height: 1.15;
  letter-spacing: -.02em;
}}
.corpo {{ flex: 1 1 auto; min-width: 0; }}
.org {{ font-size: .93rem; font-weight: 600; line-height: 1.15; }}
.escada {{ font-size: .88rem; line-height: 1.3; color: #222; }}
.it {{ white-space: nowrap; margin-right: 1.7mm; }}
.it b {{
  font-family: "SF Mono", "DejaVu Sans Mono", monospace;
  font-weight: 700; font-size: .93rem;
}}
.nota {{
  font-size: .84rem; color: #555; font-style: italic;
  /* recuo = calha + gap, para a nota começar na mesma coluna do corpo das
     linhas que ela anota; derivado, nunca digitado à mão. */
  margin: .3mm 0 .3mm {RECUO_NOTA_MM}mm; line-height: 1.2;
}}

/* ---------- rodapé: modelos e curingas ---------- */
.rodape {{ border-top: 1.6pt solid #000; margin-top: 1.6mm; padding-top: 1.4mm; }}
.rodape h3 {{
  font-size: .78rem; font-weight: 800; letter-spacing: .1em;
  margin: 0 0 .7mm; display: inline-block; margin-right: 2.5mm;
}}
.faixa {{ font-size: .87rem; line-height: 1.42; }}
.mod {{ white-space: nowrap; margin-right: 2.6mm; }}
.mod b {{
  font-family: "SF Mono", "DejaVu Sans Mono", monospace;
  font-weight: 700; font-size: .9rem;
}}
</style></head><body>

<div class="topo">
  <div class="titulo">US <em>· triggers</em></div>
  <div class="regras">
    <div class="regra"><b>prefixo</b>+<b>nº</b><br><span>órgão + achado</span></div>
    <div class="regra"><b>…c</b><br><span>vira conclusão</span></div>
    <div class="regra"><b>us…</b><br><span>modelo completo</span></div>
    <div class="regra"><b>Alt+Space</b><br><span>busca o resto</span></div>
  </div>
</div>

<div class="grade">{''.join(blocos_html)}</div>

<div class="rodape">
  <div class="faixa"><h3>MODELOS</h3>{modelos_html}</div>
  <div class="faixa"><h3>CURINGAS</h3>{curingas_html}</div>
</div>

</body></html>"""

out = REPO / "docs" / "poster-us.html"
out.write_text(DOC, encoding="utf-8")
print("gerado:", out)
