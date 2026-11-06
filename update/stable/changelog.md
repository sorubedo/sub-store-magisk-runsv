# Sub-Store 2.44.5-r3.83bf792fe8f5

- Backend: 2.44.5
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
9e6b1ad5eef657b53f9a980ec5ce801e8e20df8fbd5ce256a71012cb3bfd7736  sub-store-runsv-2.44.5-r3.83bf792fe8f5-arm64-v8a.zip
f4767755a618ee186dc70f057e4404d9cb5a45f2f2c86b826781c1bda597169d  sub-store-runsv-2.44.5-r3.83bf792fe8f5-armeabi-v7a.zip
f4adedd3a95f60ac37911fdbc806d80e6d28852864f04f14a5e15bad246a362b  sub-store-runsv-2.44.5-r3.83bf792fe8f5-x86_64.zip
6b15a7255880103f95a51a202b334e3bfb41599b8e0ecc580a56c8d7afe94fde  sub-store-runsv-2.44.5-r3.83bf792fe8f5-x86.zip
```
