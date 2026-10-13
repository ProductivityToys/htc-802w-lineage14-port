# HTC 802w · Android 7.1.1

适用于国行联通双卡 HTC One 802w 的非官方 **LineageOS 14.1** ROM，
提供 Android 7.1.1 界面、Wi-Fi 联网和基本相机功能。目前为开发者预览版。

## 功能与兼容性

| 功能 | 状态 |
| --- | --- |
| 系统启动、显示与触控 | 已验证 |
| Wi-Fi 联网、重启后重连 | 已验证 |
| 前后摄预览、JPEG 拍照保存 | 已验证 |
| 声音播放、蓝牙配对、双卡通话、录像、长期待机 | 尚未完成验证 |

仅适用于 **HTC 802w / m7cdug，MID PN0771000**。
已验证的环境为 HBOOT 2.49.0000、UNLOCKED、S-ON、802w 专用 TWRP 3.0.2-0。
802d、802t 和国际单卡 M7 不在支持范围内。

ROM 不包含 Google 服务，所需应用可自行安装。
这是基于旧版 Android 的社区适配，发布打包日期不代表新的安全补丁。

## 下载

**[下载 v0.2.0 ROM](https://github.com/ProductivityToys/htc-802w-lineage14-port/releases/tag/v0.2.0-rom-preview) · [中文刷机指南](docs/rom-install.md)**

| 文件 | 用途 |
| --- | --- |
| ROM ZIP | 完整安装包，必需 |
| SHA256SUMS | ROM 下载校验值，推荐 |
| INSTALL.md | 中文指南的离线副本，可选 |

boot 和 Wi-Fi 模块已内置，**正常安装只刷 ROM ZIP**。
GitHub 自动生成的 `Source code` 附件是源码归档，不能用于刷机。

## 刷机流程

开始前准备好已解锁的 802w 和专用 TWRP，保留这台手机自己的原厂 NV 与无线固件。
完整按键、菜单和命令见 [中文刷机指南](docs/rom-install.md)。

1. 下载并校验 ROM ZIP。
2. 进入 TWRP，在 Mount 取消 **Mount system partition read-only**。
3. 备份 **Boot / System / Data / Cache**，把备份和个人内部存储文件复制到电脑。
4. 将 ROM ZIP 复制到手机内部存储，保持 ZIP 原样。
5. 在 Wipe 使用默认 **Factory Reset** 清理 Data/Cache，这会清除应用、账号和设置。
   **不要擦除 System 或内部存储，也不要使用 Format Data**；安装器需要从 System 保存自己的 Wi-Fi 校准文件。
6. 在 Install 选择 ROM ZIP，关闭 **ZIP 签名验证**，滑动安装。
7. 成功后点击 **Reboot System**。首次启动约两分钟，随后检查触控、Wi-Fi 和前后摄，并重启复验联网。

## 安装失败与恢复

- 提示机型、NV 或无线固件不匹配：停止安装，按指南检查原厂材料。
- 明确提示 boot 写入失败：按指南从同一 ZIP 提取 `boot.img`，使用 Fastboot 补刷。
- HTC 标志循环、持续黑屏或系统写入失败：进入专用 TWRP，取消 System 只读，在 Restore 恢复自己的 **Boot / System / Data / Cache** 备份。

具体处理方式见指南中的 [故障处理与恢复](docs/rom-install.md)。

## 开发者资料与许可

- [源码构建](docs/build.md)
- [Android 集成](docs/android-integration.md)
- [内核移植说明](kernel/PORTING.md)
- [来源与许可](LICENSES.md)

内核按 GPLv2 及文件原许可提供；原创工具和文档采用 MIT。
ROM 底包及 vendor 组件保留原许可，详见来源与许可文档。
