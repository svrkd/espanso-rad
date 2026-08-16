# Onde a falha se esconde, por domínio

O procedimento da skill não muda entre contextos. O que muda é onde vale a pena gastar a rodada. Use esta lista para escolher os testes do refutador — não como checklist a percorrer inteira, mas como catálogo dos lugares onde o falso sucesso costuma se instalar em cada tipo de trabalho.

Identifique o domínio pelo artefato, não pelo repositório. Um script Python que gera um laudo é código; o laudo que ele cospe é laudo. Verifique os dois pelo que eles são.

## Código

- **A alegação "os testes passam"** — passam, mas testam o quê? Rode a suíte, depois olhe se existe teste cobrindo justamente o caminho que mudou. Teste que não exercita a mudança passa por indiferença, não por aprovação.
- **Teste silenciado** — asserção comentada, `skip`, `xfail`, expectativa afrouxada, mock que agora devolve o valor que faz o teste passar. Compare a lista de testes coletados antes e depois.
- **Caminho de erro** — quase toda mudança é exercitada no caminho feliz. Entrada vazia, `None`/`null`, lista de um elemento, unicode, número negativo, arquivo que não existe, duas chamadas seguidas.
- **Fora do diff** — o chamador que não foi atualizado, a assinatura que mudou e deixou um call site para trás, o import morto, o tipo que não bate mais. `grep` pelo nome antigo em todo o repositório.
- **Concorrência e estado** — o que acontece na segunda execução? Idempotência, arquivo parcialmente escrito, cache que agora guarda o valor errado.
- **Build e lint de verdade** — rode o que o CI roda, não uma aproximação. O comando exato do workflow.

## Pesquisa e afirmação factual

- **A fonte existe?** Abra a URL, o DOI, o número da página. Citação plausível de artigo inexistente é o modo de falha mais frequente e o mais caro.
- **A fonte diz aquilo?** Existir não basta. Leia o trecho citado e compare com a afirmação. Inversão de sentido, condição omitida ("em pacientes acima de 65 anos") e generalização de um achado restrito passam fácil.
- **Número e unidade** — refaça a conta. Porcentagem de base errada, ordem de grandeza, conversão de unidade, intervalo de confiança que virou média.
- **Data e versão** — informação correta em 2019 e falsa hoje. Confira a data da fonte contra a data do que se afirma.
- **O que foi omitido** — evidência contrária que existe e não foi mencionada. Procure ativamente pelo contra-argumento antes de aceitar a síntese.

## Laudo radiológico

- **Lateralidade** — direita/esquerda entre a descrição, a conclusão e o dado de entrada. Falha de alta gravidade e de detecção fácil; sempre teste.
- **Técnica versus descrição** — a descrição menciona realce pelo contraste e a técnica declara exame sem contraste? Sequência descrita que não consta do método? Segmento laudado que não estava no campo de estudo?
- **A conclusão decorre da descrição?** Achado na conclusão que não aparece descrito, achado descrito e relevante que sumiu da conclusão, grau de certeza que subiu entre uma e outra.
- **Medida** — unidade presente, plano de medição declarado, valor compatível com a estrutura, comparação com exame anterior usando a mesma referência.
- **Categorização** — BI-RADS, LI-RADS, TI-RADS, PI-RADS, Bosniak, Fleischner: a categoria atribuída bate com os critérios da versão vigente, e a conduta sugerida bate com a categoria.
- **Português** — concordância, regência, pontuação. Neste domínio o erro de língua é defeito do produto, não estética.
- **Contradição interna** — órgão descrito como normal em um parágrafo e alterado em outro; "sem alterações" seguido de achado.

## Explicação e texto didático

- **O erro conceitual sob a analogia** — a analogia é boa e o mecanismo por baixo está errado. Verifique o mecanismo, não a clareza.
- **Simplificação que virou falsidade** — "sempre", "nunca", "basta" onde o real é condicional.
- **A pergunta que foi feita** — o texto responde uma pergunta vizinha e mais fácil que a do usuário? Releia o pedido e case pergunta com resposta.
- **Exemplo que não funciona** — rode o código do exemplo, refaça o cálculo do exemplo, teste o caso do exemplo. Exemplo ilustrativo errado ensina o erro.
- **Nível** — pressupõe conhecimento que o pedido indicava não haver, ou explica o que não foi perguntado.

## Dados, planilha, importação e migração

- **Contagem dos dois lados** — linhas, registros, itens, antes e depois. Divergência de um único item é achado.
- **Amostragem nas bordas** — primeira linha, última linha, a linha logo depois de cada quebra de bloco. Perda por off-by-one mora nas bordas, e a inspeção do meio nunca a encontra.
- **Encoding e caractere especial** — acento, cedilha, aspas tipográficas, caractere de controle de export antigo do Windows. Procure por `Ã`, `�`, `\x9`.
- **Tipo silenciosamente convertido** — número virou texto, data virou serial, zero à esquerda sumiu, decimal trocou vírgula por ponto.
- **Duplicata e colisão de chave** — o registro que sobrescreveu outro sem avisar.
- **"Nada perdido"** — alegação que quase nunca é testada como enunciada. O predicado correto é diff linha a linha contra a origem, não contagem.

## Configuração, YAML e infraestrutura

- **Carrega?** Parse do arquivo pelo mesmo parser que o consome em produção, não por leitura visual.
- **Namespace global** — em sistemas onde tudo é carregado num conjunto único (como os `match/*.yml` do Espanso), a chave nova pode sombrear uma existente em outro arquivo. Busque a chave em todos os arquivos, não só naquele que foi editado.
- **Ordem de chave, campo obrigatório, charset** — rode o linter do projeto, se houver, e compare a saída com a de antes da mudança em vez de olhar só se está limpa.
- **Bloco literal versus escalar** — quebra de linha e linha em branco preservadas onde precisam aparecer na saída.
- **O efeito de verdade** — config que valida não é config que funciona. Carregue e exercite ao menos um caminho real.

## Sinais transversais, em qualquer domínio

Independentemente do tipo de trabalho, estes três merecem um teste dedicado sempre:

1. **A alegação mais confiante e menos evidenciada.** Confiança alta com evidência vaga é a assinatura do falso sucesso.
2. **O predicado mais estreito que a alegação.** Contou linhas e concluiu "nada perdido"; rodou um caso e concluiu "funciona"; leu o arquivo e concluiu "está consistente".
3. **O requisito do pedido que não aparece em alegação nenhuma.** Ninguém mente sobre ele — ele simplesmente não é mencionado, e é por isso que sobrevive à revisão.
