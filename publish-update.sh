#!/bin/bash
set -euo pipefail
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"
set -a
# shellcheck disable=SC1091
. out/upstream-versions.env
REPO_SLUG="${REPO_SLUG:-sorubedo/sub-store-magisk-runsv}"
RAW_BASE="${RAW_BASE:-https://raw.githubusercontent.com/$REPO_SLUG/main}"
set +a
python3 - <<'PY'
import json, os
from pathlib import Path
env = os.environ
channel = env['MODULE_CHANNEL']
assert channel in ('stable', 'prerelease')
directory = Path('update') / channel
directory.mkdir(parents=True, exist_ok=True)
notes = Path('out/release-notes.md')
(directory / 'changelog.md').write_text(notes.read_text() if notes.exists() else f"Sub-Store {env['MODULE_VERSION']}\n")
for abi in ('arm64-v8a', 'armeabi-v7a', 'x86_64', 'x86'):
    name = f"sub-store-runsv-{env['MODULE_VERSION']}-{abi}.zip"
    if not (Path('out') / name).is_file():
        raise SystemExit(f'Missing release artifact: {name}')
    target = directory / f'{abi}.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(dict(
        version=env['MODULE_VERSION'], versionCode=int(env['MODULE_VERSION_CODE']),
        zipUrl=f"https://github.com/{env['REPO_SLUG']}/releases/download/{env['RELEASE_TAG']}/{name}",
        changelog=f"{env['RAW_BASE']}/update/{channel}/changelog.md"
    ), indent=2) + '\n')
PY
