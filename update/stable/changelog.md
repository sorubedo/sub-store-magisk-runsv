# Sub-Store 2.44.31-r3.79b7dcb46dc3

- Backend: 2.44.31
- Frontend: 2.34.5
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
e41e2cf095ab03895437ae8fe856ea9ba82c953335e0b2569487a92a851b5f34  sub-store-runsv-2.44.31-r3.79b7dcb46dc3-arm64-v8a.zip
0d107f367e510d3bbccb405e8d075f3710ba77688484fdaaac3562ff07a60326  sub-store-runsv-2.44.31-r3.79b7dcb46dc3-armeabi-v7a.zip
f63e8b66497073c10d2234b9f7882d85ea926d775a60262fda65564c2aad77ca  sub-store-runsv-2.44.31-r3.79b7dcb46dc3-x86_64.zip
01614cc7260644cc9674bf33e02faa9b6fd8e02712bc43b86adaa2b28ab2a827  sub-store-runsv-2.44.31-r3.79b7dcb46dc3-x86.zip
```
