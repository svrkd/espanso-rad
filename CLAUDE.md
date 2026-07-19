# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not** a software application — it's a personal [Espanso](https://espanso.org) (cross-platform text expander) configuration for a Brazilian radiologist's reporting workflow. The "codebase" is almost entirely YAML data: trigger → replacement-text pairs that expand short mnemonics into full radiology report sentences/templates in Brazilian Portuguese. There is no build system, package manager, application server, or test suite — changes are evaluated by loading the config into Espanso and typing the triggers.

## Repository layout

- `config/default.yml` — global Espanso config (keyboard layout `br`, word separators, backspace behavior). Rarely needs changes.
- `match/*.yml` — the actual match files, one per imaging modality. Each file is a standalone Espanso match file (top-level `matches:` key, a list of trigger/replace entries):
  - `geral.yml` — general-purpose triggers not tied to a modality (site shortcuts, common phrases like "correlacionar com dados clínicos").
  - `mmg.yml` — mammography (mamografia) report templates.
  - `rx.yml` — X-ray (radiografia). ~570 triggers, largest file after `tc.yml`.
  - `tc.yml` — CT (tomografia computadorizada). The largest file by far (~2000 triggers, ~11k lines).
  - `us.yml` — ultrasound (ultrassonografia). ~380 triggers; organized under `# === SECTION ===` comment banners grouping entries by organ/anatomical region (fígado, rins, pélvica, etc.), and — unlike every other file — each entry has a `label:` field giving a human-readable description. `label` is consumed by `web/index.html` for its tab/search UI and has no effect in Espanso itself.
- `scripts/` — one-off Python migration utilities, not part of any runtime pipeline:
  - `beeftext_to_espanso.py` — converts a BeefText JSON export (`comboList.json`) into per-group Espanso YAML files, with custom manual YAML serialization (chosen over PyYAML's default output because PyYAML collapses multiline strings into ugly `"...\n..."` scalars instead of readable block literals).
  - `texter_to_espanso.py` — converts a Texter HTML export into a single Espanso YAML file, with extra handling for cp1252/C1-control-character cleanup common in old Windows exports.
  - Run standalone, e.g. `python3 scripts/beeftext_to_espanso.py comboList.json ./out/`. Not invoked by CI or by each other.
- `web/index.html` — a single self-contained static page (no build step) that lets you search/browse all triggers in a browser. It fetches raw YAML directly from GitHub (`raw.githubusercontent.com`) at load time and parses it client-side with `js-yaml`. **The list of files it indexes is hardcoded** in the `ALLOWED_PATHS` array near the top of the `<script>` block — currently `geral.yml`, `rx.yml`, `us.yml`, `tc.yml`. `mmg.yml` is not listed. When adding a new `match/*.yml` file (or renaming one), update `ALLOWED_PATHS` or it silently won't appear in the browser tool.
- `.vscode/espanso-match.code-snippets` — VS Code snippet (prefix `ematch`) that scaffolds a new `trigger`/`replace`/`word: true` block.
- `.github/workflows/claude.yml` — wires up the Claude Code GitHub Action plus an automated changelog generator action; not a test/build pipeline.

## Match file conventions

- Every match entry needs `trigger`, `replace`, and (with rare exception) `word: true` — word-boundary matching is the near-universal convention here so triggers don't fire mid-word.
- Key order is inconsistent between files (`rx.yml`/`geral.yml`/`mmg.yml` write `trigger` → `replace` → `word`; `tc.yml` writes `trigger` → `word` → `replace`; `us.yml` writes `trigger` → `label` → `replace` → `word`). When editing a file, follow that file's existing local ordering rather than imposing a global style.
- Multi-line report templates use YAML block literals (`|` or `|-`), not `\n`-escaped strings, so the template's line breaks and blank lines stay visually readable in the file. Preserve this when adding or editing multiline `replace` values.
- All trigger/replacement text is Brazilian Portuguese radiology terminology. Triggers are short mnemonics, often loosely related to the finding they expand into (e.g. `adir` → "à direita", `codc` → "Correlacionar com dados clínicos.").
- **Match files are not namespaced** — Espanso loads everything under `match/` into one global set of triggers, and splitting by modality (rx/tc/us/...) is organizational only, not isolation. There are already accidental cross-file collisions (e.g. `eap`, `cv`, `cvc`, `diu`, `dpoc`, `qil` exist in both `rx.yml` and `tc.yml` with different expansions) and even a few *within* a single file (`rx.yml` currently defines `rxcar`, `rxt1`, `iomcv`, `redub`, and `rxombro1` twice each). Before adding a new trigger, grep across all of `match/*.yml` for that trigger string to avoid silently shadowing (or being shadowed by) an existing one:
  ```
  grep -rn 'trigger: "yourtrigger"' match/
  ```

## Validating changes

There's no test suite. To sanity-check a YAML edit before committing:
```
python3 -c "import yaml; yaml.safe_load(open('match/rx.yml'))"
```
For a real functional check, follow the README setup: copy `config/` and `match/` into the Espanso config directory (`espanso path`) and restart Espanso, then type the trigger in a text field to confirm the expansion looks right.
