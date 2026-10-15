"""Installer, release, Android ELF and host Node integration checks."""
import contextlib
import copy
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock
import urllib.error
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import upstream
from upstream import ABIS, SYSTEM_LIBS  # noqa: E402


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.adb = self.base / "adb"
        self.svdir = self.adb / "runsvdir/service"
        self.svdir.mkdir(parents=True)
        self.svc = self.svdir / "sub-store"
        (self.adb / "modules/runsvdir").mkdir(parents=True)
        self.shims = self.base / "shims"
        self.shims.mkdir()
        self.commands = self.base / "commands"
        self.shim("sv", 'echo "$*" >> "$TEST_COMMANDS"\ncase "$1" in status) echo "${TEST_STATUS:-down}: service";; esac\n')
        self.shim("chown", 'exit 0\n')

    def shim(self, name, content):
        file = self.shims / name
        file.write_text("#!/bin/sh\n" + content)
        file.chmod(0o755)

    def stage(self):
        module = self.base / "module"
        if module.exists():
            shutil.rmtree(module)
        svc = module / "service/sub-store"
        shutil.copytree(ROOT / "service/sub-store", svc)
        (module / "build-info.prop").write_text("targetAbi=arm64-v8a\n")
        app = svc / "app"
        (app / "frontend").mkdir(parents=True)
        (app / "frontend/index.html").write_text("frontend-v1")
        (app / "sub-store.bundle.js").write_text("backend-v1")
        node = svc / "runtime/bin/node"
        node.parent.mkdir(parents=True)
        node.write_text("#!/bin/sh\nexit 0\n")
        node.chmod(0o755)
        return module

    def install(self, module, **extra):
        text = (ROOT / "customize.sh").read_text().replace("/data/adb", str(self.adb))
        text = text.replace("/system/bin/getevent", str(self.shims / "getevent"))
        script = self.base / "installer.sh"
        script.write_text(text)
        env = dict(os.environ, PATH=str(self.shims) + ":" + os.environ["PATH"],
                   MODPATH=str(module), ARCH="arm64", API="24", TEST_COMMANDS=str(self.commands))
        env.update(extra)
        return subprocess.run(["bash", "-c", 'ui_print() { :; }; abort() { echo "$*" >&2; exit 1; }; . "$1"',
                               "installer-test", str(script)], env=env, text=True, capture_output=True)

    def assertInstalled(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def config_path(self):
        return subprocess.check_output(["sh", "-c", '. "$1"; printf %s "$SUB_STORE_FRONTEND_BACKEND_PATH"',
                                        "read-conf", str(self.svc / "conf")], text=True)

    def test_fresh_install_is_down_and_generates_path(self):
        self.assertInstalled(self.install(self.stage()))
        self.assertTrue((self.svc / "down").exists())

        self.assertRegex(self.config_path(), r"^/[0-9a-f]{32}$")
        self.assertEqual((self.svc / "conf").stat().st_mode & 0o777, 0o600)
        self.assertFalse((self.base / "module/service").exists())

    def test_manager_reset_permissions_are_repaired_on_install_and_updates(self):
        for mode in ("fresh", "payload", "full"):
            with self.subTest(mode=mode):
                if mode == "full":
                    self.shim("getevent", "echo KEY_VOLUMEDOWN DOWN\n")
                module = self.stage()
                # Managers reset extracted files to 0644.
                for file in module.rglob("*"):
                    if file.is_file():
                        file.chmod(0o644)
                self.assertInstalled(self.install(module))
                node = self.svc / "runtime/bin/node"
                self.assertEqual(node.stat().st_mode & 0o777, 0o755)
                self.assertEqual(subprocess.run([str(node)], check=False).returncode, 0)
                self.assertEqual((self.svc / "app/frontend/index.html").stat().st_mode & 0o777, 0o644)

    def test_permission_setup_failure_leaves_existing_service_untouched(self):
        self.assertInstalled(self.install(self.stage()))
        old_node = (self.svc / "runtime/bin/node").read_bytes()
        (self.svc / "down").unlink()
        self.shim("chmod", "exit 1\n")
        result = self.install(self.stage(), TEST_STATUS="run")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Cannot prepare Node/Sub-Store permissions", result.stderr)
        self.assertEqual((self.svc / "runtime/bin/node").read_bytes(), old_node)
        self.assertFalse((self.svc / "down").exists())
        self.assertFalse(self.commands.exists())

    def test_launcher_distinguishes_missing_files_from_non_executable_node(self):
        self.assertInstalled(self.install(self.stage()))
        self.shim("sleep", "exit 0\n")
        node = self.svc / "runtime/bin/node"
        backend = self.svc / "app/sub-store.bundle.js"
        frontend = self.svc / "app/frontend/index.html"
        cases = ((node, 0o644, "Node binary is not executable"),
                 (node, None, "missing Node binary"),
                 (backend, None, "missing or unreadable backend"),
                 (frontend, None, "missing or unreadable frontend"))
        env = dict(os.environ, PATH=str(self.shims) + ":" + os.environ["PATH"])
        for file, mode, message in cases:
            with self.subTest(message=message):
                original, original_mode = file.read_bytes(), file.stat().st_mode & 0o777
                if mode is None:
                    file.unlink()
                else:
                    file.chmod(mode)
                result = subprocess.run(["sh", str(self.svc / "run")], cwd=self.base,
                                        env=env, text=True, capture_output=True, timeout=5)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message + ": " + str(file), result.stdout)
                file.write_bytes(original)
                file.chmod(original_mode)

    def test_payload_update_keeps_config_data_and_enabled_state(self):
        self.assertInstalled(self.install(self.stage()))
        old_conf = (self.svc / "conf").read_text().replace(
            'SUB_STORE_CORS_ALLOWED_ORIGINS="*"',
            'SUB_STORE_CORS_ALLOWED_ORIGINS="https://my.frontend.example"') + "\nCUSTOM_SETTING=preserve\n"
        (self.svc / "conf").write_text(old_conf)
        (self.svc / "run").write_text("custom-run")
        (self.svc / "data").mkdir()
        (self.svc / "data/state.json").write_text("persistent")
        (self.svc / "down").unlink()
        module = self.stage()
        (module / "service/sub-store/app/sub-store.bundle.js").write_text("backend-v2")
        self.assertInstalled(self.install(module, TEST_STATUS="run"))
        self.assertEqual((self.svc / "conf").read_text(), old_conf)
        self.assertEqual((self.svc / "run").read_text(), "custom-run")
        self.assertEqual((self.svc / "data/state.json").read_text(), "persistent")
        self.assertEqual((self.svc / "app/sub-store.bundle.js").read_text(), "backend-v2")
        self.assertFalse((self.svc / "down").exists())
        self.assertIn("-w 15 down", self.commands.read_text())
        self.assertIn("up ", self.commands.read_text())

    def test_launcher_exports_cors_setting(self):
        self.assertInstalled(self.install(self.stage()))
        node = self.svc / "runtime/bin/node"
        node.write_text('#!/bin/sh\nprintf "%s" "$SUB_STORE_CORS_ALLOWED_ORIGINS"\n')
        result = subprocess.run(["sh", str(self.svc / "run")], cwd=self.base,
                                text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout, "*")

    def test_full_update_preserves_path_and_down_marker(self):
        self.assertInstalled(self.install(self.stage()))
        old_path = self.config_path()
        (self.svc / "run").write_text("custom-run")
        self.shim("getevent", "echo KEY_VOLUMEDOWN DOWN\n")
        self.assertInstalled(self.install(self.stage()))
        self.assertEqual(self.config_path(), old_path)
        self.assertEqual((self.svc / "run").read_text(), (ROOT / "service/sub-store/run").read_text())
        self.assertTrue((self.svc / "down").exists())
        self.assertNotIn("\nup ", self.commands.read_text())

    def test_update_removes_obsolete_libraries_and_frontend_assets(self):
        self.assertInstalled(self.install(self.stage()))
        (self.svc / "runtime/lib").mkdir()
        (self.svc / "runtime/lib/old-icu.so").write_text("obsolete")
        (self.svc / "app/frontend/old-chunk.js").write_text("obsolete")
        module = self.stage()
        (module / "service/sub-store/runtime/lib").mkdir()
        (module / "service/sub-store/runtime/lib/new-icu.so").write_text("current")
        self.assertInstalled(self.install(module))
        self.assertFalse((self.svc / "runtime/lib/old-icu.so").exists())
        self.assertFalse((self.svc / "app/frontend/old-chunk.js").exists())
        self.assertEqual((self.svc / "runtime/lib/new-icu.so").read_text(), "current")

    def test_failed_payload_move_restores_both_old_directories(self):
        self.assertInstalled(self.install(self.stage()))
        old_node = (self.svc / "runtime/bin/node").read_text()
        old_app = (self.svc / "app/sub-store.bundle.js").read_text()
        (self.svc / "down").unlink()
        module = self.stage()
        (module / "service/sub-store/runtime/bin/node").write_text("new-node")
        (module / "service/sub-store/app/sub-store.bundle.js").write_text("new-backend")
        self.shim("mv", 'case "$1" in */payload/app) exit 1 ;; esac\nexec /usr/bin/mv "$@"\n')
        result = self.install(module, TEST_STATUS="run")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("previous payload restored", result.stderr)
        self.assertEqual((self.svc / "runtime/bin/node").read_text(), old_node)
        self.assertEqual((self.svc / "app/sub-store.bundle.js").read_text(), old_app)
        self.assertTrue((self.svc / "down").exists())

    def test_custom_path_is_preserved_without_shell_interpolation(self):
        self.assertInstalled(self.install(self.stage()))
        path = "/literal'$(echo unexpected)&\\value"
        conf = (self.svc / "conf").read_text()
        conf = re.sub(r"^SUB_STORE_FRONTEND_BACKEND_PATH=.*$",
                      lambda _: "SUB_STORE_FRONTEND_BACKEND_PATH=" + shlex.quote(path), conf, flags=re.M)
        (self.svc / "conf").write_text(conf)
        self.shim("getevent", "echo KEY_VOLUMEDOWN DOWN\n")
        self.assertInstalled(self.install(self.stage()))
        self.assertEqual(self.config_path(), path)

    def test_missing_dependency_disabled_dependency_wrong_abi_and_old_android_abort(self):
        module = self.stage()
        dep = self.adb / "modules/runsvdir"
        for marker in ("disable", "remove"):
            (dep / marker).touch()
            self.assertNotEqual(self.install(module).returncode, 0)
            self.assertFalse(self.svc.exists())
            (dep / marker).unlink()
        dep.rmdir()
        self.assertNotEqual(self.install(module).returncode, 0)
        dep.mkdir()
        for env in ({"ARCH": "x64"}, {"API": "23"}, {"ARCH": "unsupported"}):
            self.assertNotEqual(self.install(module, **env).returncode, 0)
            self.assertFalse(self.svc.exists())


class PayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (ROOT / "bin/arm64-v8a/bin/node").exists():
            raise unittest.SkipTest("run fetch.sh for Android ELF checks")

    def test_android_interpreters_and_complete_dependency_closure(self):
        for abi in ABIS:
            with self.subTest(abi=abi):
                base = ROOT / "bin" / abi
                node = base / "bin/node"
                interpreter = subprocess.check_output(["patchelf", "--print-interpreter", str(node)], text=True).strip()
                self.assertEqual(interpreter, "/system/bin/linker64" if abi in ("arm64-v8a", "x86_64") else "/system/bin/linker")
                for elf in [node, *(base / "lib").iterdir()]:
                    needed = subprocess.check_output(["patchelf", "--print-needed", str(elf)], text=True).splitlines()
                    for name in needed:
                        self.assertTrue(name in SYSTEM_LIBS or (base / "lib" / name).is_file(), (abi, elf, name))
                    rpath = subprocess.check_output(["patchelf", "--print-rpath", str(elf)], text=True)
                    self.assertNotIn("com.termux", rpath)
                self.assertIn("BEGIN CERTIFICATE", (base / "share/cacert.pem").read_text())

    def test_zip_layout_and_abi_metadata(self):
        archives = list((ROOT / "out").glob("sub-store-runsv-*.zip"))
        self.assertTrue(archives, "run package.sh first")
        for path in archives:
            with self.subTest(zip=path.name), zipfile.ZipFile(path) as archive:
                names = archive.namelist()
                info = dict(line.split("=", 1) for line in archive.read("build-info.prop").decode().splitlines())
                abi = info["targetAbi"]
                self.assertIn(abi, ABIS)
                self.assertTrue(path.name.endswith(f"-{abi}.zip"))
                self.assertIn("service/sub-store/down", names)
                self.assertFalse(any("http-meta" in n for n in names))
                self.assertIn("META-INF/com/google/android/update-binary", names)
                self.assertIn("LICENSE", names)
                self.assertNotIn("moduleVariant", info)
                self.assertIn("skip_mount", names)
                self.assertIn("service/sub-store/runtime/bin/node", names)
                self.assertIn("service/sub-store/app/frontend/index.html", names)
                self.assertFalse(any(n.startswith("system/") for n in names))
                prop = dict(line.split("=", 1) for line in archive.read("module.prop").decode().splitlines())
                components = json.loads(archive.read("service/sub-store/app/versions.json"))
                self.assertEqual(prop["version"], components["MODULE_VERSION"])
                self.assertEqual(prop["versionCode"], components["MODULE_VERSION_CODE"])
                self.assertEqual(info["nodeVersion"], components["NODE_PACKAGE_VERSION"])
                self.assertEqual(info["backendVersion"], components["SUB_STORE_TAG"])
                self.assertEqual(info["frontendVersion"], components["FRONTEND_TAG"])


class UpdateMetadataTests(unittest.TestCase):
    def test_action_channel_switch_preserves_repository_branch_and_abi(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "module.prop").write_text("version=2.42.5-r3.test\nversionCode=100\n"
                "updateJson=https://example.invalid/custom-branch/update/stable/arm64-v8a.json\n")
            script = (ROOT / "action.sh").read_text().split("GETEVENT=/system/bin/getevent", 1)[0]
            script += '\nset_channel prerelease || exit 1\n'
            (base / "action.sh").write_text(script)
            subprocess.run(["sh", str(base / "action.sh")], check=True, capture_output=True)
            prop = (base / "module.prop").read_text()
            self.assertIn("versionCode=100\n", prop)
            self.assertIn("updateJson=https://example.invalid/custom-branch/update/prerelease/arm64-v8a.json\n", prop)

    def test_published_urls_match_every_packaged_abi(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            shutil.copy2(ROOT / "publish-update.sh", base / "publish-update.sh")
            out = base / "out"
            out.mkdir()
            (out / "upstream-versions.env").write_text(
                "MODULE_CHANNEL=stable\nMODULE_VERSION=2.42.5-r3.test\n"
                "MODULE_VERSION_CODE=214255106\nRELEASE_TAG=v2.42.5-r3.test\n")
            for abi in ABIS:
                (out / f"sub-store-runsv-2.42.5-r3.test-{abi}.zip").touch()
            env = dict(os.environ, REPO_SLUG="example/custom-repo", RAW_BASE="https://example.invalid/branch")
            subprocess.run(["bash", str(base / "publish-update.sh")], env=env, check=True)
            files = list((base / "update/stable").rglob("*.json"))
            self.assertEqual(len(files), 4)
            for file in files:
                data = json.loads(file.read_text())
                self.assertEqual(file.parent.name, "stable")
                self.assertEqual(data["versionCode"], 214255106)
                self.assertIn("example/custom-repo/releases/download/v2.42.5-r3.test/", data["zipUrl"])
                self.assertTrue((out / data["zipUrl"].rsplit("/", 1)[1]).is_file())
                self.assertEqual(data["changelog"], "https://example.invalid/branch/update/stable/changelog.md")


class VersionTests(unittest.TestCase):
    def inputs(self):
        return dict(backend=dict(tag="2.42.5", asset=dict(digest="sha256:backend"),
                                 manifest=dict(digest="sha256:manifest")),
                    frontend=dict(tag="2.34.1", asset=dict(digest="sha256:frontend")),
                    channel="stable", node_package="24.18.0-1", termux_repo="https://example.invalid",
                    packages={"arm64-v8a": {"nodejs-lts": {"Version": "24.18.0-1", "SHA256": "node"},
                                              "libicu": {"Version": "78.3", "SHA256": "icu"}}})

    def test_each_component_and_module_revision_can_trigger_release(self):
        original = self.inputs()
        version = upstream.stamp_identity(copy.deepcopy(original))["version"]
        changes = [
            lambda x: x["backend"].update(tag="2.42.6"),
            lambda x: x["frontend"].update(tag="2.34.2"),
            lambda x: x["frontend"]["asset"].update(digest="sha256:reuploaded-frontend"),
            lambda x: x.update(node_package="24.19.0-1"),
            lambda x: x["packages"]["arm64-v8a"]["libicu"].update(SHA256="new-icu"),
        ]
        for change in changes:
            inputs = copy.deepcopy(original)
            change(inputs)
            self.assertNotEqual(upstream.stamp_identity(inputs)["version"], version)
        with mock.patch.object(upstream, "REVISION", upstream.REVISION + 1):
            self.assertNotEqual(upstream.stamp_identity(original)["version"], version)

    def test_unchanged_inputs_keep_the_same_release_identity(self):
        info = upstream.stamp_identity(self.inputs())
        self.assertEqual(upstream.stamp_identity(copy.deepcopy(info)), info)

    def test_version_code_increases_on_same_second_or_older_clock(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(upstream, "ROOT", Path(tmp)), \
                mock.patch.object(upstream.time, "time", return_value=1577836800 + 200):
            root = Path(tmp)
            self.assertEqual(upstream.next_version_code(), 200)
            (root / "out").mkdir()
            (root / "out/upstream-versions.env").write_text("MODULE_VERSION_CODE=200\n")
            self.assertEqual(upstream.next_version_code(), 201)
            (root / "update/prerelease").mkdir(parents=True)
            (root / "update/prerelease/arm64-v8a.json").write_text('{"versionCode": 300}\n')
            self.assertEqual(upstream.next_version_code(), 301)


class MergedServerTests(unittest.TestCase):
    def test_real_backend_frontend_api_and_persistence(self):
        app = ROOT / "assets/app"
        if not (app / "sub-store.bundle.js").exists():
            self.skipTest("run fetch.sh for integration checks")
        if not shutil.which("node"):
            self.skipTest("host Node LTS required")
        with tempfile.TemporaryDirectory() as tmp, contextlib.closing(socket.socket()) as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
            sock.close()
            prefix = "/test-private-path"
            cors_origins = subprocess.check_output(["sh", "-c",
                '. "$1"; printf %s "$SUB_STORE_CORS_ALLOWED_ORIGINS"',
                "read-conf", str(ROOT / "service/sub-store/conf")], text=True)
            env = dict(os.environ, SUB_STORE_BACKEND_MERGE="true", SUB_STORE_BACKEND_API_HOST="127.0.0.1",
                       SUB_STORE_BACKEND_API_PORT=str(port), SUB_STORE_FRONTEND_BACKEND_PATH=prefix,
                       SUB_STORE_FRONTEND_PATH=str(app / "frontend"), SUB_STORE_DATA_BASE_PATH=tmp,
                       SUB_STORE_CORS_ALLOWED_ORIGINS=cors_origins)
            with open(Path(tmp) / "server.log", "w+") as log:
                process = subprocess.Popen(["node", str(app / "sub-store.bundle.js")], cwd=tmp, env=env,
                                           stdout=log, stderr=subprocess.STDOUT)
                try:
                    base = f"http://127.0.0.1:{port}"
                    for _ in range(150):
                        if process.poll() is not None:
                            log.seek(0)
                            self.fail(log.read())
                        try:
                            response = urllib.request.urlopen(base, timeout=1)
                            break
                        except (OSError, urllib.error.URLError):
                            time.sleep(0.1)
                    else:
                        self.fail("merged backend did not start")
                    self.assertEqual(response.read(), (app / "frontend/index.html").read_bytes())
                    page = urllib.request.urlopen(base + "/settings", timeout=5)
                    self.assertIn(b"<html", page.read().lower())
                    index = (app / "frontend/index.html").read_text()
                    js = re.search(r'src="([^"]+\.js)"', index)[1]
                    self.assertGreater(len(urllib.request.urlopen(base + js, timeout=5).read()), 100)
                    api = json.load(urllib.request.urlopen(base + prefix + "/api/utils/env", timeout=5))
                    self.assertEqual(api["status"], "success")
                    for origin in (base, "http://localhost:3001", "https://sub-store.vercel.app",
                                   "https://my.frontend.example"):
                        with self.subTest(origin=origin):
                            url = base + prefix + "/api/utils/env"
                            request = urllib.request.Request(url, headers={"Origin": origin})
                            with urllib.request.urlopen(request, timeout=5) as response:
                                self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")
                                self.assertEqual(json.load(response)["status"], "success")
                            request = urllib.request.Request(url, method="OPTIONS", headers={
                                "Origin": origin, "Access-Control-Request-Method": "POST",
                                "Access-Control-Request-Headers": "Content-Type"})
                            with urllib.request.urlopen(request, timeout=5) as response:
                                self.assertEqual(response.status, 200)
                                self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")
                                self.assertIn("POST", response.headers.get("Access-Control-Allow-Methods", ""))
                                self.assertIn("content-type", response.headers.get("Access-Control-Allow-Headers", "").lower())
                    with self.assertRaises(urllib.error.HTTPError) as caught:
                        urllib.request.urlopen(base + "/api/utils/env", timeout=5)
                    self.assertEqual(caught.exception.code, 404)
                    caught.exception.close()
                    payload = json.dumps(dict(name="module-test", source="local", content="ss://YWVzLTEyOC1nY206dGVzdA==@127.0.0.1:8388#test")).encode()
                    request = urllib.request.Request(base + prefix + "/api/subs", data=payload,
                                                     headers={"Content-Type": "application/json"})
                    created = json.load(urllib.request.urlopen(request, timeout=5))
                    self.assertEqual(created["status"], "success")
                    subs = json.load(urllib.request.urlopen(base + prefix + "/api/subs", timeout=5))
                    self.assertTrue(any(s["name"] == "module-test" for s in subs["data"]))
                    self.assertTrue(any("module-test" in p.read_text() for p in Path(tmp).glob("*.json")))
                finally:
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()


if __name__ == "__main__":
    unittest.main()
