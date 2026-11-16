# Sub-Store 2.44.15-r3.237ce0ef9591

- Backend: 2.44.15
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
2e32627a0d48b78eea700b5931772752f02dd64291797acb6ecc7c20998357c8  sub-store-runsv-2.44.15-r3.237ce0ef9591-arm64-v8a.zip
3d889ffc97fc31c8fea584c570e1a38f40bd6dd8805711d74543d60e3099269f  sub-store-runsv-2.44.15-r3.237ce0ef9591-armeabi-v7a.zip
512fb695b7391805c1156efe2cdc3fd225a653b1b99bc4a5fee903f04b062497  sub-store-runsv-2.44.15-r3.237ce0ef9591-x86_64.zip
a3109f76116b8bc5e56bc63be303de6c3bee43e4c032bebae7c32e9afa667869  sub-store-runsv-2.44.15-r3.237ce0ef9591-x86.zip
```
