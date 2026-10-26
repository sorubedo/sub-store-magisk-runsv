# Sub-Store 2.44.2-r3.f183ec1d709f

- Backend: 2.44.2
- Frontend: 2.34.1
- Android Node.js LTS: 24.22.1 (Termux nodejs-lts)
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
862f1edf55fba8e5d8d3431234506051673df98b43214d5a650977347b5e3f17  sub-store-runsv-2.44.2-r3.f183ec1d709f-arm64-v8a.zip
5a414a9c079ced18db93fafb5dcf55056be88d66417d8644e28019d6aea6c4de  sub-store-runsv-2.44.2-r3.f183ec1d709f-armeabi-v7a.zip
e9d32b23f6c6a1404344d9e0f7ae24c56c4730bc0453f128d61248eeb9cfede2  sub-store-runsv-2.44.2-r3.f183ec1d709f-x86_64.zip
cfd48a719f8c60cf2bfdc4f9b16b6662471769cba723e79365b92cbb63bf4b88  sub-store-runsv-2.44.2-r3.f183ec1d709f-x86.zip
```
