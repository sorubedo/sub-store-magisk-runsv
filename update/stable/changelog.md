# Sub-Store 2.43.0-r3.045171abe2c7

- Backend: 2.43.0
- Frontend: 2.34.1
- Android Node.js LTS: 24.18.0-2 (Termux nodejs-lts)
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
e5549aad5d936e3936847a6ec20fb74c1ad0077f0b569391a6897d666e409c73  sub-store-runsv-2.43.0-r3.045171abe2c7-arm64-v8a.zip
139252cf7be32e04406a8ba3121210d7386f47101d0533b14dfdbf05169d4271  sub-store-runsv-2.43.0-r3.045171abe2c7-armeabi-v7a.zip
c348c0cb50644d338568f793f68ca438f372cb87b9f33c3f79f3c0f2f4bd8282  sub-store-runsv-2.43.0-r3.045171abe2c7-x86_64.zip
cec14628916ec289588bf8c13d173681c80ac59cd2ce8a46df48841823f2fda4  sub-store-runsv-2.43.0-r3.045171abe2c7-x86.zip
```
