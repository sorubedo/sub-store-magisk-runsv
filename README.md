# sub-store-runsv

[English](README.md) | [中文](README_zh-CN.md)

[Sub-Store](https://github.com/sub-store-org/Sub-Store) for Magisk, KernelSU and APatch, supervised by [runsvdir-magisk](https://github.com/sorubedo/runsvdir-magisk). Follows the service, installer, volume-key menu and per-ABI packaging conventions of openlist-magisk-runsv and sing-box-magisk-runsv.

Ships the official frontend, `sub-store.bundle.js`, Android **Termux `nodejs-lts`**, its shared libraries and CA certificates. Frontend and backend share `127.0.0.1:3001` with `SUB_STORE_BACKEND_MERGE=true`. No http-meta, Termux installation or npm is required on the device.

## Install

Requires Android 7.0 / API 24+, Magisk 20.4+ or compatible KernelSU/APatch module installation support. Only a no-mount package is provided: all programs and libraries live in the service folder and run as root.

1. Install runsvdir-magisk and reboot first.
2. Flash the ZIP matching your ABI. Most phones use `arm64-v8a`. Once runsvdir-magisk is active, this module can start immediately without another reboot.
3. Open the module action menu: Volume Down selects, Volume Up executes. Choose “启动并启用” to start and enable the service. Fresh installs carry a `down` marker.
4. Select “查看前后端访问地址” to see the complete URL. A random backend path is generated during installation and preserved on updates. Alternatively open `http://127.0.0.1:3001` and enter the backend URL in frontend settings.

ABIs: `arm64-v8a`, `armeabi-v7a`, `x86_64`, `x86`. Each ZIP contains one ABI. Module ID: `sub-store-runsv`; service name: `sub-store`.

## Node runtime and dependencies

Everything lives under `/data/adb/runsvdir/service/sub-store`:

| Path | Content |
| --- | --- |
| `runtime/bin/node` | Android/Bionic Node.js LTS |
| `runtime/lib` | ICU, OpenSSL, SQLite, c-ares, C++, zlib shared libraries |
| `runtime/share` | CA roots, licenses, package versions/checksums |
| `app/sub-store.bundle.js` | Official backend including its npm dependencies |
| `app/frontend` | Official frontend |
| `app/versions.json` | Module/backend/frontend/Node versions |
| `data` | Default persistent user data |
| `conf` | User configuration |

The build resolves Termux package dependencies, checks deb SHA-256 values, and recursively copies the ELF `DT_NEEDED` library closure. Android supplies the system Bionic libraries. Node's RUNPATH is relocated to `$ORIGIN/../lib`, and each bundled library uses `$ORIGIN`. The launcher sets `LD_LIBRARY_PATH` and CA paths only for the service process. Termux, npm and a separate Node module are not required on the phone.

Runtime dependencies remain bundled with Node. Updates stop the service and replace `runtime` and `app` as complete directories, removing obsolete libraries/assets. Failed replacements restore the previous payload and leave the service stopped.

## Configuration and control

Edit `/data/adb/runsvdir/service/sub-store/conf`, then restart. It is privileged shell configuration; every variable is exported to Node. Settings include `SUB_STORE_BACKEND_API_HOST`, `SUB_STORE_BACKEND_API_PORT`, `SUB_STORE_FRONTEND_BACKEND_PATH`, `SUB_STORE_DATA_BASE_PATH` and `WAIT_DECRYPT`. Additional upstream environment variables can be added. Node, library, CA and frontend paths are configured by the run script.

`SUB_STORE_CORS_ALLOWED_ORIGINS="*"` allows local and external frontend origins. To restrict origins, use a comma-separated list such as `http://127.0.0.1:3001,https://sub-store.vercel.app`.

For LAN access, set the host to `0.0.0.0`, retain the random backend path, and use the phone's IP/port/path in the frontend settings on other devices.

```sh
SVC=/data/adb/runsvdir/service/sub-store
SVDIR=/data/adb/runsvdir/service sv-enable sub-store
SVDIR=/data/adb/runsvdir/service sv-disable sub-store
sv up "$SVC"
sv down "$SVC"
sv restart "$SVC"
sv status "$SVC"
tail -f /data/adb/runsvdir/log/sv/sub-store/current
```

The action menu also shows recent logs and component versions. Services are independently registered with runsvdir; use `sv-disable` to stop and disable them, as in the reference modules.

## Update and uninstall

On updates, Volume Up refreshes Node, libraries, certificates, frontend and backend while preserving service scripts/configuration. This is the default after 30 seconds or when input is unavailable. Volume Down performs a full script/configuration update, preserving the backend path, user data and autostart marker. Back up customized configuration before a full update.

Published builds support per-channel, per-ABI manager updates. The menu can switch stable/prerelease; a prerelease update source is generated only when upstream has a prerelease. Local builds omit `updateJson` until published.

Uninstall stops the service and deletes its entire service directory, **including the default data folder**. Export a backup first. Any configured external data directory and logs are retained.

## Build and release

Linux tools: Bash, Python 3.10+, curl, dpkg-deb, patchelf and zip. Tests use host Node 24 LTS. Publishing additionally requires `gh`. Termux packages are checked against their index SHA-256; only the Android ELF dependency closure is included and its RUNPATH is relocated.

```sh
bash fetch.sh stable          # or auto, prerelease, an exact backend tag
# FRONTEND_TAG=2.34.1 bash fetch.sh 2.42.5
bash package.sh               # 4 ZIPs: one per ABI
bash package.sh arm64-v8a     # one ABI
python3 -m unittest discover -s tests -v
DRY_RUN=true bash release-channel.sh stable
```

`out/` contains ZIPs, SHA256SUMS, upstream-versions.env and resolved.json with every package version/checksum. Generated `bin/`, `assets/` and `out/` are ignored by Git.

## Update identity and version numbers

Backend, frontend and Node are checked independently at build time and shipped together. A changed backend/frontend release asset, Node package, runtime dependency checksum, CA bundle or module revision produces a new module release. Unchanged inputs with complete artifacts/metadata are skipped.

`version` looks like `2.42.5-r3.<12-character fingerprint>`: backend version, module revision, and a fingerprint covering all component identities. Frontend-only and Node-only updates retain the backend version and change the fingerprint. `versionCode` counts UTC build seconds since 2020-01-01 and is guaranteed to exceed previously recorded local/released codes, including same-second rebuilds or clock rollback. Managers compare this integer, not the fingerprint's lexical order. Component versions remain individually visible in build-info.prop, app/versions.json, release notes and the action menu. The GitHub tag is `v` plus `version`.

The phone updates the whole module through its manager. It stops and replaces Node/libraries/certificates/frontend/backend together, preserves user data/autostart state, and resumes an already running service. There are no independent device-side component updaters. Backend channel selection keeps Node on LTS and frontend on stable releases.

Increment `REVISION` in `scripts/upstream.py` for module changes. To rebuild only module scripts using the previously fetched components, run `python3 scripts/upstream.py metadata --resolved out/resolved.json`; it verifies local component identities and refreshes metadata without downloads.

GitHub Actions provides manual artifact builds and daily release detection. Releases are validated before publishing; update JSON files are committed afterwards. Missing upstream prereleases are skipped, and all four packages must exist for a release to count as complete. For forks, set `REPO_SLUG`; Actions supplies the current repository automatically. Override `RAW_BASE` for branches other than `main`, and `SUB_STORE_UPDATE_BASE` in device configuration for the action menu.

Tests cover installation/update behavior, data/configuration/path preservation, complete payload replacement/rollback, component update detection and version ordering, all Android ELF dependencies, ZIP layouts, and real merged frontend/backend HTTP requests with API persistence. Host JavaScript tests do not replace Android device compatibility tests.

## License

Packaging/scripts: [MIT](LICENSE). Sub-Store/frontend retain their upstream licenses, included in the payload. Node and its dependencies include their copyright notices and common licenses under runtime `share/`. Sources: [backend](https://github.com/sub-store-org/Sub-Store), [frontend](https://github.com/sub-store-org/Sub-Store-Front-End), [Termux Node LTS recipe](https://github.com/termux/termux-packages/tree/master/packages/nodejs-lts).
