#!/bin/bash
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"
OUT_DIR="$PROJECT_DIR/out"
REPO_SLUG="${REPO_SLUG:-sorubedo/sub-store-magisk-runsv}"
RAW_BASE="${RAW_BASE:-https://raw.githubusercontent.com/$REPO_SLUG/main}"
SUPPORTED_ABIS=(arm64-v8a armeabi-v7a x86_64 x86)

if [ "${1:-}" = --help ] || [ "${1:-}" = -h ]; then
    echo "Usage: $0 [arm64-v8a|armeabi-v7a|x86_64|x86 ...]"
    echo "Run fetch.sh first. Builds one self-contained ZIP for each ABI."
    exit 0
fi
[ -f out/upstream-versions.env ] || { echo 'Run fetch.sh first' >&2; exit 1; }
# shellcheck disable=SC1091
. out/upstream-versions.env
ABIS=("${SUPPORTED_ABIS[@]}")
[ "$#" -eq 0 ] || ABIS=("$@")
for ABI in "${ABIS[@]}"; do
    case "$ABI" in arm64-v8a|armeabi-v7a|x86_64|x86) ;; *) echo "Unsupported ABI: $ABI" >&2; exit 1 ;; esac
    [ -x "bin/$ABI/bin/node" ] && [ -f "bin/$ABI/share/cacert.pem" ] || {
        echo "Missing Android Node LTS payload for $ABI; run fetch.sh" >&2; exit 1;
    }
done
[ -f assets/app/frontend/index.html ] && [ -f assets/app/sub-store.bundle.js ]

STAGE_DIR=""
trap '[ -z "$STAGE_DIR" ] || rm -rf "$STAGE_DIR"' EXIT
PACKAGES=()
for ABI in "${ABIS[@]}"; do
    STAGE_DIR="$(mktemp -d)"
    cp -a META-INF customize.sh uninstall.sh action.sh module.prop LICENSE "$STAGE_DIR/"
    SVC="$STAGE_DIR/service/sub-store"
    mkdir -p "$SVC"
    cp -a service/sub-store/. "$SVC/"
    cp -a "bin/$ABI" "$SVC/runtime"
    cp -a assets/app "$SVC/app"
    touch "$STAGE_DIR/skip_mount"
    UPDATE_URL=""
    if [ "${PUBLISH_UPDATES:-false}" = true ]; then
        UPDATE_URL="$RAW_BASE/update/$MODULE_CHANNEL/$ABI.json"
    fi
    python3 - "$STAGE_DIR/module.prop" "$MODULE_VERSION" "$MODULE_VERSION_CODE" "$UPDATE_URL" <<'PY'
import pathlib, sys
file, version, code, url = sys.argv[1:]
values = dict(line.split('=', 1) for line in pathlib.Path(file).read_text().splitlines() if '=' in line)
values.update(name='Sub-Store (runsv)', version=version, versionCode=code)
if url:
    values['updateJson'] = url
pathlib.Path(file).write_text(''.join(f'{k}={v}\n' for k, v in values.items()))
PY
    {
        echo "moduleVersion=$MODULE_VERSION"
        echo "moduleVersionCode=$MODULE_VERSION_CODE"
        echo "moduleChannel=$MODULE_CHANNEL"
        echo "targetAbi=$ABI"
        echo "nodeVersion=$NODE_PACKAGE_VERSION"
        echo "frontendVersion=$FRONTEND_TAG"
        echo "backendVersion=$SUB_STORE_TAG"
        echo "releaseTag=$RELEASE_TAG"
    } > "$STAGE_DIR/build-info.prop"
    chmod 0755 "$STAGE_DIR/"*.sh "$STAGE_DIR/META-INF/com/google/android/update-binary" \
        "$SVC/run" "$SVC/finish" "$SVC/log/run"
    chmod 0644 "$SVC/conf" "$SVC/down"
    ZIP_NAME="sub-store-runsv-$MODULE_VERSION-$ABI.zip"
    rm -f "$OUT_DIR/$ZIP_NAME"
    (cd "$STAGE_DIR" && zip -qr "$OUT_DIR/$ZIP_NAME" .)
    PACKAGES+=("$ZIP_NAME")
    rm -rf "$STAGE_DIR"
    STAGE_DIR=""
    echo "=> out/$ZIP_NAME"
done
(cd "$OUT_DIR" && sha256sum "${PACKAGES[@]}" > SHA256SUMS)
