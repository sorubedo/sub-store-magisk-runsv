# sub-store-runsv

[English](README.md) | [中文](README_zh-CN.md)

Run [Sub-Store](https://github.com/sub-store-org/Sub-Store) as an autostart runsv service on Magisk / KernelSU / APatch.

Includes the frontend, backend, Node.js LTS and runtime libraries, with frontend and backend merged by default. Only a no-mount package is provided, running as root. No http-meta, Termux installation or npm is required on the phone.

## Install

Requires Android 7.0 or later.

1. Install [runsvdir-magisk](https://github.com/sorubedo/runsvdir-magisk) first, then reboot.
2. Download the ZIP for your device from [Releases](https://github.com/sorubedo/sub-store-magisk-runsv/releases) and flash it. Most phones use `arm64-v8a`; `armeabi-v7a`, `x86_64` and `x86` are also available.

## Start

Nothing starts by itself on a fresh install. Tap the module **action** button (Volume Down to move, Volume Up to run) and select “启动并启用” (start + enable). Or use the shell:

```sh
SVC=/data/adb/runsvdir/service/sub-store

SVDIR=/data/adb/runsvdir/service sv-enable sub-store   # start + autostart
SVDIR=/data/adb/runsvdir/service sv-disable sub-store  # stop + no autostart
sv up "$SVC"        # start this time
sv down "$SVC"      # stop this time
sv restart "$SVC"  # restart the service
sv status "$SVC"   # status
tail -n 10 /data/adb/runsvdir/log/sv/sub-store/current
```

## Access and configuration

The frontend defaults to `http://127.0.0.1:3001`. Select “查看前后端访问地址” in the action menu and open the full link, or enter the displayed backend URL in the frontend settings.

Installation generates a random backend path, which is preserved on updates.

Edit `/data/adb/runsvdir/service/sub-store/conf`:

```sh
SUB_STORE_BACKEND_MERGE=true
SUB_STORE_BACKEND_API_HOST="127.0.0.1"
SUB_STORE_BACKEND_API_PORT=3001
SUB_STORE_CORS_ALLOWED_ORIGINS="*"
```

Restart the service after editing. For LAN access, set the host to `0.0.0.0` and use the phone's IP and port. To restrict cross-origin requests, replace `*` with a comma-separated list of allowed origins.

## Update

The manager can check for updates, or you can flash a newer package over the installed one. Node, libraries, frontend and backend update together; data and autostart settings are kept. Choose with the volume keys during installation:

- Volume Up: update programs only, preserving `run` / `conf` / `log/run`. This is the default after 30 seconds without input.
- Volume Down: full update, resetting service scripts and configuration while preserving data, the random backend path and autostart settings.

An already running service resumes after the update; no phone reboot is needed. The action menu shows component versions and lets you switch between stable and prerelease channels. The prerelease channel is available when upstream provides a prerelease.

## Uninstall

Uninstall removes the whole service folder, including the default `data` directory. Back it up first. Data configured outside the service folder is retained.

## FAQ

- **Installer says runsvdir-magisk is missing**: install runsvdir-magisk, reboot, then flash this module.
- **Service is not running**: view the latest 10 log lines in the action menu, then run `sv status /data/adb/runsvdir/service/sub-store`.
- **Frontend cannot connect to the backend**: start the service and enter the full backend URL from the action menu, including its random path, in the frontend settings.
- **Want another data folder**: edit `SUB_STORE_DATA_BASE_PATH` in `conf`, then restart. Set `WAIT_DECRYPT=1` if using shared storage.
