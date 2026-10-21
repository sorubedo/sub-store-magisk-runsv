# Sub-Store 2.42.6-r3.9ef874291f83

- Backend: 2.42.6
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
b2bfdd6bb2d42220146b7838f0637fc0f599bc4b382d3d2dcb7c73609224fac6  sub-store-runsv-2.42.6-r3.9ef874291f83-arm64-v8a.zip
ef141701cf0beb46ebb1d8010d7cd467dd021ea4d8d586882451a01021ffcfc7  sub-store-runsv-2.42.6-r3.9ef874291f83-armeabi-v7a.zip
07c2c66312d0cb02a00aeb8fe95af79c410c8836229f87277d10f9a2a996ad03  sub-store-runsv-2.42.6-r3.9ef874291f83-x86_64.zip
ebdeae005b6ee1e2c176d06abfe8bcaa6a60b2c76c8ba065a8390669736226ad  sub-store-runsv-2.42.6-r3.9ef874291f83-x86.zip
```
