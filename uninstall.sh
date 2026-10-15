#!/system/bin/sh
SVC=/data/adb/runsvdir/service/sub-store
if command -v sv >/dev/null 2>&1 && [ -d "$SVC" ]; then
    touch "$SVC/down"
    sv -w 15 down "$SVC" 2>/dev/null
    sv exit "$SVC" 2>/dev/null
fi
rm -rf "$SVC"
