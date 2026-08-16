# Rubrica de nota — 0 a 100

A nota existe para uma decisão binária: **> 85 entrega, ≤ 85 dispara nova rodada**. Ela não é uma impressão geral de qualidade nem uma nota de escola. É a resposta a uma pergunta estreita: *sobrou alguma refutação de pé, e o refutador conseguiu de fato procurar?*

Por isso a nota tem duas partes, e a segunda manda na primeira: uma soma ponderada por dimensão, e um conjunto de tetos que a soma não pode furar.

## Regra de ordem

A nota é escrita **depois** dos achados, nunca antes. Nota decidida primeiro e justificada depois é nota inventada — o mesmo vício de declarar o predicado depois de ver o resultado. Se você percebeu que já tinha um número em mente antes de terminar de listar os achados, descarte-o e recomece a contagem pela rubrica.

## As cinco dimensões

| Dimensão | Peso | O que mede |
|---|---:|---|
| Correção e factualidade | 35 | O que está afirmado ou implementado está certo? Código faz o que o nome diz; laudo bate com os dados de entrada; pesquisa cita fonte que existe e que diz aquilo; explicação não carrega erro conceitual; conta fecha. |
| Completude frente ao pedido | 25 | Tudo que o pedido exigia está entregue? Requisito ignorado, pergunta não respondida, caso de borda declarado e não coberto, metade do escopo feita. |
| Integridade do entorno | 20 | O que mais foi afetado? Regressão, arquivo sobrescrito, contradição com outra parte do mesmo documento, convenção local violada, dependência quebrada, efeito colateral não mencionado. |
| Evidência verificável | 10 | As alegações se sustentam em algo checável, e isso foi checado? Cada `SEM EVIDÊNCIA` do dossiê que o refutador também não conseguiu verificar come pontos aqui. |
| Execução e adequação | 10 | Clareza, terminologia adequada ao contexto, aderência ao estilo do lugar, ausência de gambiarra e de excesso. Esta é a única dimensão onde cabe julgamento estético. |

Some as cinco. Depois aplique os tetos.

## Tetos

Teto é limite superior absoluto: se a soma deu 92 e um teto de 60 se aplica, a nota é 60. Vários tetos aplicáveis, vale o menor.

| Condição confirmada pelo refutador | Teto |
|---|---:|
| Defeito que entrega resultado errado a quem consome o trabalho — código que produz saída incorreta, lateralidade trocada em laudo, fato ou citação inventados, número errado em conta que alguém vai usar | 40 |
| Requisito explícito do pedido ausente do artefato | 60 |
| Regressão ou dano colateral confirmado — algo que funcionava antes e não funciona agora | 60 |
| Alegação central apoiada só em relato, que o refutador tentou verificar e não conseguiu | 80 |
| **Cobertura insuficiente**: o refutador não conseguiu testar ao menos uma das alegações centrais, por falta de ferramenta, de acesso, de ambiente ou de tempo | 85 |
| Apenas achados cosméticos, de estilo ou de preferência | sem teto |

O teto de cobertura é o mecanismo que impede o modo de falha mais comum desta skill: um refutador raso que não achou nada porque não procurou e assina 95. "Não encontrei erro" só vale nota alta quando vem acompanhado do que foi testado. Cobertura fraca não é sinal de trabalho bom — é sinal de que falta rodada, e é exatamente para isso que existe o portão em 85.

## Faixas, para calibrar a escrita do refutador

Não são regras — são âncoras, para que 70 signifique a mesma coisa entre refutadores diferentes.

- **90-100** — nenhuma refutação de pé, cobertura ampla, o refutador rodou os testes que derrubariam o trabalho e eles não derrubaram. Sobrou no máximo preferência de estilo.
- **86-89** — nada substantivo de pé, mas ficou um canto sem teste ou um detalhe de execução. Passa.
- **70-85** — nada catastrófico, mas há buraco real: alegação não verificada, cobertura parcial, achado menor confirmado. Nova rodada.
- **40-69** — requisito ausente ou regressão confirmada. O trabalho não faz o que foi pedido, ou quebrou algo ao fazer.
- **0-39** — resultado errado sendo entregue como certo. O caso mais grave, porque parece pronto.

## Agregação entre refutadores da mesma rodada

Quando a rodada tem mais de um refutador:

- **Nota da rodada = a menor entre elas.** Nunca a média. Média deixa dois refutadores rasos diluírem um achado real, que é precisamente o resultado que a skill existe para impedir.
- **Achados = a união.** Defeito encontrado por um só continua sendo defeito. Que os outros dois não tenham visto é informação sobre eles, não sobre o defeito.
- **Cobertura = a união também.** O que um conseguiu testar conta como testado para a rodada. O teto de cobertura só se aplica se *nenhum* refutador da rodada alcançou a alegação.
- **Discordância direta** — um diz REFUTADO, outro diz NÃO REFUTADO sobre a mesma alegação — não se resolve por votação. Vale o que tem evidência reproduzível; a etapa de contestação do Papel A decide, reproduzindo a falha descrita.

## O que a nota não é

Não é avaliação do esforço, do tamanho da mudança nem da dificuldade da tarefa. Uma correção de uma linha, certa e testada, tira 95. Uma refatoração de dois mil arquivos com uma regressão confirmada tira 60. A rubrica mede o estado do artefato, não a jornada até ele.
