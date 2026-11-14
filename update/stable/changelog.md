# Sub-Store 2.44.12-r3.95f12c5938a2

- Backend: 2.44.12
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
5d5772195d58f0f0134595cc3e4c939da063e9d5ab38bd8fb03fb978ad986695  sub-store-runsv-2.44.12-r3.95f12c5938a2-arm64-v8a.zip
4a277430f3c1cfb79a19c7a3143b4f92fbffe66855d21ae06a7772102902a282  sub-store-runsv-2.44.12-r3.95f12c5938a2-armeabi-v7a.zip
b0ce215a5a645c23f799bc941dd20902d277ab8f19a055d50ab81c2a2ef187aa  sub-store-runsv-2.44.12-r3.95f12c5938a2-x86_64.zip
0e0988dd21e5d4c4ca8c308c68b04093c5c784001d90187d40ad7f4108e8404c  sub-store-runsv-2.44.12-r3.95f12c5938a2-x86.zip
```
