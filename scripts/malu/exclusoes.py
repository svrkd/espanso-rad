"""Linhas do arquivo-fonte que ficam FORA de match/malu.yml, com o motivo.

Tabela congelada de propósito. build_malu.py recalcula as candidatas a cada
execução — toda linha não-vazia fora de todas as faixas cuja linha (já com
as correções aplicadas) não é igual a nenhuma linha de nenhum replace — e
aborta se encontrar uma que não esteja aqui, ou se uma entrada daqui deixar
de ser candidata. A comparação é por linha inteira, não por substring:
estar contida num replace maior não é o mesmo que a frase existir.
"""

EXCLUSOES = {
      4048: 'identificação de caso, paciente, data ou local',
           # JOELHO PADRÃO CEDIRP
      9838: 'título de máscara no caderno',
           # CT CÓCCIX
     10291: 'título de máscara no caderno',
           # CT BACIATRAUMA
     10353: 'título de máscara no caderno',
           # CTBACIA
     10446: 'título de máscara no caderno',
           # CT BACIA - DISJUNÇÃO SACROILIACA
        30: 'identificação de caso, paciente, data ou local',
           # po op manguito almir
        67: 'identificação de caso, paciente, data ou local',
           # kim
        87: 'rótulo de tópico do caderno',
           # Aorta Abdominal e Ilíacas
       128: 'link de referência',
           # https://hapvida-login.pixeonkorus.com/
       131: 'link de referência',
           # https://hapvida-login.pixeonkorus.com/
       132: 'link de referência',
           # https://radsource.us/common-intraosseous-cysts/
       182: 'rótulo de tópico do caderno',
           # rotura muscular
       241: 'rótulo de tópico do caderno',
           # meta bacia
       272: 'rótulo de tópico do caderno',
           # lipoma
       273: 'rótulo de tópico do caderno',
           # luxação
       305: 'nome de colega ou de paciente',
           # dr arthur
       373: 'rótulo de tópico do caderno',
           # coluna rede
       378: 'rótulo de tópico do caderno',
           # - Alinhamentos sagital e coronal:
       472: 'nota de estudo, anatomia ou valor de referência',
           # lesao agressiva
       473: 'nota de estudo, anatomia ou valor de referência',
           # destroi cortical anterior e extenso edema reacional circunjacente
       476: 'nota de estudo, anatomia ou valor de referência',
           # junto a placa fisária da apofise anteriror da tibia
       479: 'nota de estudo, anatomia ou valor de referência',
           # correlacionar com anatomo patologico
       482: 'nota de estudo, anatomia ou valor de referência',
           # osteoblastoma , condroblatoma
       483: 'nota de estudo, anatomia ou valor de referência',
           # tgc fraturado
       484: 'nota de estudo, anatomia ou valor de referência',
           # osteossacroma teleganectasico
       509: 'rótulo de tópico do caderno',
           # pediculo
       547: 'nome de colega ou de paciente',
           # paulo
       627: 'identificação de caso, paciente, data ou local',
           # 30931199
       647: 'nome de colega ou de paciente',
           # faissal coluna
       659: 'identificação de caso, paciente, data ou local',
           # TELE 01/04 -34 WTT 8 mobile
       664: 'identificação de caso, paciente, data ou local',
           # casos osteomielite rede nilson goulart 27/03/2024
       731: 'identificação de caso, paciente, data ou local',
           # MARIA INES MIQUILINO DE CASTRO
       862: 'rótulo de tópico do caderno',
           # musculatura interossea
       882: 'identificação de caso, paciente, data ou local',
           # samir coluna
       953: 'link de referência',
           # https://docs.google.com/presentation/d/F 1vmtGRCrCsdBYYZ0xZ7dbFOUyJz55dDPb/edit?usp=shar
       961: 'rótulo de tópico do caderno',
           # tomografias
      1001: 'título ou nota do caderno (marcado com seta)',
           # laminotomia →  so corte
      1002: 'título ou nota do caderno (marcado com seta)',
           # laminectomia → tira pedaço
      1019: 'rótulo de tópico do caderno',
           # raio x periostite por estresse e calo osseo
      1027: 'título de máscara no caderno',
           # ARTEFATOS
      1031: 'rótulo de tópico do caderno',
           # COTOVELO normal
      1075: 'rótulo de tópico do caderno',
           # COTOVELO alterações
      1078: 'título ou nota do caderno (marcado com seta)',
           # epicondilite medial → golfe
      1079: 'título ou nota do caderno (marcado com seta)',
           # epicondilite lateral → tenis
      1212: 'rótulo de tópico do caderno',
           # COTOVELO trauma 1
      1213: 'nota de estudo, anatomia ou valor de referência',
           # Sempre que fartura rádio proximal olhar impactação no capítulo , processo coronóide e es
      1284: 'rótulo de tópico do caderno',
           # COTOVELO trauma 2
      1376: 'rótulo de tópico do caderno',
           # COTOVELO trauma 3
      1394: 'título de máscara no caderno',
           # COTOVELO INFLAMATORIA
      1424: 'título de máscara no caderno',
           # COXA
      1427: 'título ou nota do caderno (marcado com seta)',
           # → lipodistrofia semicircular ( paranavai neide)
      1517: 'título ou nota do caderno (marcado com seta)',
           # → hemangioma intramuscular
      1535: 'título ou nota do caderno (marcado com seta)',
           # →  miosite de hepatopata, reconversao/medula hematopoietica
      1557: 'título ou nota do caderno (marcado com seta)',
           # → ROTURA RETOFEMROAL
      1564: 'título ou nota do caderno (marcado com seta)',
           # → desenluvemento do reto femoral
      1567: 'link de referência',
           # https://www.mskrad.com.br/post/estiramento-na-jun%C3%A7%C3%A3o-miotend%C3%ADnea-proximal
      1584: 'rótulo de tópico do caderno',
           # vt
      1592: 'título de máscara no caderno',
           # VT
      1607: 'rótulo de tópico do caderno',
           # pediculo curto
      1611: 'título de máscara no caderno',
           # COL CERVICAL TELE
      1668: 'rótulo de tópico do caderno',
           # sc
      1669: 'título de máscara no caderno',
           # COL CERVICAL PADRÃO
      1783: 'rótulo de tópico do caderno',
           # modic
      1784: 'identificação de caso, paciente, data ou local',
           # COL CERVICAL SAMIR
      1803: 'rótulo de tópico do caderno',
           # (acentuação)
      1837: 'anotação clínica solta, fora de qualquer frase',
           # ( líquido intra articular )
      1845: 'anotação clínica solta, fora de qualquer frase',
           # (tem uns osteófitos já )
      1867: 'nota de estudo, anatomia ou valor de referência',
           # olha as raizes um nivel acima dos discos
      1868: 'nota de estudo, anatomia ou valor de referência',
           # quantificar os abaulamento se pequenos
      1891: 'rótulo de tópico do caderno',
           # a direita ainda tem gordura na esquerda já não tem mais nada
      1921: 'rótulo de tópico do caderno',
           # um nivel acima do disco
      1925: 'rótulo de tópico do caderno',
           # nível do disco
      1941: 'rótulo de tópico do caderno',
           # um nivel acima do disco
      1943: 'rótulo de tópico do caderno',
           # nível do disco
      1992: 'nota de estudo, anatomia ou valor de referência',
           # colocar uncoartrose, listese, interfacetarias,modic , etc.
      2002: 'rótulo de tópico do caderno',
           # cirurgia
      2006: 'identificação de caso, paciente, data ou local',
           # COL CERV CIRG SAMIR
      2105: 'título de máscara no caderno',
           # COL DORSAL PADRÃO
      2140: 'identificação de caso, paciente, data ou local',
           # COL DORSAL SAMIR
      2213: 'rótulo de tópico do caderno',
           # col lombar admisional
      2279: 'rótulo de tópico do caderno',
           # colun dor paotologico
      2322: 'título de máscara no caderno',
           # COL LOMBAR TELE
      2402: 'título de máscara no caderno',
           # COL LOMBAR PADRÃO
      2477: 'rótulo de tópico do caderno',
           # Pos operatorio sem metal
      2481: 'rótulo de tópico do caderno',
           # pos op cicatriz
      2498: 'rótulo de tópico do caderno',
           # reconversão medular
      2530: 'rótulo de tópico do caderno',
           # plato
      2608: 'rótulo de tópico do caderno',
           # metastase
      2611: 'título ou nota do caderno (marcado com seta)',
           # → metastase
      2624: 'rótulo de tópico do caderno',
           # ct
      2626: 'título ou nota do caderno (marcado com seta)',
           # → fx patologica coluna
      2632: 'título ou nota do caderno (marcado com seta)',
           # → discite
      2638: 'rótulo de tópico do caderno',
           # discite por provavel tb
      2650: 'título ou nota do caderno (marcado com seta)',
           # → col lesões
      2656: 'título ou nota do caderno (marcado com seta)',
           # → preservação medular vermelha
      2660: 'título ou nota do caderno (marcado com seta)',
           # → pos trauma
      2669: 'rótulo de tópico do caderno',
           # pedículo
      2696: 'título de máscara no caderno',
           # ESCAPULA
      2697: 'nota de estudo, anatomia ou valor de referência',
           # Sempre procurar elastofibroma no serrátil, e as vezes o realce é bem sutil
      2734: 'título de máscara no caderno',
           # JOELHO TELE
      2739: 'rótulo de tópico do caderno',
           # mosaicoplastia
      2791: 'título de máscara no caderno',
           # JOELHO
      3001: 'título ou nota do caderno (marcado com seta)',
           # → defeito dorsal da patela
      3007: 'título ou nota do caderno (marcado com seta)',
           # →fx plato tibial
      3009: 'título ou nota do caderno (marcado com seta)',
           # → reconversão
      3013: 'rótulo de tópico do caderno',
           # -reconversão medular(doença hematológica/mieloproliferativa)
      3019: 'título ou nota do caderno (marcado com seta)',
           # → osteotomia valgizante
      3023: 'título ou nota do caderno (marcado com seta)',
           # → estresse/hipersolicitação mecanica
      3026: 'identificação de caso, paciente, data ou local',
           # ikawa
      3029: 'título ou nota do caderno (marcado com seta)',
           # → patela bipartida
      3031: 'título ou nota do caderno (marcado com seta)',
           # → cirurgia
      3039: 'título ou nota do caderno (marcado com seta)',
           # →  osgood
      3054: 'título ou nota do caderno (marcado com seta)',
           # → osgood criança
      3064: 'título ou nota do caderno (marcado com seta)',
           # → sinding
      3071: 'título ou nota do caderno (marcado com seta)',
           # → desmoide cortical
      3072: 'rótulo de tópico do caderno',
           # - Desmoide cortical / defeito fibroso cortical:
      3076: 'título ou nota do caderno (marcado com seta)',
           # * → fibroma não ossificante
      3078: 'nota de estudo, anatomia ou valor de referência',
           # ( fibroma nao ossificante )
      3098: 'rótulo de tópico do caderno',
           # o laranja e a fratura
      3100: 'nota de estudo, anatomia ou valor de referência',
           # o que realça é porque fraturou
      3107: 'título ou nota do caderno (marcado com seta)',
           # → encondroma
      3113: 'título ou nota do caderno (marcado com seta)',
           # → gota
      3125: 'título ou nota do caderno (marcado com seta)',
           # →infarto ósseo
      3134: 'título ou nota do caderno (marcado com seta)',
           # → osteocondrite dissecante
      3152: 'título ou nota do caderno (marcado com seta)',
           # → hemangioma
      3163: 'rótulo de tópico do caderno',
           # ponto preto é um flow void de permeio
      3173: 'título ou nota do caderno (marcado com seta)',
           # → Lipoma
      3184: 'título ou nota do caderno (marcado com seta)',
           # →osteocondroma
      3190: 'título ou nota do caderno (marcado com seta)',
           # → fratura por estresse
      3200: 'título ou nota do caderno (marcado com seta)',
           # → prótese infecção
      3234: 'título ou nota do caderno (marcado com seta)',
           # → fx avulsiva do tendão patelar
      3238: 'título ou nota do caderno (marcado com seta)',
           # → apofise patela
      3247: 'título ou nota do caderno (marcado com seta)',
           # → hemangioma criança
      3258: 'rótulo de tópico do caderno',
           # joelho criança- ossificação cartilagem
      3267: 'título de máscara no caderno',
           # JOELHO LCA ROTO AGUDO
      3428: 'título de máscara no caderno',
           # JOELHO LCA RECON
      3613: 'título ou nota do caderno (marcado com seta)',
           # → soltura de protese de joelho
      3647: 'título de máscara no caderno',
           # JOELHO LUXAÇÃO PATELA
      3652: 'identificação de caso, paciente, data ou local',
           # kim
      3668: 'nota de estudo, anatomia ou valor de referência',
           # ---- tele
      3680: 'rótulo de tópico do caderno',
           # -rotura ligamentos
      3686: 'título ou nota do caderno (marcado com seta)',
           # → anatomia joelho lig patela
      3687: 'nota de estudo, anatomia ou valor de referência',
           # O estabilizador ativo mais importante da patela é o músculo vasto medial oblíquo (VMO), 
      3718: 'título de máscara no caderno',
           # JOELHO TAGT SANTA
      3748: 'título de máscara no caderno',
           # JOELHO TAGT
      3783: 'rótulo de tópico do caderno',
           # ( o normal é ir diminuindo o angulo e a patela se encaixando)
      3786: 'rótulo de tópico do caderno',
           # Como medir
      3789: 'título ou nota do caderno (marcado com seta)',
           # tagt → meio do sulco da tróclea
      3790: 'título ou nota do caderno (marcado com seta)',
           # → no meio da inserção do ligamento patelar (quando acaba a gordurinha)
      3793: 'rótulo de tópico do caderno',
           # local certo
      3796: 'rótulo de tópico do caderno',
           # inlcinação lateral
      3797: 'título ou nota do caderno (marcado com seta)',
           # arco romado → proporção de ⅓
      3802: 'rótulo de tópico do caderno',
           # paleta na altura/ no meio da inserção da inserção dos retináculos
      3807: 'título de máscara no caderno',
           # JOELHO TAGT REDEDOR
      3810: 'rótulo de tópico do caderno',
           # modeli 1
      3954: 'rótulo de tópico do caderno',
           # modelo 3
      4019: 'título de máscara no caderno',
           # RETROVERSAO QUADRIL
      4071: 'identificação de caso, paciente, data ou local',
           # JOELHO ARTROSE CEDIRP
      4101: 'identificação de caso, paciente, data ou local',
           # JOELHO LCA ROTO CEDIRP:
      4134: 'identificação de caso, paciente, data ou local',
           # JOELHO LCA RECON CEDIRP
      4165: 'identificação de caso, paciente, data ou local',
           # JOELHO LUXAÇÃO CEDIRP:
      4197: 'nota de estudo, anatomia ou valor de referência',
           # mão- tumor glomico
      4198: 'nota de estudo, anatomia ou valor de referência',
           # tumor glômico -- baixo sinal t1, alto sinal t2 e realce pós contraste
      4199: 'título ou nota do caderno (marcado com seta)',
           # diagnóstico diferencial -- cisto de inclusão epidérmica →   que tem sinal intermediário 
      4202: 'título de máscara no caderno',
           # MÃO PADRÃO
      4255: 'rótulo de tópico do caderno',
           # corpúsculos de Pacini
      4267: 'link de referência',
           # Pacinian corpuscle | Radiology Reference Article | Radiopaedia.org https://share.google/
      4277: 'rótulo de tópico do caderno',
           # gatilho dedo
      4305: 'rótulo de tópico do caderno',
           # Dupuytren
      4343: 'título de máscara no caderno',
           # AR
      4361: 'título de máscara no caderno',
           # MAO/DEDO
      4364: 'nota de estudo, anatomia ou valor de referência',
           # --polegar
      4410: 'rótulo de tópico do caderno',
           # subluxação e rotura da placa
      4419: 'nota de estudo, anatomia ou valor de referência',
           # seta vermelha rotura proximal do ligamento ( diferente de stener que é rotura distal ) s
      4422: 'título ou nota do caderno (marcado com seta)',
           # → stener rotura distal do ligamento colateral ulnar com interposição da aponeurose
      4437: 'rótulo de tópico do caderno',
           # rotura distal do ligamento colateral radial
      4440: 'rótulo de tópico do caderno',
           # rotura e desinserção da cápsula
      4448: 'título ou nota do caderno (marcado com seta)',
           # → stener
      4456: 'título ou nota do caderno (marcado com seta)',
           # → tumor neural shcwannoma ou tgc
      4470: 'título ou nota do caderno (marcado com seta)',
           # → STENER
      4480: 'título ou nota do caderno (marcado com seta)',
           # → hemangioma criança mao
      4493: 'rótulo de tópico do caderno',
           # ( t1, dp, pos gd)
      4496: 'rótulo de tópico do caderno',
           # (dp e pos gd)
      4501: 'título ou nota do caderno (marcado com seta)',
           # → tcg
      4508: 'título ou nota do caderno (marcado com seta)',
           # snvl localizada→ tem baixo sinal no GE , varial realce pelo contraste e meio alto sinal 
      4534: 'rótulo de tópico do caderno',
           # ombro admisional
      4634: 'título de máscara no caderno',
           # OMBRO TELE
      4710: 'título de máscara no caderno',
           # OMBRO PADRÃO
      4713: 'nota de estudo, anatomia ou valor de referência',
           # medida sempre na extensão do tendão no eixo longitudinal
      4714: 'nota de estudo, anatomia ou valor de referência',
           # coloca medida no transversa quando for mais focal ( sagital)
      4716: 'rótulo de tópico do caderno',
           # eixo transvrsal  eixo longitudinal ou retração
      4719: 'nota de estudo em tópicos',
           # 1. Músculo Supra-Espinhal: realiza o início do movimento de abdução do ombro e é inervad
      4720: 'nota de estudo em tópicos',
           # 2. Músculo Infra-Espinhal: realiza o movimento de rotação externa do ombro e também é in
      4721: 'nota de estudo em tópicos',
           # 3. Músculo Redondo Menor: também realiza o movimento de rotação externa do ombro e é ine
      4722: 'nota de estudo em tópicos',
           # 4. Músculo Subescapular: realiza o movimento de rotação interna do ombro e é inervado pe
      4723: 'rótulo de tópico do caderno',
           # acromio
      4876: 'título ou nota do caderno (marcado com seta)',
           # → criança infecciosa ou osteoma
      4879: 'título ou nota do caderno (marcado com seta)',
           # → calcaria amorfo
      4889: 'título ou nota do caderno (marcado com seta)',
           # → geiser
      4893: 'título ou nota do caderno (marcado com seta)',
           # → clavicula luxação
      4901: 'título ou nota do caderno (marcado com seta)',
           # → sequela
      4917: 'título ou nota do caderno (marcado com seta)',
           # → milwaukee
      4919: 'título de máscara no caderno',
           # OMBRO ROTURA MACIÇA
      5020: 'título de máscara no caderno',
           # OMBRO HILL SACHS
      5023: 'nome de colega ou de paciente',
           # → tati
      5112: 'rótulo de tópico do caderno',
           # cálculos hill sachs:
      5117: 'título ou nota do caderno (marcado com seta)',
           # 1. estimativa da perda da glenóide : 0,6/3,0 =0,2 → 20% de perda da área de superfície a
      5118: 'nota de estudo, anatomia ou valor de referência',
           # conta : falha/diâmetro total
      5123: 'título ou nota do caderno (marcado com seta)',
           # 2. Glenoid track = 19 mm ( em mm ) → cálculo da lesão
      5124: 'título ou nota do caderno (marcado com seta)',
           # 30 x 0,84 - 6 =19,2 → 19 mm
      5125: 'rótulo de tópico do caderno',
           # diâmetro total x 0,84 - falha
      5126: 'nota de estudo em tópicos',
           # *se nao tem perda óssea faz o diâmetro total x 0,84 apenas
      5129: 'nota de estudo em tópicos',
           # 3. Intervalo Hill-Sachs = 24 mm ( próprio hill sachs no transversal)
      5132: 'título ou nota do caderno (marcado com seta)',
           # 4. ON TRACK → bom prognóstico
      5133: 'nota de estudo, anatomia ou valor de referência',
           # intervalo de hill sachs < glenoide track
      5136: 'título ou nota do caderno (marcado com seta)',
           # OFF TRACK→ sao engaging
      5137: 'nota de estudo, anatomia ou valor de referência',
           # intervalo de hill sachs > glenoide track
      5138: 'nota de estudo, anatomia ou valor de referência',
           # track menos =off
      5149: 'título de máscara no caderno',
           # OMBRO HS REVERSO
      5239: 'título de máscara no caderno',
           # OMBRO TRAUMA AC  E FX UMERAL
      5291: 'título de máscara no caderno',
           # OMBRO PÓS CIRÚRGICO
      5294: 'rótulo de tópico do caderno',
           # sirio
      5411: 'identificação de caso, paciente, data ou local',
           # OMBRO PADRÃO CEDIRP-
      5440: 'identificação de caso, paciente, data ou local',
           # OMBRO INSTABILIDADE CEDIRP
      5471: 'identificação de caso, paciente, data ou local',
           # OMBRO RUPTURA MACIÇA CEDIRP
      5498: 'identificação de caso, paciente, data ou local',
           # OMBRO TENDINOPATIA CEDIRP
      5530: 'título de máscara no caderno',
           # PAREDE ABDOMINAL
      5581: 'título de máscara no caderno',
           # PE TELE
      5646: 'título de máscara no caderno',
           # PE PADRÃO
      5793: 'título ou nota do caderno (marcado com seta)',
           # → cuneifome medial bipartido
      5803: 'título ou nota do caderno (marcado com seta)',
           # → POLIDACTILIA
      5810: 'título ou nota do caderno (marcado com seta)',
           # → Charcot geral
      5832: 'título ou nota do caderno (marcado com seta)',
           # → osteomielite + charcot
      5855: 'nota de estudo, anatomia ou valor de referência',
           # muito preto o t1, favore infecção
      5868: 'título ou nota do caderno (marcado com seta)',
           # → osteomielite
      5900: 'título ou nota do caderno (marcado com seta)',
           # → 2
      5909: 'título ou nota do caderno (marcado com seta)',
           # →  artropatia neuropática
      5913: 'nota de estudo, anatomia ou valor de referência',
           # --- neuropatia com osteomielite
      5921: 'título ou nota do caderno (marcado com seta)',
           # →    lipossubstitutição neuropatica
      5927: 'título ou nota do caderno (marcado com seta)',
           # → trombose
      5933: 'título ou nota do caderno (marcado com seta)',
           # → fibromatose plantar
      5940: 'título ou nota do caderno (marcado com seta)',
           # → fx estresse
      5946: 'título ou nota do caderno (marcado com seta)',
           # → inflamatório
      5964: 'título ou nota do caderno (marcado com seta)',
           # → osteomielite e charcot
      5978: 'título ou nota do caderno (marcado com seta)',
           # → maduromicose
      5982: 'rótulo de tópico do caderno',
           # t1, t2, gd
      5985: 'rótulo de tópico do caderno',
           # gd
      5988: 'identificação de caso, paciente, data ou local',
           # PE SANTA CATARINA
      6087: 'título de máscara no caderno',
           # PEITORAL MAIOR
      6109: 'título de máscara no caderno',
           # PERNA TELE
      6151: 'título de máscara no caderno',
           # PERNA PADRÃO
      6208: 'título ou nota do caderno (marcado com seta)',
           # → rotura miofascial
      6219: 'título ou nota do caderno (marcado com seta)',
           # → periostite pos estresse
      6243: 'título ou nota do caderno (marcado com seta)',
           # → alteração medular ósseas inesp
      6268: 'nota de estudo, anatomia ou valor de referência',
           # (dermatite ocre por estase- hemossiderina sai e fica essa pigmentação crônica)
      6299: 'título ou nota do caderno (marcado com seta)',
           # → teni leg sequela mais coleção serohematica
      6320: 'título ou nota do caderno (marcado com seta)',
           # → doms
      6322: 'título ou nota do caderno (marcado com seta)',
           # → pe caido/ denervação do fibular
      6335: 'título ou nota do caderno (marcado com seta)',
           # → sobrecarga
      6381: 'título ou nota do caderno (marcado com seta)',
           # → periostite por estresse
      6390: 'título ou nota do caderno (marcado com seta)',
           # → trombose
      6394: 'rótulo de tópico do caderno',
           # placa fisária alterações
      6395: 'nota de estudo, anatomia ou valor de referência',
           # -edema epifisario sobrecarga mecânica local sem alargamento da fise , olhar no t1 a fise
      6405: 'título de máscara no caderno',
           # PLEXO LOMBOSSACRO
      6428: 'título ou nota do caderno (marcado com seta)',
           # → Informações clínicas disponíveis:
      6429: 'indicação clínica de um paciente específico',
           # Dor glútea crônica e dor na asa do ilíaco.
      6461: 'título de máscara no caderno',
           # PLEXO BRAQUIAL
      6462: 'rótulo de tópico do caderno',
           # coronal t2 fat
      6463: 'título ou nota do caderno (marcado com seta)',
           # coronal t1 → para ver atrofia muscular
      6464: 'nota de estudo, anatomia ou valor de referência',
           # volumétrico axial da cervical para descartar pseudomeningocele e destacamento de raiz
      6465: 'título ou nota do caderno (marcado com seta)',
           # sag fat sat e um sem fta → ver pesudomeningocele e saída da raiz
      6466: 'título ou nota do caderno (marcado com seta)',
           # ventre do escaleno→ entrar no ventre é segmento escaleno gordura lisa não tem alteração
      6467: 'nota de estudo, anatomia ou valor de referência',
           # ver no fat se tem edema ao redor
      6468: 'nota de estudo, anatomia ou valor de referência',
           # ver se tem costela cervical
      6471: 'rótulo de tópico do caderno',
           # anatomia
      6472: 'nota de estudo em tópicos',
           # * O envolvimento de C5/C6 leva à paralisia dos músculos do ombro e bíceps
      6473: 'nota de estudo em tópicos',
           # * O envolvimento do C7 leva à paralisia na extensão dos músculos do punho e da mão
      6474: 'nota de estudo em tópicos',
           # * O envolvimento de C8/T1 leva à paralisia dos flexores do antebraço e dos músculos intr
      6477: 'título ou nota do caderno (marcado com seta)',
           # * foraminal →   raizes c5, c6, c7, c8 e t1
      6478: 'título ou nota do caderno (marcado com seta)',
           # * triangulo escaleno →  escaleno anterior e escaleno medio →  tronco superior, medio e i
      6479: 'título ou nota do caderno (marcado com seta)',
           # * costoclavicular→  fascículo lateral, fascículo médio e fascículo posterior (corda)
      6480: 'título ou nota do caderno (marcado com seta)',
           # * retropeitoral →   fasciculo →  n musculocutâneo, n axilar , n mediano e n.ulnar
      6481: 'rótulo de tópico do caderno',
           # avulsão é de raiz pre ganglionar
      6482: 'título de máscara no caderno',
           # RESSONÂNCIA MAGNÉTICA DO PLEXO BRAQUIAL
      6509: 'título de máscara no caderno',
           # PLEXO TELE
      6569: 'rótulo de tópico do caderno',
           # bom
      6594: 'título ou nota do caderno (marcado com seta)',
           # → neoplasico/radioterapico
      6596: 'título ou nota do caderno (marcado com seta)',
           # → TRAUMA PLEXO
      6623: 'título de máscara no caderno',
           # DESFILADEIRO REDEDOR
      6646: 'título de máscara no caderno',
           # DESFILADEIRO - PLEXO BRAQUIAL
      6681: 'título de máscara no caderno',
           # PUNHO TELE
      6730: 'título de máscara no caderno',
           # PUNHO PADRÃO
      6739: 'rótulo de tópico do caderno',
           # fibrocartilagem triangular
      6740: 'rótulo de tópico do caderno',
           # componentes:
      6741: 'nota de estudo em tópicos',
           # * O disco articular
      6742: 'nota de estudo em tópicos',
           # * Os ligamentos radioulnares dorsal e volar
      6743: 'nota de estudo em tópicos',
           # * O homólogo do menisco
      6744: 'nota de estudo em tópicos',
           # * Bainha do tendão extensor ulnar do carpo
      6745: 'nota de estudo em tópicos',
           # * Os ligamentos ulnocarpais
      6750: 'rótulo de tópico do caderno',
           # Artéria mediana persistente
      6823: 'rótulo de tópico do caderno',
           # (yamasda)
      6834: 'nota de estudo em tópicos',
           # * ROTURA PARCIAL:
      6840: 'nota de estudo em tópicos',
           # * ROTURA COMPLETA:
      6846: 'nota de estudo, anatomia ou valor de referência',
           # separar disco das lâminas
      6853: 'rótulo de tópico do caderno',
           # e 4
      6854: 'rótulo de tópico do caderno',
           # raio x periostite por estresse e calo osseo
      6858: 'rótulo de tópico do caderno',
           # impacto ulnocarpal
      6874: 'rótulo de tópico do caderno',
           # tendão extensores
      6883: 'rótulo de tópico do caderno',
           # flexores
      6909: 'rótulo de tópico do caderno',
           # descontinuidade do retinaculo.
      6947: 'título ou nota do caderno (marcado com seta)',
           # →tenossinovite infecciosa
      6964: 'título ou nota do caderno (marcado com seta)',
           # → Artrite reumatoide
      6982: 'rótulo de tópico do caderno',
           # pos
      6987: 'título ou nota do caderno (marcado com seta)',
           # → Cisto roto
      6993: 'título ou nota do caderno (marcado com seta)',
           # → mecanica / ou kienbock
      7000: 'título de máscara no caderno',
           # PUNHO DISI
      7115: 'título de máscara no caderno',
           # BRAÇO
      7116: 'título ou nota do caderno (marcado com seta)',
           # → vascular/angiodisplasico
      7127: 'título de máscara no caderno',
           # QUADRIL TELE
      7189: 'título de máscara no caderno',
           # QUADRIL PADRÃO
      7194: 'nota de estudo, anatomia ou valor de referência',
           # obs: quadril nao faz sagital
      7195: 'nota de estudo, anatomia ou valor de referência',
           # para leg carve perthes ou epifisiólise mandar injetar no começo que a primeira alteração
      7196: 'nota de estudo, anatomia ou valor de referência',
           # normal da cartilagem do quadril é aumentar o espaço para lateral/extremidades.
      7197: 'rótulo de tópico do caderno',
           # apofisite
      7372: 'título ou nota do caderno (marcado com seta)',
           # → rotura isuitibiais
      7379: 'título ou nota do caderno (marcado com seta)',
           # → meta difusa bacia
      7387: 'título ou nota do caderno (marcado com seta)',
           # → lesão óssea focal-cisto/condral
      7393: 'título ou nota do caderno (marcado com seta)',
           # → lipoenxertia
      7397: 'título ou nota do caderno (marcado com seta)',
           # → avulsao reto femoral
      7405: 'título ou nota do caderno (marcado com seta)',
           # → rotura adutor
      7411: 'título ou nota do caderno (marcado com seta)',
           # → pubeite
      7418: 'título ou nota do caderno (marcado com seta)',
           # → cirurgia
      7425: 'título ou nota do caderno (marcado com seta)',
           # → paget
      7434: 'título ou nota do caderno (marcado com seta)',
           # → gluteo procedimento - silicone/ pmma
      7444: 'título ou nota do caderno (marcado com seta)',
           # → úlcera gluteo
      7450: 'título ou nota do caderno (marcado com seta)',
           # → lesão cistica ( sangue ou conteudo proteico)
      7460: 'título ou nota do caderno (marcado com seta)',
           # → hemipelvectomia- cirurgia sarcoma bacia
      7498: 'título de máscara no caderno',
           # QUADRIL OSTEONECROSE/FX
      7598: 'identificação de caso, paciente, data ou local',
           # quadril protese rede dor
      7650: 'título de máscara no caderno',
           # IMPLANTE GLÚTEO
      7651: 'nota de estudo, anatomia ou valor de referência',
           # ( olhar o marcador para ver se a protese virou)
      7655: 'rótulo de tópico do caderno',
           # artropatia amiloide
      7664: 'link de referência',
           # https://radiopaedia.org/cases/haemodialysis-induced-amyloid-arthropathy-of-hip
      7673: 'identificação de caso, paciente, data ou local',
           # QUADRIL PADRÃO CEDIRP
      7703: 'identificação de caso, paciente, data ou local',
           # QUADRIL DEGENERATIVO CEDIRP:
      7729: 'rótulo de tópico do caderno',
           # fx insuficiencia sacro
      7741: 'título ou nota do caderno (marcado com seta)',
           # → ulcera sacral pressão
      7758: 'título ou nota do caderno (marcado com seta)',
           # → cordoma
      7761: 'rótulo de tópico do caderno',
           # ct
      7778: 'rótulo de tópico do caderno',
           # rm
      7804: 'identificação de caso, paciente, data ou local',
           # dia 28/03 novo exame recidiva
      7814: 'rótulo de tópico do caderno',
           # pos
      7815: 'título de máscara no caderno',
           # SACROCOCCÍGEA TELE
      7860: 'título de máscara no caderno',
           # SACROCOCCÍGEA PADRÃO
      7935: 'título de máscara no caderno',
           # SACROILÍACA TELE
      7938: 'link de referência',
           # https://www.mskrad.com.br/post/altera%C3%A7%C3%B5es-mec%C3%A2nicas-na-articula%C3%A7%C3%
      7992: 'título de máscara no caderno',
           # SACROILÍACA PADRÃO
      7995: 'nota de estudo, anatomia ou valor de referência',
           # tem erosão , edema e realce , apesar de ser de um lado so colocar que nao se pode descar
      7998: 'rótulo de tópico do caderno',
           # t1 erosões subcondrais
      8001: 'rótulo de tópico do caderno',
           # t2 edema
      8004: 'nota de estudo, anatomia ou valor de referência',
           # pos realça
      8012: 'rótulo de tópico do caderno',
           # - Sacroiliíte
      8016: 'rótulo de tópico do caderno',
           # - Cisto meníngeo
      8020: 'título ou nota do caderno (marcado com seta)',
           # → pos parto
      8032: 'rótulo de tópico do caderno',
           # inflamatório começa no rebordo sacral
      8114: 'título ou nota do caderno (marcado com seta)',
           # → ESPÍCULA COCIX
      8136: 'título de máscara no caderno',
           # SACROILIEITE
      8137: 'nota de estudo, anatomia ou valor de referência',
           # edema no terço médio eh totalmente inespecífico, uncia coisa que ajuda são umas faixas d
      8155: 'título ou nota do caderno (marcado com seta)',
           # → sinovite
      8241: 'título ou nota do caderno (marcado com seta)',
           # → miosite inflamatoria
      8258: 'título de máscara no caderno',
           # SÍNFISE PÚBICA
      8266: 'título de máscara no caderno',
           # F
      8277: 'título de máscara no caderno',
           # SINFISE PÚBICA
      8280: 'rótulo de tópico do caderno',
           # rotura
      8329: 'título de máscara no caderno',
           # TORAX ARCO COSTAL
      8375: 'título de máscara no caderno',
           # TORNOZELO TELE
      8477: 'título de máscara no caderno',
           # TORNOZELO PADRÃO
      8480: 'nota de estudo, anatomia ou valor de referência',
           # quando o T1 está muito escuro pode dar lesão osteocondral e esse osso já era
      8815: 'nota de estudo em tópicos',
           # * manipulação crurgica calcaneo
      8817: 'nota de estudo em tópicos',
           # * trauma
      8830: 'nota de estudo em tópicos',
           # * - Charcot
      8833: 'nota de estudo em tópicos',
           # * -Gota
      8845: 'nota de estudo em tópicos',
           # * neuropatia nervo plantar ( medial)
      8848: 'nota de estudo em tópicos',
           # *    *      *    *    *    *    * pe plano edema mecanico
      8850: 'nota de estudo, anatomia ou valor de referência',
           # ------ pe plano
      8881: 'identificação de caso, paciente, data ou local',
           # TORNOZELO ARTROSA GEMA
      8898: 'identificação de caso, paciente, data ou local',
           # TORNOZELO PADRÃO CEDIRP
      8925: 'rótulo de tópico do caderno',
           # kage
      8928: 'identificação de caso, paciente, data ou local',
           # TORNOZELO HAGLUND CEDIRP
      8959: 'identificação de caso, paciente, data ou local',
           # TORNOZELO TALOFIBULAR CEDIRP
      8993: 'rótulo de tópico do caderno',
           # osteomi
      8996: 'título de máscara no caderno',
           # PATOLOGIAS
      8997: 'rótulo de tópico do caderno',
           # lesao por arma de fogo
      8998: 'nota de estudo, anatomia ou valor de referência',
           # projetil pode ter lesoa termica
      9008: 'rótulo de tópico do caderno',
           # ciatico
      9013: 'rótulo de tópico do caderno',
           # tumor
      9014: 'nota de estudo em tópicos',
           # 1- tumor ginganto celular
      9025: 'nota de estudo, anatomia ou valor de referência',
           # segundo pos contraste
      9030: 'nota de estudo em tópicos',
           # 2- osteossarcoma parosteal?
      9052: 'nota de estudo, anatomia ou valor de referência',
           # segundo sao pós contraste
      9053: 'nota de estudo, anatomia ou valor de referência',
           # ( pode ser osteosarcoma parosteal --> esse é fora para dentro--- tgc e cisto osseo aneur
      9056: 'rótulo de tópico do caderno',
           # tumor
      9060: 'rótulo de tópico do caderno',
           # osteocondroma?
      9110: 'rótulo de tópico do caderno',
           # sarcoidose ou meta
      9120: 'rótulo de tópico do caderno',
           # pos e t2
      9123: 'rótulo de tópico do caderno',
           # pos e t2
      9136: 'título de máscara no caderno',
           # OSTEOMIELITE
      9155: 'rótulo de tópico do caderno',
           # espessamento cortico periosteal
      9158: 'rótulo de tópico do caderno',
           # descontinuidade cortical e sequestro
      9196: 'título ou nota do caderno (marcado com seta)',
           # → penumbra após retirada de parafuso cirúrgico ( periferia mais branca)
      9205: 'rótulo de tópico do caderno',
           # Osteomielite cronica
      9213: 'título de máscara no caderno',
           # TOMOGRAFIA MÚSCULO
      9216: 'rótulo de tópico do caderno',
           # ct corpo inteiro
      9217: 'rótulo de tópico do caderno',
           # mileoma
      9243: 'rótulo de tópico do caderno',
           # frase ct
      9244: 'rótulo de tópico do caderno',
           # coluna
      9248: 'rótulo de tópico do caderno',
           # exames de msk tomo
      9254: 'nota de estudo, anatomia ou valor de referência',
           # Não fala de raiz neural na tomo
      9255: 'identificação de caso, paciente, data ou local',
           # CT CERVICAL (SAMIR)
      9482: 'rótulo de tópico do caderno',
           # Cirurgia coluna
      9494: 'identificação de caso, paciente, data ou local',
           # CT COL DORSAL(SAMIR)
      9626: 'identificação de caso, paciente, data ou local',
           # CT LOMBAR ( SAMIR)
      9790: 'título de máscara no caderno',
           # CT COXA
      9834: 'título ou nota do caderno (marcado com seta)',
           # → se tomasse anticoagulante tem hematoma ( pode ter essa dúvida na Resso)
      9835: 'título ou nota do caderno (marcado com seta)',
           # → produzindo calcificação até que prove ao contrário é tumor ( no caso deve ser um sarco
      9867: 'título de máscara no caderno',
           # CT JOELHO
      9892: 'título de máscara no caderno',
           # CT JOELHOS ARTROSE
      9911: 'título de máscara no caderno',
           # CT JOELHO LUXAÇÃO PATELA E TAGT
      9970: 'título de máscara no caderno',
           # CT OMBRO TRAUMA
     10004: 'título de máscara no caderno',
           # CT OMBRO
     10053: 'rótulo de tópico do caderno',
           # ct bacia paget
     10083: 'rótulo de tópico do caderno',
           # ct quadril santa
     10091: 'rótulo de tópico do caderno',
           # Infiltração medular?
     10094: 'rótulo de tópico do caderno',
           # Osteossíntese
     10096: 'rótulo de tópico do caderno',
           # Transtrocantérica sem desalinhamento
     10098: 'rótulo de tópico do caderno',
           # Subcapital
     10101: 'rótulo de tópico do caderno',
           # Espinha ilíaca
     10104: 'rótulo de tópico do caderno',
           # Sequela
     10106: 'rótulo de tópico do caderno',
           # - Alterações degenerativas (Osteoartrose)
     10107: 'rótulo de tópico do caderno',
           # Quadril
     10110: 'rótulo de tópico do caderno',
           # Sacroilíacas / púbis
     10114: 'rótulo de tópico do caderno',
           # Entesófitos
     10116: 'rótulo de tópico do caderno',
           # - Perda da concavidade cabeça / colo femoral
     10118: 'rótulo de tópico do caderno',
           # - Teto acetabular
     10120: 'título de máscara no caderno',
           # - COLUNA
     10122: 'título de máscara no caderno',
           # - SUBCUTÂNEO
     10125: 'rótulo de tópico do caderno',
           # Calcificações
     10128: 'título de máscara no caderno',
           # - MÚSCULO
     10133: 'título de máscara no caderno',
           # - TUMOR OSSEO
     10134: 'rótulo de tópico do caderno',
           # Baixa agressividade
     10200: 'título de máscara no caderno',
           # CT QUADRIL PROTESE
     10242: 'título de máscara no caderno',
           # CT QUADRIL
     10269: 'título ou nota do caderno (marcado com seta)',
           # → luxação
     10286: 'nota de estudo, anatomia ou valor de referência',
           # olhar se tem osteonecrose porque pode ter lesão de artéria circunflexa, qlq coisa que ti
     10410: 'título de máscara no caderno',
           # CT BACIA- LIVRO ABERTO COMINUTIVA
     10481: 'identificação de caso, paciente, data ou local',
           # CT BACIA- PRÓTESE GLÚTEO ( gema)
     10524: 'título de máscara no caderno',
           # CT PÉ COALIZÃO
     10551: 'título de máscara no caderno',
           # CT PUNHO INFECCIOSA
     10587: 'título de máscara no caderno',
           # CT PUNHO TRAUMA
     10646: 'identificação de caso, paciente, data ou local',
           # CT TORNOZELO SANTA CATARINA
     10650: 'título de máscara no caderno',
           # - NAVICULAR
     10655: 'título de máscara no caderno',
           # - ENTESÓFITOS
     10658: 'título de máscara no caderno',
           # - TENDÃO CALCÂNEO
     10661: 'rótulo de tópico do caderno',
           # - Charcot
     10665: 'rótulo de tópico do caderno',
           # -Gota
     10709: 'título de máscara no caderno',
           # CT TORNOZELO
     10758: 'título ou nota do caderno (marcado com seta)',
           # → barra ossea ( pos op)
     10780: 'título ou nota do caderno (marcado com seta)',
           # → barra óssea ( antes de operar /mesmo paciente )antes de operar
     10812: 'identificação de caso, paciente, data ou local',
           # versao acetabular rede dor
     10878: 'identificação de caso, paciente, data ou local',
           # versao femoral e tibial modelo hap vida
     10905: 'rótulo de tópico do caderno',
           # Ângulos quadril
     10906: 'rótulo de tópico do caderno',
           # ÂNGULO CENTRO BORDA (da cobertura acetabular)
     10907: 'nota de estudo, anatomia ou valor de referência',
           # normal adulto 30-40°
     10914: 'título de máscara no caderno',
           # ÂNGULO ALFA
     10915: 'nota de estudo, anatomia ou valor de referência',
           # normal ate 60 °
     10937: 'identificação de caso, paciente, data ou local',
           # Versão femoral: 19,4 (antevertido)
     10938: 'nota de estudo, anatomia ou valor de referência',
           # normal adulto: 8 a 15°
     10952: 'título de máscara no caderno',
           # CÉRVICO DIAFISÁRIO
     10953: 'nota de estudo, anatomia ou valor de referência',
           # normal adulto 120 a 135°
     10960: 'título de máscara no caderno',
           # VERSÃO ACETABULAR ( RETROVERSÃO E ANTEVERSÃO)
     10961: 'título ou nota do caderno (marcado com seta)',
           # abaixo de 10→ retrovertida
     10962: 'nota de estudo, anatomia ou valor de referência',
           # ângulo reto em relação a borda acetabular anterior.
     10987: 'rótulo de tópico do caderno',
           # obs joelho roto
     10992: 'rótulo de tópico do caderno',
           # tirads
     11003: 'título de máscara no caderno',
           # TUMOR
     11006: 'rótulo de tópico do caderno',
           # biceps femoral e semitendieo
     11009: 'identificação de caso, paciente, data ou local',
           # nida oliveira da silva pereira
     11010: 'título ou nota do caderno (marcado com seta)',
           # → pos op tumor
     11015: 'título ou nota do caderno (marcado com seta)',
           # → cotrole de ressecção de tumor ombro
     11028: 'nota de estudo, anatomia ou valor de referência',
           # nao tem aspecto expansivo de recidiva
     11029: 'rótulo de tópico do caderno',
           # infeção falta periostite e inflamação
     11044: 'nota de estudo, anatomia ou valor de referência',
           # pode corresponder a infarto ósseo
     11049: 'nota de estudo, anatomia ou valor de referência',
           # nao tem aspecto expansivo de recidiva
     11050: 'rótulo de tópico do caderno',
           # infeção falta periostite e inflamação
     11053: 'título ou nota do caderno (marcado com seta)',
           # → Lipossarcoma
     11060: 'título ou nota do caderno (marcado com seta)',
           # → tcg
     11070: 'título ou nota do caderno (marcado com seta)',
           # → provável linfoma
     11074: 'rótulo de tópico do caderno',
           # (t1, t2, t2ft, t1 pos)
     11077: 'título de máscara no caderno',
           # T2,T1, T1POS
     11080: 'título de máscara no caderno',
           # INSAÃO DA CAVA
     11083: 'título de máscara no caderno',
           # AORTA E SACRO
     11098: 'identificação de caso, paciente, data ou local',
           # tornozelo santa cat
     11100: 'título de máscara no caderno',
           # - NAVICULAR
     11105: 'título de máscara no caderno',
           # - ENTESÓFITOS
     11108: 'título de máscara no caderno',
           # - TENDÃO CALCÂNEO
     11111: 'rótulo de tópico do caderno',
           # - Charcot
     11115: 'rótulo de tópico do caderno',
           # -Gota
     11164: 'rótulo de tópico do caderno',
           # us msk
     11215: 'rótulo de tópico do caderno',
           # us msuk punho
     11319: 'rótulo de tópico do caderno',
           # us figado
     11326: 'título de máscara no caderno',
           # CASOS INTERESSANTES TELE
     11342: 'título de máscara no caderno',
           # ---> TUMORES
     11349: 'nota de estudo em tópicos',
           # 1-- CONDROSSARCOMA
     11352: 'rótulo de tópico do caderno',
           # idioso
     11353: 'rótulo de tópico do caderno',
           # ossos longos
     11356: 'nota de estudo em tópicos',
           # 2- TGC
     11359: 'rótulo de tópico do caderno',
           # extremidade/ epífise  / ultrapassa a  fise
     11362: 'nota de estudo em tópicos',
           # 3- condroblastoma
     11363: 'rótulo de tópico do caderno',
           # epífise
     11370: 'título de máscara no caderno',
           # TORAX
     11378: 'título ou nota do caderno (marcado com seta)',
           # → supeito de osteoma osteoide
     11404: 'rótulo de tópico do caderno',
           # pbmicose
     11412: 'título de máscara no caderno',
           # FISTULA
     11465: 'rótulo de tópico do caderno',
           # escoliose coluna lombar
     11515: 'rótulo de tópico do caderno',
           # acondroplasia
     11570: 'identificação de caso, paciente, data ou local',
           # rede dor arrumar
     11653: 'nome de colega ou de paciente',
           # marco b
     11811: 'identificação de caso, paciente, data ou local',
           # kim
     11889: 'nome de colega ou de paciente',
           # alfredo
     11947: 'identificação de caso, paciente, data ou local',
           # kim
     11972: 'identificação de caso, paciente, data ou local',
           # kim
     11979: 'nome de colega ou de paciente',
           # marco
     12008: 'identificação de caso, paciente, data ou local',
           # kim
     12034: 'identificação de caso, paciente, data ou local',
           # kim
     12177: 'identificação de caso, paciente, data ou local',
           # KIM
     12178: 'título de máscara no caderno',
           # ARTRODESE
     12203: 'nome de colega ou de paciente',
           # faissal
     12217: 'nome de colega ou de paciente',
           # faissa
     12311: 'nome de colega ou de paciente',
           # paola
     12320: 'nome de colega ou de paciente',
           # TOR KIM
     12351: 'nome de colega ou de paciente',
           # hernani
     12373: 'nome de colega ou de paciente',
           # paulo
     12383: 'identificação de caso, paciente, data ou local',
           # hemangioma intramuscular mao rede dor
     12388: 'título de máscara no caderno',
           # ESSONÂNCIA MAGNÉTICA DA MÃO ESQUERDA
     12417: 'identificação de caso, paciente, data ou local',
           # kim
     12540: 'nome de colega ou de paciente',
           # pedro
     12547: 'identificação de caso, paciente, data ou local',
           # kim
     12569: 'rótulo de tópico do caderno',
           # retroversao
}
