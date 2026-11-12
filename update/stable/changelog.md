# Sub-Store 2.44.7-r3.4b6a37bdf70d

- Backend: 2.44.7
- Frontend: 2.34.2
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
d434c23c87d8902fffd3b4fc9781ab8211680d6f5c2faaa3f931e69c5defc3fb  sub-store-runsv-2.44.7-r3.4b6a37bdf70d-arm64-v8a.zip
830583e5c8b77997a5ba78b17c0e31e29ba09c290320a74b48595f349d553651  sub-store-runsv-2.44.7-r3.4b6a37bdf70d-armeabi-v7a.zip
05901e7cb329fd0438efaae97919aa7d291fc9b80c3bad68ec1bea9ba32362ee  sub-store-runsv-2.44.7-r3.4b6a37bdf70d-x86_64.zip
bdd8a6defba140c5a807afd02b22d607b3f8b133b731a1255484c859cd0533ac  sub-store-runsv-2.44.7-r3.4b6a37bdf70d-x86.zip
```
