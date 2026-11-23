# Sub-Store 2.44.26-r3.b36c9c936186

- Backend: 2.44.26
- Frontend: 2.34.3
- Android Node.js LTS: 24.22.3 (Termux nodejs-lts)
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
70bffff659514b0e5174dfb86f25f1d1614fe20c5b6bc67c0d3c08d1422c802f  sub-store-runsv-2.44.26-r3.b36c9c936186-arm64-v8a.zip
094eb74f7300f6aae5aedbd1fa3a222f7e41a9b9a41fb1bd0188cd2209f62d6e  sub-store-runsv-2.44.26-r3.b36c9c936186-armeabi-v7a.zip
6ae5f4c0c9bbd878a94d91986aad432b8dde07a26091be7eeb8757ddf9d4c5eb  sub-store-runsv-2.44.26-r3.b36c9c936186-x86_64.zip
bccbbc24cbf95981ddbc4f8621feadd482f00b03dc6a8737a52963b6554ae603  sub-store-runsv-2.44.26-r3.b36c9c936186-x86.zip
```
