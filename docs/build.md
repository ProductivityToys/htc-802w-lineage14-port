# HTC 802w 源码构建与 Android 集成

本文面向构建内核及打包工具的开发者。安装现成 ROM 请使用 [中文刷机指南](rom-install.md)。

## 仓库结构

- `kernel/`：完整内核与 Prima 源码，保留 LineageOS 上游 Git 历史。
- `scripts/`、`src/`、`config/`：构建、boot 重打包、WCNSS 助手及实测 init 片段。
- `docs/`、`sources.json`：构建记录、来源、Android 集成说明和发布检查表。
- 根目录 `Dockerfile`：Linux x86 构建环境。

技术背景见 [内核移植说明](../kernel/PORTING.md)。

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
见 [构建验证记录](build-verification.json)。记录对应构建提交；后续仅说明更新
也会改变项目版本号，因此不能要求重建结果具有相同二进制 SHA。

## Android 集成与 boot 重打包

见 [集成说明](android-integration.md)。本仓库提供构建与重打包工具，
已验证的预览安装包实现设备校准处理、用户空间补丁与型号保护；
安装要求及验收范围见 [刷机说明](rom-install.md)。

```bash
python3 scripts/repack_boot.py known-good-boot.img zImage boot-new.img
```

boot 分区为 mmcblk0p36，上限 16 MiB；recovery 为 p37，system 为 p38，
cache 为 p39，data 为 p40。刷机前备份自己的 boot 和原厂固件，核对机型。
不能使用国际单卡 M7 的分区编号或删除型号检查后强刷。

## 来源与验证资料

- [构建验证记录](build-verification.json)
- [ROM 验证范围](rom-verification.json)
- [ROM 来源与二进制映射](rom-manifest.json)
- [首版源码说明及更正](source-preview-release.md)
- [来源与许可](../LICENSES.md)
