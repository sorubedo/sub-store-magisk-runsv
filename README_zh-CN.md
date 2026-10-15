# sub-store-runsv

[English](README.md) | [中文](README_zh-CN.md)

把 [Sub-Store](https://github.com/sub-store-org/Sub-Store) 做成开机自启的 runsv 服务，适用于 Magisk / KernelSU / APatch。

自带前端、后端、Node.js LTS 和运行库，默认前后端合并。仅提供不挂载版本，以 root 运行；不包含 http-meta，手机无需安装 Termux 或 npm。

## 安装

要求 Android 7.0 及以上。

1. 先安装 [runsvdir-magisk](https://github.com/sorubedo/runsvdir-magisk) 并重启手机。
2. 从 [Releases](https://github.com/sorubedo/sub-store-magisk-runsv/releases) 下载并刷入对应架构的 ZIP。多数手机选 `arm64-v8a`，另有 `armeabi-v7a`、`x86_64`、`x86`。

## 启动

首次安装不会自动启动。用模块的「操作」按钮（音量下切换，音量上执行），选「启动并启用」。也可以直接用命令：

```sh
SVC=/data/adb/runsvdir/service/sub-store

SVDIR=/data/adb/runsvdir/service sv-enable sub-store   # 启动并开机自启
SVDIR=/data/adb/runsvdir/service sv-disable sub-store  # 停止并取消自启
sv up "$SVC"        # 本次启动
sv down "$SVC"      # 本次停止
sv restart "$SVC"  # 重启服务
sv status "$SVC"   # 查看状态
tail -n 10 /data/adb/runsvdir/log/sv/sub-store/current
```

## 访问和配置

默认前端地址为 `http://127.0.0.1:3001`。在操作菜单中选择「查看前后端访问地址」，按显示的完整链接访问，或在前端设置中填入显示的后端地址。

安装时会生成随机后端路径，更新时保留。

配置文件位于 `/data/adb/runsvdir/service/sub-store/conf`：

```sh
SUB_STORE_BACKEND_MERGE=true
SUB_STORE_BACKEND_API_HOST="127.0.0.1"
SUB_STORE_BACKEND_API_PORT=3001
SUB_STORE_CORS_ALLOWED_ORIGINS="*"
```

修改后重启服务。要从局域网访问，将监听地址改为 `0.0.0.0`，再用手机的 IP 和端口访问。跨域来源可将 `*` 改为逗号分隔的 Origin 白名单。

## 更新

管理器可以检测更新，也可以覆盖刷入新包。Node、运行库、前端和后端一起更新，数据和自启设置保留。安装时用音量键选择：

- 音量上：仅更新程序，保留 `run` / `conf` / `log/run`；30 秒内不操作默认选此项。
- 音量下：完整更新，重置服务脚本和配置，保留数据、随机后端路径和自启设置。

原来正在运行的服务会在更新后恢复运行，无需重启手机。在操作菜单中可查看各组件版本、切换稳定版和预发布版渠道；预发布渠道在上游有预发布版本时提供。

## 卸载

卸载会删除整个服务目录，包括默认的 `data` 数据目录，请提前备份。自行配置在服务目录外的数据不会删除。

## 常见问题

- **安装提示缺少 runsvdir-magisk**：先安装 runsvdir-magisk 并重启，再刷本模块。
- **服务没起来**：用操作菜单查看最近 10 行日志，再执行 `sv status /data/adb/runsvdir/service/sub-store`。
- **前端连接不上后端**：确认服务已启动，并在前端设置中填写操作菜单显示的完整后端地址，包含随机路径。
- **想换数据目录**：修改 `conf` 中的 `SUB_STORE_DATA_BASE_PATH`，再重启服务。若放在共享存储，设置 `WAIT_DECRYPT=1`。
