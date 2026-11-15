# Sub-Store 2.44.14-r3.8294c361aae7

- Backend: 2.44.14
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
3abfcf0bfd571016b4be089bd992eb2d307c4c969bb869c1416db83b5c354cee  sub-store-runsv-2.44.14-r3.8294c361aae7-arm64-v8a.zip
9074b742e25e7d73b934aee2a6228c85a0945a78bff2bc1e80f4623c554f8e3b  sub-store-runsv-2.44.14-r3.8294c361aae7-armeabi-v7a.zip
d41607fcdd40f8f9f0cbe1851b165b50e1236e9849a0d362f9a999ddcc6464e8  sub-store-runsv-2.44.14-r3.8294c361aae7-x86_64.zip
e0112f53c029c5d8018ba6e3062d28a4f8130bb8dfaa8f9daebb5ec085baca02  sub-store-runsv-2.44.14-r3.8294c361aae7-x86.zip
```
