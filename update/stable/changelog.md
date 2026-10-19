# Sub-Store 2.42.6-r3.7a9a9347c367

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
e194a665c8481ae4dfad7382757849bb8265e2c4de066b18be4613a1acc2b4ce  sub-store-runsv-2.42.6-r3.7a9a9347c367-arm64-v8a.zip
c8807765d092dfe0f1fb6b5cec7bce2438d0954b2e4e8b944c9617b535531c4b  sub-store-runsv-2.42.6-r3.7a9a9347c367-armeabi-v7a.zip
b7accd535f2cb3d4e01ec93080c76dba02f0818e4407cddef05490f907ba409d  sub-store-runsv-2.42.6-r3.7a9a9347c367-x86_64.zip
1479506b60e67beaf1047006f2b59db005446f206a530fd322f59482ea1016d8  sub-store-runsv-2.42.6-r3.7a9a9347c367-x86.zip
```
