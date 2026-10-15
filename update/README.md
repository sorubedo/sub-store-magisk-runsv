# Manager update metadata

`publish-update.sh` generates `<channel>/<abi>.json` and the channel changelog
after all four packages exist. `release.yml` commits them after publishing.
No fictitious release URLs are committed before the first release.

Channels: `stable`, and `prerelease` only when upstream provides one.
ABIs: `arm64-v8a`, `armeabi-v7a`, `x86_64`, `x86`.
Each channel has one update source per ABI; all payloads use the service folder.
