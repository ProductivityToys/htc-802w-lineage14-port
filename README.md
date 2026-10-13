# HTC 802w 重新跑起 Android 7.1

**Unofficial HTC 802w / m7cdug Android 7.1.1 community port · ROM Developer Preview**

让国行双卡 HTC One 802w 运行 LineageOS 14.1，具备可操作界面、Wi-Fi
联网和基本相机功能。test44 已在一台 802w 上完成实测。

| 功能 | 实测状态 |
| --- | --- |
| Android 7.1.1 启动、显示与触控 | 通过 |
| Wi-Fi 自动加载、关联、DHCP | 通过 |
| HTTPS 浏览 | test42 阶段通过 |
| 前后摄预览与 JPEG 保存 | test44 通过 |
| SELinux | Enforcing |
| 声音、蓝牙、双卡通信、录像、长期待机 | 未完成验收 |

适用范围为 **HTC 802w / m7cdug**，实测 HBOOT 2.49.0000、UNLOCKED、
S-ON、TWRP 3.0.2-0。802d、802t、国际单卡 M7 未验证。企业微信是应用
兼容性实验，不属于系统适配验收条件。

## 下载入口

**源码与可安装 ROM 都放在本仓库的 [Releases](https://github.com/ProductivityToys/htc-802w-lineage14-port/releases)。**

当前 ROM 预览版 v0.2.0-rom-preview 提供可安装 ZIP、匹配 boot 与校验文件。
使用每台手机自身的 MAC/NV/无线固件，不分发本机配置。[刷机说明](docs/rom-install.md)。
已从清空 data/cache 的状态验证启动，并复验最终 ZIP、Wi-Fi 重连和前后摄。
Google 服务停用等精简仍属于运行时设置，未作为 Lite ROM 打包。

**首版源码更正：v0.1.0-source 误保留早期 Prima 3.2.0.71 实验驱动。**
当前源码已补齐成功基线实际使用的参考 Prima 3.2.3.22，并增加模块调试信息
剥离及 8 MiB 启动缓冲上限检查。请使用后续版本重建 Wi-Fi 模块。

## 仓库结构

- `kernel/`：完整内核与 Prima 源码，保留 LineageOS 上游 Git 历史。
- `scripts/`、`src/`、`config/`：构建、boot 重打包、WCNSS 助手及实测 init 片段。
- `docs/`、`sources.json`：构建记录、来源、Android 集成说明和发布检查表。
- 根目录 `Dockerfile`：Linux x86 构建环境。

技术背景见 [内核移植说明](kernel/PORTING.md)。

## 构建

需要 Docker、Python 3、Git checkout 和固定版本的 Linux x86 Android GCC
4.9。Apple Silicon 使用 Docker 的 linux/amd64 环境。构建脚本依赖 Git
版本信息，不能只解压不含 `.git` 的源码归档；请 clone 后 checkout Release
标明的 tag 或 commit。

```bash
git clone https://github.com/ProductivityToys/htc-802w-lineage14-port.git
cd htc-802w-lineage14-port
# 如复现某次发布，在此 checkout 其 tag / commit。
git clone https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/arm/arm-linux-androideabi-4.9 ../arm-linux-androideabi-4.9
git -C ../arm-linux-androideabi-4.9 checkout 0390252b6bcc6217966ade31d07f8b12f6f78f89
docker build --platform linux/amd64 -t htc-kernel-builder:18.04 .
python3 scripts/build.py --toolchain ../arm-linux-androideabi-4.9 --output ../build-m7cdug
```

结果为 output 下的 `kernel/arch/arm/boot/zImage`、
`kernel/drivers/staging/prima/wlan.ko` 和 `wcnss-init`，附有日志、配置和
SHA-256 清单。使用 `m7cdug_test44_defconfig`，内核和 WLAN 模块必须同次
构建。新二进制仍需独立实机验证，不能沿用原 test44 镜像的验收结论。

合并仓库已完成干净构建，配置 SHA 与成功 test44 一致，内核/WLAN 模块版本匹配。
见 [构建验证记录](docs/build-verification.json)。记录对应构建提交；后续仅说明更新
也会改变项目版本号，因此不能要求重建结果具有相同二进制 SHA。

## Android 集成与刷机

见 [集成说明](docs/android-integration.md)。本仓库提供构建与重打包工具，
已验证的预览安装包实现设备校准处理、用户空间补丁与型号保护；
安装要求及验收范围见 [刷机说明](docs/rom-install.md)。

```bash
python3 scripts/repack_boot.py known-good-boot.img zImage boot-new.img
```

boot 分区为 mmcblk0p36，上限 16 MiB；recovery 为 p37，system 为 p38，
cache 为 p39，data 为 p40。刷机前备份自己的 boot 和原厂固件，核对机型。
不能使用国际单卡 M7 的分区编号或删除型号检查后强刷。

## 来源与许可

内核遵循 `kernel/COPYING`（GPLv2）及各文件原许可证；Prima 有文件级 ISC
声明和 Dual BSD/GPL 模块声明。新增工具和原创说明使用 [MIT](LICENSES/MIT.txt)。
本机原厂 WCNSS 固件、NV、账户、应用与备份均未导入。ROM 包含原始
公开底包中的 vendor HAL，来源及许可证保持原样；新增工具的 MIT 许可不覆盖它们。

见 [sources.json](sources.json)、[LICENSES.md](LICENSES.md) 和
[发布检查表](docs/release-checklist.md)。
