# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not** a software application — it's a personal [Espanso](https://espanso.org) (cross-platform text expander) configuration for a Brazilian radiologist's reporting workflow. The "codebase" is almost entirely YAML data: trigger → replacement-text pairs that expand short mnemonics into full radiology report sentences/templates in Brazilian Portuguese. There is no build system, package manager, application server, or test suite — changes are evaluated by loading the config into Espanso and typing the triggers.

## Repository layout

- `config/default.yml` — global Espanso config (keyboard layout `br`, word separators, backspace behavior). Rarely needs changes.
- `CONVENTIONS.md` — the style guide for `match/*.yml`: canonical key order, `label` rules, trigger charset, the `match/legado.yml` mechanism, section-banner taxonomy, and trigger-naming conventions. Read this before adding or editing entries.
- `match/*.yml` — the actual match files, mostly one per imaging modality. Each file is a standalone Espanso match file (top-level `matches:` key, a list of trigger/replace entries). All files follow the canonical key order `trigger` → `label` → `replace` → `word` (see `CONVENTIONS.md`), and every entry has a `label`:
  - `geral.yml` — general-purpose triggers not tied to a modality (site shortcuts, common phrases like "correlacionar com dados clínicos").
  - `mmg.yml` — mammography (mamografia) report templates.
  - `rx.yml` — X-ray (radiografia). ~560 triggers, organized under `# === SECTION ===` comment banners by anatomical region/system.
  - `tc.yml` — CT (tomografia computadorizada). The largest file by far (~1900 triggers, ~11k lines), also organized under section banners.
  - `us.yml` — ultrasound (ultrassonografia). ~380 triggers; organized under `# === SECTION ===` comment banners grouping entries by organ/anatomical region (fígado, rins, pélvica, etc.). This file originated the `label:` convention that all other files now follow.
  - `legado.yml` — old trigger spellings retired by the charset convention (accented/uppercase triggers, e.g. `cabeçote`, `TCBACIA`), preserved here with the same `replace` as their canonical replacement so existing muscle memory keeps working. Organized by origin-file comment banners. Also holds a handful of punctuation-only triggers (`a/e`, `aneurisma?`, `v/q`, `c#`, `c=`) that were moved here as-is rather than renamed, since no canonical charset-compliant spelling replaces them. Only shrinks/grows when a trigger is renamed (or moved for charset reasons) — never add a brand-new trigger here directly. See `CONVENTIONS.md` for the full mechanism.
- `scripts/` — standalone Python utilities, not part of any runtime pipeline:
  - `beeftext_to_espanso.py` — converts a BeefText JSON export (`comboList.json`) into per-group Espanso YAML files, with custom manual YAML serialization (chosen over PyYAML's default output because PyYAML collapses multiline strings into ugly `"...\n..."` scalars instead of readable block literals).
  - `texter_to_espanso.py` — converts a Texter HTML export into a single Espanso YAML file, with extra handling for cp1252/C1-control-character cleanup common in old Windows exports.
  - `check_matches.py` — read-only lint over all `match/*.yml`: flags duplicate triggers (within a file and across files), missing `word`/`label`, wrong key order, and triggers outside the `[a-z0-9]` charset that live outside `legado.yml`. Fixes nothing automatically. Currently returns `OK` with zero problems — the previous punctuation-only triggers (`a/e`, `v/q`, `c#`, `c=`, `aneurisma?`) were moved into `legado.yml` for this reason. The release workflow (`.github/workflows/release.yml`) runs this and aborts the build if it fails, so it must keep returning clean.
  - `espanso_to_beeftext.py` — converts one or more `match/*.yml` files into a single BeefText-importable `comboList.json` (`fileFormatVersion` 10), one group per input file. Used by `scripts/build_release.sh` to build the BeefText portable release artifact.
  - `build_release.sh` — assembles the release artifacts published by `.github/workflows/release.yml`: a base `match/`+`config/` zip; a Windows portable bundle (the real espanso "Portable Edition" zip, downloaded from the latest `espanso/espanso` GitHub release); a Linux bundle using `Espanso-X11.AppImage` (espanso has no official portable Linux build — the AppImage, a chmod-and-run single executable, is the closest equivalent); a macOS bundle with no binary at all (espanso ships only a `.dmg` installer for macOS, so this is just `match/`+`config/` plus install instructions); and a portable BeefText bundle (downloaded from the latest `xmichelo/Beeftext` release, pre-loaded with a generated `comboList.json`). Runs `check_matches.py` first and aborts on failure. Usage: `scripts/build_release.sh <version> [--with-portable]`.
  - Run standalone, e.g. `python3 scripts/beeftext_to_espanso.py comboList.json ./out/`. Not invoked by CI or by each other, except `build_release.sh`/`espanso_to_beeftext.py`/`check_matches.py` which the release workflow does invoke.
- `web/index.html` — a single self-contained static page (no build step) that lets you search/browse all triggers in a browser. It fetches raw YAML directly from GitHub (`raw.githubusercontent.com`) at load time and parses it client-side with `js-yaml`. **The list of files it indexes is hardcoded** in the `ALLOWED_PATHS` array near the top of the `<script>` block — currently `geral.yml`, `rx.yml`, `us.yml`, `tc.yml`, `legado.yml`. `mmg.yml` is not listed. When adding a new `match/*.yml` file (or renaming one), update `ALLOWED_PATHS` or it silently won't appear in the browser tool.
- `.vscode/espanso-match.code-snippets` — VS Code snippet (prefix `ematch`) that scaffolds a new `trigger`/`replace`/`word: true` block.
- `.claude/skills/add-espanso/SKILL.md` — the `/add-espanso` Claude Code skill: adds a new trigger/match entry to `match/*.yml` from a pasted report snippet, following `CONVENTIONS.md`. Must live here (project-scoped, committed) rather than only in a user's personal `~/.claude/skills/`, or it won't be available in fresh/remote sessions of this repo.
- `.github/workflows/claude.yml` — wires up the Claude Code GitHub Action plus an automated changelog generator action; not a test/build pipeline.
- `.github/workflows/release.yml` — manually-triggered (`workflow_dispatch`) release pipeline: validates the version input, runs `scripts/build_release.sh`, tags the commit, and publishes a GitHub Release with the resulting `dist/*.zip` artifacts.

## Match file conventions

See `CONVENTIONS.md` for the full style guide (key order, `label` rules, trigger charset, `legado.yml`, section taxonomy, trigger-naming patterns). Summary of what matters most day to day:

- Every match entry needs `trigger`, `label`, `replace`, and `word: true`, in that order.
- Multi-line report templates use YAML block literals (`|` or `|-`), not `\n`-escaped strings, so the template's line breaks and blank lines stay visually readable in the file. Preserve this when adding or editing multiline `replace` values.
- All trigger/replacement text is Brazilian Portuguese radiology terminology. Triggers are short mnemonics, often loosely related to the finding they expand into (e.g. `adir` → "à direita", `codc` → "Correlacionar com dados clínicos.").
- New triggers use only `[a-z0-9]` (no accents/uppercase/punctuation) — see `CONVENTIONS.md` for why and for the `legado.yml` mechanism that preserves old spellings when a trigger is renamed for this reason.
- **Match files are not namespaced** — Espanso loads everything under `match/` into one global set of triggers, and splitting by modality (rx/tc/us/...) is organizational only, not isolation. Before adding a new trigger, grep across all of `match/*.yml` for that trigger string to avoid silently shadowing (or being shadowed by) an existing one:
  ```
  grep -rn 'trigger: "yourtrigger"' match/
  ```

## Validating changes

There's no test suite. To sanity-check a YAML edit before committing:
```
python3 -c "import yaml; yaml.safe_load(open('match/rx.yml'))"
```
To check the edit against the conventions in `CONVENTIONS.md` (duplicate triggers, missing `word`/`label`, key order, charset):
```
python3 scripts/check_matches.py
```
For a real functional check, follow the README setup: copy `config/` and `match/` into the Espanso config directory (`espanso path`) and restart Espanso, then type the trigger in a text field to confirm the expansion looks right.
