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
  - `rx_h.yml` — X-ray (radiografia). ~560 triggers, organized under `# === SECTION ===` comment banners by anatomical region/system.
  - `tc_e.yml` — CT (tomografia computadorizada). The largest file by far (~1900 triggers, ~11k lines), also organized under section banners.
  - `us.yml` — ultrasound (ultrassonografia). ~380 triggers; organized under `# === SECTION ===` comment banners grouping entries by organ/anatomical region (fígado, rins, pélvica, etc.). This file originated the `label:` convention that all other files now follow.
  - `rm_a.yml` — MRI (ressonância magnética). ~780 triggers, organized under `# === SECTION ===` comment banners following the same 10-category taxonomy as `rx_h.yml`/`tc_e.yml`. Imported in bulk from a Texter export via `scripts/texter_to_espanso.py`; entries that duplicated triggers or text already consolidated in the other match files were dropped during that import, so this file holds only MRI content that did not already exist elsewhere.
  - `legado.yml` — old trigger spellings retired by the charset convention (accented/uppercase triggers, e.g. `cabeçote`, `TCBACIA`), preserved here with the same `replace` as their canonical replacement so existing muscle memory keeps working. Organized by origin-file comment banners. Also holds a handful of punctuation-only triggers (`a/e`, `aneurisma?`, `v/q`, `c#`, `c=`) that were moved here as-is rather than renamed, since no canonical charset-compliant spelling replaces them. Only shrinks/grows when a trigger is renamed (or moved for charset reasons) — never add a brand-new trigger here directly. See `CONVENTIONS.md` for the full mechanism.
- `scripts/` — standalone Python utilities, not part of any runtime pipeline:
  - `beeftext_to_espanso.py` — converts a BeefText JSON export (`comboList.json`) into per-group Espanso YAML files, with custom manual YAML serialization (chosen over PyYAML's default output because PyYAML collapses multiline strings into ugly `"...\n..."` scalars instead of readable block literals).
  - `texter_to_espanso.py` — converts a Texter HTML export into a single Espanso YAML file, with extra handling for cp1252/C1-control-character cleanup common in old Windows exports.
  - `check_matches.py` — read-only lint over all `match/*.yml`: flags duplicate triggers (within a file and across files), missing `word`/`label`, wrong key order, and triggers outside the `[a-z0-9]` charset that live outside `legado.yml`. Fixes nothing automatically. Currently returns `OK` with zero problems — the previous punctuation-only triggers (`a/e`, `v/q`, `c#`, `c=`, `aneurisma?`) were moved into `legado.yml` for this reason. The release workflow (`.github/workflows/release.yml`) runs this and aborts the build if it fails, so it must keep returning clean.
  - `espanso_to_beeftext.py` — converts one or more `match/*.yml` files into a single BeefText-importable `comboList.json` (`fileFormatVersion` 10), one group per input file. Used by `scripts/build_release.sh` to build the BeefText portable release artifact.
  - `check_poster_coverage.py` — read-only lint over the same lines as `check_matches.py`, but for wall-poster drift: diffs `match/us.yml` triggers against what `docs/poster/poster_data.py` claims to cover (via that module's `todos_os_triggers()`), plus its `EXCLUSOES` list of `(regex, motivo)` editorial exclusions (MSK-by-segment, conclusion variants, fetal malformations, dedicated-slot Doppler, Graf hip). Errors on a poster trigger that doesn't exist (broken reference) or a `us.yml` trigger that's neither on the poster nor excluded (undecided drift). Fixes nothing. Run by `build_release.sh` right after `check_matches.py`, so it must keep returning clean.
  - `gen_poster.py` — renders `docs/poster/poster_data.py` into `docs/poster-us.html` (a print-CSS page, A4 landscape, no external dependency). `build_release.sh` converts that HTML to `docs/poster-us.pdf` via `weasyprint`. Font floor is `11.8px` (legibility at 1-2m) — never shrink it to force a page count; if curated content grows, let the poster spill onto additional pages instead.
  - `gen_cheatsheet.py` — regenerates `docs/cheatsheet-us.md`, an exhaustive uncurated trigger→label dump of `match/us.yml` grouped by section banner. Unlike the poster, there's no editorial judgment here (no achado/conclusão pairing, no D/E collapsing), so it never drifts — treat `docs/cheatsheet-us.md` as generated output, not something to hand-edit; rerun this script instead.
  - `build_release.sh` — assembles the release artifacts published by `.github/workflows/release.yml`: a base `match/`+`config/`+`poster-us.pdf` zip; a Windows portable bundle (the real espanso "Portable Edition" zip, downloaded from the latest `espanso/espanso` GitHub release); a Linux bundle using `Espanso-X11.AppImage` (espanso has no official portable Linux build — the AppImage, a chmod-and-run single executable, is the closest equivalent); a macOS bundle with no binary at all (espanso ships only a `.dmg` installer for macOS, so this is just `match/`+`config/` plus install instructions); a portable BeefText bundle (downloaded from the latest `xmichelo/Beeftext` release, pre-loaded with a generated `comboList.json`); and `docs/poster-us.pdf` also as a standalone release asset. Runs `check_matches.py` then `check_poster_coverage.py` first and aborts on failure of either, then regenerates and renders the poster before staging anything. Usage: `scripts/build_release.sh <version> [--with-portable]`.
  - Run standalone, e.g. `python3 scripts/beeftext_to_espanso.py comboList.json ./out/`. Not invoked by CI or by each other, except `build_release.sh`/`espanso_to_beeftext.py`/`check_matches.py`/`check_poster_coverage.py`/`gen_poster.py` which the release workflow does invoke.
- `docs/` — generated/curated reference material, not source of truth (that's always `match/*.yml`):
  - `docs/cheatsheet-us.md` — generated by `scripts/gen_cheatsheet.py`, see above. Regenerate after any `match/us.yml` change instead of hand-editing.
  - `docs/poster/poster_data.py` — the curated content of the US wall poster: which triggers get a line, how numeric/letter escadas collapse into one row per prefix, and the `EXCLUSOES` regexes documenting what's deliberately left off. Every item declares its real, reconstructible trigger(s) (see the module docstring) — `scripts/check_poster_coverage.py` and `scripts/gen_poster.py` both derive the covered-trigger set from this data, never from parsing display strings. Editing this file is a clinical/editorial decision (which finding gets wall space, how it's worded) — treat it differently from the generated cheatsheet.
  - `docs/poster-us.html` / `docs/poster-us.pdf` — generated by `scripts/gen_poster.py` (+ `weasyprint` for the PDF). Regenerate, don't hand-edit.
- `web/index.html` — a single self-contained static page (no build step) that lets you search/browse all triggers in a browser. It fetches raw YAML directly from GitHub (`raw.githubusercontent.com`) at load time and parses it client-side with `js-yaml`. **The list of files it indexes is hardcoded** in the `ALLOWED_PATHS` array near the top of the `<script>` block — currently `geral.yml`, `rx_h.yml`, `us.yml`, `tc_e.yml`, `rm_a.yml`, `mmg.yml`, `legado.yml` (i.e. every file in `match/`). When adding a new `match/*.yml` file (or renaming one), update `ALLOWED_PATHS` or it silently won't appear in the browser tool.
- `.vscode/espanso-match.code-snippets` — VS Code snippet (prefix `ematch`) that scaffolds a new `trigger`/`replace`/`word: true` block.
- `.claude/skills/add-espanso/SKILL.md` — the `/add-espanso` Claude Code skill: adds a new trigger/match entry to `match/*.yml` from a pasted report snippet, following `CONVENTIONS.md`. Must live here (project-scoped, committed) rather than only in a user's personal `~/.claude/skills/`, or it won't be available in fresh/remote sessions of this repo.
- `.claude/rules/verificacao-adversarial.md` — project rule, loaded automatically into every session alongside this file (no `paths:` frontmatter, so it is unconditional): no claim of completion may be reported until a separate refuting subagent has tried and failed to break it. Committed here, rather than living only in a maintainer's `~/.claude/CLAUDE.md`, so it also applies in fresh/remote sessions of this repo. Like all CLAUDE.md-layer instructions it is advisory, not enforcement — see the file's own closing section.
- `.github/workflows/claude.yml` — wires up the Claude Code GitHub Action plus an automated changelog generator action; not a test/build pipeline.
- `.github/workflows/release.yml` — manually-triggered (`workflow_dispatch`) release pipeline: validates the version input, installs `weasyprint`'s system libs, runs `scripts/build_release.sh`, tags the commit, and publishes a GitHub Release with the resulting `dist/*.zip` and `dist/*.pdf` artifacts.

## Match file conventions

See `CONVENTIONS.md` for the full style guide (key order, `label` rules, trigger charset, `legado.yml`, section taxonomy, trigger-naming patterns). Summary of what matters most day to day:

- Every match entry needs `trigger`, `label`, `replace`, and `word: true`, in that order.
- Multi-line report templates use YAML block literals (`|` or `|-`), not `\n`-escaped strings, so the template's line breaks and blank lines stay visually readable in the file. Preserve this when adding or editing multiline `replace` values.
- Full-report templates always use the same three section headings, in Title Case: `Técnica:` → `Descrição:` → `Conclusão:`, each preceded by exactly one blank line and followed immediately by its content. The older spellings (`Análise:`, `Opinião:`, `Impressão:`, `RELATÓRIO:`, and the ALL-CAPS variants) were normalized away — don't reintroduce them. See `CONVENTIONS.md`.
- All trigger/replacement text is Brazilian Portuguese radiology terminology. Triggers are short mnemonics, often loosely related to the finding they expand into (e.g. `adir` → "à direita", `codc` → "Correlacionar com dados clínicos.").
- New triggers use only `[a-z0-9]` (no accents/uppercase/punctuation) — see `CONVENTIONS.md` for why and for the `legado.yml` mechanism that preserves old spellings when a trigger is renamed for this reason.
- **Match files are not namespaced** — Espanso loads everything under `match/` into one global set of triggers, and splitting by modality (rx/tc/us/...) is organizational only, not isolation. Before adding a new trigger, grep across all of `match/*.yml` for that trigger string to avoid silently shadowing (or being shadowed by) an existing one:
  ```
  grep -rn 'trigger: "yourtrigger"' match/
  ```

## Validating changes

There's no test suite. To sanity-check a YAML edit before committing:
```
python3 -c "import yaml; yaml.safe_load(open('match/rx_h.yml'))"
```
To check the edit against the conventions in `CONVENTIONS.md` (duplicate triggers, missing `word`/`label`, key order, charset):
```
python3 scripts/check_matches.py
```
For a real functional check, follow the README setup: copy `config/` and `match/` into the Espanso config directory (`espanso path`) and restart Espanso, then type the trigger in a text field to confirm the expansion looks right.
