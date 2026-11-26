---
name: laude
description: "Monta laudo radiológico completo, qualquer método/território, exclusivamente com texto da base fechada em references/ (templates, achados e conclusões gerados de match/*.yml). Não redige frase clínica própria nem presume lateralidade, medida, achado ou comparação: pergunta antes de montar e marca [COMPLETAR] onde a base não tem frase. Classificações (BI-RADS, TI-RADS, LI-RADS, O-RADS, Bosniak etc.) só com dados suficientes, com critérios das skills irmãs /carotidas, /mamas, /arterial-mmii e /mapa. Aciona ao invocar /laude ou colar dado bruto/parcial pedindo para montar/fechar o laudo. Não aciona para reescrita de texto pronto (/melhore), diferencial sem laudo (/dx) ou ordem de revisão sem achado (/roteiro-leitura)."
---

`/laude`: monta laudo completo a partir de dado bruto ou parcial, usando só a biblioteca fechada em `references/`.

PRINCÍPIO: BIBLIOTECA FECHADA
- Todo texto do laudo vem da base: templates, achados, conclusões e fragmentos lidos por `busca.py`. Proibido redigir frase clínica própria, parafrasear, fundir ou "melhorar" frase da base.
- Edição permitida sobre o texto da base, e só ela: preencher `_` com o dado informado; escolher uma das alternativas separadas por `/`; retirar frase normal contradita; inserir frase de achado; trocar a conclusão normal pela conclusão dos achados. A coluna `alternativas` do índice diz se a entrada tem escolha real (`sim`); `/` fixo (`inflamatório/infeccioso`) não é alternativa.
- Nunca presumir lateralidade, medida, achado, fase de contraste ou dado comparativo. Dado do usuário entra exatamente como veio, sem arredondar nem trocar unidade.
- Sem frase na base para um achado informado: inserir `[COMPLETAR: descrição de <achado>]` no ponto exato do laudo e avisar fora do bloco. Nunca improvisar a frase.

FLUXO DE CONSULTA (nesta ordem, sem desvio)
a) Ler `references/rotas.md`. Identificar modalidade, região e seção.
b) Abrir só os índices pertinentes em `references/indices/` (1 a 3 por consulta; um índice partido em `__1`, `__2`... conta como um). O índice de templates do arquivo (`<arquivo>__templates`) conta entre eles. Ler a linha `# ATENÇÃO` do topo: os `Xc` listados ali não são conclusões.
c) Escolher os triggers pelo `label` e pelo `tipo`. Vários templates candidatos para o mesmo exame: listar pelos labels e perguntar qual (conta entre as perguntas da rodada).
d) Uma única chamada: `python3 references/busca.py <trigger> [<trigger> ...]` com todos os triggers escolhidos. A saída traz o par de conclusão logo abaixo de cada achado.
Proibido grep livre em `textos.json`, leitura de arquivo inteiro fora de `rotas.md` e dos índices escolhidos, e chamadas repetidas de `busca.py` por trigger. Faltou trigger depois da chamada (erro de trigger inexistente ou achado que só apareceu na resposta do usuário): uma chamada adicional com todos os que faltam.

MÁSCARA
- Partir do template do método e região. Sem template no arquivo do território (`angio.yml`, `tc_abd.yml`): usar o template de TC da região em `tc.yml` e inserir as frases de achado do arquivo do território. Sem template nem assim: `[COMPLETAR: máscara de <exame>]` e avisar fora do bloco.
- Cabeçalhos do template ficam como estão (`Técnica:`, `Análise:`, `Conclusão:`).
- Linhas de `malu.yml` abertas por marcador de linha opcional (`XXX`, `XX`, `###`, `#`): entram só se o achado da linha foi informado, sem o marcador; não informado, a linha sai.

PERGUNTAS ANTES DE MONTAR
- Pergunta-se ANTES de montar, sempre que faltar: dado exigido por `_` (coluna `lacunas` > 0) em entrada que vai ao laudo; escolha entre alternativas `/`; lateralidade; dado que muda classificação, limiar ou par de conclusão; escolha entre templates candidatos.
- No máximo 3 perguntas por rodada, numeradas, de resposta curta, sem preâmbulo. Prioridade: o que muda classificação ou lateralidade, depois escolha de template, depois medidas. Faltando mais de 3, nova rodada com o resto depois da resposta.
- Sem laudo parcial, rascunho ou versão provisória junto da pergunta: o rascunho é o que será copiado e anula a pergunta.
- Usuário diz que não tem o dado ou manda seguir: o `_` vira `[COMPLETAR: <dado>]`, a alternativa não escolhida vira `[COMPLETAR: <opção A> / <opção B>]`, e a lacuna é listada fora do bloco.

MONTAGEM DA ANÁLISE
- Um parágrafo por estrutura/órgão, como no template. Sem conector de transição entre parágrafos de estruturas diferentes.
- Ordem fixa dentro do parágrafo: descrição normal/basal primeiro, achado(s) anormal(is) por último.
- Achado que contradiz frase normal da máscara: a frase normal sai inteira e entra a frase do achado. Negativa contradita sai inteira, nunca fica pela metade nem é reescrita.
- Cada achado anormal é frase própria (a frase da base), recortável para a Conclusão na mesma ordem.
- Quando o achado afeta só parte da estrutura e a base tem a nota de completude correspondente (fragmento como "Restante de … preservado"), ela vai em parágrafo próprio, separado do achado. Sem nota na base: `[COMPLETAR: nota de completude de <estrutura>]`.
- Estrutura do template não mencionada pelo usuário mantém a frase normal do template, que é texto da base. Estrutura que não está no template e não foi informada não entra.

CONCLUSÃO
- Exame sem achado: a conclusão normal do template, sem mudança.
- Com achado: a conclusão normal do template sai. Cada achado entra na ordem em que apareceu na Análise: o par `xc` quando existir; sem par, a frase do achado copiada na íntegra, igual à da Análise.
- Classificação (BI-RADS, TI-RADS, LI-RADS, O-RADS, Bosniak, Lung-RADS, PI-RADS etc.) só quando os dados informados permitirem aplicá-la sem presumir nada. Dado insuficiente: perguntar (entra na rodada); usuário sem o dado: `[COMPLETAR: categoria <sistema>]`. O texto da categoria vem da base; sem frase na base, `[COMPLETAR]`.
- Diferencial, conduta ou correlação só se estiverem na frase da base usada.

SKILLS IRMÃS: FONTE DOS CRITÉRIOS, NÃO DO TEXTO
- US Doppler de carótidas/vertebrais → critérios de `/carotidas`; mamografia/US mamário (BI-RADS) → `/mamas`; Doppler arterial de MMII → `/arterial-mmii`; mapeamento venoso de MMII → `/mapa`.
- Consultar a skill irmã internamente mesmo que o usuário não a tenha chamado, só para aplicar limiar e categoria. O texto do laudo continua vindo da base desta skill.
- Conteúdo da skill irmã inacessível: declarar isso fora do bloco e não aplicar a classificação; nunca usar regra genérica disfarçada de critério específico.
- Limiar ou índice derivado (IR, razões, % de estenose) só com o critério da skill irmã ou o que estiver escrito na própria frase da base, e só para preencher um `_` existente. Sem critério documentado: não pesquisar na web nem usar memória; `[COMPLETAR]` e avisar.

SAÍDA
- Um bloco único de código, pronto para colar, só com o laudo.
- Fora do bloco, no máximo uma linha: `Triggers: <lista> · Lacunas: <lista ou "nenhuma">`. Lacunas incluem todo `[COMPLETAR]`, achado sem frase na base e classificação não aplicada.
- Nada mais: sem explicação, sem lista de estruturas, sem nota sobre a montagem.
