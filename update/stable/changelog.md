# Sub-Store 2.42.5-r3.ebec723efd14

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
90c1d0576e30d435cd59f0051177a5109635d406b9f31fb6fb153b112a73c18e  sub-store-runsv-2.42.5-r3.ebec723efd14-arm64-v8a.zip
b6f299661ff293ab574f3f7bc0b8693233b20dc9e75f86c1fca91348a0034f87  sub-store-runsv-2.42.5-r3.ebec723efd14-armeabi-v7a.zip
06c0b03bdcf33c2b47ce1f1982299294cd480656d6d8fa6af215ddbc7208d68d  sub-store-runsv-2.42.5-r3.ebec723efd14-x86_64.zip
5a03903101bb5ee748c1fe207286f925b3d4534933c784026d5b2cc9359f51da  sub-store-runsv-2.42.5-r3.ebec723efd14-x86.zip
```
