# Sub-Store 2.44.9-r3.cd2b0cdf31a2

- Backend: 2.44.9
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
ba36d35d111fecf817c8e095c0aac6a0c82db1b4de2b78b54107de7fccf55c78  sub-store-runsv-2.44.9-r3.cd2b0cdf31a2-arm64-v8a.zip
8bad508af6c6d5aae5504bad39fb820f3871f9ea0e8cb71c1aff8235d92f22e8  sub-store-runsv-2.44.9-r3.cd2b0cdf31a2-armeabi-v7a.zip
0def8c35705368d7ee9dd4a4f76f923f38b597e6cba67a1b8d9f92572cef7058  sub-store-runsv-2.44.9-r3.cd2b0cdf31a2-x86_64.zip
30a132530eef431d21f8189ea63609d0d8443ed7c530296a9caaaf01088a274d  sub-store-runsv-2.44.9-r3.cd2b0cdf31a2-x86.zip
```
