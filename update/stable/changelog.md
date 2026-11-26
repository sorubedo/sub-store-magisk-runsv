# Sub-Store 2.44.30-r3.c8c6e086d1aa

- Backend: 2.44.30
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
e4911b644a26a18228f6731559ff067ba7502cf9b1dc7ca9dad583aae2b0f983  sub-store-runsv-2.44.30-r3.c8c6e086d1aa-arm64-v8a.zip
f6c3a783de3c40a29e5cb287eb2884da31379ad0f853e4cb5f7b1c4aa4420cfe  sub-store-runsv-2.44.30-r3.c8c6e086d1aa-armeabi-v7a.zip
0433a9cfab7728db71c2182bf2778a10ef87023a95caa49fe475466eb2f79a59  sub-store-runsv-2.44.30-r3.c8c6e086d1aa-x86_64.zip
18455afa1d5ed45d748ffa2fae05d46bc731c5ebaa476ae007dd19943d02e8b2  sub-store-runsv-2.44.30-r3.c8c6e086d1aa-x86.zip
```
