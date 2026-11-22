# Sub-Store 2.44.23-r3.2bd2debe004c

- Backend: 2.44.23
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
a009697488742d7a9bc15b76252f35f55b99d92595aa45b486e06d263e912cd6  sub-store-runsv-2.44.23-r3.2bd2debe004c-arm64-v8a.zip
1463456afadce6c2f319b0b5784b03beaffe4cb3e2c476d93553b45b3fad7925  sub-store-runsv-2.44.23-r3.2bd2debe004c-armeabi-v7a.zip
c3796ce3e5cd9bd051557f07c468ca3ee95dadea2842e25b2aee6a9e442f08aa  sub-store-runsv-2.44.23-r3.2bd2debe004c-x86_64.zip
c2371792759682f45081f6968cff44b959a94ceea811be816bfa2e53f687401e  sub-store-runsv-2.44.23-r3.2bd2debe004c-x86.zip
```
