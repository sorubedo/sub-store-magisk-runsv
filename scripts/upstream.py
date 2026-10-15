#!/usr/bin/env python3
"""Fetch Sub-Store and a self-contained Android Node LTS runtime."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ABIS = {"arm64-v8a": "aarch64", "armeabi-v7a": "arm", "x86_64": "x86_64", "x86": "i686"}
TERMUX = os.environ.get("TERMUX_REPO", "https://packages.termux.dev/apt/termux-main").rstrip("/")
BACKEND = "sub-store-org/Sub-Store"
FRONTEND = "sub-store-org/Sub-Store-Front-End"
# Increment for module changes.
REVISION = 3
SYSTEM_LIBS = {"libc.so", "libdl.so", "libm.so", "liblog.so", "libandroid.so"}


def download(url, path, digest=None, authenticated=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    args = ["curl", "-fsSL", "--http1.1", "--retry", "3", "--retry-delay", "2",
            "--retry-all-errors", "--connect-timeout", "30", "--max-time", "600"]
    # API credentials must never be forwarded to arbitrary download hosts.
    if authenticated and os.environ.get("GH_TOKEN"):
        args += ["-H", "Authorization: Bearer " + os.environ["GH_TOKEN"]]
    subprocess.run(args + [url, "-o", str(path)], check=True)
    if digest and hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise ValueError(f"SHA256 mismatch: {url}")


def api(path):
    with tempfile.TemporaryDirectory() as tmp:
        file = Path(tmp) / "response.json"
        download("https://api.github.com/repos/" + path, file, authenticated=True)
        return json.loads(file.read_text())


def release(repo, selector):
    if selector == "stable":
        return api(repo + "/releases/latest")
    if selector in ("auto", "prerelease"):
        items = api(repo + "/releases?per_page=100")
        pre = next((item for item in items if item["prerelease"] and not item["draft"]), None)
        if pre:
            return pre
        if selector == "prerelease":
            return None
        return release(repo, "stable")
    return api(repo + "/releases/tags/" + urllib.parse.quote(selector, safe=""))


def asset(info, name):
    return next(a for a in info["assets"] if a["name"] == name)


def parse_packages(content):
    packages = {}
    for paragraph in content.split("\n\n"):
        fields = {}
        for line in paragraph.splitlines():
            if line and not line[0].isspace() and ": " in line:
                key, value = line.split(": ", 1)
                fields[key] = value
        if "Package" in fields:
            packages[fields["Package"]] = fields
    return packages


def dependency_closure(index):
    selected = {}

    def add(name):
        if name in selected:
            return
        package = index[name]
        selected[name] = {k: package[k] for k in ("Package", "Version", "Filename", "SHA256")}
        for group in package.get("Depends", "").split(","):
            if not group.strip():
                continue
            candidates = [re.split(r"[\s:(]", p.strip())[0] for p in group.split("|")]
            choice = next((p for p in candidates if p in index), None)
            if not choice:
                raise ValueError(f"Unresolved dependency for {name}: {group}")
            add(choice)

    add("nodejs-lts")
    add("ca-certificates")
    add("termux-licenses")
    return dict(sorted(selected.items()))


def resolve(selector):
    backend = release(BACKEND, selector)
    if backend is None:
        return None
    frontend = release(FRONTEND, os.environ.get("FRONTEND_TAG", "stable"))
    channel = "prerelease" if backend["prerelease"] else "stable"
    bundles = {}
    with tempfile.TemporaryDirectory() as tmp:
        for abi, arch in ABIS.items():
            path = Path(tmp) / f"{arch}.gz"
            download(f"{TERMUX}/dists/stable/main/binary-{arch}/Packages.gz", path)
            bundles[abi] = dependency_closure(parse_packages(gzip.decompress(path.read_bytes()).decode()))
    versions = {packages["nodejs-lts"]["Version"] for packages in bundles.values()}
    if len(versions) != 1:
        raise ValueError(f"Termux Node LTS architectures are out of sync: {versions}; retry later")
    info = {
        "revision": REVISION, "channel": channel,
        "backend": {"tag": backend["tag_name"], "asset": asset(backend, "sub-store.bundle.js"),
                    "manifest": asset(backend, "runtime-manifest.json")},
        "frontend": {"tag": frontend["tag_name"], "asset": asset(frontend, "dist.zip")},
        "node_package": next(iter(versions)), "packages": bundles, "termux_repo": TERMUX,
    }
    return stamp_identity(info)


def stamp_identity(info):
    info["revision"] = REVISION
    identity = {"revision": REVISION, "channel": info["channel"],
                "node_package": info["node_package"], "packages": info["packages"],
                "termux_repo": info["termux_repo"],
                "backend": {"tag": info["backend"]["tag"],
                "assets": [backend_asset.get("digest") or backend_asset["updated_at"]
                           for backend_asset in (info["backend"]["asset"], info["backend"]["manifest"])]},
                "frontend": {"tag": info["frontend"]["tag"],
                "digest": info["frontend"]["asset"].get("digest") or info["frontend"]["asset"]["updated_at"]}}
    fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:12]
    tag = re.sub(r"[^0-9A-Za-z.+-]", "-", info["backend"]["tag"].removeprefix("v"))
    info["version"] = f"{tag}-r{REVISION}.{fingerprint}"
    info["release_tag"] = "v" + info["version"]
    return info


def fetch_asset(item, path):
    digest = item.get("digest") or ""
    download(item["browser_download_url"], path,
             digest.removeprefix("sha256:") if digest.startswith("sha256:") else None)


def run(*args):
    return subprocess.check_output(args, text=True).strip()


def fetch_node(info, abi, destination):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        extracted = tmp / "extracted"
        versions = {}
        for name, package in info["packages"][abi].items():
            print(f"  {abi}: {name} {package['Version']}", flush=True)
            deb = tmp / (name + ".deb")
            download(info["termux_repo"] + "/" + package["Filename"], deb, package["SHA256"])
            subprocess.run(["dpkg-deb", "-x", str(deb), str(extracted)], check=True)
            versions[name] = package
        prefix = extracted / "data/data/com.termux/files/usr"
        (destination / "bin").mkdir(parents=True)
        (destination / "lib").mkdir()
        shutil.copy2(prefix / "bin/node", destination / "bin/node")
        pending = [destination / "bin/node"]
        while pending:
            elf = pending.pop()
            for needed in run("patchelf", "--print-needed", str(elf)).splitlines():
                if needed in SYSTEM_LIBS or (destination / "lib" / needed).exists():
                    continue
                source = prefix / "lib" / needed
                if not source.is_file():
                    raise ValueError(f"Missing Android library: {needed} (from {elf.name})")
                target = destination / "lib" / needed
                shutil.copy2(source.resolve(), target)
                pending.append(target)
        for elf in [destination / "bin/node", *(destination / "lib").iterdir()]:
            subprocess.run(["patchelf", "--set-rpath",
                            "$ORIGIN/../lib" if elf.name == "node" else "$ORIGIN", str(elf)], check=True)
            elf.chmod(0o755)
        interpreter = run("patchelf", "--print-interpreter", str(destination / "bin/node"))
        expected = "/system/bin/linker64" if abi in ("arm64-v8a", "x86_64") else "/system/bin/linker"
        if interpreter != expected:
            raise ValueError(f"Not an Android Node binary: {interpreter}")
        share = destination / "share"
        share.mkdir()
        shutil.copy2(prefix / "etc/tls/cert.pem", share / "cacert.pem")
        (share / "cacert.pem").chmod(0o644)
        licenses = share / "licenses"
        licenses.mkdir()
        for name in versions:
            src = prefix / "share/doc" / name
            if src.is_dir():
                shutil.copytree(src, licenses / name, symlinks=False)
        shutil.copytree(prefix / "share/LICENSES", licenses / "common", symlinks=False)
        for path in share.rglob("*"):
            path.chmod(0o755 if path.is_dir() else 0o644)
        (share / "termux-packages.json").write_text(json.dumps(versions, indent=2) + "\n")


def fetch(info):
    for tool in ("curl", "dpkg-deb", "patchelf"):
        if not shutil.which(tool):
            raise ValueError(f"Missing build tool: {tool}")
    (ROOT / "out").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sub-store-fetch-") as tmp:
        tmp = Path(tmp)
        app = tmp / "assets/app"
        app.mkdir(parents=True)
        fetch_asset(info["backend"]["asset"], app / "sub-store.bundle.js")
        fetch_asset(info["backend"]["manifest"], app / "runtime-manifest.json")
        manifest = json.loads((app / "runtime-manifest.json").read_text())
        if manifest.get("npm") or manifest.get("externalBinary"):
            raise ValueError("Upstream now requires external npm packages/binaries; review runtime-manifest.json")
        node_major = int(info["node_package"].split(".")[0].split(":")[-1])
        tested_major = int(manifest["testedNode"].split(".")[0])
        if node_major < tested_major:
            raise ValueError(f"Android Node LTS {node_major} is older than upstream testedNode {tested_major}")
        frontend_zip = tmp / "frontend.zip"
        fetch_asset(info["frontend"]["asset"], frontend_zip)
        frontend = tmp / "frontend"
        with zipfile.ZipFile(frontend_zip) as archive:
            for member in archive.infolist():
                if not (frontend / member.filename).resolve().is_relative_to(frontend.resolve()):
                    raise ValueError("Unsafe frontend ZIP path")
            archive.extractall(frontend)
        candidates = list(frontend.rglob("index.html"))
        if len(candidates) != 1:
            raise ValueError("Expected one frontend index.html")
        shutil.copytree(candidates[0].parent, app / "frontend")
        for repo, tag, filename in ((BACKEND, info["backend"]["tag"], "Sub-Store-LICENSE"),
                                     (FRONTEND, info["frontend"]["tag"], "Frontend-LICENSE")):
            download(f"https://raw.githubusercontent.com/{repo}/{urllib.parse.quote(tag, safe='')}/LICENSE", app / filename)
        for abi in ABIS:
            fetch_node(info, abi, tmp / "bin" / abi)
        for directory in ("assets", "bin"):
            old = ROOT / directory
            if old.exists():
                shutil.rmtree(old)
            shutil.move(str(tmp / directory), old)
    write_metadata(info)


def next_version_code():
    code = int(time.time()) - 1577836800
    env_file = ROOT / "out/upstream-versions.env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("MODULE_VERSION_CODE="):
                code = max(code, int(shlex.split(line.split("=", 1)[1])[0]) + 1)
    for path in (ROOT / "update").rglob("*.json"):
        code = max(code, int(json.loads(path.read_text())["versionCode"]) + 1)
    if not 0 < code < 2147483648:
        raise ValueError("versionCode is outside Magisk's signed 32-bit range")
    return code


def write_metadata(info):
    code = next_version_code()
    env = {
        "SUB_STORE_TAG": info["backend"]["tag"], "FRONTEND_TAG": info["frontend"]["tag"],
        "NODE_PACKAGE_VERSION": info["node_package"], "MODULE_VERSION": info["version"],
        "MODULE_VERSION_CODE": str(code), "MODULE_CHANNEL": info["channel"],
        "RELEASE_TAG": info["release_tag"], "MODULE_REVISION": str(REVISION),
    }
    (ROOT / "out/upstream-versions.env").write_text("".join(f"{k}={shlex.quote(v)}\n" for k, v in env.items()))
    (ROOT / "assets/app/versions.json").write_text(json.dumps(env, indent=2) + "\n")
    print(f"=> {info['version']} / Node LTS {info['node_package']} / {info['channel']}")


def check_local_payload(info):
    local = json.loads((ROOT / "assets/app/versions.json").read_text())
    for key, expected in (("SUB_STORE_TAG", info["backend"]["tag"]),
                          ("FRONTEND_TAG", info["frontend"]["tag"]),
                          ("NODE_PACKAGE_VERSION", info["node_package"])):
        if local[key] != expected:
            raise ValueError(f"Local {key} differs from resolved inputs; run fetch.sh")
    for key, name in (("asset", "sub-store.bundle.js"), ("manifest", "runtime-manifest.json")):
        digest = info["backend"][key].get("digest") or ""
        if digest.startswith("sha256:") and hashlib.sha256((ROOT / "assets/app" / name).read_bytes()).hexdigest() != digest[7:]:
            raise ValueError(f"Local {name} checksum mismatch; run fetch.sh")
    for abi in ABIS:
        local = json.loads((ROOT / "bin" / abi / "share/termux-packages.json").read_text())
        if local != info["packages"][abi]:
            raise ValueError(f"Local {abi} Node dependencies differ from resolved inputs; run fetch.sh")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("resolve", "fetch", "metadata"))
    parser.add_argument("selector", nargs="?", default="stable", help="stable|prerelease|auto|TAG")
    parser.add_argument("--resolved", type=Path, help="reuse previously resolved JSON inputs")
    parser.add_argument("--output", type=Path, default=ROOT / "out/resolved.json")
    args = parser.parse_args()
    if args.command == "metadata" and not args.resolved:
        parser.error("metadata requires --resolved pointing to previously fetched inputs")
    info = json.loads(args.resolved.read_text()) if args.resolved else resolve(args.selector)
    if info is None:
        print("No upstream prerelease is available", file=sys.stderr)
        return 3
    info = stamp_identity(info)
    if args.command == "metadata":
        check_local_payload(info)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(info, indent=2) + "\n")
    if args.command == "fetch":
        fetch(info)
    elif args.command == "metadata":
        write_metadata(info)
    else:
        print(info["release_tag"])
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, StopIteration, subprocess.CalledProcessError) as error:
        sys.exit(f"ERROR: {error}")
