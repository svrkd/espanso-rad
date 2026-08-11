#!/usr/bin/env bash
# Monta os artefatos de release do espanso-rad.
#
# Gera:
#   dist/espanso-rad-<version>.zip                    (só match/ + config/, uso com espanso já instalado)
#   dist/espanso-rad-portable-win-<version>.zip       (match/ + config/ + espanso Portable Edition Windows x64)
#   dist/espanso-rad-portable-linux-<version>.zip     (match/ + config/ + Espanso-X11.AppImage — espanso não
#                                                       tem build "portátil" oficial para Linux, o AppImage é
#                                                       o equivalente mais próximo: executável único, chmod +x
#                                                       e rodar, sem gerenciador de pacotes)
#   dist/espanso-rad-mac-<version>.zip                (só match/ + config/ + instruções — espanso não distribui
#                                                       nenhum build standalone para macOS, só um .dmg para
#                                                       /Applications que exige permissão de Acessibilidade)
#   dist/espanso-rad-beeftext-portable-<version>.zip  (BeefText Portable Edition + comboList.json pré-gerado)
#   dist/poster-us-<version>.pdf                      (pôster de parede de referência rápida — US, também
#                                                       incluído dentro do pacote base)
#
# Uso:
#   scripts/build_release.sh <version> [--with-portable]
#
# --with-portable baixa os binários do espanso/espanso (Windows Portable Edition + Linux AppImage) e do
# xmichelo/Beeftext (releases mais recentes) e monta os quatro zips adicionais. Requer GITHUB_TOKEN no
# ambiente para evitar rate limit da API do GitHub (o workflow do Actions já injeta isso).

set -euo pipefail

VERSION="${1:?uso: build_release.sh <version> [--with-portable]}"
WITH_PORTABLE="${2:-}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="$REPO_ROOT/dist"
STAGE="$REPO_ROOT/.stage"

rm -rf "$DIST" "$STAGE"
mkdir -p "$DIST" "$STAGE"

# --- validação prévia: aborta se check_matches.py encontrar problema ---
echo "==> Validando match/*.yml"
python3 "$REPO_ROOT/scripts/check_matches.py"

# --- validação de deriva do pôster: aborta se poster_data.py e match/us.yml divergirem ---
echo "==> Validando cobertura do pôster (docs/poster/poster_data.py x match/us.yml)"
python3 "$REPO_ROOT/scripts/check_poster_coverage.py"

# --- gera o pôster e renderiza o PDF ---
echo "==> Gerando pôster de parede"
python3 "$REPO_ROOT/scripts/gen_poster.py"
python3 - "$REPO_ROOT/docs/poster-us.html" "$REPO_ROOT/docs/poster-us.pdf" <<'PYEOF'
import sys
from weasyprint import HTML
html_path, pdf_path = sys.argv[1], sys.argv[2]
doc = HTML(filename=html_path).render()
doc.write_pdf(pdf_path)
print(f"    -> {pdf_path} ({len(doc.pages)} página(s))")
PYEOF

# --- pacote base: match/ + config/ + pôster ---
echo "==> Montando pacote base"
BASE_STAGE="$STAGE/base"
mkdir -p "$BASE_STAGE"
cp -r "$REPO_ROOT/match" "$BASE_STAGE/match"
cp -r "$REPO_ROOT/config" "$BASE_STAGE/config"
cp "$REPO_ROOT/docs/poster-us.pdf" "$BASE_STAGE/poster-us.pdf"

BASE_ZIP="$DIST/espanso-rad-${VERSION}.zip"
(cd "$BASE_STAGE" && zip -rq "$BASE_ZIP" match config poster-us.pdf)
echo "    -> $BASE_ZIP"

# --- pôster também como asset solto, para download direto sem descompactar ---
POSTER_PDF_OUT="$DIST/poster-us-${VERSION}.pdf"
cp "$REPO_ROOT/docs/poster-us.pdf" "$POSTER_PDF_OUT"
echo "    -> $POSTER_PDF_OUT"

if [ "$WITH_PORTABLE" != "--with-portable" ]; then
    echo "==> Concluído (sem pacotes portáteis)"
    exit 0
fi

AUTH_HEADER=()
if [ -n "${GITHUB_TOKEN:-}" ]; then
    AUTH_HEADER=(-H "Authorization: Bearer $GITHUB_TOKEN")
fi

# Seleciona um asset de uma release do GitHub via regex sobre o nome (case-insensitive).
# $1 = regex do nome do asset, $2 = caminho do JSON da release (default: $RELEASE_JSON).
pick_asset_url() {
    local pattern="$1"
    local json_file="${2:-$RELEASE_JSON}"
    python3 -c "
import json, re, sys
data = json.load(open('$json_file'))
pattern = re.compile('$pattern', re.IGNORECASE)
for a in data.get('assets', []):
    if pattern.search(a['name']):
        print(a['browser_download_url'])
        sys.exit(0)
sys.exit(1)
"
}

# --- resolve assets da release mais recente do espanso/espanso via API ---
echo "==> Consultando release mais recente de espanso/espanso"
RELEASE_JSON="$STAGE/espanso_release.json"
curl -sSL "${AUTH_HEADER[@]}" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/espanso/espanso/releases/latest" \
    -o "$RELEASE_JSON"

ESPANSO_VERSION="$(python3 -c "import json; print(json.load(open('$RELEASE_JSON'))['tag_name'])")"
echo "    espanso ${ESPANSO_VERSION}"

# Assets confirmados no pipeline de release do espanso/espanso (podem mudar
# entre versões, vale conferir manualmente após falha de match):
#   Windows : Espanso-Win-Portable-x86_64.zip (build "Portable Edition" real)
#   Linux   : Espanso-X11.AppImage (executável único, sem instalação — não há .tar.gz)
#   macOS   : não há build portátil oficial (só .dmg para /Applications) — ver build_mac_bundle()
build_portable_zip() {
    local platform="$1"       # win | linux | mac
    local url_pattern="$2"
    local inner_dirname="$3"  # nome da subpasta onde o binário/app vai dentro do zip final

    echo "==> Montando pacote portátil: $platform"
    local url
    if ! url="$(pick_asset_url "$url_pattern")"; then
        echo "    [aviso] nenhum asset encontrado para padrão '$url_pattern', pulando $platform"
        return 0
    fi

    local asset_file="$STAGE/${platform}_asset$(basename "$url" | grep -o '\.[a-zA-Z0-9.]*$' || echo '.zip')"
    curl -sSL "${AUTH_HEADER[@]}" "$url" -o "$asset_file"

    local platform_stage="$STAGE/portable_$platform"
    mkdir -p "$platform_stage/$inner_dirname"
    cp -r "$REPO_ROOT/match" "$platform_stage/match"
    cp -r "$REPO_ROOT/config" "$platform_stage/config"

    case "$asset_file" in
        *.zip)
            (cd "$platform_stage/$inner_dirname" && unzip -q "$asset_file")
            ;;
        *.tar.gz|*.tgz)
            (cd "$platform_stage/$inner_dirname" && tar -xzf "$asset_file")
            ;;
        *)
            cp "$asset_file" "$platform_stage/$inner_dirname/"
            chmod +x "$platform_stage/$inner_dirname/$(basename "$asset_file")"
            ;;
    esac

    cat > "$platform_stage/LEIA-ME.txt" <<EOF
espanso-rad ${VERSION} — pacote portátil (${platform}, espanso ${ESPANSO_VERSION})

1. Extraia este zip em qualquer pasta.
2. Rode o executável do espanso dentro de ${inner_dirname}/.
3. O espanso vai procurar config em ~/.config/espanso (Linux/macOS) ou %APPDATA%\\espanso (Windows) —
   copie o conteúdo de match/ e config/ deste pacote para lá, ou rode em modo portátil se disponível.
EOF

    local out_zip="$DIST/espanso-rad-portable-${platform}-${VERSION}.zip"
    (cd "$platform_stage" && zip -rq "$out_zip" .)
    echo "    -> $out_zip"
}

build_portable_zip "win"   'Win-Portable.*\.zip$' "espanso-win"
build_portable_zip "linux" '\.AppImage$' "espanso-linux"

# macOS: espanso não publica nenhum build standalone (só um .dmg notarizado
# para instalar em /Applications), então não há binário para baixar/empacotar.
build_mac_bundle() {
    echo "==> Montando pacote: mac (sem binário — espanso não tem build portátil para macOS)"
    local mac_stage="$STAGE/mac_bundle"
    mkdir -p "$mac_stage"
    cp -r "$REPO_ROOT/match" "$mac_stage/match"
    cp -r "$REPO_ROOT/config" "$mac_stage/config"

    cat > "$mac_stage/LEIA-ME.txt" <<EOF
espanso-rad ${VERSION} — pacote para macOS

O espanso não distribui um build portátil para macOS — apenas um instalador
(.dmg) que deve ser movido para /Applications, além de exigir permissão de
Acessibilidade e registro do serviço do sistema operacional.

1. Instale o espanso normalmente:
   - via Homebrew: brew install espanso
   - ou baixando o .dmg oficial em https://espanso.org/install/
2. Com o espanso instalado e rodando ao menos uma vez, rode "espanso path"
   no terminal para descobrir a pasta de configuração.
3. Copie o conteúdo de match/ e config/ deste pacote para essa pasta.
EOF

    local out_zip="$DIST/espanso-rad-mac-${VERSION}.zip"
    (cd "$mac_stage" && zip -rq "$out_zip" .)
    echo "    -> $out_zip"
}

build_mac_bundle

# Localiza (ou cria) o diretório Data/ da BeefText Portable Edition dentro de
# $1, considerando que o zip pode extrair "achatado" ou dentro de uma única
# subpasta aninhada, e que Data/ pode ou não já vir presente no zip.
beeftext_data_dir() {
    local root="$1" base="" exe="" data="" subdirs=()

    exe="$(find "$root" -maxdepth 3 -type f -iname 'beeftext.exe' -print -quit 2>/dev/null || true)"
    if [ -n "$exe" ]; then
        base="$(dirname "$exe")"
    else
        mapfile -t subdirs < <(find "$root" -mindepth 1 -maxdepth 1 -type d 2>/dev/null || true)
        if [ "${#subdirs[@]}" -eq 1 ]; then base="${subdirs[0]}"; else base="$root"; fi
    fi

    data="$(find "$base" -mindepth 1 -maxdepth 1 -type d -iname 'data' -print -quit 2>/dev/null || true)"
    if [ -z "$data" ]; then
        data="$(find "$root" -maxdepth 3 -type d -iname 'data' -printf '%d\t%p\n' 2>/dev/null \
                | sort -n | awk -F'\t' 'NR==1 { print $2 }')"
    fi

    if [ -z "$data" ]; then
        data="$base/Data"
        mkdir -p "$data"
    fi

    printf '%s\n' "$data"
}

build_beeftext_portable() {
    echo "==> Montando pacote portátil: beeftext"

    local BEEFTEXT_RELEASE_JSON="$STAGE/beeftext_release.json"
    curl -sSL "${AUTH_HEADER[@]}" \
        -H "Accept: application/vnd.github+json" \
        "https://api.github.com/repos/xmichelo/Beeftext/releases/latest" \
        -o "$BEEFTEXT_RELEASE_JSON"

    local BEEFTEXT_VERSION
    BEEFTEXT_VERSION="$(python3 -c "import json; print(json.load(open('$BEEFTEXT_RELEASE_JSON'))['tag_name'])")"
    echo "    beeftext ${BEEFTEXT_VERSION}"

    local url
    if ! url="$(pick_asset_url 'PortableEdition.*\.zip$' "$BEEFTEXT_RELEASE_JSON")"; then
        echo "    [aviso] nenhum asset PortableEdition encontrado para xmichelo/Beeftext, pulando pacote beeftext"
        return 0
    fi

    local asset_file="$STAGE/beeftext_asset.zip"
    curl -sSL "${AUTH_HEADER[@]}" "$url" -o "$asset_file"

    local beeftext_root="$STAGE/beeftext"
    mkdir -p "$beeftext_root"
    (cd "$beeftext_root" && unzip -q "$asset_file")

    echo "==> Gerando comboList.json a partir de match/*.yml"
    python3 "$REPO_ROOT/scripts/espanso_to_beeftext.py" \
        "$REPO_ROOT/match/geral.yml" "$REPO_ROOT/match/us.yml" "$REPO_ROOT/match/tc.yml" \
        "$REPO_ROOT/match/rx.yml" "$REPO_ROOT/match/rm.yml" "$REPO_ROOT/match/mmg.yml" \
        "$REPO_ROOT/match/legado.yml" \
        -o "$beeftext_root/comboList.json.tmp"

    local data_dir
    data_dir="$(beeftext_data_dir "$beeftext_root")"
    mv "$beeftext_root/comboList.json.tmp" "$data_dir/comboList.json"
    echo "    comboList.json -> ${data_dir#$beeftext_root/}/comboList.json"

    cat > "$beeftext_root/LEIA-ME.txt" <<EOF
espanso-rad ${VERSION} — pacote portátil BeefText (beeftext ${BEEFTEXT_VERSION})

1. Extraia este zip em qualquer pasta.
2. Rode o executável do BeefText dentro da pasta extraída.
3. O comboList.json já vem pré-carregado com todos os combos de match/*.yml,
   organizados em grupos por arquivo de origem (geral, us, tc, rx, mmg, legado).
EOF

    local out_zip="$DIST/espanso-rad-beeftext-portable-${VERSION}.zip"
    (cd "$beeftext_root" && zip -rq "$out_zip" .)
    echo "    -> $out_zip"
}

build_beeftext_portable

echo "==> Concluído"
ls -la "$DIST"
