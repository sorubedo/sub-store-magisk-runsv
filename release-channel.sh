#!/bin/bash
set -euo pipefail
CHANNEL="${1:?Usage: release-channel.sh <stable|prerelease>}"
case "$CHANNEL" in stable|prerelease) ;; *) echo 'Invalid channel' >&2; exit 1 ;; esac
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"
export REPO_SLUG="${REPO_SLUG:-sorubedo/sub-store-magisk-runsv}"
if [ -n "${RESOLVED_FILE:-}" ]; then
    bash fetch.sh "$CHANNEL" --resolved "$RESOLVED_FILE"
else
    bash fetch.sh "$CHANNEL"
fi
# shellcheck disable=SC1091
. out/upstream-versions.env
[ "$MODULE_CHANNEL" = "$CHANNEL" ]
rm -f out/*.zip out/SHA256SUMS
PUBLISH_UPDATES=true bash package.sh
python3 -m unittest discover -s tests -v
ASSETS=()
for abi in arm64-v8a armeabi-v7a x86_64 x86; do
    ASSETS+=("out/sub-store-runsv-$MODULE_VERSION-$abi.zip")
done
ASSETS+=(out/SHA256SUMS out/upstream-versions.env out/resolved.json)
for asset in "${ASSETS[@]}"; do [ -f "$asset" ]; done
{
    echo "# Sub-Store $MODULE_VERSION"
    echo
    echo "- Backend: $SUB_STORE_TAG"
    echo "- Frontend: $FRONTEND_TAG"
    echo "- Android Node.js LTS: $NODE_PACKAGE_VERSION (Termux nodejs-lts)"
    echo "- Channel: $MODULE_CHANNEL"
    echo
    echo 'Requires runsvdir-magisk installed and rebooted first. Android 7.0+.'
    echo 'Merged frontend/backend, localhost port 3001, random backend path. No http-meta.'
    echo 'First install is down; use the action menu to view the URL and enable the service.'
    echo
    echo 'All programs and shared libraries live in /data/adb/runsvdir/service/sub-store.'
    echo 'Runs as root; default data is service/data. A running service restarts after update.'
    echo 'Node and libraries are replaced as a complete set; removed libraries are cleaned up.'
    echo 'Each ZIP contains one ABI: arm64-v8a, armeabi-v7a, x86_64 or x86.'
    echo 'The release ID covers backend, frontend, Node, dependency checksums and module revision.'
    echo
    echo '```text'
    cat out/SHA256SUMS
    echo '```'
} > out/release-notes.md
if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then cat out/release-notes.md >> "$GITHUB_STEP_SUMMARY"; fi
if [ "${DRY_RUN:-false}" = true ]; then
    echo "DRY_RUN: prepared $RELEASE_TAG (no GitHub writes)"
else
    FLAGS=(--prerelease=false)
    [ "$CHANNEL" != prerelease ] || FLAGS=(--prerelease)
    if gh release view "$RELEASE_TAG" --repo "$REPO_SLUG" >/dev/null 2>&1; then
        gh release upload "$RELEASE_TAG" --repo "$REPO_SLUG" "${ASSETS[@]}" --clobber
        gh release edit "$RELEASE_TAG" --repo "$REPO_SLUG" --title "Sub-Store $MODULE_VERSION" \
            --notes-file out/release-notes.md "${FLAGS[@]}"
    else
        gh release create "$RELEASE_TAG" --repo "$REPO_SLUG" --title "Sub-Store $MODULE_VERSION" \
            --notes-file out/release-notes.md "${FLAGS[@]}" "${ASSETS[@]}"
    fi
fi
bash publish-update.sh
