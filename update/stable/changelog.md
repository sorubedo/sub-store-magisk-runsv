# Sub-Store 2.44.1-r3.15a1e98f0ee9

- Backend: 2.44.1
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
ed543edc900f4d6adc51fc8fd23eadb63ab5df077a1cf42072ccc92d8f2e9bde  sub-store-runsv-2.44.1-r3.15a1e98f0ee9-arm64-v8a.zip
b0e773c8d4948285b9f200a69f6a555a8b766f870882cf87d81778d73a449b42  sub-store-runsv-2.44.1-r3.15a1e98f0ee9-armeabi-v7a.zip
9eda2730bbc0e0fb5ef93776874e4c65c7df1dcfd100354f6e04008fe8927bb2  sub-store-runsv-2.44.1-r3.15a1e98f0ee9-x86_64.zip
63a4716326d7374204869fb0fa69497d235b38f064fd0cd14e57b4d196fc4a20  sub-store-runsv-2.44.1-r3.15a1e98f0ee9-x86.zip
```
