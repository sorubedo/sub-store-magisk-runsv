# Sub-Store 2.44.2-r3.21c4c1531193

- Backend: 2.44.2
- Frontend: 2.34.2
- Android Node.js LTS: 24.22.2 (Termux nodejs-lts)
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
869858c1bdb59838d437e9d2b54370fcd41125fedfb4b584d566a0af41d676f1  sub-store-runsv-2.44.2-r3.21c4c1531193-arm64-v8a.zip
e2abe0c7d610c1066fdca071e2db1d7645a6c15fb3aa653b9578539bbaa488f5  sub-store-runsv-2.44.2-r3.21c4c1531193-armeabi-v7a.zip
fc603ad0088ae6fb0106f954f1186041663fabda2e4373cde608fb07307ca5cf  sub-store-runsv-2.44.2-r3.21c4c1531193-x86_64.zip
fce4a2c86e7713490607ee61e8abd5a2082d73fec0c40bdf8d31e13001339473  sub-store-runsv-2.44.2-r3.21c4c1531193-x86.zip
```
