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
| Evidência verificável | 10 | As alegações do artefato se sustentam em algo checável, e o refutador conseguiu checar? Cada alegação que ele identificou por conta própria e não conseguiu verificar come pontos aqui. |
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

A penúltima linha é o **teto guarda-chuva**, e existe porque as linhas acima dela nunca cobrirão o espaço inteiro dos defeitos possíveis. Sem ela, um `REFUTADO` real que não se encaixa em nenhuma categoria nomeada sai por cima do portão pela soma: uma convenção local violada é achado menor em Integridade, custa 4 pontos e assina 96. É defeito confirmado entregue como aprovado, que é exatamente o resultado que a skill inteira existe para impedir. Com ela, a regra vira simples e verdadeira como enunciada no `SKILL.md`: **sobrou qualquer `REFUTADO` não cosmético de pé, a nota não passa de 85, e há outra rodada.** O portão mede a ausência de refutação sobrevivente, e não o tamanho do estrago.

Os tetos de 80 e 85 por alegação não verificada se distinguem pela tentativa, não pelo resultado: 80 é "ataquei e a alegação resistiu sem me mostrar evidência"; 85 é "não cheguei perto dela". Se ambos couberem, vale o menor, 80.

### Central ou periférica

Os dois tetos acima só disparam sobre alegação **central**, então essa fronteira controla o portão tanto quanto a do cosmético, e por isso precisa ser tão apertada quanto ela. Solta, basta chamar de periférica a alegação que ficou sem teste, descontar 10 em Evidência e assinar 90.

**É central** toda alegação em que se apoia a resposta ao pedido: que o artefato faz o que foi pedido, que o que ele afirma é verdade, que nada ao redor quebrou. Na prática, se a alegação fosse falsa e o usuário descobrisse depois, ele diria que a verificação falhou — então ela é central.

**É periférica** a alegação acessória, cuja falsidade o usuário registraria como detalhe e não como falha da verificação: um caminho alternativo de instalação que não foi exercitado, um ambiente secundário, um exemplo ilustrativo.

Na dúvida, é central — pela mesma razão que na dúvida não é cosmético.

O teto de cobertura é o mecanismo que impede o modo de falha mais comum desta skill: um refutador raso que não achou nada porque não procurou e, sem achado a nomear, não tem desconto a fazer e assina 100. "Não encontrei erro" só vale nota alta quando vem acompanhado do que foi testado. Cobertura fraca não é sinal de trabalho bom — é sinal de que falta rodada.

## Quanto descontar por achado

Os tetos resolvem o caso grave. Abaixo deles a soma ainda precisa de calibração, ou "35 em correção" vira opinião. Desconte dentro de cada dimensão assim:

- **Achado que invalida o propósito da dimensão** — a dimensão inteira zera. Correção: o artefato produz resultado errado. Completude: metade do escopo não existe.
- **Achado substantivo confirmado** — entre um terço e metade do peso da dimensão. Dois achados substantivos na mesma dimensão praticamente a zeram; não some descontos até passar do peso, use zero como piso.
- **Achado menor confirmado** — até um quinto do peso.
- **Cosmético ou preferência** — no máximo **1 ponto no total**, e só em Execução e adequação. É um teto sobre a soma dos cosméticos, não por achado: dez achados cosméticos custam o mesmo 1 ponto que um. Sem isso, uma pilha de preferências de redação derruba a nota abaixo do portão sem que exista defeito nenhum. Não desconte estilo em Correção.
- **Alegação não verificada** — desconte em Evidência verificável, nunca em Correção. Não saber se algo está certo não é o mesmo que saber que está errado, e confundir os dois faz o refutador punir a própria falta de alcance como se fosse defeito do artefato. Central sem teste também aciona o teto de 85 ou de 80; periférica sem teste só desconta aqui, e o que ficou fora vai descrito na seção COBERTURA nos dois casos.

Escreva o desconto ao lado de cada dimensão, com o achado que o motivou. Dimensão com desconto e sem achado nomeado é nota inventada.

## Faixas, para calibrar a escrita do refutador

Não são regras — são âncoras, para que 70 signifique a mesma coisa entre refutadores diferentes.

- **89-100** — nenhum `REFUTADO` não cosmético de pé e as alegações centrais foram todas alcançadas. Passa. Dentro da faixa: 100 é cobertura ampla sem nenhuma ressalva; descontos em Evidência verificável (alegação periférica que ficou sem teste) e o desconto cosmético de Execução puxam para baixo até 89.
- **61-85** — há buraco real, mas o trabalho faz o que foi pedido e não quebrou nada: um `REFUTADO` não cosmético confirmado, alegação central não verificada, ou cobertura que não alcançou o essencial. Nova rodada.
- **41-60** — requisito ausente ou regressão confirmada. O trabalho não faz o que foi pedido, ou quebrou algo ao fazer.
- **40 ou menos** — resultado errado sendo entregue como certo. O caso mais grave, porque parece pronto.

As faixas são os tetos, e não outra escala por cima deles — é por isso que os cortes caem em 85, 60 e 40 e não em números redondos. Note que **40 é o valor mais comum do caso mais grave**, não um extremo raro: resultado errado zera Correção e deixa 65 de soma, que o teto de 40 corta. Descer abaixo de 40 exige que o trabalho também esteja incompleto ou tenha quebrado o entorno. Não estranhe ver 40 com frequência no pior caso, e não force um número menor para "expressar gravidade" — a gravidade já está dita pelo teto que disparou.

**Não existe faixa 86-88, e isso é consequência do desenho, não descuido.** Para ficar acima do portão é preciso não ter nenhum `REFUTADO` não cosmético (senão o guarda-chuva trava em 85), nenhuma alegação central sem teste (85) e nenhuma tentada sem sucesso (80). Sobram então só dois descontos possíveis, Evidência verificável (até 10) e o cosmético de Execução (até 1), e o piso deles é 89. Não force uma nota em 86, 87 ou 88: se você chegou lá, algum desconto seu não tem achado nomeado por trás, ou você aplicou em Correção o que devia ir em Evidência.

Vale dizer com todas as letras o que isso significa: **acima do portão a nota é grossa de propósito.** A escada fina de descontos em Correção, Completude e Integridade só entra em operação nos casos que já estão travados em 85 ou menos, onde a granularidade serve para ordenar gravidade e orientar a rodada seguinte. Acima de 85 a única pergunta que importa já foi respondida — não sobrou refutação — e a nota vira quase binária. Se você está caprichando na terceira casa de uma nota 94, está gastando esforço onde ele não muda nenhuma decisão.

## Cosmético, e por que a fronteira importa

O portão inteiro se apoia numa distinção: `REFUTADO` cosmético não trava a nota, qualquer outro trava em 85. Se essa fronteira ficar solta, o teto guarda-chuva vira letra morta — basta chamar o defeito de cosmético.

**É cosmético** o achado que não muda nem o resultado que o trabalho produz, nem o que um leitor conclui dele, nem o que acontece quando alguém o usa: preferência de redação, ordem de parágrafos, nome de variável, formatação, sinônimo mais feliz, verbosidade.

**Não é cosmético**, por mais que pareça pequeno: qualquer coisa que muda o resultado, mesmo que raramente; qualquer coisa que torna falsa uma afirmação do artefato, mesmo que lateral; violação de convenção do lugar, porque convenção existe para ser executável por terceiros; contradição interna, porque quem executar o documento vai parar nela; erro de português que altera o sentido, e em laudo qualquer erro de português.

Na dúvida, não é cosmético. O custo de errar para o lado severo é uma rodada a mais; o custo de errar para o outro lado é defeito confirmado entregue como aprovado, que é o resultado que esta rubrica inteira existe para tornar impossível.

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

Os refutadores focados de rodada 3 recebem uma única dimensão e são instruídos a olhar só para ela. Avaliar o teto de cobertura deles contra *todas* as alegações centrais os reprovaria por construção, e o ciclo nunca fecharia. Portanto: **o teto de cobertura de um refutador focado se avalia apenas sobre as alegações da dimensão que lhe coube.**

Isso deixaria um buraco, e o generalista que acompanha a rodada 3 (ver `SKILL.md`, passo 5) existe para tapá-lo: cobertura **não se herda através de uma mudança**. O artefato da rodada 3 não é o da rodada 2 — você corrigiu coisas no meio —, então dizer que as dimensões verdes já foram cobertas é atestar uma versão que não existe mais. A cobertura da rodada 3 é a do generalista, unida à dos focados; a da rodada 2 não conta para o teto da rodada 3.

## O que a nota não é

Não é avaliação do esforço, do tamanho da mudança nem da dificuldade da tarefa. Uma correção de uma linha, certa, testada e integralmente coberta, tira 100 — não há desconto a fazer quando não há achado a nomear, e inventar um arredondamento para baixo por modéstia é tão errado quanto inventar um para cima. Uma refatoração de dois mil arquivos com uma regressão confirmada tira 60. A rubrica mede o estado do artefato, não a jornada até ele.
