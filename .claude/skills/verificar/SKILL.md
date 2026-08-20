---
name: verificar
description: Roda verificação adversarial cega sobre trabalho recém-executado nesta sessão — código, pesquisa, laudo, explicação, planilha, config. Um subagente refutador que não vê o raciocínio do executor tenta derrubá-lo, dá nota de 0 a 100 por rubrica, e nota igual ou menor que 85 dispara nova rodada com mais refutadores, até 3 rodadas. Use quando o usuário invocar `/verificar`, pedir para "conferir se está certo mesmo", "auditar o que você acabou de fazer", "rodar o refutador", "checar antes de commitar/mandar/assinar", ou quando você mesmo for alegar que algo está completo, corrigido, passando ou verificado. Distingue-se das vizinhas pelo objeto e pelo método, não pelo assunto — o objeto é sempre trabalho que esta sessão acabou de produzir, e quem dá a nota é sempre um agente cego e separado. Para auditar laudo já redigido sem abrir subagente use `/critica`; para reescrever prosa, `/melhore`; para só a gramática, `/portugues`.
---

# Verificação adversarial cega (`/verificar`)

Quem executa não dá a nota. Esta skill entrega o trabalho recém-feito a um refutador que não viu como ele foi feito, cuja tarefa é derrubá-lo — não confirmá-lo — e que precisa justificar uma nota de 0 a 100. Acima de 85 entrega ao usuário; 85 ou menos corrige e chama mais refutadores.

Ela funciona em qualquer contexto: código, pesquisa factual, laudo radiológico, explicação didática, dados, configuração. O que muda entre domínios é onde a falha costuma se esconder, não o procedimento — ver `references/angulos-por-dominio.md`.

## Relação com `.claude/rules/verificacao-adversarial.md`

Quando o repositório tiver esse arquivo, leia-o: ele é a política, esta skill é o procedimento que a executa, e ele pode trazer exigências locais que a skill não conhece. Quando não tiver, a skill se basta sozinha.

Onde os dois textos divergirem, saiba exatamente em quê, porque a divergência é deliberada e estreita. São **três** pontos, e nenhum outro:

- **Achado puramente cosmético não força rodada nova.** A regra manda repetir o ciclo diante de qualquer `REFUTADO`. Preferência de redação não é defeito, e tratá-la como defeito faria o ciclo nunca fechar. A fronteira do cosmético está fixada em `references/rubrica.md` e é estreita de propósito: na dúvida, não é cosmético.
- **Achado que não reproduz vira `CONTESTADO` em vez de correção.** A regra não previu falso positivo do refutador; corrigir defeito fantasma degrada o trabalho. A contestação exige reteste documentado e morre no terceiro levantamento independente, virando divergência aberta para o usuário.
- **O registro de alegações não vai ao refutador.** Aqui a skill inverte a regra, não a estende: o Papel A dela diz que alegação marcada `SEM EVIDÊNCIA` "passa ao refutador como suspeita prioritária", e o prompt dela manda atacar essas marcas primeiro. Esta skill mantém o registro com o executor (documento 1b) porque uma lista de alegações de sucesso redigida pelo auditado dirige o olhar de quem audita, ainda que sem mentir uma palavra. Onde os dois se contradizem neste ponto, **prevalece a skill**.

Fora dessas três, vale a regra: qualquer `REFUTADO` de pé é rodada nova, e remendar para declarar pronto está proibido.

A regra também carrega um prompt de refutador próprio, mais curto, sem nota e sem rodadas. O de `references/prompt-refutador.md` é a versão estendida dele e é o que esta skill usa — a instrução de "copiar literalmente" se refere a esse, não ao da regra.

## 0. Delimitar o que está sob verificação

`/verificar` sem argumento = o trabalho executado nesta conversa desde o último pedido do usuário. Com argumento (`/verificar o laudo`, `/verificar só o parser`) = o recorte que o usuário nomeou.

Antes de qualquer outra coisa, determine o estado real, por ferramenta e não por memória:

```
git status --porcelain && git diff --stat HEAD
```

Se não houver repositório git, ou se o produto for texto entregue na conversa (laudo, explicação, resposta de pesquisa), o artefato é o texto literal da entrega.

Se você concluir que nada foi executado nesta sessão e não há artefato a verificar, diga isso ao usuário e pare. Não invente um objeto de verificação.

## 1. Papel A — executor: montar o dossiê cego

Você escreve **dois** documentos, e a separação entre eles é o coração da skill: um vai ao refutador, o outro nunca.

### 1a. O dossiê — vai ao refutador

Escreva `dossie-verificacao.md` **fora do repositório**: no diretório temporário da sessão, ou em `/tmp`. Nunca na raiz do projeto — é arquivo de trabalho, é regenerado a cada rodada, e um dossiê esquecido no repo entra em commit alheio depois. Apague-o ao fim do ciclo.

O dossiê tem **exatamente** estas três seções, e nada além delas:

1. **PEDIDO ORIGINAL** — o pedido do usuário copiado literalmente, palavra por palavra. Não parafraseie, não resuma, não "esclareça". Se o pedido veio em várias mensagens, cole todas em ordem.
2. **ARTEFATO** — o produto, **colado inteiro**, extraído por ferramenta: a saída de `git diff HEAD` (ou `git diff <base>...HEAD`) em si, o conteúdo dos arquivos, o texto entregue na íntegra. Colar o comando em vez da saída não cumpre esta seção; obriga o refutador a reconstruir o artefato e é uma forma discreta de escolher o que ele vê. Se o diff for grande demais para caber, cole o que couber e diga qual comando dá o resto — nessa ordem, nunca só o comando.
3. **COMO ALCANÇAR O ESTADO REAL** — caminhos de arquivo, comandos para rodar testes/lint/build, onde o artefato vive. Informação de navegação, não avaliação. Cuidado com dois vazamentos fáceis aqui: não cole `git log` nem histórico que revele rodadas anteriores desta skill, e não escreva o motivo pelo qual um caminho é interessante ("para checar colisão com X") — liste o caminho e cale-se.

### 1b. O registro de alegações — nunca vai ao refutador

Um documento separado, seu para o **usuário**. Uma linha por alegação factual que o trabalho sustenta, com a evidência exata ao lado. Alegação que você não consegue sustentar recebe a marca `SEM EVIDÊNCIA`. Não fabrique evidência para preencher a coluna.

```
ALEGAÇÃO                              EVIDÊNCIA
os 3 testes passam                    saída de `pytest -q`, colada abaixo
nenhum conteúdo perdido no split      diff linha a linha contra o backup
o trigger novo não colide             `grep -rn 'trigger: "vb3"' match/` vazio
a dose citada está correta            SEM EVIDÊNCIA
```

**Por que ele não vai ao refutador.** Uma lista de alegações de sucesso escrita pelo auditado é exatamente o material que enviesa: quem escolhe o que entra, o que fica de fora e o que recebe a marca é quem está sendo auditado, e uma lista curta e conveniente dirige o olhar para longe do problema sem mentir uma vírgula. O refutador monta a lista dele a partir do pedido e do artefato, do zero.

**Para que ele serve, então.** Duas coisas, ambas depois da refutação:

- **Prestação de contas ao usuário.** No relatório final você cruza as duas listas. Alegação sua que nenhum refutador tocou é a informação mais útil que o ciclo produz, porque é onde a verificação não chegou — e sem o registro escrito antes você não teria como saber que ela existia.
- **Disciplina sua.** Escrever "SEM EVIDÊNCIA" ao lado de uma linha antes de qualquer refutador rodar força você a admitir o que está apoiado em confiança. Toda afirmação de fato que o artefato sustenta entra, inclusive — sobretudo — a que você preferiria não escrever.

### O que o dossiê não pode conter

O dossiê é a única coisa que você escreve e que o refutador lê. Contaminá-lo destrói o valor da skill inteira. Fora, sem exceção:

- Seu raciocínio, sua abordagem, por que você escolheu o que escolheu.
- Qualquer avaliação do próprio trabalho: "funcionando", "corrigido", "testado", "simples", "trivial", "conforme a convenção", "já validei".
- Resumo do que você fez em prosa. O diff já diz o que você fez.
- O registro de alegações, que é o documento 1b e fica com você.
- Nota, expectativa de nota, ou o resultado de rodadas anteriores desta skill.
- Instruções ao refutador sobre onde olhar ou o que ignorar.

A coluna EVIDÊNCIA é o único lugar onde algo pode soar afirmativo, e mesmo lá ela aponta para uma saída de comando verificável, nunca para a sua confiança.

## 2. Papel B — refutador: rodada 1

Abra **um** subagente (`subagent_type: general-purpose`, ou o tipo generalista disponível no ambiente) com o prompt de `references/prompt-refutador.md`, ângulo **generalista**. Rode em primeiro plano — o próximo passo depende do resultado.

O subagente nasce com contexto limpo: ele não vê esta conversa. A cegueira vem de graça, desde que o dossiê esteja limpo. O prompt manda ele tratar o dossiê como possivelmente incompleto ou tendencioso e ir ao estado real por conta própria.

Ele devolve, obrigatoriamente:
- Uma linha `REFUTADO: <alegação> — <evidência da falha>` ou `NÃO REFUTADO: <alegação> — <predicado testado e resultado>` por alegação. Não existe "aprovado", "tudo certo", "parece bom".
- Uma seção **COBERTURA**: o que ele conseguiu testar de fato e o que ficou fora do alcance do teste dele.
- Uma **NOTA 0-100** com o cálculo por rubrica, escrita depois dos achados, nunca antes.

## 3. Ler a nota

**Nota > 85** → vá para o passo 6 e entregue.

**Nota ≤ 85** → passo 4, depois nova rodada.

A nota sai da rubrica de `references/rubrica.md`. Ela tem tetos nomeados para os defeitos graves e um **teto guarda-chuva** que pega todo o resto: qualquer `REFUTADO` confirmado que não seja puramente cosmético trava a nota em 85. É esse guarda-chuva que torna a regra verdadeira como enunciada — sem ele, um defeito real que não se encaixe em nenhuma categoria nomeada sairia por cima do portão pela soma das dimensões. Com ele, o portão não é impressão geral: é a ausência de refutação sobrevivente. Cobertura insuficiente também trava em 85, porque "não achei erro" sem ter conseguido testar não é o mesmo que ter procurado.

Se a rodada teve mais de um refutador, a nota que você lê aqui é a nota **agregada**, depois dos três passos de `references/rubrica.md` — recompor as notas individuais, descontar contestações reconhecidas, e só então tirar o mínimo. Ler o mínimo cru das notas como vieram trava artefato limpo abaixo do portão.

## 4. Antes de corrigir: contestar o que não reproduz

Refutador adversarial produz falso positivo. Corrigir um defeito fantasma piora o trabalho e ainda gasta uma rodada.

Para cada `REFUTADO`, reproduza a falha descrita antes de mexer em qualquer coisa:

- **Reproduziu** → corrija de verdade, na causa, não no sintoma. Não silencie teste, não remova asserção, não relaxe lint para ficar verde.
- **Não reproduziu** → marque `CONTESTADO: <alegação> — <o comando que rodei e a saída que contradiz o refutador>` e **não corrija**. Anote a linha no livro de contestações (abaixo) e leve-a ao relatório final.

### Livro de contestações

Mantenha uma lista acumulada das contestações, uma linha por achado contestado, com o comando e a saída que o contradizem. Ela sobrevive entre rodadas — o dossiê, não.

Uma contestação não corrige nada por definição, então o mesmo falso positivo vai ser reencontrado pelos refutadores cegos da rodada seguinte, e sem uma regra explícita ele seria recontado contra a nota para sempre. Por isso, e só por isso, existe esta autoridade:

> **O executor pode ajustar a nota de uma rodada em um único caso.** Quando um achado dessa rodada coincide com uma contestação já no livro, reteste a falha **agora**, sobre o estado atual. Se continuar não reproduzindo, remova o achado do cômputo daquele refutador, recomponha a nota dele conforme o passo 2 de `references/rubrica.md`, e cole no relatório o comando e a saída que sustentam a remoção. Qualquer outro ajuste de nota pelo executor é proibido — é o vício que a skill inteira existe para impedir.

Duas travas contra o abuso desta porta:

- **Reteste sempre, nunca reaproveite.** A contestação vale para o estado em que foi levantada. Você mexeu no artefato desde então; a falha pode ter passado a reproduzir. Contestação reaproveitada sem novo comando é autoindulgência com nome técnico.
- **Três é o limite.** Se três refutadores independentes e cegos entre si levantarem o mesmo achado, pare de contestar mesmo que ele siga não reproduzindo no seu ambiente. Nesse ponto a hipótese mais provável já não é falso positivo em série — é que o predicado deles alcança algo que o seu não alcança. Leve ao usuário como divergência aberta, com os dois lados e as duas evidências, e deixe a decisão com ele.

Se uma correção exigir decisão que só o usuário pode tomar — requisito ambíguo, escolha clínica, mudança destrutiva, troca de escopo — pare o ciclo e pergunte. Não decida por ele para fechar a nota.

## 5. Rodadas seguintes: fan-out crescente

Regenere o dossiê do zero a partir do estado corrigido. Os refutadores da rodada nova **nunca** recebem a nota anterior, os achados anteriores nem as contestações — isso é ancoragem, e um refutador ancorado só reconfere o que já foi mexido.

**Rodada 2** — três subagentes em paralelo (emita as três chamadas no mesmo bloco), cada um com um ângulo de `references/prompt-refutador.md`:
- **Correção e factualidade** — o que está afirmado ou implementado está errado?
- **Requisitos e omissão** — o que o pedido exigia e não aparece em lugar nenhum?
- **Efeito colateral e regressão** — o que mais quebrou, contradisse ou sobrescreveu?

**Rodada 3** — um refutador por dimensão vermelha, **mais um generalista** sobre o artefato inteiro. **Vermelha** é a dimensão que perdeu um terço ou mais do seu peso na rodada 2, ou que recebeu qualquer achado substantivo confirmado; desconto menor isolado não pinta a dimensão de vermelho.

O generalista não é opcional e não é redundância. Sem ele, a rodada 3 examina só as dimensões que já estavam ruins, enquanto o artefato mudou desde a rodada 2 — você corrigiu coisas — e a cobertura das dimensões verdes atesta uma versão que não existe mais. No limite em que só uma dimensão ficou vermelha, um único refutador de escopo estreito não acharia nada, assinaria 100, e o portão abriria com um quinto do artefato reexaminado depois da correção. Cobertura não se herda através de uma mudança.

Como o escopo dos focados é estreito por instrução, o teto de cobertura deles se avalia só sobre a dimensão que lhes coube; o do generalista se avalia normalmente, sobre todas as alegações centrais.

**Agregação de uma rodada com vários refutadores:** siga os três passos de `references/rubrica.md` — (1) recompor cada nota individual, derrubando o teto de cobertura que outro refutador da mesma rodada desmentiu; (2) descontar contestações reconhecidas e retestadas; (3) só então tirar o **mínimo** entre as notas recompostas, nunca a média. Os achados são a **união**: um defeito encontrado por um só continua sendo um defeito.

O passo 1 não é formalidade. Sem ele o mínimo cru trava o caso mais comum que existe — um refutador sem ferramenta para uma alegação assina 85 pelo teto de cobertura enquanto os outros dois cobrem tudo e assinam 100 — e um artefato que a rodada inteira cobriu e não conseguiu derrubar cai para outra rodada, e depois para o teto de rodadas, e sai marcado como não concluído.

**Teto de 3 rodadas.** Bateu o teto ainda em ≤ 85: entregue assim mesmo, com a nota final e a lista do que sobrou. Nunca estenda o ciclo para forçar uma nota bonita, nunca reporte como concluído.

## 6. Entregar ao usuário

O relatório final, em português, contém:

- **Nota final** e em que rodada ela saiu.
- **O que foi refutado e corrigido** ao longo do ciclo — o que estava errado de fato, com a correção aplicada.
- **O que foi contestado** — achado do refutador que não reproduziu, com a evidência que o contradiz.
- **O que continua sem cobertura** — cruze aqui o seu registro de alegações (documento 1b) com o que os refutadores efetivamente atacaram. Toda linha do registro que nenhum refutador tocou entra nesta seção, junto com o que eles próprios declararam fora de alcance. É a razão de o registro existir, e é a informação mais honesta que o ciclo produz: não é o que foi verificado, é onde a verificação não chegou. Obrigatória, e nunca vazia por conveniência.
- **Achados remanescentes**, se a nota final ficou ≤ 85.

Ao terminar, apague o `dossie-verificacao.md`. Ele é arquivo de trabalho, foi regenerado a cada rodada, e não é registro de nada — o relatório é.

Vocabulário do fechamento: com nota > 85 e todos os achados resolvidos, o trabalho é **não refutado** — nunca "verificado", "aprovado" ou "tudo certo". A ausência de refutação sobrevivente é o que se pode afirmar; correção não é.

## Quando não houver subagente disponível

Em ambiente sem ferramenta de subagente, não substitua o refutador por auto-revisão no seu próprio contexto — isso é exatamente o viés que a skill existe para eliminar.

Faça o seguinte: monte o dossiê normalmente, monte o prompt do refutador com ele embutido, e entregue os dois ao usuário em um bloco pronto para colar em **uma conversa nova e vazia** — que é um contexto tão limpo quanto o de um subagente. Marque o resultado como `SEM REFUTAÇÃO` até o usuário trazer o veredito de volta. Nunca como concluído.

## Racionalizações que não valem

| Desculpa | Realidade |
|---|---|
| "É uma mudança simples" | Tarefa fácil tem taxa de falso sucesso maior, não menor |
| "Eu já conferi" | Quem executou não dá a nota. É o ponto inteiro |
| "O grep não achou nada" | Grep errado não acha nada. Qual era o predicado? |
| "O subagente disse que passou" | Relatório de subagente é alegação, não evidência |
| "Rodar de novo é desperdício" | O ciclo custa segundos; a regressão silenciosa custa a confiança |
| "Só falta uma coisinha" | Então não está completo. Diga isso |
| "A nota deu 85, arredonda" | O portão é acima de 85. 85 é uma rodada nova |

## Arquivos de referência

- `references/rubrica.md` — as cinco dimensões, os pesos, os tetos e a agregação entre refutadores. Leia antes de interpretar qualquer nota.
- `references/prompt-refutador.md` — os prompts literais a passar ao subagente, um por ângulo. Copie, não improvise.
- `references/angulos-por-dominio.md` — onde a falha se esconde em código, pesquisa, laudo, explicação, dados e configuração.
