# Sub-Store 2.44.7-r3.ba14ab76d667

- Backend: 2.44.7
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
9d9537d09550e7dc22f58c9161d334712999fe0e7a708967243a14bfddc6b7fa  sub-store-runsv-2.44.7-r3.ba14ab76d667-arm64-v8a.zip
0dd3d47133644d153579b278262bd22ce9299e88b7eeb907e62805f0ca25ea83  sub-store-runsv-2.44.7-r3.ba14ab76d667-armeabi-v7a.zip
4b245db83084bfefd3d9cc8f82dbc3415f031dc9c83ec259573af907dbf600a3  sub-store-runsv-2.44.7-r3.ba14ab76d667-x86_64.zip
99c8290fcc8e56707a62ca46136ab03a3c01d835453628eeb523928c74702c29  sub-store-runsv-2.44.7-r3.ba14ab76d667-x86.zip
```
