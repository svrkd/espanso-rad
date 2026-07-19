---
name: add-espanso
description: Adiciona um novo trigger/match ao repositório de configuração do Espanso (match/*.yml) a partir de um texto de "replace" fornecido pelo usuário. Use sempre que o usuário invocar `/add-espanso`, pedir para "adicionar um trigger novo", "criar um match", "adicionar esse texto ao espanso", "criar um snippet/atalho de laudo" ou colar um trecho de laudo (radiografia, tomografia, ultrassom, mamografia) pedindo para transformá-lo em atalho de texto. Também use quando o usuário mencionar `tc.yml`, `us.yml`, `rx.yml`, `mmg.yml` ou `geral.yml` no contexto de adicionar uma entrada nova.
---

# Adicionar match ao Espanso (`/add-espanso`)

Esta skill automatiza a adição de uma nova entrada `trigger`/`label`/`replace`/`word` a um dos arquivos em `match/*.yml` deste repositório, seguindo as convenções em `CONVENTIONS.md` (leia esse arquivo agora, ele pode ter mudado desde a última vez).

O objetivo é reduzir o trabalho manual de digitar a entrada certa no formato certo — mas as duas decisões que só o usuário pode tomar com segurança (qual mnemônico usar e em qual arquivo/modalidade a entrada vive) continuam sendo perguntadas a ele, exceto quando ele já respondeu isso no próprio prompt.

## 1. Interpretar o prompt

Tudo que vier depois de `/add-espanso` é, por padrão, o texto candidato ao `replace`. Mas antes de tratar o texto inteiro como `replace`, procure por indicações explícitas do próprio usuário sobre:

- **trigger** — ex.: "trigger: vb3", "trigger vb3", "atalho vb3"
- **arquivo/modalidade de destino** — ex.: "arquivo: tc.yml", "vai pro us.yml", "é de tomografia", "coloca no rx"

Se o usuário já informou um desses diretamente no prompt, use o valor informado e **não pergunte de novo por ele** — pule direto para o próximo passo que ainda falta. O que sobrar do prompt depois de remover essas indicações é o `replace`.

## 2. Trigger

Se o trigger não foi informado no prompt, pergunte por pop-up usando `AskUserQuestion`. Não invente nem assuma um trigger sozinho nesse caso — a escolha do mnemônico é do usuário, é ele quem vai memorizar e digitar isso todo dia.

Ao montar a pergunta:
- Sugira 1-2 candidatos plausíveis como opções, seguindo o charset `[a-z0-9]` (sem acento/maiúscula/pontuação) e, quando fizer sentido, o padrão órgão+número de `CONVENTIONS.md` (ex. `vb3`, `rv14`) ou o padrão achado+conclusão (`trigger`/`triggerc`) quando o texto tiver claramente uma versão longa de corpo de laudo e uma frase-conclusão separável.
- Sempre deixe uma opção livre disponível (o usuário pode digitar outro valor além das sugestões).

Depois de obter o trigger (informado no prompt ou respondido no pop-up), rode a checagem de colisão:

```
grep -rn 'trigger: "SEUTRIGGER"' match/
```

Se já existir em qualquer arquivo, **não sobrescreva silenciosamente**: avise o usuário do conflito (mostre onde já existe) e peça um trigger alternativo — por pop-up de novo, a menos que o usuário já tenha antecipado um plano B.

## 3. Arquivo de destino

Mesmo quando o conteúdo do `replace` parece deixar óbvia a modalidade (por exemplo, o texto menciona "tomografia" ou já começa com "RADIOGRAFIA DE TÓRAX"), **sempre confirme o arquivo de destino com o usuário por `AskUserQuestion`** — a menos que ele já tenha indicado isso diretamente no prompt. Não decida isso sozinho por inferência silenciosa: o objetivo é que o usuário veja e confirme onde a entrada vai parar.

Opções da pergunta — apresente as que fizerem sentido, com a mais provável primeiro (baseado em palavras-chave do `replace`, ex. "tomografia"/"TC" → `tc.yml` primeiro; "ultrassom"/"USG" → `us.yml`; "radiografia"/"RX" → `rx.yml`; "mamografia" → `mmg.yml`; texto genérico sem modalidade clara → `geral.yml`):

- `tc.yml` — Tomografia computadorizada
- `us.yml` — Ultrassonografia
- `rx.yml` — Radiografia
- `mmg.yml` — Mamografia
- `geral.yml` — Geral (não específico de uma modalidade: siglas, conectores, frases de correlação clínica, atalhos de busca)

**Nunca ofereça `legado.yml` como opção.** Esse arquivo só recebe grafias antigas quando um trigger existente é renomeado — nunca recebe triggers novos diretamente (ver `CONVENTIONS.md`).

## 4. Label

Decida o `label` sozinho — esta é a parte que fica a seu critério, sem precisar perguntar. Siga a "regra de ouro" de `CONVENTIONS.md` (menos é mais):

- Fragmento curto/gramatical sem conteúdo clínico próprio (abreviação, lateralidade, conector) → o label pode ser o próprio texto do `replace`, ou uma descrição de 2-4 palavras.
- Achado clínico real (frase/parágrafo descrevendo um achado) → nomeie a patologia/achado central em poucas palavras (3-8), não repita a frase inteira.
- Template de laudo completo (multilinha, começa com um título tipo "RADIOGRAFIA DE TÓRAX") → o nome do exame, com um qualificador curto se fizer sentido (ex.: "Radiografia de tórax — normal").
- Nunca repita o trigger como label, a menos que o trigger já seja uma palavra legível.

## 5. Inserir a entrada no arquivo

Edite o arquivo de destino diretamente como texto (com a ferramenta de edição), **não** escreva um script Python que faça `yaml.dump` — isso colapsa blocos multilinha em escalares `"...\n..."` feios (o mesmo motivo pelo qual `scripts/beeftext_to_espanso.py` usa serialização manual). Regras de formatação a preservar:

- Ordem canônica de chaves: `trigger` → `label` → `replace` → `word: true`.
- `trigger` sempre entre aspas duplas, charset `[a-z0-9]` apenas.
- `replace` multilinha usa bloco literal YAML (`|` ou `|-`), nunca `\n` escapado — preserve quebras de linha e linhas em branco do jeito que devem aparecer expandidas.
- Uma linha em branco separando a nova entrada das vizinhas.

Onde inserir dentro do arquivo:
- **`rx.yml` / `tc.yml`**: dentro do banner de seção temático apropriado (`# === NOME DA SEÇÃO ===`). A taxonomia de 10 categorias está em `CONVENTIONS.md` (Crânio/Encéfalo/SNC, Face/Órbitas/..., Coluna, Tórax, Abdome/Pelve, Membros Superiores, Membros Inferiores, Vascular, Templates completos/Cabeçalhos/Assinaturas, Gerais/Diversos). Insira no fim do bloco da seção correspondente.
- **`us.yml`**: dentro do banner de órgão/região correspondente (ex. fígado, rins, pélvica).
- **`geral.yml` / `mmg.yml`**: não usam banners de seção — insira no fim do arquivo.

## 6. Validar

Depois de editar, rode:

```
python3 -c "import yaml; yaml.safe_load(open('match/<arquivo>.yml'))"
python3 scripts/check_matches.py
```

O YAML precisa carregar sem erro. `check_matches.py` já reporta alguns problemas pré-existentes fora de escopo (colisões antigas entre modalidades, triggers de pontuação legados) — isso é esperado, não é regressão sua. O que importa é que a saída não ganhe um problema novo referente à entrada que você acabou de adicionar (ordem de chave errada, falta de `label`/`word`, charset inválido, ou uma nova duplicata).

## 7. Resumir para o usuário

Ao final, informe em poucas linhas: trigger escolhido, label, arquivo e seção onde a entrada entrou, e o texto de `replace` usado — para que o usuário possa conferir rapidamente antes de usar.
