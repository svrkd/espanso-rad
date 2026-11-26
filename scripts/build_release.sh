#!/usr/bin/env bash
# Monta os artefatos de release do espanso-rad.
#
# Gera:
#   dist/espanso-rad-<version>.zip                    (só match/ + config/, uso com espanso já instalado)
#   dist/espanso-rad-portable-win-<version>.zip       (espanso Portable Edition Windows x64, com match/ + config/
#                                                       já dentro de .espanso/, pronto para uso)
#   dist/espanso-rad-portable-linux-<version>.zip     (Espanso-X11.AppImage + .espanso/{match,config} + scripts
#                                                       iniciar/parar que apontam ESPANSO_CONFIG_DIR — espanso não
#                                                       tem build "portátil" oficial para Linux, o AppImage é
#                                                       o equivalente mais próximo: executável único, chmod +x
#                                                       e rodar, sem gerenciador de pacotes)
#   dist/espanso-rad-mac-<version>.zip                (só match/ + config/ + instruções — espanso não distribui
#                                                       nenhum build standalone para macOS, só um .dmg para
#                                                       /Applications que exige permissão de Acessibilidade)
#   dist/espanso-rad-beeftext-portable-<version>.zip  (BeefText Portable Edition + comboList.json pré-gerado)
#   dist/laude-skill.zip                              (skills/laude/: base de referência da skill /laude,
#                                                       gerada por scripts/gen_laude_index.py)
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

# --- validação de deriva do BeefText: aborta se beeftext/comboList.json não refletir match/*.yml ---
echo "==> Validando beeftext/comboList.json x match/*.yml"
python3 "$REPO_ROOT/scripts/espanso_to_beeftext.py" --check

# --- validação de deriva da skill /laude: aborta se skills/laude/references/ não refletir match/*.yml ---
echo "==> Validando skills/laude/references/ x match/*.yml"
python3 "$REPO_ROOT/scripts/gen_laude_index.py" --check

# --- validação de deriva do CLAUDE.md: aborta se os blocos AUTO não refletirem o repositório e esta versão ---
echo "==> Validando blocos automáticos do CLAUDE.md"
python3 "$REPO_ROOT/scripts/update_claude_md.py" --check --versao "$VERSION"

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

# --- skill /laude: skills/laude/ inteira como asset (nome fixo, sem versão) ---
echo "==> Montando pacote da skill /laude"
LAUDE_ZIP="$DIST/laude-skill.zip"
(cd "$REPO_ROOT/skills" && zip -rq "$LAUDE_ZIP" laude -x '*/__pycache__/*' '*.pyc')
echo "    -> $LAUDE_ZIP"

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
    local platform="$1"       # win | linux
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

    case "$asset_file" in
        *.zip)
            (cd "$platform_stage/$inner_dirname" && unzip -q "$asset_file")
            ;;
        *.tar.gz|*.tgz)
            (cd "$platform_stage/$inner_dirname" && tar -xzf "$asset_file")
            ;;
        *)
            cp "$asset_file" "$platform_stage/$inner_dirname/$(basename "$url")"
            chmod +x "$platform_stage/$inner_dirname/$(basename "$url")"
            ;;
    esac

    # match/ e config/ vão direto para a pasta de configuração que o espanso
    # lê, para o pacote funcionar logo depois de extraído, sem cópia manual.
    local espanso_dir
    case "$platform" in
        win)
            # Portable Edition: o espanso entra em modo portátil quando existe
            # uma pasta .espanso/ ao lado de espansod.exe e lê a config de lá.
            local exe
            exe="$(find "$platform_stage/$inner_dirname" -type f -iname 'espansod.exe' -print -quit)"
            if [ -z "$exe" ]; then
                echo "    [erro] espansod.exe não encontrado no asset do Windows" >&2
                exit 1
            fi
            espanso_dir="$(dirname "$exe")/.espanso"
            ;;
        linux)
            # AppImage: o executável roda de um squashfs montado, então o modo
            # portátil por .espanso/ ao lado do binário não se aplica. Os scripts
            # apontam ESPANSO_CONFIG_DIR/ESPANSO_RUNTIME_DIR para pastas ao lado
            # do AppImage e sobem o espanso sem systemd (start --unmanaged).
            espanso_dir="$platform_stage/$inner_dirname/.espanso"
            local appimage
            appimage="$(basename "$url")"
            write_linux_script "$platform_stage/$inner_dirname/iniciar-espanso.sh" "$appimage" 'start --unmanaged'
            write_linux_script "$platform_stage/$inner_dirname/parar-espanso.sh" "$appimage" 'stop'
            ;;
    esac
    mkdir -p "$espanso_dir"
    cp -r "$REPO_ROOT/match" "$espanso_dir/match"
    cp -r "$REPO_ROOT/config" "$espanso_dir/config"
    local espanso_rel="${espanso_dir#"$platform_stage"/}"
    echo "    match/ + config/ -> $espanso_rel/"

    if [ "$platform" = "win" ]; then
        local rel_win="${espanso_rel//\//\\}"
        local bat_dir_win="${rel_win%\\.espanso}"
        cat > "$platform_stage/LEIA-ME.txt" <<EOF
espanso-rad ${VERSION} — pacote portátil (Windows, espanso ${ESPANSO_VERSION})

1. Extraia este zip em qualquer pasta.
2. Dê dois cliques em ${bat_dir_win}\\START_ESPANSO.bat.

Pronto: match\\ e config\\ já estão em ${rel_win}\\, a pasta que o espanso
lê no modo portátil. Não precisa copiar nada.

Para atualizar para uma release nova, substitua só as pastas match\\ e
config\\ dentro de ${rel_win}\\.

Se a pasta ${inner_dirname}\\ sumir depois de extrair, ou se faltar o
espansod.exe, foi o antivírus do computador que removeu o executável.
EOF
    else
        cat > "$platform_stage/LEIA-ME.txt" <<EOF
espanso-rad ${VERSION} — pacote portátil (Linux X11, espanso ${ESPANSO_VERSION})

1. Extraia este zip em qualquer pasta. Se o gerenciador de arquivos perder a
   permissão de execução, rode: chmod +x ${inner_dirname}/*.sh ${inner_dirname}/*.AppImage
2. Rode ${inner_dirname}/iniciar-espanso.sh. Para parar: ${inner_dirname}/parar-espanso.sh.

Pronto: match/ e config/ já estão em ${espanso_rel}/, e os scripts fazem o
espanso ler a configuração de lá, sem instalar nada nem mexer em
~/.config/espanso. Rodar o AppImage direto, sem os scripts, ignora essa pasta.

Para atualizar para uma release nova, substitua só as pastas match/ e
config/ dentro de ${espanso_rel}/.
EOF
    fi

    local out_zip="$DIST/espanso-rad-portable-${platform}-${VERSION}.zip"
    (cd "$platform_stage" && zip -rq "$out_zip" .)
    echo "    -> $out_zip"
}

# Escreve um script de Linux que roda o AppImage com a config da própria pasta.
# $1 = caminho do script, $2 = nome do AppImage, $3 = argumentos do espanso.
# O espanso recusa ESPANSO_RUNTIME_DIR inexistente, por isso o mkdir.
write_linux_script() {
    local path="$1" appimage="$2" args="$3"
    cat > "$path" <<EOF
#!/usr/bin/env bash
# Roda o espanso com a configuração desta pasta (.espanso/), sem instalar nada.
DIR="\$(cd "\$(dirname "\${BASH_SOURCE[0]}")" && pwd)"
export ESPANSO_CONFIG_DIR="\$DIR/.espanso"
export ESPANSO_RUNTIME_DIR="\$DIR/.espanso-runtime"
mkdir -p "\$ESPANSO_RUNTIME_DIR"
exec "\$DIR/${appimage}" ${args}
EOF
    chmod +x "$path"
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

    # Usa o beeftext/comboList.json versionado, que a validação prévia já
    # confirmou idêntico ao gerado a partir de match/*.yml.
    local data_dir
    data_dir="$(beeftext_data_dir "$beeftext_root")"
    cp "$REPO_ROOT/beeftext/comboList.json" "$data_dir/comboList.json"
    echo "    comboList.json -> ${data_dir#$beeftext_root/}/comboList.json"

    cat > "$beeftext_root/LEIA-ME.txt" <<EOF
espanso-rad ${VERSION} — pacote portátil BeefText (beeftext ${BEEFTEXT_VERSION})

1. Extraia este zip em qualquer pasta.
2. Rode o executável do BeefText dentro da pasta extraída.
3. O comboList.json já vem pré-carregado com todos os combos de match/*.yml,
   organizados em grupos por arquivo de origem (geral, us, tc, tc_abd, angio, rx,
   rm, mmg, malu, legado).

ATENÇÃO — diferença em relação ao espanso: o BeefText não tem equivalente do
"word: true", e a conversão descarta esse campo. No espanso o gatilho só
dispara delimitado por espaço ou quebra de linha; aqui ele pode disparar no
meio de uma palavra. Os gatilhos foram escolhidos para não colidirem com
palavras de laudo, mas se algum disparar sozinho onde não devia, desative-o
pelo próprio BeefText.
EOF

    local out_zip="$DIST/espanso-rad-beeftext-portable-${VERSION}.zip"
    (cd "$beeftext_root" && zip -rq "$out_zip" .)
    echo "    -> $out_zip"
}

build_beeftext_portable

echo "==> Concluído"
ls -la "$DIST"
