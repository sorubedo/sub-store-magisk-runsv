# Sub-Store 2.44.16-r3.c2449dee31af

- Backend: 2.44.16
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
48909e6784e0899ce759e166af500f8e0f4a4d5c55e9f174bf7ef6e4d485b795  sub-store-runsv-2.44.16-r3.c2449dee31af-arm64-v8a.zip
ea6b2377246f2d6d9dd9f9387181cded40fe3a1ec5bf7a112e81ef5c64529ec7  sub-store-runsv-2.44.16-r3.c2449dee31af-armeabi-v7a.zip
c959ef3baf6a718c01d876319b781633223511574f6f89fb1e9800b73cb68b56  sub-store-runsv-2.44.16-r3.c2449dee31af-x86_64.zip
db9755986eced279634ff57f136e50285b12095a3f77ce1e9dc75c4faa7c62fc  sub-store-runsv-2.44.16-r3.c2449dee31af-x86.zip
```
