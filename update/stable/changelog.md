# Sub-Store 2.42.5-r3.e514069d53a6

- Backend: 2.42.5
- Frontend: 2.34.1
- Android Node.js LTS: 24.18.0-1 (Termux nodejs-lts)
- Channel: stable

Requires runsvdir-magisk installed and rebooted first. Android 7.0+.
Merged frontend/backend, localhost port 3001, random backend path. No http-meta.
First install is down; use the action menu to view the URL and enable the service.

All programs and shared libraries live in /data/adb/runsvdir/service/sub-store.
Runs as root; default data is service/data. A running service restarts after update.
Node and libraries are replaced as a complete set; removed libraries are cleaned up.
Each ZIP contains one ABI: arm64-v8a, armeabi-v7a, x86_64 or x86.
The release ID covers backend, frontend, Node, dependency checksums and module revision.

```text
95169b581e58b55ae0f598859fe54b9808ae228db0414b80b3da933239000063  sub-store-runsv-2.42.5-r3.e514069d53a6-arm64-v8a.zip
39f9faf43c786203bfc36ee255fbfecfebaf139333d592b76e371cbd5ef07ce1  sub-store-runsv-2.42.5-r3.e514069d53a6-armeabi-v7a.zip
c3fbfd2b03908c744aafc80f1ab60280d25b58555d6cdc2953c56c8fd3c0e009  sub-store-runsv-2.42.5-r3.e514069d53a6-x86_64.zip
7a5f8b969119659148cf094221684124804887f32ad464537749f5edc5122f9c  sub-store-runsv-2.42.5-r3.e514069d53a6-x86.zip
```
