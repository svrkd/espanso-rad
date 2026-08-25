#!/usr/bin/env python3
"""
Gera match/malu.yml a partir de intervalos de linha do caderno de trabalho da
radiologista de origem (mascaras_luisa.txt). O texto NUNCA é redigitado: cada
entrada aponta para as linhas da fonte, o que garante fidelidade verbatim por
construção.

    python3 scripts/build_malu.py <mascaras_luisa.txt> [--check]

O arquivo-fonte NÃO está no repositório: é o caderno pessoal de outra pessoa e
traz nome de paciente, nome de colega e datas de exame. Sem ele o YAML não
regenera — mas o registro das decisões continua auditável aqui mesmo:

  - scripts/malu/secoes/*.py  o que virou entrada, com a faixa de linhas
  - scripts/malu/exclusoes.py o que ficou de fora, com o motivo de cada linha
  - docs/malu-alteracoes.txt  o que foi alterado no texto, por regra e classe

Seis guardas abortam antes de escrever qualquer coisa: charset e duplicata de
trigger, replace repetido (dentro do arquivo e contra os demais match/*.yml,
comparação normalizada), colisão com triggers existentes, regra de correção
sem uso, cobertura (linha da fonte fora de toda faixa precisa de motivo
declarado), e rótulo do caderno dentro do texto de uma entrada.
"""
import re
import sys
import unicodedata
import yaml as _yaml_mod
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "match" / "malu.yml"
LOG = REPO / "docs" / "malu-alteracoes.txt"
sys.path.insert(0, str(Path(__file__).resolve().parent))

# --------------------------------------------------------------------------
# Correções de português. (errado, certo, nota). Aplicadas como substituição
# literal sobre o texto extraído. Uma regra que nunca casa é erro — o log tem
# de refletir só o que de fato mudou.
# --------------------------------------------------------------------------
CORRECOES = [
    # --- placeholders uniformizados para `_` (pedido do dono do repositório).
    # Aqui só o caso multi-dimensional: lesão nodular, que ela mede sempre em
    # três eixos ("medindo cerca de 0,8 x 1,3 x 0,6 cm"). O resto é regex.
    ("extensor, medindo mm ,", "extensor, medindo _ x _ x _ mm,",
     "placeholder uniformizado para _"),
    # --- revisão clínica, segunda leva (lotes pé/colunas e quadril/joelho).
    # Mesmas classes A e B já autorizadas.
    # laudo de antepé (II metatarsofalângica): fêmur não existe no campo.
    ("achatamento da cabeça femoral", "achatamento da cabeça do II metatarso",
     "anatomia/clínica corrigida a pedido do usuário"),
    # em L5-S1 a emergente é L5; S1 é a descendente. As outras ~30 entradas
    # dela usam a convenção certa.
    ("tocando a raiz emergente esquerda de S1", "tocando a raiz descendente esquerda de S1",
     "anatomia/clínica corrigida a pedido do usuário"),
    # no forame L3-L4 emerge L3; abaullomb3 e abaullomb25, mesmo nível, dizem
    # "emergente de L3".
    ("raiz emergente foraminal de L4", "raiz emergente foraminal de L3",
     "anatomia/clínica corrigida a pedido do usuário"),
    # fibromatose plantar: a fáscia é plantar, e o resto do bloco é antepé.
    ("banda central da fáscia palmar", "banda central da fáscia plantar",
     "anatomia/clínica corrigida a pedido do usuário"),
    # 1,1 x 0,8 x 0,5 cm pela elipsoide (0,52·a·b·c) dá 0,2 cm³, não 2,3 —
    # e "diminuta" contradizia o valor. As outras duas entradas com volume
    # declarado batem com a mesma fórmula.
    ("volume de 2,3 cm³", "volume de 0,2 cm³",
     "anatomia/clínica corrigida a pedido do usuário"),
    # "iliopúbico" designa o ramo púbico superior; o inferior é o
    # isquiopúbico, como ela escreve em fxisquiopubico1 e ulceragluteo1.
    ("ramo iliopúbico inferior", "ramo isquiopúbico",
     "anatomia/clínica corrigida a pedido do usuário"),
    # Judet-Letournel: as colunas acetabulares são anterior e posterior.
    ("colunas anterior e medial", "colunas anterior e posterior",
     "anatomia/clínica corrigida a pedido do usuário"),
    # canal não espessa: as frases gêmeas (abaulcerv14, 15, abaulcervtc4)
    # terminam em "estreitamento do canal vertebral".
    ("determina pequeno espessamento do canal vertebral",
     "determina pequeno estreitamento do canal vertebral",
     "anatomia/clínica corrigida a pedido do usuário"),
    # --- revisão clínica: níveis A e B, autorizados pelo dono do repositório
    # (radiologista) depois da revisão de 2026-08. Mudam conteúdo clínico, o
    # que o mandato original proibia, por isso contam em classe própria.
    #
    # Nível A — a própria máscara prova o erro.
    # gadolínio é contraste de RM; esta máscara é TC da mão.
    ("técnica helicoidal/multislice com aquisições axiais e reconstruções multiplanares. Administrado meio de contraste paramagnético",
     "técnica helicoidal/multislice com aquisições axiais e reconstruções multiplanares. Administrado meio de contraste iodado",
     "anatomia/clínica corrigida a pedido do usuário"),
    # os colaterais da metacarpofalângica inserem na base da falange proximal;
    # o próprio laudo diz "subluxação volar da base da falange proximal".
    ("junto à inserção na base da falange distal",
     "junto à inserção na base da falange proximal",
     "anatomia/clínica corrigida a pedido do usuário"),
    # não existe: o "longo" é do extensor radial longo do carpo. Ela escreve
    # "flexor radial do carpo" corretamente em outras duas entradas.
    ("flexor radial longo do carpo", "flexor radial do carpo",
     "anatomia/clínica corrigida a pedido do usuário"),
    # o par anatômico do reto femoral é direta/indireta; "direita" ainda punha
    # lateralidade direita dentro de uma RM de coxa esquerda.
    ("cabeça direita do retofemoral", "cabeça direta do retofemoral",
     "anatomia/clínica corrigida a pedido do usuário"),
    # veia porta de 1,2 mm é impossível, e a referência da própria frase diz
    # "nl até 12mm".
    ("medindo 1,2 mm (nl até 12mm)", "medindo 1,2 cm (nl até 12mm)",
     "anatomia/clínica corrigida a pedido do usuário"),
    # o achado inteiro é à esquerda (interescalênico esquerdo, duas vezes).
    ("espaço costoclavicular direito", "espaço costoclavicular esquerdo",
     "anatomia/clínica corrigida a pedido do usuário"),
    #
    # Nível B — coerente consigo mesmo, mas contraria a literatura.
    # ACR TI-RADS: TR3 = 1/3/5 anos (correto na máscara), TR4 = 1/2/3/5,
    # TR5 = anual por até 5 anos. Só os intervalos estavam errados.
    ("US ≥1,0cm – 1 / 3 / 5 anos", "US ≥1,0cm – 1 / 2 / 3 / 5 anos",
     "anatomia/clínica corrigida a pedido do usuário"),
    ("US ≥0,5cm – 1 / 3 / 5 anos", "US ≥0,5cm – anual por até 5 anos",
     "anatomia/clínica corrigida a pedido do usuário"),
    # Bankart é lesão do lábio ântero-inferior; a frase seguinte descreve
    # separadamente a variante ântero-superior (complexo de Buford).
    ("na região anterossuperior, sugerindo lesão de Bankart",
     "na região anteroinferior, sugerindo lesão de Bankart",
     "anatomia/clínica corrigida a pedido do usuário"),
    # com retináculo insuficiente o ulnar subluxa anteriormente, por sobre o
    # epicôndilo medial; posteromedial é a posição normal dele no túnel.
    ("subluxação posteromedial do nervo ulnar", "subluxação anterior do nervo ulnar",
     "anatomia/clínica corrigida a pedido do usuário"),
    # I sobre II compartimento é a intersecção proximal; a distal é III sobre
    # II, no tubérculo de Lister.
    ("síndrome da intersecção do antebraço distal", "síndrome da intersecção proximal",
     "anatomia/clínica corrigida a pedido do usuário"),
    # no espaço costoclavicular o vaso é a subclávia; a axilar só existe
    # lateral à borda lateral da primeira costela.
    ("veia axilar bilateral", "veia subclávia bilateral",
     "anatomia/clínica corrigida a pedido do usuário"),
    # nódulo justatendíneo de dedo: o epônimo é o da bainha tendínea. Ela
    # escreve a forma completa corretamente em outras duas entradas.
    ("sugerindo lesão tumoral (tumor de células gigantes?)",
     "sugerindo lesão tumoral (tumor de células gigantes da bainha tendínea?)",
     "anatomia/clínica corrigida a pedido do usuário"),
    # a bursa do semimembranoso é do joelho; na origem isquiática é a
    # isquioglútea.
    ("Mínima bursite do semimembranoso", "Mínima bursite isquioglútea",
     "anatomia/clínica corrigida a pedido do usuário"),
    # a técnica não declarava gadolínio, mas a análise descreve realce em três
    # pontos.
    ("Exame realizado com sequências FSE e Gradient echo, com cortes multiplanares de 2 e 3 mm de espessura.",
     "Exame realizado com sequências FSE e Gradient echo, com cortes multiplanares de 2 e 3 mm de espessura. Administrado meio de contraste paramagnético por via intravenosa.",
     "anatomia/clínica corrigida a pedido do usuário"),
    # --- anatomia: lapsos da autora, corrigidos a pedido explícito do dono do
    # repositório (radiologista). Fora do mandato original "só português e
    # typo", por isso contam em classe própria no log, nunca como português.
    # Rizartrose é a artrose trapeziometacarpal: o osso é o metacarpo.
    ("trapézio e a base do primeiro metatarso",
     "trapézio e a base do primeiro metacarpo",
     "anatomia corrigida a pedido do usuário"),
    # Metacarpofalângica do polegar: a própria frase, adiante, diz "inserção
    # no metacarpo". O literal é longo porque "cabeça do metatarso" também
    # ocorre num laudo de pé, onde está certo.
    ("junto a origem da cabeça do metatarso",
     "junto a origem da cabeça do metacarpo",
     "anatomia corrigida a pedido do usuário"),
    # --- ombro ---
    ("Reção", "Reação", "typo"),
    ("DAS PERNAS E COXAS (miosite de hepatopata, reconversao/medula hematopoietica)", "DAS PERNAS E COXAS", "nota de estudo removida"),
    ("(SUBCLAVIAS E JUGULARES) meu", "(SUBCLÁVIAS E JUGULARES)", "marca de rascunho removida"),
    ("Luxação inveterada posterior glenoumeral. (luxação que nao voltou).", "Luxação inveterada posterior glenoumeral.", "nota de estudo removida"),
    ("componente extra ósseo", "componente extraósseo", "grafia"),
    ("subcondral dpa faceta", "subcondral da faceta", "typo"),
    ("com com pequeno fragmento", "com pequeno fragmento", "palavra repetida"),
    ("hipertrofia ósseas dos processos espinhosos", "hipertrofia óssea dos processos espinhosos", "concordância"),
    ("Estes materiais  manipulação geram", "Estes materiais geram", "resíduo de rascunho"),
    ("(normal de 0,3 a 0,6- passo de 0,6 é chiare antes da insinuação)", "(normal de 0,3 a 0,6 cm)", "unidade faltante inserida, além de nota de estudo removida"),
    ("Análise: ( geralmente rompe mais distal", "Análise:", "nota de estudo removida"),
    ("Demais/  Ligamentos intrínsecos", "Ligamentos intrínsecos", "resíduo de rascunho"),
    ("id Tendinopatia e tenossinovite do I compartimento", "Tendinopatia e tenossinovite do I compartimento", "resíduo de rascunho"),
    ("subcondrais. id Artropatia", "subcondrais. Artropatia", "resíduo de rascunho"),
    ("relacionado a atrito.( id Sinais de impacto isquiofemoral)", "relacionado a atrito.", "nota de estudo removida"),
    ("atrito/hipersolicitação mecânica.(Sinais de atrito do trato iliotibial. id)", "atrito/hipersolicitação mecânica.", "nota de estudo removida"),
    (".Herniações intrassomáticas", "Herniações intrassomáticas", "pontuação espúria"),
    ("radiocárpical", "radiocárpica", "typo"),
    ("porçào", "porção", "acentuação"),
    ("intrínsecas e extrínsecos do punho", "intrínsecas e extrínsecas do punho", "concordância"),
    ("tuberosidades isquiáticas .", "tuberosidades isquiáticas.", "espaço antes do ponto"),
    ("dos limites da normalidade.]", "dos limites da normalidade.", "colchete do export"),
    ("DO JOELHO ESQUERDO (MARCO B)", "DO JOELHO ESQUERDO", "nome de colega removido"),
    ("anteriores e posteriores.calci", "anteriores e posteriores.", "resíduo de rascunho"),
    ("cisto artrossinovial.fratura", "cisto artrossinovial.", "resíduo de rascunho"),
    ("inferindo sinovite.artrite", "inferindo sinovite.", "resíduo de rascunho"),
    ("sem retração.//// sobrecarga mecanica", "sem retração.", "resíduo de rascunho"),
    ("(sesamoidite).l", "(sesamoidite).", "resíduo de rascunho"),
    ("impacto subtalar.(Impacto subtalar processo lateral do talus com a margem do calcâneo adjacente ) tem que tem desvio de eixo do pe para ter impacto",
     "impacto subtalar.", "nota de estudo removida"),
    ("do ligamento iliofemoral.( se oblitera eh capsulite)", "do ligamento iliofemoral.", "nota de estudo removida"),
    ("id ?: O conjunto", "O conjunto", "resíduo de rascunho"),
    (". guinel coloca na conclusão impacto isquiofemoral", ".", "nota de estudo removida"),
    ("lipomatose→ aumento da gordua", "Aumento da gordura", "nota de estudo e typo"),
    ("C7-T1: (nao tem uncovertebral)", "C7-T1:", "nota de estudo removida"),
    ("C2,  T2 e T2", "C2, T2 e T2", "espaço duplo"),
    ("compativel", "compatível", "acentuação"),
    ("esquerda.Controle", "esquerda. Controle", "espaço após ponto"),
    ("eletroneuromiografia.F", "eletroneuromiografia.", "resíduo de rascunho"),
    ("RESSONANCIA MAGNETICA", "RESSONÂNCIA MAGNÉTICA", "acentuação"),
    ("radial. id Extensa", "radial. Extensa", "resíduo de rascunho"),
    ("intrassubstancias, sem", "intrassubstanciais, sem", "concordância"),
    ("componentes,além", "componentes, além", "espaço após vírgula"),
    ("subjacente as tuberosidades", "subjacentes às tuberosidades", "concordância/crase"),
    ("rotura parcial insercionais", "rotura parcial insercional", "concordância"),
    ("superiores,sem", "superiores, sem", "espaço após vírgula"),
    ("muscular xxcom edema", "muscular XX com edema", "marcador de preenchimento reconstruído"),
    ("denervação., sem", "denervação, sem", "pontuação espúria"),
    ("dos ligamento acromioclaviculares", "dos ligamentos acromioclaviculares", "concordância"),
    ("Conclusão:calcari", "Conclusão:", "resíduo de rascunho"),
    ("supraepinhal", "supraespinhal", "typo"),
    ("acomentendo", "acometendo", "typo"),
    ("tendinea,sem", "tendínea, sem", "acentuação e espaço"),
    ("0,6 no eixo", "0,6 cm no eixo", "unidade faltante"),
    # --- casos em que a forma sem acento é typo de OUTRA palavra: têm de vir
    # antes das regras genéricas de acentuação, senão estas as pré-empitam ---
    ("exposição do osseo subcondral", "exposição do osso subcondral", "typo: o substantivo é osso, não o adjetivo ósseo"),
    ("area de alteração ossea", "Área de alteração óssea", "acentuação e maiúscula inicial"),
    ("I, II,III e IV ,metatarsos", "I, II, III e IV metatarsos", "pontuação"),
    ("com intensidade de sinal normal. , exceto", "com intensidade de sinal normal, exceto", "pontuação espúria"),
    ("medular ´óssea", "medular óssea", "acento solto do export"),
    ("edema subcorticais junto a areas", "Edemas subcorticais junto a áreas", "concordância inferida: a fonte é ambígua entre singular e plural"),
    # --- geral ---
    ("presevardos", "preservados", "typo"),
    ("curvatuva", "curvatura", "typo"),
    ("Espassador", "Espaçador", "typo"),
    ("Espessrotamento", "Espessamento", "palavra reconstruída: fragmento colado no meio dela"),
    ("mielomalcea", "mielomalácia", "typo"),
    ("significaticas", "significativas", "typo"),
    ("Braastup", "Baastrup", "grafia do epônimo"),
    ("fibricicatricial", "fibrocicatricial", "typo"),
    ("coonente", "componente", "typo"),
    ("adjacantes", "adjacentes", "typo"),
    ("Discoparia", "Discopatia", "typo"),
    ("intrassubstancias", "intrassubstanciais", "concordância"),
    ("adjancentes", "adjacentes", "typo"),
    ("anatomopatologica.", "anatomopatológico.", "concordância/acentuação"),
    ("parosteoal", "parosteal", "typo"),
    ("cabela femoral", "cabeça femoral", "typo"),
    ("iprovavelmente", "provavelmente", "typo"),
    ("re  tificação", "retificação", "espaço espúrio"),
    ("evidência ruptura", "evidencia ruptura", "verbo x substantivo"),
    ("Apesa do estudo", "Apesar do estudo", "typo"),
    ("no entendo", "no entanto", "typo"),
    ("de generativa", "degenerativa", "espaço espúrio"),
    ("unocarpico", "ulnocárpico", "typo"),
    ("ossos do capo", "ossos do carpo", "typo"),
    ("polger", "polegar", "typo"),
    ("relacionadas a manipulação", "relacionadas à manipulação", "crase"),
    ("fascia plamar", "fáscia palmar", "typo e acentuação"),
    ("possiblidade", "possibilidade", "typo"),
    ("má formação vascular", "malformação vascular", "grafia"),
    ("hidrosiringomielia", "hidrossiringomielia", "grafia"),
    ("inespecífica, suspeita", "inespecífico, suspeito", "concordância"),
    ("Não se observam realce nodulares", "Não se observam realces nodulares", "concordância"),
    ("na topografia da lesão o na área", "na topografia da lesão ou na área", "typo"),
    ("difusamento", "difusamente", "typo"),
    ("Hipoidratação", "Hipo-hidratação", "grafia"),
    ("osteossintese", "osteossíntese", "acentuação"),
    ("parafuxo", "parafuso", "typo"),
    ("estrututas", "estruturas", "typo"),
    ("locorregionias", "locorregionais", "typo"),
    ("Permance", "Permanece", "typo"),
    ("Não de caracterizam", "Não se caracterizam", "typo"),
    ("porem", "porém", "acentuação"),
    ("ate", "até", "acentuação"),
    ("nevros", "nervos", "typo"),
    ("raizes", "raízes", "acentuação"),
    ("Raizes", "Raízes", "acentuação"),
    ("tambem", "também", "acentuação"),
    ("tibia", "tíbia", "acentuação"),
    ("clinica", "clínica", "acentuação"),
    ("clinico", "clínico", "acentuação"),
    ("clinicos", "clínicos", "acentuação"),
    ("ossea", "óssea", "acentuação"),
    ("osseo", "ósseo", "acentuação"),
    ("medio", "médio", "acentuação"),
    ("umero", "úmero", "acentuação"),
    ("nivel", "nível", "acentuação"),
    ("cronica", "crônica", "acentuação"),
    ("cirurgica", "cirúrgica", "acentuação"),
    ("raíz", "raiz", "hipercorreção"),
    ("óssos", "ossos", "hipercorreção"),
    ("inserçao", "inserção", "acentuação"),
    ("tendineas", "tendíneas", "acentuação"),
    ("inflamatoria", "inflamatória", "acentuação"),
    # depois da regra genérica `medio -> médio` (limitada a palavra inteira, e
    # que por isso não toca "mediopé"): aqui "médio" é truncamento de mediopé,
    # como prova a descrição da mesma máscara.
    ("do tornozelo e médio", "do tornozelo e mediopé", "palavra truncada"),
    ("estudo do mediopé evidência", "estudo do mediopé evidencia", "verbo x substantivo"),
    ("devido a baixa fratura do cosensibilidade", "devido a baixa sensibilidade",
     "palavra reconstruída: pedaço de outra frase colado no meio dela"),
]

# Anotações que a autora deixou coladas na frase e que NÃO entram no texto do
# laudo: nome de quem passou o caso, dado do paciente, lembrete de técnica,
# marca de origem do caso. Só entram aqui alternativas que de fato casam.
#
# As quatro últimas alternativas são anotação clínica da autora (pincer,
# indício de pince, quase madelung, osgood) — antes ficavam no texto, por serem
# achado dela; saem a pedido do dono do repositório, porque são rótulo de
# raciocínio, não frase de laudo. A alternativa casa só quando ocupa o
# parêntese inteiro, então "(sequela de Osgood-Schlatter)" continua intacto.
# As variantes de grafia do caderno (pince/pincer, indicio sem acento,
# madelung sem o "quase") entram na própria alternativa: sem a fonte aqui não
# dá para saber qual grafia ela usou, e alternativa que não dispara passa
# despercebida — o guarda de "regra sem uso" cobre CORRECOES, não AUTOR_TAGS.
AUTOR_TAGS = re.compile(
    r"\s*[（(]\s*(?:yamada|yamda|tati|jan|guinel|neto|ikawa|bruno|samir|"
    r"pcte 9 anos|tele|so ve no t1 sem fat|"
    r"pincer?|osgood|(?:quase\s+)?madelung|ind[íi]cio\s+de\s+pincer?)\s*[)）]",
    re.IGNORECASE,
)

# Anotação composta: qualificador clínico + nome de quem passou o caso
# (qualificador + nome numa só anotação). Sai só o nome; o qualificador é achado
# da autora e fica.
NOME_EM_ANOT = re.compile(
    r"(?<=[（(])([^()）]*\S)\s+\b(?:yamada|yamda|tati|jan|guinel|neto|ikawa|"
    r"bruno|samir|ivan|fais)\b(?=\s*[)）])",
    re.IGNORECASE,
)

# Cabeçalhos de seção: recebem exatamente uma linha em branco antes.
CABECALHO = re.compile(
    r"^(?:Técnica|Tecnica|TÉCNICA|TÉCNICA DE EXAME|Técnica de exame|Método|Metodologia|"
    r"MÉTODO|Análise|ANÁLISE|Analise|Descrição|Relatório|Comentários|Comparação|"
    r"Conclusão|CONCLUSÃO|Opinião|OPINIÃO|Impressão|IMPRESSÃO|Impressão Diagnóstica|"
    r"IMPRESSÃO DIAGNÓSTICA|Indicação clínica|Indicação|Medidas|Referências|"
    r"Achados adicionais|Demais achados|Alterações|Observação|Resultado|"
    r"Exame anterior|Análise \(comparativa|Medidas \(|I\.D\.)\s*:?\s*$",
)

AUTOR_SOLTO = re.compile(
    r"\s*\b(?:tati|jan|neto|yamada|ya|fais|ivan)\b\.?\s*$",
    re.IGNORECASE,
)

ZAP = str.maketrans({"‌": None, "﻿": None, " ": " "})


# linhas não-vazias que uma spec descarta com '!' — registradas no log, porque
# descartar linha de dentro de uma máscara altera a saída tanto quanto trocar
# uma palavra.
DESCARTADAS: list[tuple[int, str]] = []

# linhas fora de toda faixa que saem por outras duas portas, contadas no log
SO_PONTUACAO: list[tuple[int, str]] = []
IGUAIS: list[int] = []

# faixas cobertas por alguma entrada, para a checagem de cobertura
COBERTAS: set[int] = set()


def _norm(s: str) -> str:
    """Texto reduzido a [a-z0-9] sem acento, para comparar frase da fonte com
    frase já no YAML sem tropeçar em pontuação, caixa ou acentuação."""
    s = unicodedata.normalize("NFKD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if not unicodedata.combining(c)))


def _norm_tok(s: str) -> list[str]:
    """Tokens sem acento e sem pontuação, para comparar label com replace."""
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.findall(r"[a-z]+", s)


def _faixas(txt: str):
    for parte in txt.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if "-" in parte:
            a, b = (int(x) for x in parte.split("-"))
        else:
            a = b = int(parte)
        yield a, b


def extrair(spec: str) -> list[str]:
    """spec: '123' | '123-140' | '123-130,140-145', com '!linhas' para excluir
    (ex.: '1674-1782 !1677,1733') — usado para tirar notas de estudo de dentro
    de uma máscara."""
    incluir, _, excluir = spec.partition("!")
    fora = set()
    for a, b in _faixas(excluir):
        fora.update(range(a, b + 1))
    linhas = []
    for a, b in _faixas(incluir):
        COBERTAS.update(range(a, b + 1))
        for n in range(a, b + 1):
            if n in fora:
                if FONTE[n - 1].strip():
                    DESCARTADAS.append((n, FONTE[n - 1].strip()))
            else:
                linhas.append(FONTE[n - 1])
    return linhas


# `·` NÃO entra aqui: é marcador de lista de segundo nível da autora, não
# marca de caderno. Sai só em modo bullet, junto com os outros marcadores.
SETA = re.compile(r"^\s*[→@\[]\s*")
MARCADOR = re.compile(r"^\s*(?:[-*·.]|\d+\.)\s+")

# No caderno, título de tópico vem marcado com seta; achado, não. Como a
# limpeza come o marcador, é por aqui que um título entra disfarçado de frase.
SETA_TITULO = re.compile(r"^\s*[→@]\s*")

# Linhas com seta que são achado da autora, não título — conferidas uma a uma
# contra a fonte. Congelada: linha nova com seta dentro de faixa aborta.
SETAS_OK = {
    4895,   # luxac1 — Sinais de evento recente de luxação acromioclavicular
    6198,   # fibularcomum1 — Feixes neurovasculares: espessamento do fibular comum
    6232,   # fxestresse1 — Alteração de sinal na cortical da diáfise
    6233,   # reacaoestresse1 — Alteração de sinal periosteal
    6234,   # estiramgastroc1 — Edema/estiramento da junção miotendínea
    6235,   # estiramgastroc2 — Rotura parcial do ventre medial do gastrocnêmio
    6236,   # estiramgastroc3 — Rotura completa do ventre medial do gastrocnêmio
    6237,   # grupamentosnl1 — Demais grupamentos musculotendíneos habituais
    8142,   # sacroiliite1 — Irregularidade das superfícies condrais sacroilíacas
}

# marcador de linha no log para "anotação removida" (não é correção de texto)
ANOT = "\x00anotação"


def limpar(linhas: list[str], modo: str, contador: dict) -> str:
    out = []
    for l in linhas:
        l = l.translate(ZAP)
        for m in AUTOR_TAGS.finditer(l):
            k = (f"anotação removida: {m.group(0).strip()}", ANOT)
            contador[k] = contador.get(k, 0) + 1
        l = AUTOR_TAGS.sub("", l)
        for m in NOME_EM_ANOT.finditer(l):
            k = (f"nome removido de dentro de anotação clínica: ({m.group(0).strip()}) "
                 f"-> ({m.group(1).strip()})", ANOT)
            contador[k] = contador.get(k, 0) + 1
        l = NOME_EM_ANOT.sub(r"\1", l)
        while SETA.match(l):
            l = SETA.sub("", l)
        if modo == "bullet":
            while MARCADOR.match(l):
                l = MARCADOR.sub("", l)
        m = AUTOR_SOLTO.search(l)
        if m and m.group(0).strip():
            k = (f"anotação removida no fim da linha: {m.group(0).strip()}", ANOT)
            contador[k] = contador.get(k, 0) + 1
        l = AUTOR_SOLTO.sub("", l)
        # a indentação da fonte é artefato do export (Google Docs) e quebraria
        # o bloco literal do YAML; os marcadores de lista em si são preservados
        l = aplicar_correcoes(l.strip(), contador)
        out.append(l)
    # colchete de fechamento órfão do export
    if out and out[-1].strip() == "]":
        out.pop()
    # tira brancos das pontas
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    if modo == "raw":
        return "\n".join(out)
    # remove toda linha em branco (ruído do export para .txt)
    corpo = [l for l in out if l.strip()]
    if modo == "unir":
        return " ".join(corpo)
    if modo in ("flat", "bullet"):
        return "\n".join(corpo)
    # modo 'sections': uma linha em branco antes de cada cabeçalho de seção
    res = []
    for i, l in enumerate(corpo):
        if i and CABECALHO.match(l.strip()):
            res.append("")
        res.append(l)
    return "\n".join(res)


PALAVRA = re.compile(r"^[0-9A-Za-zÀ-ÿ]+$")

REGRAS_REGEX = [
    # --- placeholders numéricos uniformizados para `_`.
    # NÃO toca: `XX` usado como separador de alternativa ("normotróficos XX
    # hipotróficos", "à direita XX esquerda"), data mascarada (XX/XX/XXXX),
    # "raio-X", o `X` de eixo ("AP X LL") e os marcadores `#`/`###` de título.
    # O gatilho é sempre a vizinhança numérica: unidade, verbo de medida ou
    # campo "Medida:".
    (re.compile(r"\bX{1,4}\b(?=\s*(?:mm|cm|ml|cm³|cc|º|%|graus)\b)"), "_",
     "placeholder numérico uniformizado para _"),
    (re.compile(r"((?:medindo|mede|estimad[ao] em|de at[ée]|calibre de|"
                r"espessura de|volume de|retração de|afundamento estimado em)"
                r"\s+(?:cerca de\s+)?)X{1,4}\b"), r"\1_",
     "placeholder numérico uniformizado para _"),
    (re.compile(r"((?:Medida|Ângulo|Índice|Intervalo)[^:\n]{0,70}:\s*)X{1,4}\b"),
     r"\1_", "placeholder numérico uniformizado para _"),
    (re.compile(r"(\"Glenoid Track\":\s*)X{1,4}\b"), r"\1_",
     "placeholder numérico uniformizado para _"),
    # linha de tabela de medida ("Direito: XX  Esquerdo: XX (Normal < 20 mm)")
    (re.compile(r"\b(Direito|Esquerdo):\s*X{1,4}\b"), r"\1: _",
     "placeholder numérico uniformizado para _"),
    # posição no relógio do orifício da fístula
    (re.compile(r"\bàs\s+X{1,4}\s+horas\b"), "às _ horas",
     "placeholder numérico uniformizado para _"),
    # lacuna vazia antes da unidade ("diâmetro proximal de  mm")
    (re.compile(r"(\b(?:de|medindo|mede)\s)\s*(?=(?:mm|cm|ml)\b)"), r"\1_ ",
     "lacuna vazia uniformizada para _"),
    # formas de lacuna não-numérica que já eram underline/colchete: só o
    # comprimento é normalizado, o campo continua sendo o mesmo
    (re.compile(r"_{2,}"), "_", "underline de preenchimento normalizado para _"),
    (re.compile(r"\[\s*\]"), "_", "colchete vazio uniformizado para _"),
    (re.compile(r"\bde\s+\.{3,}"), "de _", "reticências de preenchimento para _"),
    (re.compile(r"(discos intervertebrais de)\s+\."), r"\1 _.",
     "lacuna por ponto uniformizada para _"),
    (re.compile(r"(?<=[a-zà-ÿ])\.(?=[A-ZÀ-Ý])"), ". ", "espaço após ponto"),
    (re.compile(r"(?<=[a-zà-ÿ]),(?=[A-Za-zÀ-ÿ])"), ", ", "espaço após vírgula"),
    # não colapsa a lacuna de preenchimento que antecede uma unidade
    # ("retração de cerca de  cm" é campo a preencher, não espaço duplo)
    (re.compile(r"(?<=[0-9])[ \t]{2,}(?=\S)"), " ", "espaço duplo após valor"),
    (re.compile(r"(?<=[^0-9\s])[ \t]{2,}(?!(?:cm|mm|ml|cc|graus|º|%)\b)(?=\S)"), " ", "espaço duplo interno"),
    # espaço solto antes de vírgula/ponto e vírgula. Exige UM espaço só: dois ou
    # mais são lacuna de preenchimento da máscara e ficam intactos.
    (re.compile(r"(?<=[^\s])[ \t](?=[,;])"), "", "espaço antes de vírgula"),
    # o lookbehind ` de` preserva a lacuna de preenchimento em
    # "altura dos discos intervertebrais de ___ ." — ali o espaço é o campo.
    (re.compile(r"(?<=[^\s.])(?<! de)[ \t](?=\.(?:[\s(]|$))"), "", "espaço antes do ponto final"),
    # Datas concretas de exame dos casos da autora viram lacuna de preenchimento,
    # no mesmo formato dos marcadores que ela já usa (XXX, XX, ###). Decisão do
    # dono do repositório — não é correção de português, e por isso tem classe
    # própria no log.
    (re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b"), "XX/XX/XXXX", "data de exame mascarada"),
    (re.compile(r"\b\d{1,2}/\d{1,2}/\d{2}\b"), "XX/XX/XX", "data de exame mascarada"),
    (re.compile(r"\b\d{1,2}/\d{4}\b"), "XX/XXXX", "data de exame mascarada"),
    # por extenso: as três acima só veem data numérica
    (re.compile(r"\bde (?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|"
                r"setembro|outubro|novembro|dezembro) de \d{4}\b", re.I),
     "de XX/XXXX", "data de exame mascarada"),
]


def aplicar_correcoes(texto: str, contador: dict) -> str:
    """Regras literais primeiro (são as específicas); só depois as automáticas
    de digitação, senão uma normalização genérica pré-empita a regra literal."""
    for errado, certo, _nota in CORRECOES:
        if errado == certo:
            continue
        if PALAVRA.match(errado):
            padrao = re.compile(rf"(?<![0-9A-Za-zÀ-ÿ]){re.escape(errado)}(?![0-9A-Za-zÀ-ÿ])")
            texto, n = padrao.subn(certo, texto)
        else:
            n = texto.count(errado)
            texto = texto.replace(errado, certo)
        if n:
            contador[(errado, certo)] = contador.get((errado, certo), 0) + n
    for padrao, novo_txt, nota in REGRAS_REGEX:
        texto, n = padrao.subn(novo_txt, texto)
        if n:
            contador[(nota, "")] = contador.get((nota, ""), 0) + n
    return texto


# Nomes que o gerador remove do texto. Aparecem nos padrões acima porque sem o
# literal o padrão não casa — mas não têm por que ser reimpressos no log, que é
# saída de auditoria e não padrão de casamento.
NOMES_NO_LOG = re.compile(
    r"\b(?:yamada|yamda|tati|jan|guinel|neto|ikawa|bruno|samir|ivan|fais|ya|"
    r"marco b|almir|kim|arthur|paulo|pedro|alfredo|hernani|paola|nilson|"
    r"goulart|miquilino|nida|neide|paranavai|faissal|cedirp|santa catarina|"
    r"rede dor|hap vida)\b",
    re.IGNORECASE,
)


def _sem_nome(txt: str) -> str:
    """Troca nome próprio por marcador antes de escrever no log."""
    return NOMES_NO_LOG.sub("[identificação removida]", txt)


def _classe(nota: str) -> str:
    """Nem toda regra da seção 1 é correção de português — o rótulo da seção
    mentia enquanto somava tudo num número só."""
    # a mais estrita vem primeiro: regra que faz as duas coisas conta como a
    # que mexe em conteúdo, não como a que só limpa
    if any(x in nota for x in ("unidade faltante", "truncada", "reconstruíd", "inferida")):
        return "inferência de conteúdo a partir do contexto"
    if "placeholder" in nota or "lacuna" in nota or "underline" in nota \
            or "colchete" in nota or "reticências" in nota:
        return "placeholder uniformizado para _"
    if "anatomia" in nota:
        return "anatomia/clínica corrigida a pedido do usuário"
    if "data de exame" in nota:
        return "data de exame mascarada"
    if "nota de estudo" in nota:
        return "nota de estudo removida"
    if "rascunho" in nota:
        return "resíduo de rascunho removido"
    if "nome de colega" in nota:
        return "nome de colega removido"
    if "export" in nota:
        return "artefato do export"
    return "correção de português"


def yaml_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def main():
    global FONTE
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__.strip())
    src = Path(args[0])
    if not src.is_file():
        sys.exit(f"ERRO: arquivo-fonte não encontrado: {src}")
    FONTE = src.read_text(encoding="utf-8").split("\n")

    from malu.entradas import ENTRADAS  # tabela de entradas, por seção

    contador = {}
    vistos = {}
    textos = {}
    entradas_para_guarda: list[tuple[str, str, str]] = []
    blocos = ["matches:\n"]
    n_entradas = 0

    for item in ENTRADAS:
        if item[0] == "#":
            titulo = item[1]
            blocos.append(
                "  # ==========================================================================\n"
                f"  # {titulo}\n"
                "  # ==========================================================================\n"
            )
            continue

        trigger, label, spec = item[0], item[1], item[2]
        modo = item[3] if len(item) > 3 else "sections"

        if not re.fullmatch(r"[a-z0-9]+", trigger):
            sys.exit(f"ERRO: trigger fora do charset [a-z0-9]: {trigger!r}")
        if trigger in vistos:
            sys.exit(f"ERRO: trigger duplicado em malu.yml: {trigger!r}")
        vistos[trigger] = spec

        texto = limpar(extrair(spec), modo, contador)
        entradas_para_guarda.append((trigger, label, texto))
        if texto.count("]") > texto.count("["):
            texto = texto.rstrip()
            if texto.endswith("]"):
                texto = texto[:-1].rstrip()
        textos[trigger] = texto
        if not texto.strip():
            sys.exit(f"ERRO: entrada vazia para {trigger!r} (spec {spec})")

        bloco = [f'  - trigger: "{trigger}"\n', f'    label: "{yaml_escape(label)}"\n']
        if "\n" in texto:
            bloco.append("    replace: |-\n")
            bloco.extend(f"      {l}\n" if l else "\n" for l in texto.split("\n"))
        else:
            bloco.append(f'    replace: "{yaml_escape(texto)}"\n')
        bloco.append("    word: true\n")
        blocos.append("".join(bloco))
        n_entradas += 1

    # ---- texto duplicado entre entradas ----
    # Comparação normalizada, igual à do guarda entre arquivos: diferença só de
    # acento, hífen ou pontuação não faz duas máscaras distintas para quem
    # digita. Caixa inicial faz, quando uma abre frase e a outra é fragmento
    # que segue um prefixo de nível — esses pares vão declarados aqui.
    DUPLICATAS_OK = {
        frozenset({"abaullombmask1", "abaullombtc1"}):
            "mesma frase em caixa diferente de propósito: abaullombmask1 é o "
            "fragmento que segue 'L4-L5:', abaullombtc1 abre a frase",
    }
    porTexto = {}
    for t, txt in textos.items():
        porTexto.setdefault(_norm(txt), []).append(t)
    iguais = {k: sorted(ts) for k, ts in porTexto.items()
              if len(ts) > 1 and frozenset(ts) not in DUPLICATAS_OK}
    if iguais:
        sys.exit("ERRO: entradas com replace igual (comparação normalizada): "
                 + "; ".join(", ".join(ts) for ts in iguais.values()))
    orfas_dup = [p for p in DUPLICATAS_OK if p not in {frozenset(ts) for ts in porTexto.values()}]
    if orfas_dup:
        sys.exit(f"ERRO: DUPLICATAS_OK tem par que já não é duplicata: {orfas_dup}")

    # ---- cobertura: nenhuma linha da fonte fica de fora sem motivo ----
    from malu.exclusoes import EXCLUSOES

    cobertas = COBERTAS

    # Comparação por LINHA, não por substring: conter o texto dentro de um
    # replace maior não é o mesmo que a frase existir no arquivo, e a versão
    # anterior desta checagem dava cobertura falsa a frases curtas que só
    # apareciam como pedaço de outra.
    # o corpo de comparação é TODO o match/, não só malu.yml: uma frase que já
    # existe em rm.yml/tc.yml não precisa de entrada nova nem de motivo, porque
    # o espanso carrega tudo num namespace só
    linhas_yaml = {_norm(x) for t in textos.values() for x in t.split("\n") if _norm(x)}
    for arq in sorted((REPO / "match").glob("*.yml")):
        if arq.name == "malu.yml":
            continue
        for m in _yaml_mod.safe_load(arq.read_text(encoding="utf-8"))["matches"]:
            for x in str(m.get("replace", "")).split("\n"):
                if _norm(x):
                    linhas_yaml.add(_norm(x))
    candidatas = set()
    for n, l in enumerate(FONTE, 1):
        if n in cobertas:
            continue
        t = l.strip().translate(ZAP).strip()
        if not t:
            continue
        k = _norm(aplicar_correcoes(t, {}))
        if not k:
            # linha só de pontuação/régua ('*', '--', '____', ']'). Não tem
            # palavra nenhuma, mas some do arquivo: entra na contagem.
            SO_PONTUACAO.append((n, t))
            continue
        if k in linhas_yaml:
            IGUAIS.append(n)
            continue
        candidatas.add(n)
    orfas = sorted(candidatas - set(EXCLUSOES))
    if orfas:
        sys.exit("ERRO: linha(s) da fonte fora de toda faixa e sem motivo em "
                 "exclusoes_malu.py:\n"
                 + "\n".join(f"  L{n}: {FONTE[n - 1].strip()[:100]}" for n in orfas))
    # Simétrico da checagem acima: ela só procura linha que FALTA. Esta procura
    # linha que ENTROU — rótulo do caderno que virou primeira linha de um laudo
    # porque a faixa começou cedo demais. Se um texto é rótulo num ponto, não
    # pode ser texto de laudo em outro.
    # Todo motivo que declara "isto não é texto de laudo" entra aqui. A versão
    # anterior listava só três e deixava de fora justamente a maior bolsa de
    # títulos do caderno, a dos marcados com seta.
    ROTULO = ("título de máscara no caderno",
              "identificação de caso, paciente, data ou local",
              "rótulo de tópico do caderno",
              "título ou nota do caderno (marcado com seta)",
              "nota de estudo, anatomia ou valor de referência",
              "nota de estudo em tópicos",
              "link de referência",
              "indicação clínica de um paciente específico",
              "nome de colega ou de paciente",
              "anotação clínica solta, fora de qualquer frase")
    # o vocabulário do guarda tem de cobrir TODO motivo da tabela: foi por um
    # motivo de fora que a maior bolsa de títulos escapou antes
    orfaos = sorted(set(EXCLUSOES.values()) - set(ROTULO))
    if orfaos:
        sys.exit("ERRO: motivo de exclusão fora do vocabulário do guarda de rótulo: "
                 + repr(orfaos))
    rotulos = {_norm(aplicar_correcoes(FONTE[n - 1].strip().translate(ZAP).strip(), {})): n
               for n, motivo in EXCLUSOES.items() if motivo in ROTULO}
    rotulos.pop("", None)
    intrusos = []
    for trigger, txt in textos.items():
        for linha in txt.split("\n"):
            k = _norm(linha)
            if k in rotulos:
                intrusos.append((trigger, rotulos[k], linha.strip()))
    if intrusos:
        sys.exit("ERRO: rótulo do caderno dentro do texto de uma entrada "
                 "(faixa começou ou terminou fora do laudo):\n"
                 + "\n".join(f"  {t} <- L{n}: {l[:70]}" for t, n, l in intrusos))

    # O guarda acima só pega rótulo que tenha gêmeo fora de faixa. Rótulo que
    # ocorre uma vez só, dentro da faixa, escapa dele — mas no caderno o título
    # vem marcado com seta, e a limpeza come a seta. Então: toda linha de dentro
    # de uma faixa que na fonte começava com seta precisa estar declarada aqui
    # como achado, não título.
    setas = []
    for trigger, spec in vistos.items():
        inc, _, exc = spec.partition("!")
        fora = set()
        for a, b in _faixas(exc):
            fora.update(range(a, b + 1))
        for a, b in _faixas(inc):
            for n in range(a, b + 1):
                if n not in fora and SETA_TITULO.match(FONTE[n - 1].translate(ZAP)):
                    setas.append((trigger, n))
    novas = [(t, n) for t, n in setas if n not in SETAS_OK]
    if novas:
        sys.exit("ERRO: linha marcada com seta (formato de título do caderno) dentro "
                 "de uma entrada, sem estar declarada como achado em SETAS_OK:\n"
                 + "\n".join(f"  {t} <- L{n}: {FONTE[n - 1].strip()[:70]}" for t, n in novas))
    sobrando = sorted(set(SETAS_OK) - {n for _, n in setas})
    if sobrando:
        sys.exit(f"ERRO: SETAS_OK tem linha que já não está em faixa nenhuma: {sobrando}")

    obsoletas = sorted(set(EXCLUSOES) - candidatas)
    if obsoletas:
        sys.exit(f"ERRO: {len(obsoletas)} entrada(s) de exclusoes_malu.py já não são "
                 f"candidatas (viraram entrada ou mudaram de texto): {obsoletas}")

    # ---- colisão com triggers já existentes no repo ----
    existentes = set()
    for p in sorted((REPO / "match").glob("*.yml")):
        if p.name == "malu.yml":
            continue
        for m in re.finditer(r'^  - trigger: "([^"]+)"', p.read_text(encoding="utf-8"), re.M):
            existentes.add(m.group(1))
    colisoes = sorted(set(vistos) & existentes)
    if colisoes:
        sys.exit(f"ERRO: {len(colisoes)} colisão(ões) com triggers existentes: {colisoes}")

    # label descrevendo o texto PRÉ-correção. `label` não é comentário: é o
    # campo indexado por web/index.html e o que o espanso mostra na busca, então
    # um label desatualizado devolve o erro que a correção tirou do replace.
    # Escopo por regra: só as entradas que aquela regra de fato tocou, senão
    # vocabulário comum ("medial", "distal") acusa label correto.
    rotulos = []
    for errado, certo, nota in CORRECOES:
        if not certo or "anatomia" not in nota:
            continue
        # bigrama, não token solto: a sequência que a correção desfez. Token
        # isolado acusa label correto ("longo" de "flexor longo do polegar"
        # contra a regra do flexor radial).
        te, tc = _norm_tok(errado), _norm_tok(certo)
        # bigrama âncora+alterado: o 2º token é o que a correção tirou, o 1º
        # é compartilhado com a versão certa. "radial longo" pega o defeito;
        # "longo do" pegaria "flexor longo do polegar", que está correto.
        so_velho = {f"{a} {b}" for a, b in zip(te, te[1:])
                    if b not in tc and a in tc}
        # correção aditiva (o certo só acrescenta ao errado): não há token
        # removido para ancorar, então o teste é o literal curto sem o longo.
        aditiva = _norm(errado) in _norm(certo)
        if not so_velho and not aditiva:
            continue
        for trig, lab, rep in entradas_para_guarda:
            if _norm(certo) not in _norm(rep):
                continue
            nlab = " ".join(_norm_tok(lab))
            if aditiva:
                # o literal da regra carrega contexto que o label não tem, então
                # compara-se âncora (últimos tokens do errado) + complemento.
                anc = [w for w in te if len(w) > 3][-2:]
                add = [w for w in tc if w not in te and len(w) > 3]
                if anc and add and " ".join(anc) in nlab and \
                        not any(w in nlab for w in add):
                    rotulos.append(f"{trig} (label sem {' '.join(add)!r})")
                continue
            resto = sorted(b for b in so_velho if b in nlab)
            if resto:
                rotulos.append(f"{trig} (label mantém {resto})")
    if rotulos:
        sys.exit(f"ERRO: {len(rotulos)} label com texto pré-correção: {rotulos[:8]}")

    # Regra que nunca casa é erro — e a checagem tem de rodar ANTES de escrever,
    # senão o arquivo do repositório já foi sobrescrito quando o processo aborta.
    # Cobre as duas tabelas: literais e automáticas.
    inativas = [f"{e!r}->{c!r}" for e, c, _ in CORRECOES if e != c and (e, c) not in contador]
    inativas += [f"regra automática {nota!r}" for _p, _n, nota in REGRAS_REGEX
                 if (nota, "") not in contador]
    if inativas:
        sys.exit(f"ERRO: {len(inativas)} regra(s) de correção sem uso: {inativas[:12]}")

    # texto idêntico a entrada de OUTRO arquivo de match: o espanso carrega
    # tudo num namespace só, então isso é trigger a mais para o mesmo texto
    por_texto_repo = {}
    for arq in sorted((REPO / "match").glob("*.yml")):
        if arq.name == "malu.yml":
            continue
        for m in _yaml_mod.safe_load(arq.read_text(encoding="utf-8"))["matches"]:
            por_texto_repo.setdefault(_norm(str(m.get("replace", ""))), []).append(
                f"{arq.name}:{m['trigger']}")
    por_texto_repo.pop("", None)
    # compara normalizado: diferença só de marcador de lacuna, pontuação ou
    # espaço não faz duas máscaras serem diferentes para quem digita
    repetidos = [(t, txt, por_texto_repo[_norm(txt)])
                 for t, txt in textos.items() if _norm(txt) in por_texto_repo]
    if repetidos:
        sys.exit("ERRO: replace idêntico a entrada de outro arquivo de match "
                 "(o espanso carrega tudo num namespace só):\n"
                 + "\n".join(f"  {t} == {', '.join(o)}: {txt[:55]}" for t, txt, o in repetidos))

    if "--check" not in sys.argv:
        OUT.write_text("\n\n".join(b.rstrip("\n") for b in blocos) + "\n", encoding="utf-8")
        notas = {(e, c): n for e, c, n in CORRECOES}
        corr = {k: v for k, v in contador.items() if k[1] != ANOT}
        anot = {k: v for k, v in contador.items() if k[1] == ANOT}

        linhas_log = [
            "Alterações aplicadas ao texto da autora em match/malu.yml",
            "=" * 60,
            "",
            "O texto é extraído por faixas de linha do arquivo-fonte, nunca redigitado.",
            "As três listas abaixo são exaustivas: fora delas, o que muda entre a fonte",
            "e o YAML é só formatação, nunca palavra. As classes de formatação são estas",
            "e mais nenhuma:",
            "",
            "  - a indentação do export e o espaço em branco no fim da linha são removidos;",
            "  - linhas em branco internas ao bloco são descartadas, e no modo de laudo",
            "    completo uma linha em branco é INSERIDA antes de cada cabeçalho de seção",
            "    (Técnica:, Análise:, Conclusão: ...);",
            "  - setas e colchete de abertura (→, @, [) saem do início da linha em",
            "    qualquer entrada; os marcadores de lista (-, *, ·, ., 1.) só saem nas 182",
            "    entradas em modo bullet — nas demais o marcador é preservado; colchete",
            "    órfão de fechamento do export é descartado;",
            "  - em 7 entradas curtas, linhas-fonte consecutivas são unidas numa só frase",
            "    (a quebra de linha vira espaço);",
            "  - caracteres invisíveis do export (ZWNJ U+200C, BOM) são removidos e o",
            "    espaço não-separável (U+00A0) vira espaço comum.",
            "",
            "-" * 60,
            "1. SUBSTITUIÇÕES DE TEXTO APLICADAS POR REGRA",
            "-" * 60,
            "",
            "A maioria é correção de português, mas não toda: a coluna final diz de que",
            "classe é cada uma, e o subtotal por classe vem no fim da seção.",
            "",
        ]
        classes = {}
        for (errado, certo), n in sorted(corr.items()):
            # em regra automática a própria chave é a nota; usá-la aqui é o que
            # faz a classificação valer também para elas
            nota = errado if certo == "" else notas.get((errado, certo), "")
            cl = _classe(nota)
            classes[cl] = classes.get(cl, 0) + n
            if certo == "":
                linhas_log.append(f"{n:3d}x  regra automática: {errado}   [{cl}]")
            else:
                linhas_log.append(f"{n:3d}x  {_sem_nome(repr(errado))} -> "
                                  f"{_sem_nome(repr(certo))}   ({nota}) [{cl}]")
        linhas_log += [
            "",
            "por classe:",
        ]
        for cl, n in sorted(classes.items(), key=lambda kv: -kv[1]):
            linhas_log.append(f"  {n:3d}x  {cl}")
        linhas_log += [
            "",
            f"subtotal: {sum(corr.values())} substituições, {len(corr)} regras ativas",
            "",
            "-" * 60,
            "2. ANOTAÇÕES REMOVIDAS DO TEXTO",
            "-" * 60,
            "",
            "Marginália que não é conteúdo do laudo: nome de quem passou o caso, dado do",
            "paciente, lembrete de técnica, marca de origem. Também sai a anotação clínica",
            "da autora — (pincer), (indício de pince), (quase madelung), (osgood) —, a",
            "pedido do dono do repositório: é rótulo de raciocínio, não frase de laudo.",
            "",
        ]
        for (rotulo, _), n in sorted(anot.items()):
            linhas_log.append(f"{n:3d}x  {_sem_nome(rotulo)}")
        linhas_log += [
            "",
            f"subtotal: {sum(anot.values())} remoções, {len(anot)} anotações distintas",
            "",
            "-" * 60,
            "3. LINHAS DESCARTADAS DE DENTRO DE UMA MÁSCARA",
            "-" * 60,
            "",
            "Linhas que caem dentro da faixa de um laudo completo mas não são texto do",
            "laudo: rótulo de caderno, nota de estudo, lembrete. Descartar uma delas muda",
            "a saída tanto quanto trocar uma palavra, então vão listadas com o número da",
            "linha na fonte.",
            "",
        ]
        for n, txt in sorted(set(DESCARTADAS)):
            linhas_log.append(f"  L{n:<6d} {txt}")
        linhas_log += [
            "",
            f"subtotal: {len(set(DESCARTADAS))} linhas descartadas",
            "",
            "-" * 60,
            "4. LINHAS DA FONTE QUE NÃO VIRARAM ENTRADA",
            "-" * 60,
            "",
            "Toda linha não-vazia que fica fora de todas as faixas e que, já com as",
            "correções aplicadas, não é igual a nenhuma linha de nenhum replace precisa de",
            "um motivo registrado em exclusoes_malu.py. A comparação é por linha inteira,",
            "não por substring: estar contida num replace maior não é a frase existir. O",
            "gerador aborta se aparecer linha sem motivo, e também se um motivo ficar",
            "obsoleto. Abaixo, quantas por motivo.",
            "",
        ]
        porMotivo = {}
        for _n, motivo in EXCLUSOES.items():
            porMotivo[motivo] = porMotivo.get(motivo, 0) + 1
        for motivo, n in sorted(porMotivo.items(), key=lambda kv: -kv[1]):
            linhas_log.append(f"{n:4d}  {motivo}")
        linhas_log += [
            "",
            f"subtotal: {len(EXCLUSOES)} linhas fora com motivo declarado.",
            "",
            "Outras linhas também ficam fora de toda faixa, mas sem perda de conteúdo, e",
            "por isso não exigem motivo individual:",
            f"  {len(IGUAIS)}  o texto da linha já existe, igual, em alguma entrada",
            f"  {len(SO_PONTUACAO)}  linha sem nenhuma palavra (régua, asterisco, colchete solto)",
            f"  total de linhas não-vazias fora de toda faixa: "
            f"{len(EXCLUSOES) + len(IGUAIS) + len(SO_PONTUACAO)}",
            "",
            "-" * 60,
            f"TOTAL: {sum(corr.values())} substituições por regra (seção 1) + "
            f"{sum(anot.values())} anotações removidas (seção 2) + "
            f"{len(set(DESCARTADAS))} linhas descartadas de dentro de máscara (seção 3)",
            f"       + {len(EXCLUSOES)} linhas da fonte deixadas de fora (seção 4)",
        ]
        LOG.write_text("\n".join(linhas_log) + "\n", encoding="utf-8")

    n_corr = sum(v for k, v in contador.items() if k[1] != ANOT)
    n_anot = sum(v for k, v in contador.items() if k[1] == ANOT)
    print(f"OK — {n_entradas} entradas, {n_corr} substituições por regra, "
          f"{n_anot} anotações removidas, {len(set(DESCARTADAS))} linhas descartadas, "
          f"0 colisões")


if __name__ == "__main__":
    main()
