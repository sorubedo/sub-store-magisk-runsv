#!/system/bin/sh
# shellcheck disable=SC3043,SC2034
SVDIR=/data/adb/runsvdir/service
SVC="$SVDIR/sub-store"
DEP_URL=https://github.com/sorubedo/runsvdir-magisk
SKIPMOUNT=true

prop() { sed -n "s/^$1=//p" "$MODPATH/build-info.prop" | head -n 1; }
runsvdir_module_ok() {
    local root
    for root in /data/adb/modules /data/adb/lite_modules; do
        if [ -d "$root/runsvdir" ] && [ ! -e "$root/runsvdir/remove" ] && [ ! -e "$root/runsvdir/disable" ]; then
            return 0
        fi
    done
    return 1
}

ui_print '=============================================='
ui_print '              Sub-Store (runsv)'
ui_print '=============================================='
runsvdir_module_ok && [ -d "$SVDIR" ] || {
    ui_print '! 缺少依赖 runsvdir-magisk，或依赖未启用'
    ui_print "  请先安装并重启: $DEP_URL"
    abort '! Installation aborted: runsvdir-magisk is missing or inactive'
}
case "$ARCH" in
    arm64) ABI=arm64-v8a ;; arm) ABI=armeabi-v7a ;;
    x64) ABI=x86_64 ;; x86) ABI=x86 ;;
    *) abort "! Unsupported architecture: $ARCH" ;;
esac
TARGET_ABI="$(prop targetAbi)"
[ "$TARGET_ABI" = "$ABI" ] || abort "! Wrong ABI: package=$TARGET_ABI, device=$ABI"
DEVICE_API="${API:-$(getprop ro.build.version.sdk)}"
case "$DEVICE_API" in ''|*[!0-9]*) abort '! Cannot determine Android API level' ;; esac
[ "$DEVICE_API" -ge 24 ] || abort '! Android 7.0 / API 24 or newer is required'
PAYLOAD="$MODPATH/service/sub-store/app"
NODE_SRC="$MODPATH/service/sub-store/runtime/bin/node"
[ -f "$NODE_SRC" ] && [ -f "$PAYLOAD/sub-store.bundle.js" ] && [ -f "$PAYLOAD/frontend/index.html" ] \
    || abort '! Incomplete Node/Sub-Store package'
ui_print "- 架构: $ABI / Node 和依赖均安装到服务目录"
ui_print "- Sub-Store: $(prop backendVersion) / 前端: $(prop frontendVersion)"
ui_print "- Android Node.js LTS: $(prop nodeVersion)"

UPDATE=0
[ ! -d "$SVC" ] || UPDATE=1
UPDATE_MODE=payload
GETEVENT=/system/bin/getevent
[ -x "$GETEVENT" ] || GETEVENT="$(command -v getevent 2>/dev/null)"
choose_update_mode() {
    if [ -z "$GETEVENT" ] || ! command -v timeout >/dev/null 2>&1; then
        ui_print '- 无音量键输入，默认仅更新 Node / 前端 / 后端'; return 0;
    fi
    ui_print '  音量上: 仅更新 Node / 前端 / 后端，保留 run / conf / log/run'
    ui_print '  音量下: 完整更新（重置服务脚本和配置，保留数据及访问路径）'
    ui_print '  30 秒无操作则默认仅更新程序'
    local i=0 ev
    while [ "$i" -lt 6 ]; do
        ev="$(timeout 5 "$GETEVENT" -lqc 1 2>/dev/null)"
        case "$ev" in
            *KEY_VOLUMEUP*DOWN*) return 0 ;;
            *KEY_VOLUMEDOWN*DOWN*) UPDATE_MODE=full; return 0 ;;
        esac
        i=$((i + 1))
    done
}
if [ "$UPDATE" -eq 1 ]; then
    choose_update_mode
fi
OLD_BACKEND_PATH=""
if [ -f "$SVC/conf" ]; then
    # shellcheck disable=SC1091
    OLD_BACKEND_PATH="$(. "$SVC/conf"; printf '%s' "$SUB_STORE_FRONTEND_BACKEND_PATH")"
fi
case "$OLD_BACKEND_PATH" in
    /*) BACKEND_PATH="$OLD_BACKEND_PATH" ;;
    *)
        NONCE="$(od -An -N16 -tx1 /dev/urandom | tr -d ' \n')"
        [ "${#NONCE}" -eq 32 ] || abort '! Cannot generate backend path'
        BACKEND_PATH="/$NONCE"
        ;;
esac
CONF_SRC="$MODPATH/service/sub-store/conf"
CONF_TMP="$MODPATH/conf.new"
while IFS= read -r line; do
    case "$line" in
        SUB_STORE_FRONTEND_BACKEND_PATH=*)
            escaped="$(printf '%s' "$BACKEND_PATH" | sed "s/'/'\\\\''/g")"
            printf "SUB_STORE_FRONTEND_BACKEND_PATH='%s'\n" "$escaped" ;;
        *) printf '%s\n' "$line" ;;
    esac
done < "$CONF_SRC" > "$CONF_TMP"
mv -f "$CONF_TMP" "$CONF_SRC" || abort '! Cannot prepare service configuration'

STAGE="$(mktemp -d /data/adb/runsvdir/.sub-store-install.XXXXXX)" || abort '! Cannot stage service'
mkdir -p "$STAGE/service" "$STAGE/payload" "$STAGE/previous" || {
    rm -rf "$STAGE"; abort '! Cannot stage service directories';
}
if [ "$UPDATE" -eq 0 ] || [ "$UPDATE_MODE" = full ]; then
    if ! cp -af "$MODPATH/service/sub-store/." "$STAGE/service/" \
        || ! mv "$STAGE/service/runtime" "$STAGE/service/app" "$STAGE/payload/"; then
        rm -rf "$STAGE"; abort '! Cannot stage service files'
    fi
else
    cp -a "$MODPATH/service/sub-store/runtime" "$MODPATH/service/sub-store/app" "$STAGE/payload/" \
        || { rm -rf "$STAGE"; abort '! Cannot stage payload'; }
fi
if ! find "$STAGE/payload" -type d -exec chmod 0755 {} + \
    || ! find "$STAGE/payload" -type f -exec chmod 0644 {} + \
    || ! chmod 0755 "$STAGE/payload/runtime/bin/node" \
    || ! chown -R 0:0 "$STAGE/payload" \
    || [ ! -x "$STAGE/payload/runtime/bin/node" ]; then
    rm -rf "$STAGE"; abort '! Cannot prepare Node/Sub-Store permissions'
fi
HAD_DOWN=0
[ ! -e "$SVC/down" ] || HAD_DOWN=1
if [ "$UPDATE" -eq 1 ]; then rm -f "$STAGE/service/down"; fi
chmod 0755 "$STAGE/service/run" "$STAGE/service/finish" "$STAGE/service/log/run" 2>/dev/null
chmod 0600 "$STAGE/service/conf" 2>/dev/null

SV="$(command -v sv 2>/dev/null)"
WAS_RUNNING=0
if [ "$UPDATE" -eq 1 ]; then
    [ -n "$SV" ] || { rm -rf "$STAGE"; abort '! sv not found; reboot after installing runsvdir-magisk'; }
    if SERVICE_STATUS="$("$SV" status "$SVC" 2>/dev/null)"; then
        case "$SERVICE_STATUS" in run:*) WAS_RUNNING=1 ;; esac
        "$SV" -w 15 down "$SVC" || { rm -rf "$STAGE"; abort '! Could not stop running service'; }
    fi
fi
mkdir -p "$SVC" || { rm -rf "$STAGE"; abort '! Cannot create service directory'; }
touch "$SVC/down"
overlay_copy() {
    local src="$1" dst="$2" entry name temp
    mkdir -p "$dst" || return 1
    for entry in "$src"/* "$src"/.[!.]* "$src"/..?*; do
        [ -e "$entry" ] || continue
        name="${entry##*/}"
        if [ -d "$entry" ]; then
            overlay_copy "$entry" "$dst/$name" || return 1
        else
            temp="$dst/.$name.install"
            cp -pf "$entry" "$temp" && mv -f "$temp" "$dst/$name" || return 1
        fi
    done
}
restore_payload() {
    local part failed=0
    for part in $REPLACED_PARTS; do
        rm -rf "${SVC:?}/${part:?}" || failed=1
        if [ -e "$STAGE/previous/$part" ]; then
            mv "$STAGE/previous/$part" "$SVC/$part" || failed=1
        fi
    done
    return "$failed"
}
replace_payload() {
    local part
    for part in runtime app; do
        if [ -e "$SVC/$part" ]; then
            mv "$SVC/$part" "$STAGE/previous/$part" || return 1
        fi
        REPLACED_PARTS="$REPLACED_PARTS $part"
        mv "$STAGE/payload/$part" "$SVC/$part" || return 1
    done
}
REPLACED_PARTS=""
if ! replace_payload || ! overlay_copy "$STAGE/service" "$SVC"; then
    if restore_payload; then
        rm -rf "$STAGE"
        abort '! Update failed; previous payload restored and service left down. Reflash to repair.'
    fi
    abort "! Update failed; service left down. Recovery files retained at $STAGE/previous"
fi
rm -rf "$STAGE"
chmod 0755 "$SVC/run" "$SVC/finish" "$SVC/log/run"
chmod 0600 "$SVC/conf"
chown 0:0 "$SVC/run" "$SVC/conf" "$SVC/finish" "$SVC/log/run"
if [ "$UPDATE" -eq 1 ] && [ "$HAD_DOWN" -eq 0 ]; then rm -f "$SVC/down"; fi
if [ "$WAS_RUNNING" -eq 1 ]; then
    "$SV" up "$SVC" || ui_print '! 程序已更新，请手动启动服务'
fi
rm -rf "$MODPATH/service"

ui_print '- 安装完成：默认前后端合并，监听 127.0.0.1:3001'
ui_print "- 服务配置: $SVC/conf"
ui_print '- 首次访问请在模块操作菜单中查看访问地址（含随机后端路径）'
if [ "$UPDATE" -eq 0 ]; then ui_print '- 首次安装已停用，请在操作菜单选择「启动并启用」'; fi
ui_print "- 启动并启用: SVDIR=$SVDIR sv-enable sub-store"
ui_print '- 日志: /data/adb/runsvdir/log/sv/sub-store/current'
