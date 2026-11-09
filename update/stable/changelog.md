# Sub-Store 2.44.6-r3.ec4846f99834

- Backend: 2.44.6
- Frontend: 2.34.2
- Android Node.js LTS: 24.22.2-1 (Termux nodejs-lts)
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
6e3c460f3625657d2dbe0c0fb39a48f44ebc093827af47a5d83ae97609122cbc  sub-store-runsv-2.44.6-r3.ec4846f99834-arm64-v8a.zip
b82f91ee1d86b4782c30461139213ff18623cc37cfde3429746684660d016c74  sub-store-runsv-2.44.6-r3.ec4846f99834-armeabi-v7a.zip
b4dd405cecd07563ec27b7b6fb6a1dd659794c2c93d71f5a7bd092b8a0fddbeb  sub-store-runsv-2.44.6-r3.ec4846f99834-x86_64.zip
e8734a71c4896c0b83d713a9af3fbeadab900a986d90b5c21045b2b9f43915fe  sub-store-runsv-2.44.6-r3.ec4846f99834-x86.zip
```
