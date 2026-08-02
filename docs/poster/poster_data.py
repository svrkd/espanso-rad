# -*- coding: utf-8 -*-
"""Conteúdo curado do pôster de parede — US (match/us.yml).

Cada linha do pôster declara o(s) trigger(s) real(is) que ela cobre, de forma
reconstruível sem heurística de string (split por "/", etc.) — é isso que
scripts/check_poster_coverage.py usa para conferir a cobertura contra
match/us.yml. Ver `linha_triggers()` abaixo para a regra de derivação.

Formato de cada bloco em BLOCOS:

    (titulo_bloco, [LINHA, ...])

Uma LINHA é uma das tuplas:

    ("escada", prefixo, orgao, [ITEM, ...])
        Cobre um trigger por ITEM: trigger = prefixo + sufixo.
        ITEM é (sufixo, rotulo) ou (sufixo, rotulo, [aliases]), onde
        `aliases` é a lista de triggers extras (grafias antigas/duplicadas)
        que expandem para o mesmo achado.

    ("triggers", [trigger, ...], orgao, rotulo)
        Lista explícita de triggers para achados irregulares: modelos
        completos com variante D/E, pares que não seguem prefixo+sufixo,
        ou aliases sem prefixo comum.

    ("nota", texto)
        Linha sem trigger nenhum — só aponta para o Alt+Space.

MODELOS e CURINGAS seguem o mesmo princípio: cada entrada declara a lista
explícita de triggers que cobre (nunca uma string tipo "usinguinald/e" para
ser quebrada depois — isso é exatamente o defeito que este arquivo corrigiu).
"""

BLOCOS = [
    ("ABDOME", [
        ("escada", "vb", "vesícula", [
            ("0", "colecistectomia"), ("1", "litíase"), ("2", "colecistite aguda"),
            ("3", "barro"), ("4", "pólipo"), ("5", "colesterolose"),
            ("6", "calculosa crônica"), ("7", "repleta de cálculos"),
            ("8", "porcelana"), ("9", "paredes espessas/ascite"), ("10", "hipodistendida"),
            ("11", "c/ hidropsia + vias biliares dilatadas", ["vbcole"]),
        ]),
        ("escada", "ch", "fígado difuso", [
            ("1", "incipiente"), ("2", "cirrose"), ("3", "fibrose periportal"), ("4", "congestivo"),
        ]),
        ("escada", "eh", "esteatose", [("1", "grau I"), ("2", "grau II"), ("3", "grau III")]),
        ("escada", "fh", "fígado focal", [
            ("1", "cisto"), ("2", "cistos múltiplos"), ("3", "hemangioma?"),
            ("4", "nódulo indeterminado"), ("5", "secundários?"),
        ]),
        ("escada", "ca", "vias biliares", [
            ("1", "dilatação s/ causa"), ("2", "cálculo colédoco"), ("3", "massa periampular"),
            ("4", "aerobilia"), ("5", "Von Meyenburg"), ("6", "cisto de colédoco"),
        ]),
        ("escada", "ba", "baço", [
            ("1", "subcostal"), ("2", "esplenomegalia"), ("3", "Gamna-Gandy"), ("4", "acessório"),
        ]),
        ("escada", "ap", "apêndice", [("1", "apendicite"), ("2", "processo inflamatório")]),
        ("escada", "dh", "Doppler porta", [("0", "normal")]),
    ]),

    ("RINS · BEXIGA", [
        ("escada", "rv", "rins/vias urinárias", [
            ("1", "nefropatia crônica"), ("2", "nefropatia dim. preservadas"),
            ("3", "nefrolitíase"), ("4", "nefrolitíase"), ("5", "dilatação s/ causa"),
            ("6", "cálculo obstrutivo"), ("7", "cisto simples"), ("8", "cistos múltiplos"),
            ("9", "cisto complexo"), ("10", "AML?"), ("11", "policística"),
            ("12", "parapiélico"), ("13", "nefrocalcinose"), ("14", "nódulo indeterminado"),
            ("15", "dilatação acentuada"), ("16", "focos ecogênicos", ["usfocos"]),
        ]),
        ("escada", "bx", "bexiga", [
            ("1", "pouca repleção"), ("2", "de esforço"), ("3", "neobexiga"),
            ("4", "material imóvel"), ("5", "massa c/ fluxo"), ("6", "conteúdo hemático"),
            ("7", "ecos em suspensão"), ("8", "balão de sonda"), ("9", "focos gasosos"),
        ]),
        ("escada", "usjuv", "cálculo em JUV", [("1", "direita"), ("2", "esquerda")]),
        ("triggers", ["prostn"], "próstata", "impressão vesical"),
    ]),

    ("BOLSA ESCROTAL", [
        ("escada", "te", "testículo/bolsa escrotal", [
            ("1", "torção testicular (ausência de fluxo)"),
            ("2", "varicocele à _"),
            ("3", "orquiepididimite à _"),
            ("4", "hérnia inguinoescrotal encarcerada à _"),
            ("5", "microlitíase testicular à _"),
            ("6", "coleção c/ hematocele pós-traumática à _"),
        ]),
        ("triggers", ["te7"], "testículo/bolsa escrotal", "testículo ectópico (não visualizado na bolsa)"),
    ]),

    ("PÉLVICA · TRANSVAGINAL", [
        ("escada", "ut", "útero", [
            ("0", "histerectomia total"), ("1", "endométrio espessado"), ("2", "pólipo?"),
            ("3", "adenomiose"), ("4", "ectasia venosa"), ("6", "histerectomia parcial"),
            ("9", "istmocele", ["istmocele1"]),
            ("10", "lâmina anecoica", ["uslamina"]),
            ("13", "cisto de Naboth", ["usnaboth"]),
        ]),
        ("triggers", ["ut7", "bicorno"], "útero", "alteração mülleriana (septado/bicorno)"),
        ("triggers", ["ut5", "ut8", "utbicorno"], "útero", "eco endometrial bipartido (mülleriana?)"),
        ("escada", "mm", "miométrio", [("1", "leiomioma"), ("2", "múltiplos"), ("3", "útero miomatoso")]),
        ("escada", "ov", "ovário", [
            ("1", "conteúdo espesso"), ("2", "cisto simples"), ("3", "micropolicísticos"),
            ("4", "teratoma?"), ("5", "septado"), ("6", "componente sólido"),
            ("7", "endometrioma"), ("8", "heterogêneo"),
            ("9", "SOP", ["sop"]),
            ("10", "teratoma", ["terat1"]),
        ]),
        ("escada", "an", "anexos", [("1", "cisto simples"), ("2", "massa/ectópica?"), ("3", "hidrossalpinge")]),
        ("escada", "diu", "DIU", [
            ("1", "tópico"), ("2", "atravessa colo"), ("3", "deslocado"), ("4", "inserção baixa"),
        ]),
        ("triggers", ["utnc"], "útero não caracterizado", "não caracterizado no presente estudo (histerectomia prévia)"),
        ("triggers", ["ovdnao", "ovenao", "ovbnao"], "ovário", "não caracterizado (D/E/ambos)"),
    ]),

    ("OBSTÉTRICA", [
        ("escada", "ob", "gestacional", [
            ("1", "restos ovulares/coágulos", ["usrestos"]),
            ("2", "hematoma retrocoriônico", ["hretro"]),
        ]),
        ("nota", "malformações fetais ob3–ob45 → Alt+Space"),
    ]),

    ("MAMAS · TIREOIDE", [
        ("triggers", ["ma1", "mms1"], "mama", "cistos subcentimétricos (ambas)"),
        ("escada", "ma", "mama", [
            ("11", "cistos subcentimétricos D"), ("12", "cistos subcentimétricos E"),
            ("3", "nódulo único"),
        ]),
        ("triggers", ["ma3s", "ma4"], "mama", "múltiplos nódulos (≥2 sítios)"),
        ("escada", "usl", "linfonodo axilar normal", [
            ("b", "bilateral"), ("d", "direito"), ("e", "esquerdo"),
        ]),
        ("escada", "ti", "tireoide", [
            ("1", "Chammas II"), ("2", "Chammas III/IV"), ("3", "Graves?"),
            ("4", "Hashimoto?"), ("5", "linfonodo suspeito"),
        ]),
    ]),

    ("MÚSCULO-ESQUELÉTICO", [
        ("escada", "mskd", "derrame", [
            ("1", "ausente"), ("2", "pequeno"), ("3", "mod/acentuado"), ("4", "c/ sinovite"),
        ]),
        ("escada", "msks", "sinovite", [("1", "s/ Doppler"), ("2", "c/ Doppler"), ("3", "c/ erosões")]),
        ("escada", "mskb", "bursa", [
            ("1", "normal"), ("2", "lâmina fisiológica"), ("3", "espessamento"),
            ("4", "bursite"), ("5", "c/ sinovite"),
        ]),
        ("escada", "mskt", "tendão", [
            ("1", "normal"), ("2", "tendinopatia"), ("3", "tenossinovite"), ("4", "teno+tendinopatia"),
            ("5", "rotura parcial"), ("6", "rotura completa"), ("7", "rotura crônica"), ("8", "pós-op"),
        ]),
        ("nota", "por segmento: co· jo· mo· om· pd· pu· qd· tz· lm· → Alt+Space"),
    ]),

    ("PARTES MOLES · TÓRAX", [
        ("escada", "pm", "parede/partes moles", [
            ("1", "hérnia"), ("2", "lipoma"), ("3", "coleção"), ("4", "cisto sebáceo"),
            ("5", "edema", ["usedema"]),
            ("6", "diástase do reto", ["diastase1"]),
        ]),
        ("escada", "tx", "tórax (US pulmonar/POCUS)", [
            ("1", "derrame simples"), ("2", "derrame septado + atelectasia"),
            ("3", "consolidação c/ broncograma dinâmico (pneumonia)"),
            ("4", "consolidação c/ broncograma estático (atelectasia/consolidação)"),
            ("5", "consolidação s/ broncograma"),
            ("6", "ausência de deslizamento pleural (pneumotórax)"),
            ("7", "lung point (pneumotórax)"),
            ("8", "massa sólida c/ contato pleural"),
            ("9", "nodularidade pleural + derrame (neoplasia?)"),
            ("10", "linhas A (padrão normal)"),
            ("11", "linhas B focais (inespecífico)"),
            ("12", "síndrome intersticial, perfil B (edema cardiogênico)"),
            ("13", "síndrome intersticial, perfil B' (SDRA/pneumonia extensa)"),
            ("14", "padrão assimétrico, perfil A/B (pneumonia)"),
        ]),
    ]),

    ("CRÂNIO · TRANSFONTANELA", [
        ("escada", "tf", "achados neonatais", [
            ("1", "cavum do septo pelúcido"), ("2", "cavum vergae"),
            ("3", "cavum septo pelúcido + vergae"), ("4", "cisto de plexo coroide"),
            ("5", "assimetria ventricular discreta"),
            ("6", "leucomalácia periventricular inicial"), ("7", "leucomalácia periventricular cística"),
            ("8", "ventriculomegalia leve"), ("9", "ventriculomegalia moderada"),
            ("10", "ventriculomegalia acentuada/hidrocefalia"), ("11", "cisto subependimário"),
            ("12", "agenesia de corpo caloso"), ("13", "complexo de Dandy-Walker"),
            ("14", "malformação de Chiari tipo II"),
        ]),
        ("escada", "tfp", "HPIV (Papile)", [
            ("1", "grau I"), ("2", "grau II"), ("3", "grau III"), ("4", "grau IV"),
        ]),
    ]),

    ("VASCULAR", [
        ("escada", "tvp", "venoso", [("1", "TVP aguda"), ("2", "TVP crônica")]),
        ("triggers", ["ustvpc"], "venoso", "trombose venosa profunda (conclusão genérica)"),
        ("escada", "dc", "carótidas", [
            ("1", "EMI"), ("2", "placa"), ("3", "placa instável"), ("4", "<50%"),
            ("5", "50–69%"), ("6", "≥70%"), ("7", "oclusão ACI"), ("8", "carotidínia"),
            ("9", "paraganglioma?"), ("10", "intrastent"), ("11", "stent sem estenose"),
        ]),
        ("escada", "dv", "vertebral", [("1", "hipoplasia"), ("2", "roubo subclávia"), ("3", "oclusão")]),
        ("escada", "ds", "roubo subclávio", [
            ("1", "completo"), ("2", "tipo 1"), ("3", "tipo 2"), ("4", "tipo 3"), ("5", "parcial t4"),
        ]),
        ("escada", "dam", "arterial de membros", [
            ("1", "ateromatose incipiente"),
            ("2", "ateromatose incipiente (todos os segmentos)"),
            ("3", "ateromatose difusa s/ estenose"),
            ("4", "ateromatose difusa (todos os segmentos)"),
            ("5", "variação anatômica do trajeto"),
            ("6", "estenose leve-moderada (<50%)"),
            ("7", "fluxo monofásico distal (DAOP proximal)"),
            ("8", "estenose 50–69%"),
            ("9", "estenose grave (>70%)"),
            ("10", "stent/prótese pérvio"),
            ("11", "oclusão segmentar c/ colaterais"),
            ("12", "não caracterização de vaso"),
            ("13", "oclusão extensa crônica"),
            ("14", "aneurisma arterial periférico"),
            ("15", "aneurisma parcialmente trombosado"),
            ("16", "aneurisma trombosado"),
            ("17", "pseudoaneurisma"),
            ("18", "fístula arteriovenosa"),
        ]),
    ]),
]

# Modelos de exame completo ("us..." → laudo inteiro). Cada entrada é
# (triggers, descricao) com a lista EXPLÍCITA de triggers cobertos — pares
# D/E não são mais uma string tipo "usinguinald/e" para quebrar por "/".
MODELOS = [
    (("usabdtotal",), "abdome total"), (("usabdsup",), "abdome superior"),
    (("usrv",), "rins e vias urinárias"), (("usprostata",), "próstata"),
    (("uspelvica",), "pélvica"), (("ustv",), "transvaginal"),
    (("usbolsa",), "bolsa escrotal"), (("usbolsad",), "bolsa escrotal c/ Doppler"),
    (("usob",), "obstétrica"), (("usobd",), "obstétrica c/ Doppler"), (("usob1t",), "obstétrica 1ºT"),
    (("usmamas",), "mamas"), (("ustireoide",), "tireoide"), (("ustireoidedop",), "tireoide c/ Doppler"),
    (("uscervical",), "cervical"), (("ustorax",), "tórax"), (("usestsup",), "partes moles"),
    (("usparede",), "parede abdominal"),
    (("usinguinald", "usinguinale"), "inguinal D/E"),
    (("usvenosod", "usvenosoe"), "duplex venoso MID/MIE"),
    (("ustvpmid", "ustvpmie"), "venoso MI completo"),
    (("ustvpmsd", "ustvpmse"), "venoso MS completo"),
    (("ustransfontanela",), "transfontanela"), (("usquadrilinfantil",), "quadril infantil (Graf)"),
    (("usrvrn",), "urinário neonatal"),
    (("uscotovelod", "uscotoveloe"), "cotovelo D/E — normal"),
    (("usjoelhod", "usjoelhoe"), "joelho D/E — normal"),
    (("usmaod", "usmaoe"), "mão D/E — normal"),
    (("usombrod", "usombroe"), "ombro D/E — normal"),
    (("uspunhod", "uspunhoe"), "punho D/E — normal"),
    (("usquadrild", "usquadrile"), "quadril D/E — normal"),
    (("ustornozelod", "ustornozeloe"), "tornozelo D/E — normal"),
    (("usped", "uspee"), "pé D/E — normal"),
    (("usmsk",), "coxa/perna/braço/antebraço — normal"),
]

CURINGAS = [
    (("migue1",), "…nas janelas acústicas disponíveis"),
    (("migue2",), "…nas porções caracterizadas"),
    (("gordoo",), "limitação por panículo"),
    (("papv",), "pâncreas/aorta parcialmente visualizados"),
    (("limitgas",), "limitação por gás"),
    (("usnc",), "nódulo mama D/E c/ achados acima"),
    (("usncs",), "nódulos mama D/E c/ achados acima"),
    (("tvppaulo",), "bloco normal duplex venoso MI (femorais/poplítea/tibiais/fibular/safenas)"),
]

# Triggers de match/us.yml que deliberadamente NÃO entram no pôster, com o
# motivo editorial documentado. scripts/check_poster_coverage.py usa esta
# lista para decidir o que é "fora por decisão" versus "esquecido".
#
# Atenção à regra de conclusão (…c$): ela exclui tudo que termina em "c",
# exceto os três triggers abaixo que terminam em "c" por coincidência e não
# são variante de conclusão de nada (não existe "usn", "utn" nem "ustvp"
# como trigger-base): usnc, utnc, ustvpc. Esses três são cobertos
# explicitamente em BLOCOS/CURINGAS acima, não por esta lista.
EXCLUSOES = [
    (r'^(co|jo|mo|om|pd|pu|qd|tz|lm)', 'MSK por segmento — volume alto, cobertura via Alt+Space'),
    (r'^me[12]$', 'MSK por segmento (tendão calcâneo / joelho) — prefixo legado fora do padrão co/jo/…/tz'),
    (r'^(?!usnc$|utnc$|ustvpc$).*c$', 'variante de conclusão (regra de gramática "…c")'),
    (r'^ob([3-9]|[1-4]\d)c?$', 'malformação fetal — não é agenda de rotina'),
    (r'^(dc|dv|ds|di|da|sdt)\d*c?$', 'Doppler vascular em slot dedicado (carótidas/vertebral/desfiladeiro/aorto-ilíaco)'),
    (r'^graf', 'quadril infantil, método Graf'),
]


def linha_triggers(linha):
    """Retorna o conjunto de triggers cobertos por uma LINHA de BLOCOS."""
    tipo = linha[0]
    if tipo == "nota":
        return set()
    if tipo == "triggers":
        _, triggers, _orgao, _rotulo = linha
        return set(triggers)
    if tipo == "escada":
        _, prefixo, _orgao, itens = linha
        triggers = set()
        for item in itens:
            sufixo = item[0]
            triggers.add(prefixo + sufixo)
            if len(item) > 2:
                triggers.update(item[2])
        return triggers
    raise ValueError(f"tipo de linha desconhecido: {tipo!r}")


def todos_os_triggers():
    """Todos os triggers cobertos pelo pôster (BLOCOS + MODELOS + CURINGAS)."""
    triggers = set()
    for _titulo, linhas in BLOCOS:
        for linha in linhas:
            triggers |= linha_triggers(linha)
    for triggers_grupo, _desc in MODELOS:
        triggers.update(triggers_grupo)
    for triggers_grupo, _desc in CURINGAS:
        triggers.update(triggers_grupo)
    return triggers
