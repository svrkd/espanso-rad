---
name: laude
description: "Monta laudo radiológico completo, qualquer método/território, exclusivamente com texto da base fechada em references/ (templates, achados e conclusões gerados de match/*.yml). Não presume lateralidade, medida, achado ou comparação: pergunta antes de montar. Texto ditado por voz entra no lugar da frase da base, com pontuação falada convertida, português corrigido e ordem de descrição arrumada; redige frase só quando a base e o ditado não cobrem o achado. Classificações (BI-RADS, TI-RADS, LI-RADS, O-RADS, Bosniak etc.) só com dados suficientes, com critérios das skills irmãs /carotidas, /mamas, /arterial-mmii e /mapa. Aciona ao invocar /laude ou colar dado bruto/parcial pedindo para montar/fechar o laudo. Não aciona para reescrita de texto pronto (/melhore), diferencial sem laudo (/dx) ou ordem de revisão sem achado (/roteiro-leitura)."
---

`/laude`: monta laudo completo a partir de dado bruto ou parcial, usando só a biblioteca fechada em `references/`.

PRINCÍPIO: BIBLIOTECA FECHADA
- Fonte de cada frase, nesta ordem: (1) a base (templates, achados, conclusões e fragmentos lidos por `busca.py`); (2) o texto ditado pelo usuário (seção TEXTO DITADO); (3) frase redigida pela skill, só como último recurso (seção FRASE REDIGIDA). Proibido parafrasear, fundir ou "melhorar" frase da base, e redigir frase própria quando a base ou o ditado cobrem o achado.
- Edição permitida sobre o texto da base, e só ela: preencher `_` com o dado informado; escolher uma das alternativas separadas por `/`; retirar frase normal contradita; inserir frase de achado; trocar a conclusão normal pela conclusão dos achados; ajustar lateralidade e unidade de medida ao que o usuário informou (seção DADO DO USUÁRIO PREVALECE). A coluna `alternativas` do índice diz se a entrada tem escolha real (`sim`); `/` fixo (`inflamatório/infeccioso`) não é alternativa.
- Nunca presumir lateralidade, medida, achado, fase de contraste (salvo a do template padrão) ou dado comparativo. Dado do usuário entra como veio, sem arredondar, com a unidade que o usuário usou.
- Sem frase na base para um achado informado de forma coloquial ("tem uma fratura no quinto arco costal esquerdo"), e sem texto ditado: redigir a frase (seção FRASE REDIGIDA).

FLUXO DE CONSULTA (nesta ordem, sem desvio)
a) Ler `references/rotas.md` e `references/padroes.tsv` (uma chamada). Identificar modalidade, região e seção.
b) Abrir só os índices pertinentes em `references/indices/` (1 a 3 por consulta; um índice partido em `__1`, `__2`... conta como um). O índice de templates do arquivo (`<arquivo>__templates`) conta entre eles. Ler a linha `# ATENÇÃO` do topo: os `Xc` listados ali não são conclusões.
c) Escolher os triggers pelo `label` e pelo `tipo`. O template sai da seção TEMPLATE PADRÃO, sem pergunta; só se ela não resolver, listar os candidatos pelos labels e perguntar qual (conta entre as perguntas da rodada).
d) Uma única chamada: `python3 references/busca.py <trigger> [<trigger> ...]` com todos os triggers escolhidos. A saída traz o par de conclusão logo abaixo de cada achado.
Proibido grep livre em `textos.json`, leitura de arquivo inteiro fora de `rotas.md`, `padroes.tsv` e dos índices escolhidos, e chamadas repetidas de `busca.py` por trigger. Faltou trigger depois da chamada (erro de trigger inexistente ou achado que só apareceu na resposta do usuário): uma chamada adicional com todos os que faltam.

TEMPLATE PADRÃO (sem perguntar)
- Ordem de decisão, parando na primeira que resolve:
  1. Padrão escolhido pelo usuário antes nesta conversa ou guardado na memória do Claude (`Padrão /laude: <exame> → <trigger>`).
  2. `references/padroes.tsv` (ler junto com `rotas.md` no passo a). TC de crânio: "crânio de adulto" → `tccrad`; "crânio de idoso" → `tccrid`; "crânio de jovem" ou nada dito → `tccr`. A faixa vem só dessas palavras: idade informada não escolhe template e não gera pergunta.
  3. Regra geral: entre os candidatos do exame, o normal sem contraste (S/C) e sem Doppler, salvo se o usuário citar contraste, fase ou Doppler. Exceções sempre com contraste (C/C): TC de pescoço e qualquer angiotomografia.
  4. Ainda mais de um candidato: perguntar qual, uma vez, e guardar a resposta como padrão (abaixo).
- Guardar o padrão escolhido pelo usuário: (a) com ferramenta de memória disponível, salvar `Padrão /laude: <exame> [condição] → <trigger>`; (b) com `references/padroes.tsv` gravável (Claude Code com o repositório), acrescentar a linha `<exame>\t<condição>\t<trigger>\tusuário, <data>`; (c) sempre propor o prompt para o Claude Code (seção PROPOSTA DE PADRÃO). O padrão vale para as próximas consultas da conversa mesmo sem (a) nem (b).
- A fase do template padrão conta como informada: S/C (ou C/C nas exceções) vale para classificação e limiar sem pergunta, salvo se o usuário disser outra.
- Template padrão com lado, sexo ou outro dado fixo que o pedido contradiz: usar o template assim mesmo e ajustar o texto (seção DADO DO USUÁRIO PREVALECE), sem perguntar.

DADO DO USUÁRIO PREVALECE
- Lateralidade: template ou frase da base com lado diferente do informado (no título, na análise ou na conclusão): trocar o lado em todas as ocorrências do mesmo achado ou da mesma estrutura, com a concordância correspondente ("direito" → "esquerdo", "à direita" → "à esquerda", "artéria lobar inferior direita" → "esquerda"). Frase normal do lado oposto, que não descreve o achado, fica como está.
- Medida em milímetros: entra em mm com uma casa decimal ("6 mm" → "6,0 mm"; "6,5 mm" fica "6,5 mm"), mesmo quando a frase da base traz `_ cm`: o `_ cm` vira `<valor> mm`. Medida em centímetros entra como veio.
- Outro dado fixo da frase da base que o usuário contradiz (grau, segmento, número de lesões): trocar pelo informado. Dado fixo que o usuário não confirmou nem contradisse fica como está na base, sem pergunta.

MÁSCARA
- Partir do template do método e região. Sem template no arquivo do território (`angio.yml`, `tc_abd.yml`): usar o template de TC da região em `tc.yml` e inserir as frases de achado do arquivo do território. Sem template nem assim: `[COMPLETAR: máscara de <exame>]` e avisar fora do bloco.
- Cabeçalhos do template ficam como estão (`Técnica:`, `Análise:`, `Conclusão:`).
- Linhas de `malu.yml` abertas por marcador de linha opcional (`XXX`, `XX`, `###`, `#`): entram só se o achado da linha foi informado, sem o marcador; não informado, a linha sai.

TEXTO DITADO
- Reconhecimento: frase completa, com verbo e redação de laudo, é texto ditado; entra no laudo e não se busca frase na base para ela. Dado telegráfico ("nódulo 1,2 cm lobo direito") é dado: busca-se a frase na base. Ambíguo: perguntar (conta na rodada).
- Pontuação falada vira sinal: "vírgula", "ponto", "ponto final", "dois pontos", "ponto e vírgula". "Parágrafo" e "nova linha" viram quebra.
- Números ditados por extenso viram algarismos arábicos com a unidade abreviada ("um vírgula dois centímetros" → "1,2 cm"). Exceção: categoria de classificação cuja notação é em romano (ex.: Bosniak II, IIF) fica em romano; na dúvida, seguir a notação da frase da base para aquela classificação.
- Correção de português objetiva (ortografia, acentuação, concordância, regência, pontuação) e de termo técnico que o reconhecimento de voz trocou, só quando a troca é inequívoca ("hipo ecoico" → "hipoecoico"). Termo duvidoso: perguntar, nunca chutar.
- Liberdade de organização, sem acrescentar nem retirar conteúdo clínico (achado, medida, lado, grau, hipótese): achado como sujeito da frase, sem "observa-se", "identifica-se", "nota-se", "evidencia-se"; frases fragmentadas do mesmo achado unidas por gerúndio/particípio; achado associado ao principal unido por "Associa-se…"; repetições e muletas do ditado ("é… é", "tá", "né") removidas.
- Ordem da descrição de lesão, reordenando o que vier fora dela: natureza (formação nodular, massa, lesão sólido-cística…) → características do aspecto (ecogenicidade, densidade, sinal) → forma → margens → limites → conteúdo, realce ou Doppler → localização → relação com estruturas vizinhas → medidas → volume → inferência ditada, se houver ("podendo corresponder a…"), ao fim da frase.
- Posição: no parágrafo da estrutura correspondente do template, depois da descrição normal. Contradiz frase normal da máscara: a frase normal sai inteira.
- Conclusão: conclusão ditada entra como ditada, com as mesmas correções. Sem conclusão ditada: a frase do achado, como ficou na Análise, copiada na íntegra para a Conclusão, na ordem da Análise. Não se busca par `xc` para texto ditado.

FRASE REDIGIDA (último recurso)
- Só para achado informado sem frase na base e sem redação de laudo ditada.
- Padrão /descreva e das regras de MONTAGEM DA ANÁLISE: achado como sujeito, sem "observa-se", "identifica-se" e afins, o mais curta que a precisão permitir ("Fratura do quinto arco costal esquerdo."). Achado mais complexo admite redação radiológica completa, na ordem de descrição de lesão da seção TEXTO DITADO.
- Leva só o que o usuário informou. Não acrescenta desvio, consolidação, medida, lado, grau, negativa ("sem desvio") nem hipótese. Faltando dado que a frase exige (ex.: lado): perguntar (conta na rodada).
- Conclusão: a frase redigida copiada na íntegra, na ordem da Análise.
- Listada fora do bloco em `Redigido:`.

PERGUNTAS ANTES DE MONTAR
- Pergunta-se ANTES de montar, sempre que faltar: dado exigido por `_` (coluna `lacunas` > 0) em entrada que vai ao laudo; escolha entre alternativas `/`; lateralidade não informada; dado que muda classificação, limiar ou par de conclusão; escolha de template que a seção TEMPLATE PADRÃO não resolveu.
- Não se pergunta: lado, unidade ou dado fixo que o usuário já informou diferente da base (ajusta-se); template que a seção TEMPLATE PADRÃO resolve.
- No máximo 3 perguntas por rodada, numeradas, de resposta curta, sem preâmbulo. Prioridade: o que muda classificação ou lateralidade, depois escolha de template, depois medidas. Faltando mais de 3, nova rodada com o resto depois da resposta.
- Sem laudo parcial, rascunho ou versão provisória junto da pergunta: o rascunho é o que será copiado e anula a pergunta.
- Usuário diz que não tem o dado ou manda seguir: o `_` vira `[COMPLETAR: <dado>]`, a alternativa não escolhida vira `[COMPLETAR: <opção A> / <opção B>]`, e a lacuna é listada fora do bloco.

MONTAGEM DA ANÁLISE
- Um parágrafo por estrutura/órgão, como no template. Sem conector de transição entre parágrafos de estruturas diferentes.
- Ordem fixa dentro do parágrafo: descrição normal/basal primeiro, achado(s) anormal(is) por último.
- Achado que contradiz frase normal da máscara: a frase normal sai inteira e entra a frase do achado. Negativa contradita sai inteira, nunca fica pela metade nem é reescrita.
- Cada achado anormal é frase própria (a frase da base), recortável para a Conclusão na mesma ordem.
- Quando o achado afeta só parte da estrutura e a base tem a nota de completude correspondente (fragmento como "Restante de … preservado"), ela vai em parágrafo próprio, separado do achado. Sem nota na base: frase redigida no padrão "Restante de <estrutura> preservado."
- Estrutura do template não mencionada pelo usuário mantém a frase normal do template, que é texto da base. Estrutura que não está no template e não foi informada não entra.

CONCLUSÃO
- Exame sem achado: a conclusão normal do template, sem mudança.
- Com achado: a conclusão normal do template sai. Cada achado entra na ordem em que apareceu na Análise: o par `xc` quando existir; sem par, a frase do achado copiada na íntegra, igual à da Análise.
- Classificação (BI-RADS, TI-RADS, LI-RADS, O-RADS, Bosniak, Lung-RADS, PI-RADS etc.) só quando os dados informados permitirem aplicá-la sem presumir nada. Dado insuficiente: perguntar (entra na rodada); usuário sem o dado: `[COMPLETAR: categoria <sistema>]`. O texto da categoria vem da base; sem frase na base, frase redigida só com a categoria.
- Diferencial, conduta ou correlação só se estiverem na frase da base usada.

SKILLS IRMÃS: FONTE DOS CRITÉRIOS, NÃO DO TEXTO
- US Doppler de carótidas/vertebrais → critérios de `/carotidas`; mamografia/US mamário (BI-RADS) → `/mamas`; Doppler arterial de MMII → `/arterial-mmii`; mapeamento venoso de MMII → `/mapa`.
- Consultar a skill irmã internamente mesmo que o usuário não a tenha chamado, só para aplicar limiar e categoria. O texto do laudo continua vindo da base desta skill.
- Conteúdo da skill irmã inacessível: declarar isso fora do bloco e não aplicar a classificação; nunca usar regra genérica disfarçada de critério específico.
- Limiar ou índice derivado (IR, razões, % de estenose) só com o critério da skill irmã ou o que estiver escrito na própria frase da base, e só para preencher um `_` existente. Sem critério documentado: não pesquisar na web nem usar memória; `[COMPLETAR]` e avisar.

PROPOSTA DE PADRÃO
- Quando a consulta mostra algo que deveria virar padrão, a resposta termina com um prompt pronto para o usuário mandar ao Claude Code no repositório `espanso-rad`. Casos:
  - template escolhido pelo usuário depois de pergunta → linha nova em `skills/laude/references/padroes.tsv`;
  - frase redigida pela skill (`Redigido:`) ou texto ditado para achado sem frase na base → novo match via `/add-espanso`, com o texto final e o par de conclusão;
  - usuário corrigiu ou reescreveu a frase da base, ou pediu outro jeito de escrever → alterar aquele match (arquivo e trigger nomeados) ou criar variante;
  - lado, sexo ou outro dado fixo do template trocado porque o usuário disse outro → transformar o dado fixo em alternativa (`DIREITO / ESQUERDO`) no match;
  - pergunta que a skill teve de fazer e que dependia de preferência, não de dado do exame (alternativa `/` escolhida, formato de medida, ordem, unidade, fase) → regra nova no `skills/laude/SKILL.md` ou alternativa padrão no match;
  - frase da base com dado fixo que gerou pergunta ou `[COMPLETAR]` (ex.: "segmentares e subsegmentares") → partir a frase em variantes ou trocar o dado por `_`.
- Formato: depois da linha de triggers, uma linha por proposta, no máximo 3: `Proposta para o Claude Code: "<prompt>"`. O prompt é autossuficiente: nomeia arquivo, trigger, texto atual e texto ou regra pedida, sem depender desta conversa.
- Nada a propor: nenhuma linha. Não propor o que já está em `padroes.tsv` ou nas regras desta skill.

SAÍDA
- Um bloco único de código, pronto para colar, só com o laudo.
- Fora do bloco, no máximo uma linha: `Triggers: <lista> · Ditado: <estruturas ou "nenhum"> · Redigido: <achados ou "nenhum"> · Lacunas: <lista ou "nenhuma">`. Lacunas incluem todo `[COMPLETAR]` e classificação não aplicada.
- Depois dela, só as linhas `Proposta para o Claude Code:` quando houver (seção PROPOSTA DE PADRÃO).
- Nada mais: sem explicação, sem lista de estruturas, sem nota sobre a montagem.
