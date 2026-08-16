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
| Alegação central que o refutador **tentou** verificar e não conseguiu, ficando de pé só por relato do executor | 80 |
| **Cobertura insuficiente**: existe alegação central que o refutador **nem chegou a tentar** testar — faltou ferramenta, acesso, ambiente ou tempo, e ele não sabe se ela é verdadeira | 85 |
| **Qualquer outro `REFUTADO` confirmado que não seja puramente cosmético** — convenção violada, contradição interna, erro factual que não chega ao consumidor final, lacuna de tratamento de caso, imprecisão em afirmação load-bearing | 85 |
| Apenas achados cosméticos, de estilo ou de preferência | sem teto |

A penúltima linha é o **teto guarda-chuva**, e existe porque as linhas acima dela nunca cobrirão o espaço inteiro dos defeitos possíveis. Sem ela, um `REFUTADO` real que não se encaixa em nenhuma categoria nomeada sai por cima do portão pela soma: uma convenção local violada custa uns 5 pontos em Integridade e assina 95. É defeito confirmado entregue como aprovado, que é exatamente o resultado que a skill inteira existe para impedir. Com ela, a regra vira simples e verdadeira como enunciada no `SKILL.md`: **sobrou qualquer `REFUTADO` não cosmético de pé, a nota não passa de 85, e há outra rodada.** O portão mede a ausência de refutação sobrevivente, e não o tamanho do estrago.

Os tetos de 80 e 85 por alegação não verificada se distinguem pela tentativa, não pelo resultado: 80 é "ataquei e a alegação resistiu sem me mostrar evidência"; 85 é "não cheguei perto dela". Se ambos couberem, vale o menor, 80.

O teto de cobertura é o mecanismo que impede o modo de falha mais comum desta skill: um refutador raso que não achou nada porque não procurou e assina 95. "Não encontrei erro" só vale nota alta quando vem acompanhado do que foi testado. Cobertura fraca não é sinal de trabalho bom — é sinal de que falta rodada.

## Quanto descontar por achado

Os tetos resolvem o caso grave. Abaixo deles a soma ainda precisa de calibração, ou "35 em correção" vira opinião. Desconte dentro de cada dimensão assim:

- **Achado que invalida o propósito da dimensão** — a dimensão inteira zera. Correção: o artefato produz resultado errado. Completude: metade do escopo não existe.
- **Achado substantivo confirmado** — entre um terço e metade do peso da dimensão. Dois achados substantivos na mesma dimensão praticamente a zeram; não some descontos até passar do peso, use zero como piso.
- **Achado menor confirmado** — até um quinto do peso.
- **Cosmético ou preferência** — no máximo 1 ponto, e só em Execução e adequação. Não desconte estilo em Correção.
- **Alegação não verificada** — desconte em Evidência verificável, nunca em Correção. Não saber se algo está certo não é o mesmo que saber que está errado, e confundir os dois faz o refutador punir a própria falta de alcance como se fosse defeito do artefato.

Escreva o desconto ao lado de cada dimensão, com o achado que o motivou. Dimensão com desconto e sem achado nomeado é nota inventada.

## Faixas, para calibrar a escrita do refutador

Não são regras — são âncoras, para que 70 signifique a mesma coisa entre refutadores diferentes.

- **90-100** — nenhuma refutação de pé, cobertura ampla, o refutador rodou os testes que derrubariam o trabalho e eles não derrubaram. Sobrou no máximo preferência de estilo.
- **86-89** — nenhum `REFUTADO` de pé e as alegações centrais foram alcançadas; sobrou um detalhe de execução ou uma alegação periférica sem teste. Passa. Note que "um canto central sem teste" não mora nesta faixa: isso é o teto de 85, e desce.
- **70-85** — nada catastrófico, mas há buraco real: achado menor confirmado, alegação central não verificada, cobertura que não alcançou o essencial. Nova rodada.
- **40-69** — requisito ausente ou regressão confirmada. O trabalho não faz o que foi pedido, ou quebrou algo ao fazer.
- **0-39** — resultado errado sendo entregue como certo. O caso mais grave, porque parece pronto.

## Agregação entre refutadores da mesma rodada

Cada refutador entrega a nota dele calculada sobre o que **ele** alcançou. Agregar é trabalho do executor, em três passos e nesta ordem. Pular o passo 1 quebra o ciclo: sem ele a regra da união é inerte e um artefato limpo nunca sai da rodada 2.

### Passo 1 — recompor as notas individuais

Antes de comparar qualquer coisa, refaça a nota de cada refutador removendo os tetos que a rodada como um todo desmente:

- **Teto de cobertura (85) ou de alegação não verificada (80)** aplicado por um refutador sobre uma alegação que **outro refutador da mesma rodada alcançou e testou** → esse teto cai. Recomponha a nota daquele refutador pela soma das dimensões dele, mantendo os demais tetos que ele aplicou, e devolva os pontos que ele havia descontado em Evidência verificável por não ter alcance.
- **Teto de qualquer outra natureza** → permanece. Cobertura se soma entre refutadores; achado, não.

Sem este passo, o cenário mais banal trava o ciclo: A não tem ferramenta para uma alegação central e assina 85 pelo teto de cobertura, B e C testam tudo e assinam 100. O mínimo cru dá 85 e manda para outra rodada um trabalho que a rodada inteira cobriu e não conseguiu derrubar. Recompondo, A vira 100 e o mínimo é 100.

### Passo 2 — descontar as contestações reconhecidas

Se um achado desta rodada coincide com uma contestação já registrada em rodada anterior e o executor **retestou agora** e a falha continua não reproduzindo, remova esse achado do cômputo do refutador que o levantou, recomponha a nota dele e registre no relatório o comando e a saída que sustentam a remoção. Ver a regra de autoridade no `SKILL.md`, passo 4 — este é o **único** ajuste de nota que o executor pode fazer, e ele custa mostrar a evidência ao usuário.

### Passo 3 — agregar

- **Nota da rodada = a menor entre as notas recompostas.** Nunca a média. Média deixa dois refutadores rasos diluírem um achado real, que é precisamente o resultado que a skill existe para impedir.
- **Achados = a união.** Defeito encontrado por um só continua sendo defeito. Que os outros dois não tenham visto é informação sobre eles, não sobre o defeito.
- **Cobertura = a união.** O que um alcançou conta como alcançado pela rodada — é isso que o passo 1 materializa.
- **Discordância direta** — um diz REFUTADO, outro diz NÃO REFUTADO sobre a mesma alegação — não se resolve por votação. Vale o que tem evidência reproduzível; a etapa de contestação do `SKILL.md` decide, reproduzindo a falha descrita.

### Rodada 3, onde a cobertura é estreita de propósito

O refutador de rodada 3 recebe uma única dimensão e é instruído a olhar só para ela. Avaliar o teto de cobertura dele contra *todas* as alegações centrais o reprovaria por construção, e o ciclo nunca fecharia. Portanto: **na rodada 3, o teto de cobertura de cada refutador se avalia apenas sobre as alegações da dimensão que lhe coube.** A cobertura das demais dimensões é herdada da rodada 2 e não é reaberta.

## O que a nota não é

Não é avaliação do esforço, do tamanho da mudança nem da dificuldade da tarefa. Uma correção de uma linha, certa e testada, tira 95. Uma refatoração de dois mil arquivos com uma regressão confirmada tira 60. A rubrica mede o estado do artefato, não a jornada até ele.
