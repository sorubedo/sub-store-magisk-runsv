# Sub-Store 2.44.30-r3.5ebc3c27897a

- Backend: 2.44.30
- Frontend: 2.34.4
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
30e36d18c9e8832a3dd356da0af6d0d45f2fff2f17a52069c9c715fb201c0039  sub-store-runsv-2.44.30-r3.5ebc3c27897a-arm64-v8a.zip
74de45693289bf9f782a29672b4f0dc8f25181bef4ba53cc169f437b6dc94ffa  sub-store-runsv-2.44.30-r3.5ebc3c27897a-armeabi-v7a.zip
5f52d660dc94ba33f046cea860fd4aec2200a0bf663c5647d9744482789c3baf  sub-store-runsv-2.44.30-r3.5ebc3c27897a-x86_64.zip
2b90e1f4e072aae2815a03e5000ae43a3a13f67a9bd9180d94b4b9651a9d174d  sub-store-runsv-2.44.30-r3.5ebc3c27897a-x86.zip
```
