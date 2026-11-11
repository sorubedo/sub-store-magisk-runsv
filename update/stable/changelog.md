# Sub-Store 2.44.7-r3.2ed856776e99

- Backend: 2.44.7
- Frontend: 2.34.2
- Android Node.js LTS: 24.22.2-1 (Termux nodejs-lts)
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
fac03f5a1bbc8bd94e6f2488b3bae9def3acffff75d60ac48b2f4d4b7ebc060d  sub-store-runsv-2.44.7-r3.2ed856776e99-arm64-v8a.zip
e1218a10c40ec78691ea38b367df83af604ed934ee16cfc489e125a9033bce3f  sub-store-runsv-2.44.7-r3.2ed856776e99-armeabi-v7a.zip
324a4d07ea87be8400818b2d8f9dd541f051f46974b54bf1f9e1d0c28a631b9c  sub-store-runsv-2.44.7-r3.2ed856776e99-x86_64.zip
5298d4f2b563daa9240a5c6ef83fed96bacafa0380db4a6530404a2a2c22a80b  sub-store-runsv-2.44.7-r3.2ed856776e99-x86.zip
```
