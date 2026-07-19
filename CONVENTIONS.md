# CONVENTIONS.md

Convenção de estilo para os arquivos `match/*.yml` deste repositório. Este documento é o resultado de uma padronização revisada entrada a entrada com o mantenedor do repositório — não é um estilo imposto de fora, é o que já era praticado na maior parte do repositório, formalizado e completado onde faltava.

## Ordem de chaves

Toda entrada usa a ordem canônica:

```yaml
- trigger: "exemplo"
  label: "Descrição curta e pesquisável"
  replace: Texto ou template a expandir.
  word: true
```

`trigger` e `word` são sempre obrigatórios. `replace` é sempre obrigatório. `label` é obrigatório em toda entrada — ver seção abaixo.

## `label`

Todo trigger tem um `label` curto, pensado para busca (é o campo indexado pela ferramenta em `web/index.html`). Regra de ouro: **menos é mais**.

- Fragmento curto/gramatical sem conteúdo clínico próprio (abreviação, lateralidade, conector) → o label pode ser o próprio texto do `replace`, ou uma descrição de 2-4 palavras.
- Achado clínico real (frase ou parágrafo descrevendo um achado) → o label nomeia a patologia/achado central em poucas palavras (3-8), não repete a frase inteira. Ex.: um `replace` descrevendo cálculo na vesícula biliar com sombra acústica posterior → `label: "Colecistolitíase"`.
- Template de laudo completo (multi-linha, começa com um título tipo "RADIOGRAFIA DE TÓRAX") → o label é o nome do exame, com um qualificador curto se fizer sentido (ex.: `"Radiografia de tórax — normal"`).
- Nunca repita o `trigger` como label, a menos que o trigger já seja uma palavra legível.

## Charset do trigger

Todo trigger **novo** usa só `[a-z0-9]` — sem acento, maiúscula ou pontuação. Isso garante digitação confiável independente de layout de teclado/SO. Essa regra vale para triggers novos e para renomeações; **não se aplica retroativamente** a triggers antigos preservados em `match/legado.yml` (ver abaixo).

## `match/legado.yml`

Quando um trigger existente precisa ser renomeado para se adequar à convenção (tipicamente por charset), a grafia **antiga** não é apagada — ela é movida para `match/legado.yml`, com o mesmo `replace` do trigger canônico, preservando a memória muscular de quem já digita aquele mnemônico há anos. A grafia **nova**, em conformidade com o charset, passa a viver no arquivo de modalidade correto (`rx.yml`, `tc.yml`, etc.).

`match/legado.yml` é organizado por comentários indicando o arquivo de origem e, acima de cada entrada, o trigger canônico correspondente:

```yaml
  # ============================================================
  # ORIGEM: rx.yml
  # ============================================================

  # substituído por "cabecote" em rx.yml
  - trigger: "cabeçote"
    label: "..."
    replace: "..."
    word: true
```

`match/legado.yml` só cresce por esse motivo — nunca recebe triggers novos diretamente. Espanso carrega todos os arquivos de `match/` num único namespace global, então esse arquivo não "isola" nada tecnicamente; a separação é só organizacional, para deixar claro que aquela grafia é legada.

## Seções temáticas

Arquivos com muitas entradas (`rx.yml`, `tc.yml`) são organizados sob banners de comentário por região anatômica/sistema, no mesmo estilo já usado em `us.yml`:

```yaml
  # ==========================================================================
  # NOME DA SEÇÃO
  # ==========================================================================
```

Taxonomia usada (mesma lista em ambos os arquivos, pulando seções vazias):

1. Crânio / Encéfalo / SNC
2. Face / Órbitas / Seios da Face / Pescoço / ATM
3. Coluna (cervical, torácica, lombar, sacrococcígea)
4. Tórax (pulmão, mediastino, coração, arcos costais)
5. Abdome / Pelve
6. Membros Superiores
7. Membros Inferiores
8. Vascular
9. Templates completos / Cabeçalhos de exame / Assinaturas
10. Gerais / Diversos

A classificação é heurística (por palavras-chave no trigger/replace) e revisada por amostragem — não é perfeita. Fragmentos genéricos que não mencionam uma região específica (ex. "Fratura oblíqua", "Textura óssea preservada.") legitimamente ficam em "Gerais / Diversos".

## Nomenclatura de triggers novos

- **Código de órgão + número**, no estilo já usado em `us.yml` (`vb1`, `vb2`, `ba3`, `rv14`...): padrão recomendado para achados novos em qualquer arquivo, não só `us.yml`. O mesmo código de órgão é reaproveitado entre modalidades (ex. `vb` para vesícula biliar vale tanto para uma entrada nova em `us.yml` quanto em `tc.yml`).
- **Par achado + conclusão** (`trigger` / `triggerc`): use quando o achado tiver uma versão descritiva longa (para o corpo do laudo) E uma frase-conclusão curta útil separadamente (para a seção de conclusão). Se não houver essa separação natural, não force o par.
- **Sem prefixo de modalidade por padrão** (`rx`/`tc`/`us`). Prefixo só entra como válvula de escape para desambiguar uma colisão real entre modalidades — não é obrigatório em todo trigger novo.
- Antes de adicionar um trigger novo, sempre grep em todos os `match/*.yml` para evitar colisão silenciosa:
  ```
  grep -rn 'trigger: "seutrigger"' match/
  ```

## O que preservar ao editar

- Blocos literais (`|`, `|-`) para `replace` multilinha — preserva quebras de linha e linhas em branco do template do jeito que aparecem no arquivo.
- Uma linha em branco entre entradas.
- Triggers sempre entre aspas duplas.
