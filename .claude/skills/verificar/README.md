# Skill `/verificar` — instalação

Verificação adversarial cega de trabalho recém-executado. Um refutador sem acesso ao raciocínio do executor tenta derrubar o trabalho, dá nota de 0 a 100, e nota ≤ 85 dispara nova rodada com mais refutadores (teto de 3 rodadas).

A skill é genérica: não depende de nada deste repositório e roda igual em qualquer projeto. Ela está versionada aqui porque este repositório é a origem dela — a regra `.claude/rules/verificacao-adversarial.md`, que a skill implementa, nasceu neste projeto.

## Conteúdo

```
verificar/
├── SKILL.md                          o procedimento
├── README.md                         este arquivo
└── references/
    ├── rubrica.md                    dimensões, pesos, tetos, agregação
    ├── prompt-refutador.md           os prompts literais do subagente
    └── angulos-por-dominio.md        onde a falha se esconde em cada contexto
```

Mantenha a pasta inteira junta. O `SKILL.md` referencia os três arquivos de `references/` por caminho relativo, e sem eles a skill perde a rubrica e os prompts.

## Claude Code — todos os projetos

Copie a pasta para o diretório de skills pessoais:

```bash
mkdir -p ~/.claude/skills
cp -r .claude/skills/verificar ~/.claude/skills/
```

Disponível como `/verificar` em qualquer sessão do Claude Code, em qualquer repositório. Sessões já abertas precisam ser reiniciadas.

## Claude Code — um projeto só

```bash
mkdir -p <projeto>/.claude/skills
cp -r .claude/skills/verificar <projeto>/.claude/skills/
```

Versionada junto com o projeto, o que também a torna disponível em sessões remotas e em containers novos — que é o motivo de ela estar comitada aqui em vez de viver só em `~/.claude/`.

## claude.ai e app de desktop

Gere o zip e faça o upload em **Settings → Capabilities → Skills → Upload skill**:

```bash
cd .claude/skills && zip -r verificar-skill.zip verificar/
```

O zip precisa conter a pasta `verificar/` na raiz, com o `SKILL.md` dentro dela — não o `SKILL.md` solto na raiz do zip.

## Verificar se instalou

Digite `/verificar` na caixa de mensagem: a skill deve aparecer no autocomplete. Se não aparecer no Claude Code, confirme o caminho com `ls ~/.claude/skills/verificar/SKILL.md` e reinicie a sessão.

## Uso

```
/verificar                    verifica o trabalho feito nesta conversa desde o último pedido
/verificar o parser           verifica só o recorte nomeado
/verificar o laudo acima      verifica um artefato específico da conversa
```

A skill também se aciona sozinha quando você está prestes a alegar que algo está pronto, corrigido ou passando — que é o momento em que ela vale mais e o momento em que ninguém lembra de pedi-la.

## Como ela se comporta

- Monta um dossiê cego: pedido original literal, artefato extraído por ferramenta, caminhos para o estado real, e um registro de alegações com a evidência de cada uma. Nada do raciocínio do executor entra.
- Abre um subagente refutador com contexto limpo, que precisa declarar o predicado antes de rodar o teste e só pode responder `REFUTADO` ou `NÃO REFUTADO` — nunca "aprovado".
- Lê a nota. Acima de 85 entrega; 85 ou menos corrige e roda de novo, com três refutadores em paralelo na rodada 2 e refutadores focados na rodada 3.
- Antes de corrigir qualquer achado, reproduz a falha descrita. O que não reproduz vira `CONTESTADO` e não é "corrigido".
- Fecha dizendo **não refutado**, nunca "verificado" ou "tudo certo", e sempre lista o que ficou sem cobertura.

Em ambiente sem subagente, ela entrega o dossiê e o prompt prontos para colar numa conversa nova e vazia, e marca o resultado como `SEM REFUTAÇÃO` — nunca como concluído.
