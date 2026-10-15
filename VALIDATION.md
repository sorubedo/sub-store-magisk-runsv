# 验证记录

组件：Sub-Store 2.42.5、前端 2.34.1、Termux nodejs-lts 24.18.0-1。

- 安装与更新：首次停用、配置和数据保留、自启状态、载荷整体替换、失败回退。
- 权限：模拟管理器将解压文件设为 0644，验证首次安装、程序更新、完整更新后 Node 均为 0755。
- 跨域：确认配置导出到服务进程；主机 Node 执行官方后端，携带本机、localhost、官方及自定义前端 Origin 的 GET 和 OPTIONS 请求均通过。
- 四架构：检查 ELF 解释器、共享库闭包、RUNPATH、ZIP 结构和版本元数据。
- ShellCheck、Python 单元测试及安装包 SHA-256 校验。

验证范围为本地脚本、静态载荷和主机 Node。未验证当前安装包在 Magisk/KernelSU 真机上的运行。

```sh
python3 -m unittest discover -s tests -v
shellcheck *.sh service/sub-store/run service/sub-store/log/run
```
