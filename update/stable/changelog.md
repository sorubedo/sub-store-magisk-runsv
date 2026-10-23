# Sub-Store 2.43.1-r3.3ef9234143b5

- Backend: 2.43.1
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
5bf112ea3ce012d6ee23ca4918f0387b5d6c2b0e044e7b4f27e2bb177068c718  sub-store-runsv-2.43.1-r3.3ef9234143b5-arm64-v8a.zip
d66dd68f7109a5135b3975b406312569c483ec1c12f74298744ac976e0f1f211  sub-store-runsv-2.43.1-r3.3ef9234143b5-armeabi-v7a.zip
8f51b4874b74f9fa62208729916ea95965540f7cc56a32228868612e7e61b6c7  sub-store-runsv-2.43.1-r3.3ef9234143b5-x86_64.zip
c64bc3adf826d79a73cbbe3d8535dfeb5a4b5bc3fb47586e3781ba6c72c6bac2  sub-store-runsv-2.43.1-r3.3ef9234143b5-x86.zip
```
