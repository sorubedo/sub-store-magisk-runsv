#!/system/bin/sh

SVDIR=/data/adb/runsvdir/service
SVC="$SVDIR/sub-store"

NODE_BIN="$SVC/runtime/bin/node"
APP_ROOT="$SVC/app"
NODE_LIBDIR="$SVC/runtime/lib"

# shellcheck disable=SC1091
[ -f "$SVC/conf" ] && . "$SVC/conf"

MODDIR="${0%/*}"
[ -d "$MODDIR" ] || MODDIR="/data/adb/modules/sub-store-runsv"
MODPROP="$MODDIR/module.prop"

PACKAGE_UPDATE_URL="$(sed -n 's/^updateJson=//p' "$MODPROP" | head -n 1)"
case "$PACKAGE_UPDATE_URL" in
    */update/*) DEFAULT_UPDATE_BASE="${PACKAGE_UPDATE_URL%/update/*}" ;;
    *) DEFAULT_UPDATE_BASE=https://raw.githubusercontent.com/sorubedo/sub-store-magisk-runsv/main ;;
esac
RAW_BASE="${SUB_STORE_UPDATE_BASE:-$DEFAULT_UPDATE_BASE}"

export SVDIR

say() { echo "$1"; }


read_update_fields() {
    path="$(sed -n 's/^updateJson=//p' "$MODPROP" | head -n 1)"
    [ -n "$path" ] || return 1
    rest="${path##*/update/}"
    [ "$rest" != "$path" ] || return 1
    ch="${rest%%/*}"
    abi="${rest#*/}"; abi="${abi%.json}"
    case "$ch" in stable|prerelease) ;; *) return 1 ;; esac
    case "$abi" in arm64-v8a|armeabi-v7a|x86_64|x86) ;; *) return 1 ;; esac
    echo "$ch|$abi"
}

current_channel() {
    ch="$(read_update_fields 2>/dev/null)"
    ch="${ch%%|*}"
    if [ -z "$ch" ] && [ -f "$MODDIR/build-info.prop" ]; then
        ch="$(sed -n 's|^moduleChannel=||p' "$MODDIR/build-info.prop" 2>/dev/null | head -n 1)"
    fi
    case "$ch" in
        stable | prerelease) echo "$ch" ;;
        *) echo "" ;;
    esac
}

current_abi() {
    f="$(read_update_fields 2>/dev/null)"
    abi="${f##*|}"
    if [ -z "$abi" ] && [ -f "$MODDIR/build-info.prop" ]; then
        abi="$(sed -n 's|^targetAbi=||p' "$MODDIR/build-info.prop" 2>/dev/null | head -n 1)"
    fi
    echo "$abi"
}

channel_label() {
    case "$1" in
        stable) echo "稳定版" ;;
        prerelease) echo "预发布版" ;;
        *) echo "未设置" ;;
    esac
}

set_channel() {
    new_ch="$1"
    if ! grep -q '^updateJson=' "$MODPROP"; then
        echo '! 此本地构建未配置在线更新，请使用已发布的安装包'
        return 1
    fi
    abi="$(current_abi)"
    if [ -z "$abi" ]; then
        return 1
    fi
    url="$RAW_BASE/update/$new_ch/$abi.json"
    tmp="$MODPROP.tmp"
    sed "s|^updateJson=.*|updateJson=$url|" "$MODPROP" > "$tmp"
    cat "$tmp" > "$MODPROP"
    rm -f "$tmp"
    return 0
}

GETEVENT=/system/bin/getevent
if [ ! -x "$GETEVENT" ]; then
    say "! 找不到 getevent，无法使用音量键菜单"
    exit 1
fi

if [ -x /system/bin/sv ]; then
    SV=/system/bin/sv
elif command -v sv >/dev/null 2>&1; then
    SV=sv
else
    say "! 找不到 sv，请先安装 runsvdir-magisk 并重启设备"
    exit 1
fi

if [ -x /system/bin/sv-enable ]; then
    SV_ENABLE=/system/bin/sv-enable
    SV_DISABLE=/system/bin/sv-disable
else
    SV_ENABLE=sv-enable
    SV_DISABLE=sv-disable
fi

if [ ! -d "$SVC" ]; then
    say "! 服务目录不存在: $SVC"
    say "  请重新刷入本模块"
    exit 1
fi

if command -v timeout >/dev/null 2>&1; then
    TIMEOUT="timeout 5"
else
    TIMEOUT=""
fi

read_key() {
    while :; do
        ev="$($TIMEOUT "$GETEVENT" -lqc 1 2>/dev/null)"
        case "$ev" in
            *KEY_VOLUMEUP*DOWN*) echo up; return 0 ;;
            *KEY_VOLUMEDOWN*DOWN*) echo down; return 0 ;;
        esac
    done
}

menu_count() {
    n=0
    old_ifs="$IFS"; IFS='
'
    for line in $MENU; do n=$((n + 1)); done
    IFS="$old_ifs"
    echo "$n"
}

menu_line() {
    want="$1"; n=0
    old_ifs="$IFS"; IFS='
'
    for line in $MENU; do
        n=$((n + 1))
        if [ "$n" -eq "$want" ]; then
            IFS="$old_ifs"
            echo "$line"
            return 0
        fi
    done
    IFS="$old_ifs"
    return 1
}

menu_render() {
    sel="$1"; n=0
    old_ifs="$IFS"; IFS='
'
    for line in $MENU; do
        n=$((n + 1))
        label="${line#*|}"
        if [ "$n" -eq "$sel" ]; then
            printf '  ==> %d) %s\n' "$n" "$label"
        else
            printf '      %d) %s\n' "$n" "$label"
        fi
    done
    IFS="$old_ifs"
}

build_menu() {
    ch="$(current_channel)"
    MENU="up|启动服务 (仅本次)
down|停止服务 (仅本次)
restart|重启服务
enable|启用开机自启 (删除 down)
disable|停用开机自启 (创建 down)
sv-enable|启动并启用
sv-disable|停止并停用
channel|切换更新渠道 (当前: $(channel_label "$ch"))
url|查看前后端访问地址
logs|查看最近 10 行日志
version|查看 Sub-Store / 前端 / Node LTS 版本
quit|结束"
    COUNT="$(menu_count)"
}

do_action() {
    case "$1" in
        up)         "$SV" up "$SVC" 2>&1 ;;
        down)       "$SV" down "$SVC" 2>&1 ;;
        restart)    "$SV" restart "$SVC" 2>&1 ;;
        enable)     rm -f "$SVC/down" && echo "已启用开机自启 (down 已删除)" ;;
        disable)    touch "$SVC/down" && echo "已停用开机自启 (down 已创建)" ;;
        sv-enable)  "$SV_ENABLE" sub-store 2>&1 && echo "已启动并启用" ;;
        sv-disable) "$SV_DISABLE" sub-store 2>&1 && echo "已停止并停用" ;;
        channel)
            cur="$(current_channel)"
            if [ "$cur" = "stable" ]; then
                new="prerelease"
            else
                new="stable"
            fi
            if set_channel "$new"; then
                echo "更新渠道已切换为: $(channel_label "$new")"
                echo "重新打开模块列表即可按新渠道检查更新"
            else
                echo "! 切换失败：请检查在线更新地址和架构"
            fi
            ;;
        url)
            host="${SUB_STORE_BACKEND_API_HOST:-127.0.0.1}"
            case "$host" in 0.0.0.0|::) host=127.0.0.1 ;; *:*) host="[$host]" ;; esac
            base="http://$host:${SUB_STORE_BACKEND_API_PORT:-3001}"
            echo "前端: $base"
            echo "后端: $base${SUB_STORE_FRONTEND_BACKEND_PATH%/}"
            echo "打开前端后，在后端设置中填入上面的后端地址。"
            echo "也可直接打开: $base?api=$base${SUB_STORE_FRONTEND_BACKEND_PATH%/}"
            ;;
        logs) tail -n 10 /data/adb/runsvdir/log/sv/sub-store/current 2>&1 ;;
        version)
            cat "$APP_ROOT/versions.json" 2>/dev/null || cat "$MODDIR/build-info.prop"
            if [ -x "$NODE_BIN" ]; then
                LD_LIBRARY_PATH="$NODE_LIBDIR" OPENSSL_CONF=/dev/null "$NODE_BIN" --version 2>&1
            else
                echo "! 找不到 Android Node LTS，请重新刷入模块"
            fi
            ;;

    esac
}

print_frame() {
    sel="$1"
    printf '\033[H\033[J'
    echo "=============================================="
    echo "            sub-store (runsv)"
    echo "=============================================="
    echo "服务目录: $SVC"
    echo "Node LTS: ${NODE_BIN:-未找到}"
    echo ""
    echo "当前状态:"
    "$SV" status "$SVC" 2>&1 | while IFS= read -r l; do echo "  $l"; done
    echo ""
    menu_render "$sel"
    echo ""
    echo "【音量下 = 切换选项】  【音量上 = 执行选中项】"
    echo ""
    if [ -n "$RESULT" ]; then
        echo "上次操作: $RESULT_TITLE"
        printf '%s\n' "$RESULT" | while IFS= read -r l; do echo "  $l"; done
        echo ""
    fi
}

sel=1
RESULT=""
RESULT_TITLE=""

while :; do
    build_menu
    [ "$sel" -gt "$COUNT" ] && sel=1

    print_frame "$sel"

    key="$(read_key)"
    if [ "$key" = "down" ]; then
        sel=$((sel % COUNT + 1))
        continue
    fi

    line="$(menu_line "$sel")"
    name="${line%%|*}"
    label="${line#*|}"

    if [ "$name" = "quit" ]; then
        sleep 0.3
        break
    fi

    out="$(do_action "$name")"
    [ -n "$out" ] || out="完成"
    RESULT="$out"
    RESULT_TITLE="$label"
done

printf '\033[H\033[J'
say "已退出 sub-store (runsv) 操作菜单"
