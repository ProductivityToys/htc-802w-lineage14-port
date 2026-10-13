# HTC 802w Android 7.1.1 中文刷机指南

适用版本：**v0.2.0-rom-preview**。这是非官方 LineageOS 14.1 开发者预览版。

**正常安装只刷一个 ROM ZIP。boot 和 Wi-Fi 模块已经包含在 ZIP 中，会随安装写入，不需要分别下载或安装。**

## 一、先确认手机满足条件

本指南从“已解锁并安装专用 TWRP”的手机开始，不包含 Bootloader 解锁或首次安装 Recovery 的步骤。

- 机型必须为 **HTC One 802w（联通双卡版）**，代号 `m7cdug`，MID `PN0771000`。
- Bootloader 显示 `UNLOCKED`；实测版本为 HBOOT `2.49.0000`，`S-ON`。
- 已安装能正常显示、触控和挂载的 **802w 专用 TWRP 3.0.2-0**（`twrp-3.0.2-0-m7cdug.img`）。
- 手机保留自己的原厂 Wi-Fi NV 校准文件，以及完整的原厂 WCNSS 固件分区。原厂固件实测版本为 `7.19.1402.1`，安装器只接受已验证的无线固件哈希。

**不要用于 802d、802t 或国际单卡 M7。不要先擦除 System。**
安装器需要从现有 System 保存这台手机自己的 Wi-Fi 校准文件；如果 System 已擦除、缺少原厂 NV，先恢复这台手机自己的原厂系统或备份。

安装器会检查机型、分区和无线固件，输入不符会拒绝写入。此版本不能直接套用国际单卡 M7 的刷机教程。

## 二、下载什么

打开 [v0.2.0 ROM 下载页](https://github.com/ProductivityToys/htc-802w-lineage14-port/releases/tag/v0.2.0-rom-preview)，下载以下文件：

| 文件 | 用途 | 是否需要 |
| --- | --- | --- |
| `lineage-14.1-20261013-UNOFFICIAL-m7cdug-preview.zip` | 完整刷机安装包，约 364 MiB | 必需 |
| `SHA256SUMS` | 检查 ROM 下载是否完整 | 推荐 |
| `INSTALL.md` | 本中文指南的离线副本 | 可选，可直接在线阅读 |

GitHub 自动提供的 `Source code (zip)` 和 `Source code (tar.gz)` 是给开发者的源码归档，**不要拿它们刷机**。

### 校验 ROM

在电脑上进入下载目录，将 ROM ZIP 和 `SHA256SUMS` 放在同一个目录。

macOS：

```bash
shasum -a 256 -c SHA256SUMS
```

Linux：

```bash
sha256sum -c SHA256SUMS
```

输出 ROM 文件名和 `OK` 才表示校验通过。Windows PowerShell 可计算哈希，再与下方值比较：

```powershell
Get-FileHash .\lineage-14.1-20261013-UNOFFICIAL-m7cdug-preview.zip -Algorithm SHA256
```

本版 ROM 的 SHA-256：

```text
5bbeef87d067666d1de6df6baddde7c8bf95b27a4c65b574841e3746cb9d3023
```

校验不一致时重新下载，不继续安装。

## 三、进入 TWRP 并备份

### 1. 进入 Recovery

手机关机后，按住 **音量下 + 电源键** 进入 HBOOT，用音量键选择 `RECOVERY`，按电源键确认。

如果 Android 可以启动且已启用 USB 调试，也可以连接电脑执行：

```bash
adb reboot recovery
```

使用 ADB/Fastboot 命令时，电脑只连接本次待刷的 802w。命令行方法需要电脑已经装好 ADB/Fastboot。

### 2. 允许 System 修改

在 TWRP 打开 `Mount（挂载）`，取消勾选 **Mount system partition read-only（以只读方式挂载系统分区）**。
如果出现首次提示，滑动 `Swipe to Allow Modifications（允许修改）`。

### 3. 保存可恢复的备份

打开 `Backup（备份）`，勾选：

- `Boot`
- `System`
- `Data`
- `Cache`

滑动开始备份，等待完成。**把备份复制到电脑后再继续**。
TWRP 通常将备份放在内部存储的 `TWRP/BACKUPS/`；可通过 MTP 复制，或执行：

```bash
adb pull /sdcard/TWRP/BACKUPS ./TWRP-BACKUPS
```

照片、下载等内部存储文件另行复制到电脑，TWRP 的 Data 备份不包含这部分文件。

## 四、把 ROM 放进手机

通过 USB/MTP 把 ROM ZIP 复制到手机内部存储根目录；也可在 TWRP 中执行：

```bash
adb push lineage-14.1-20261013-UNOFFICIAL-m7cdug-preview.zip /sdcard/
```

保持 ZIP 原样，不解压。TWRP 的内部存储目录通常对应 `/sdcard`。

## 五、清理 Data/Cache，再安装 ZIP

本版验收使用全新安装基线，建议按以下步骤操作。

### 1. 恢复出厂设置

打开 `Wipe（清除）`，使用默认的 **Swipe to Factory Reset（滑动恢复出厂设置）**。
这会清除应用、账号和设置，并清理 Data/Cache；默认保留内部存储中的 ROM 文件。

**不要选择 System、Internal Storage，也不要使用 Format Data。**
System 中的原厂 NV 必须留到安装器提取完成。

### 2. 安装 ROM

回到 TWRP 首页，打开 `Install（安装）`：

1. 选择内部存储中的 `lineage-14.1-20261013-UNOFFICIAL-m7cdug-preview.zip`。
2. 取消 `Zip signature verification（ZIP 签名验证）`。本开发者预览 ZIP 未签名，校验文件用于确认下载完整性。
3. 滑动 `Swipe to confirm Flash（确认刷入）`。
4. 等待安装结束，确认没有红色错误，显示安装成功。

安装器会保存手机自己的校准数据、写入系统，并安装配套 boot 和 Wi-Fi 模块。
**无需再安装 `.ko` 模块或单独刷 boot。** 如果明确提示 Boot 写入失败，按后面的“补刷 boot”处理。

### 3. 重启系统

点击 `Reboot System（重启系统）`。如果 TWRP 提示安装它的 App 或额外 Root，选择不安装。

## 六、第一次启动与检查

首次启动实测约两分钟。先耐心等待；如果 HTC 标志反复自动重启，按下一节恢复，不把循环重启当成正常等待。

进入 Android 后完成初始设置，再检查：

1. 桌面显示正常，触控可以操作。
2. 设置中开启 WLAN，连接自己的 Wi-Fi，并实际打开网页。
3. 相机中切换前后摄，确认能预览和拍照保存。
4. 重启一次，确认系统可再次启动、Wi-Fi 能重新连接。

当前已验证界面、触控、Wi-Fi 和前后摄；声音播放、蓝牙配对、双卡通话、录像及长期稳定性尚未完成验收。
ROM 不包含 Google 服务或企业微信；这些应用可以另行处理。运行时精简设置也没有打包进此 ROM。

## 七、失败时怎么处理

| 现象 | 下一步 |
| --- | --- |
| ZIP 签名验证失败 | 确认下载哈希正确，再关闭 TWRP 的 ZIP 签名验证 |
| 提示 Wrong device / Wrong MID / Wrong board | 停止安装，核对是否为 802w；不要绕过机型检查 |
| 提示 Own stock NV missing | 恢复这台手机自己的原厂 System 或备份，再安装；不要借用其他手机的 NV |
| 提示 Unsupported firmware version / Unsupported NV layout | 当前原厂材料不匹配此预览版；保存日志并恢复自己的备份 |
| System 写入失败、无法挂载或只读 | 核对专用 TWRP，并在 Mount 取消 System 只读；若已部分写入，先恢复自己的备份 |
| 明确提示 Boot write failed | System 安装完成后，按下方方法从同一个 ZIP 提取并补刷 boot |
| HTC Logo 循环、持续黑屏或不能进入系统 | 重新进入专用 TWRP，恢复刷机前备份 |
| Wi-Fi 已开启但没有连接 | 先关闭再开启 WLAN、重新连接；仍失败则保存日志并恢复备份 |

TWRP 首页选择 `Advanced（高级）→ Copy Log（复制日志）` 保存安装日志，或用电脑执行：

```bash
adb pull /tmp/recovery.log ./recovery-install.log
```

### 仅在 Boot 写入失败时：补刷 boot

boot 已在 ROM ZIP 内，无需另下镜像。Windows 可以在电脑上打开 ZIP，单独提取根目录中的 `boot.img`。
macOS/Linux 可以执行：

```bash
unzip -p lineage-14.1-20261013-UNOFFICIAL-m7cdug-preview.zip boot.img > boot.img
```

本版 `boot.img` 的 SHA-256 为：

```text
938ae5a0eaaf2bf97a7fa1a75df45ac6b9ecfaa095c575bb4df6a01441631d3f
```

手机进入 HBOOT，选择 `FASTBOOT` 并连接电脑。在包含 `boot.img` 的目录执行：

```bash
fastboot devices
fastboot getvar product
```

确认连接的是待刷的 802w，product 为 `m7cdug`，再执行：

```bash
fastboot flash boot boot.img
fastboot reboot
```

正常 ZIP 安装成功时不需要执行这些命令。补刷 boot 不能替代完整 ROM 安装。

### 恢复原系统

1. 进入这台 802w 的专用 TWRP。
2. 打开 `Mount`，取消 `Mount system partition read-only`。
3. 打开 `Restore（恢复）`，选择刷机前自己的备份。
4. 勾选 `Boot / System / Data / Cache`，滑动恢复。
5. 等待成功后重启系统。如果备份已移至电脑，先复制回原来的 `TWRP/BACKUPS/` 目录。

若 Recovery 明确无法恢复 boot，可在电脑 Fastboot 中刷回自己备份的 boot 镜像。本安装器不修改 HBOOT、radio 或 WCNSS 固件分区。

## 八、来源与开发者资料

底包是 [Flyhalf205 的 2017-01-21 M7 Android 7.1.1](https://androidfilehost.com/?fid=673368273298925517)，本项目在该公开底包上加入 802w 适配。打包日期不代表新的 Android 安全补丁。

源码、构建记录和打包细节见仓库中的 `docs/android-integration.md`、`docs/build-verification.json`、`docs/rom-manifest.json` 及 `sources.json`。
