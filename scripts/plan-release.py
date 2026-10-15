#!/usr/bin/env python3
"""Select upstream channels that need all four module artifacts published."""
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
from upstream import ABIS, ROOT, resolve

repo = os.environ.get("REPO_SLUG", "sorubedo/sub-store-magisk-runsv")
selector = os.environ.get("CHANNEL_INPUT", "auto")
if selector not in ("auto", "stable", "prerelease"):
    raise SystemExit("CHANNEL_INPUT must be auto, stable or prerelease")
selected = []
for channel in (["stable", "prerelease"] if selector == "auto" else [selector]):
    info = resolve(channel)
    if info is None:
        print(f"skip {channel}: upstream has no prerelease")
        continue
    output = ROOT / "out" / f"resolved-{channel}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(info, indent=2) + "\n")
    expected = {f"sub-store-runsv-{info['version']}-{abi}.zip" for abi in ABIS}
    expected.update(("SHA256SUMS", "upstream-versions.env", "resolved.json"))
    request = urllib.request.Request(f"https://api.github.com/repos/{repo}/releases/tags/{info['release_tag']}")
    if os.environ.get("GH_TOKEN"):
        request.add_header("Authorization", "Bearer " + os.environ["GH_TOKEN"])
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            existing = json.load(response)
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise
        existing = {"assets": []}
    metadata_ok = True
    for abi in ABIS:
        path = ROOT / "update" / channel / f"{abi}.json"
        if not path.is_file() or f"/download/{info['release_tag']}/" not in json.loads(path.read_text())["zipUrl"]:
            metadata_ok = False
    complete = expected <= {a["name"] for a in existing["assets"]}
    if os.environ.get("FORCE") == "true" or not complete or not metadata_ok:
        selected.append(channel)
        print(f"select {channel}: {info['release_tag']}")
    else:
        print(f"skip {channel}: all payload inputs and artifacts are current")
channels = " ".join(selected)
if os.environ.get("GITHUB_OUTPUT"):
    with Path(os.environ["GITHUB_OUTPUT"]).open("a") as output:
        output.write(f"channels={channels}\n")
print(channels)
