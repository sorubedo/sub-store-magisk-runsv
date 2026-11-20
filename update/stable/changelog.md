# Sub-Store 2.44.20-r3.f2627b0dcd1b

- Backend: 2.44.20
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
28e30b55d23306632f3e360df27cf669461435778cc8248d3e88744c09f4ef3d  sub-store-runsv-2.44.20-r3.f2627b0dcd1b-arm64-v8a.zip
a9f36edc1ad5e9690a4408cff846c15f128446061af8c7d5335a2d5dcd4774c0  sub-store-runsv-2.44.20-r3.f2627b0dcd1b-armeabi-v7a.zip
8e8bfb9e04f76ce90ccb6b269a3f2628a3b3afd07cc2307903c3491768daac15  sub-store-runsv-2.44.20-r3.f2627b0dcd1b-x86_64.zip
b96dfb653bc5acac15fab9c6914affc04e8428d4f1d3e34d454e88044854c8b6  sub-store-runsv-2.44.20-r3.f2627b0dcd1b-x86.zip
```
