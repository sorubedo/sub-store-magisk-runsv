# sub-store-runsv

[English](README.md) | [中文](README_zh-CN.md)

将 [Sub-Store](https://github.com/sub-store-org/Sub-Store) 制作为 Magisk / KernelSU / APatch 模块，使用 [runsvdir-magisk](https://github.com/sorubedo/runsvdir-magisk) 监管进程。沿用 openlist-magisk-runsv、sing-box-magisk-runsv 的安装、服务目录、音量键操作菜单和分架构打包方式。

默认打包官方前端、官方 `sub-store.bundle.js` 和 Termux **`nodejs-lts`**，开启前后端合并模式，只监听 `127.0.0.1:3001`。不包含 http-meta，也无需在手机上安装 Termux 或 npm。Node、ICU、OpenSSL、SQLite、c-ares、C++ 运行库、zlib 和 CA 证书随包携带。

## 安装

要求 Android 7.0 / API 24 以上、Magisk 20.4+ 或支持标准模块安装脚本的 KernelSU/APatch。模块仅提供不挂载版本，以 root 运行，Node、共享库和前后端均放在服务目录。

1. 先安装 runsvdir-magisk 并重启，确认 `/data/adb/runsvdir/service` 存在。
2. 下载对应架构的 ZIP 并刷入，多数手机用 `arm64-v8a`。依赖已经生效时，可直接通过操作菜单启动，无需为本模块重启。
3. 在模块「操作」菜单中，用**音量下切换、音量上执行**，选择「启动并启用」。首次安装带有 `down` 文件，不自动启动。
4. 在同一菜单选择「查看前后端访问地址」，打开显示的完整地址。也可先打开 `http://127.0.0.1:3001`，在前端设置中填入菜单显示的后端地址。

安装时为 `SUB_STORE_FRONTEND_BACKEND_PATH` 生成随机路径，更新时保留。该路径存放于服务目录的 `conf`；完整访问链接包含它，请妥善保存。

| ZIP 后缀 | Magisk 架构 | Node 架构 |
| --- | --- | --- |
| arm64-v8a | arm64 | aarch64 |
| armeabi-v7a | arm | arm |
| x86_64 | x64 | x86_64 |
| x86 | x86 | i686 |

## 服务目录和 Node 依赖

模块 ID 为 `sub-store-runsv`，服务名为 `sub-store`。所有程序都在 `/data/adb/runsvdir/service/sub-store` 下，不向系统目录安装程序或共享库。

| 相对路径 | 内容 |
| --- | --- |
| `runtime/bin/node` | Android / Bionic 版 Node.js LTS |
| `runtime/lib` | Node 所需的 ICU、OpenSSL、SQLite、c-ares、C++、zlib 共享库 |
| `runtime/share/cacert.pem` | HTTPS CA 证书 |
| `runtime/share/termux-packages.json` | Node 和依赖包的版本、来源和 SHA-256 |
| `app/sub-store.bundle.js` | 官方后端，已打包 npm 依赖 |
| `app/frontend` | 官方前端静态文件 |
| `app/versions.json` | 模块、后端、前端、Node 的版本信息 |
| `data` | 默认数据目录 |
| `conf` | 用户配置 |

构建时先解析 Termux `nodejs-lts` 的包依赖，再从 Node 的 ELF `DT_NEEDED` 递归提取实际使用的共享库。系统自带的 Bionic 库继续由 Android 提供。Node 的 RUNPATH 改为 `$ORIGIN/../lib`，各共享库的 RUNPATH 改为 `$ORIGIN`；启动脚本仅对服务进程设置 `LD_LIBRARY_PATH=服务目录/runtime/lib` 和证书路径。无需安装 Termux、npm 或另外刷入 Node 模块。

共享库依赖仍是 Node 运行时的一部分，随安装包完整携带。更新时整体替换 `runtime` 和 `app`，清理已移除的旧库、旧前端资源。若替换失败，恢复旧程序并保持服务停止，避免混用新旧组件。

## 配置和服务命令

编辑 `/data/adb/runsvdir/service/sub-store/conf`，再重启服务。该文件是以 root 加载的 shell 配置，所有变量都会导出给 Node，支持额外添加上游的环境变量。

```sh
SUB_STORE_BACKEND_MERGE=true
SUB_STORE_BACKEND_API_HOST="127.0.0.1"
SUB_STORE_BACKEND_API_PORT=3001
SUB_STORE_CORS_ALLOWED_ORIGINS="*"
SUB_STORE_FRONTEND_BACKEND_PATH="/你的后端路径"
```

`SUB_STORE_DATA_BASE_PATH` 指定数据目录，默认 `./data`。服务固定以 root 运行；如果将数据改到共享存储，可设置 `WAIT_DECRYPT=1` 等待用户 0 的共享存储解密。`SUB_STORE_FRONTEND_PATH`、Node 路径、共享库路径、CA 路径由启动脚本配置。

默认 `SUB_STORE_CORS_ALLOWED_ORIGINS="*"`，允许本机和其他来源的前端请求。可改为逗号分隔的 Origin 白名单，例如 `http://127.0.0.1:3001,https://sub-store.vercel.app`。

如果要从局域网访问，将监听地址改为 `0.0.0.0` 并保留随机后端路径，在其他设备的前端设置中填入手机的实际 IP、端口和后端路径。默认配置仅供本机访问。

```sh
SVC=/data/adb/runsvdir/service/sub-store
SVDIR=/data/adb/runsvdir/service sv-enable sub-store   # 启动并开机自启
SVDIR=/data/adb/runsvdir/service sv-disable sub-store  # 停止并取消自启
sv up "$SVC"         # 仅本次启动
sv down "$SVC"       # 仅本次停止
sv restart "$SVC"    # 重启服务
sv status "$SVC"     # 查看状态
tail -f /data/adb/runsvdir/log/sv/sub-store/current
```

音量键菜单还提供修改自启标记、查看最近日志和各组件版本的功能。模块本身不再启动第二套守护进程，由依赖模块统一管理 runsvdir。

## 更新和卸载

更新时音量上选择**仅更新程序**（默认；同时更新 Node、共享库、证书、前后端），保留 `run` / `conf` / `finish` / `log/run`。音量下选择**完整更新**，重置服务脚本和默认配置，但保留随机后端路径、数据和自启标记。30 秒内不操作或没有 getevent 时默认仅更新程序。若改过端口、数据目录等配置，完整更新前先备份 `conf`。

本地构建不写入尚未发布的 `updateJson`。通过发布脚本生成的包包含按渠道和架构区分的管理器更新地址，菜单可切换 stable / prerelease；**上游尚无预发布版本时不会生成 prerelease 更新源**，请继续使用 stable。

卸载会先停止服务，再删除整个 `/data/adb/runsvdir/service/sub-store`，**包括默认的 data 数据目录**，请先导出备份。自行配置在服务目录外的数据和服务日志会保留。与参照模块一致，临时禁用或停止服务请使用 `sv-disable`；服务注册独立于管理器的模块禁用标记。

## 构建和发布

Linux 构建依赖：Bash、Python 3.10+、curl、dpkg-deb、patchelf、zip。发布额外需要 GitHub CLI `gh`；验证需要主机 Node 24 LTS。下载器根据 Termux 的 Packages 索引解析依赖，核对每个 deb 的 SHA-256，按 ELF `DT_NEEDED` 提取所需库，并将 Termux RUNPATH 改为模块内的路径。

```sh
bash fetch.sh stable           # 最新稳定后端 + 最新稳定前端 + nodejs-lts
bash fetch.sh 2.42.5           # 指定后端 tag；前端仍取最新稳定版
# FRONTEND_TAG=2.34.1 bash fetch.sh stable  # 也可固定前端 tag
bash package.sh                # 每个架构一个 ZIP，共 4 个
bash package.sh arm64-v8a      # 只打包指定架构
python3 -m unittest discover -s tests -v
```

产物在 `out/`，附带 `SHA256SUMS`、`upstream-versions.env` 和记录所有下载版本/校验值的 `resolved.json`。`assets/`、`bin/`、`out/` 为构建产物，不提交到 Git。

## 更新检测与版本号

后端、前端、Node 有各自独立的上游版本；模块将它们作为一套完整载荷发布。每天的工作流分别检查后端渠道、前端稳定版以及四架构的 Termux `nodejs-lts` 和依赖包。

| 变化 | 是否发布新的模块版本 |
| --- | --- |
| 后端 tag 或发布资产变化 | 是 |
| 前端 tag 或发布资产变化 | 是 |
| Node LTS 包更新或重新构建 | 是 |
| ICU、OpenSSL、证书等依赖版本/校验值变化 | 是 |
| 模块脚本修改并增加 `REVISION` | 是 |
| 所有输入相同，且四个安装包和更新元数据完整 | 跳过 |

- **显示版本 `version`**：`2.42.5-r3.<12位指纹>`。`2.42.5` 是后端版本，`r3` 是模块修订号，指纹覆盖前后端、Node 及所有依赖的版本/校验值。前端或 Node 单独更新时，后端版本不变，指纹会变。
- **升级比较 `versionCode`**：以从 2020-01-01 开始的 UTC 构建秒数为基础，并保证大于本地构建和已记录发布版本。同一秒重建或时钟回退时仍可递增。管理器使用这个整数判断是否升级，不比较指纹的字典顺序。
- **组件版本**：分别写入 `build-info.prop`、`app/versions.json`、发布说明；操作菜单可查看后端、前端、Node 版本。
- **发布 tag**：`v` 加模块显示版本，区分后端版本相同的不同组件组合。

手机通过管理器更新整个模块，安装时先停止服务，再一起替换 Node/共享库/证书/前后端，保留数据和自启状态；原先运行的服务会恢复运行。手机端不分别自动更新三个组件。更换后端渠道只影响后端选择，Node 始终取 LTS，前端默认取最新稳定版。

修改模块实现后应递增 `scripts/upstream.py` 中的 `REVISION`。仅修改模块脚本、保留已经下载的组件时，可执行 `python3 scripts/upstream.py metadata --resolved out/resolved.json` 核对本地组件并刷新版本信息，无需重新下载。

- `build.yml`：手动构建并保存 4 个 ZIP，不发布。
- `release.yml`：每天检测稳定/预发布渠道，组件变化或资产不全时构建，验证后发布，再提交管理器更新 JSON。
- `plan-release.sh`：检查四架构资产是否完整；上游没有预发布时跳过该渠道。
- `DRY_RUN=true bash release-channel.sh stable`：本地完成构建、校验和更新元数据生成，不写入 GitHub。
- Fork 后设置 `REPO_SLUG=你的账号/仓库`；Actions 自动使用当前仓库。默认 RAW 地址基于 `main`，其他分支可设置 `RAW_BASE`。设备菜单可通过 `SUB_STORE_UPDATE_BASE` 覆盖更新地址。

测试覆盖安装依赖/架构/API 拒绝、首次停用、普通和完整更新、配置/路径/数据保留、完整替换和失败回退、组件更新触发和版本号递增、四架构 ELF 依赖、ZIP 结构，以及真实 Sub-Store 前后端同端口访问、静态资源、API 和数据落盘。主机上的 JS 测试不能替代不同 Android 真机的兼容性测试。

## 许可

本仓库脚本和打包代码使用 [MIT](LICENSE)。Sub-Store 和前端遵循各自上游许可证，许可证随包携带。Node.js 使用 MIT，并携带其第三方许可；Termux 依赖的版权文件和通用许可证、包来源/版本/SHA-256 均附在运行时 `share/` 中。源码见 [Sub-Store](https://github.com/sub-store-org/Sub-Store)、[Sub-Store-Front-End](https://github.com/sub-store-org/Sub-Store-Front-End)、[Termux nodejs-lts 构建配方](https://github.com/termux/termux-packages/tree/master/packages/nodejs-lts)。
