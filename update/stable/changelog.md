# Sub-Store 2.44.28-r3.8a7ba56b15a3

- Backend: 2.44.28
- Frontend: 2.34.4
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
4052fcb98dd9e565a3b122510d33bba63fd7db9e4c0353573b46e01986a2e341  sub-store-runsv-2.44.28-r3.8a7ba56b15a3-arm64-v8a.zip
c545c940a9950aef45e26d60f842ac2825e1a2d1d79b387a72591aead2f32908  sub-store-runsv-2.44.28-r3.8a7ba56b15a3-armeabi-v7a.zip
8997be5cc9192aad4714d1ce928c79ab238db814e2921df7650e1c4336c75a14  sub-store-runsv-2.44.28-r3.8a7ba56b15a3-x86_64.zip
9118d712a3834c5c554a24593ff771b6eeadb9a1f3d1bb69aca5294e9666817a  sub-store-runsv-2.44.28-r3.8a7ba56b15a3-x86.zip
```
