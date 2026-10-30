# Sub-Store 2.44.2-r3.34a756ec5627

- Backend: 2.44.2
- Frontend: 2.34.2
- Android Node.js LTS: 24.22.1 (Termux nodejs-lts)
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
dee4334f161a1f1d05a52638566e436446f5750f7357e3a945e2a4d280b4f4a2  sub-store-runsv-2.44.2-r3.34a756ec5627-arm64-v8a.zip
fef1e363713798e2d1d121f98b62d9771e70800b59c58d2bfec1aa281faae2d5  sub-store-runsv-2.44.2-r3.34a756ec5627-armeabi-v7a.zip
abfb816175c32667923de78585ed0e19282255806deb8c16d577f2984eb648d2  sub-store-runsv-2.44.2-r3.34a756ec5627-x86_64.zip
d7e580ce7b0e8c46c7bda82fdc673655e1374e5acfb79472c66cc9f8bd2c55fd  sub-store-runsv-2.44.2-r3.34a756ec5627-x86.zip
```
