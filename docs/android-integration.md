# Android integration: remaining work before a public ROM

The kernel is only one part of the tested system. The tested base is
`lineage-14.1-20170121-UNOFFICIAL-m7.zip`; its complete Android build manifest
and original distributor/provenance still need to be established. Do not claim
that this project currently builds a full ROM from Android source.

## Required components

| Component | Tested integration | Publication approach |
| --- | --- | --- |
| boot kernel | test44 with original Android ramdisk | build from kernel/ source; pair with same-build wlan.ko |
| wlan.ko | Prima 3.2.3.22 | included source; freshly build alongside kernel |
| wcnss-init | ARM EABI legacy init_module bootstrap | source supplied here; compile with pinned GCC |
| init trigger | post-fs-data exec runs /system/bin/wcnss-init as init/root | exact tested fragment in config/wcnss-bootstrap.rc; integrate once into the target init.rc |
| file label / policy | wcnss-init labeled init_exec; init execute_no_trans | provide reviewed policy source / exact guarded transformation |
| hardware_legacy | Broadcom firmware path redirected to /dev/null | provide guarded patch tool with input hash and exact bytes; provenance pending |
| WCNSS config | Prima CFG and INI | separate shared model settings from per-device MAC |
| firmware / NV | original-device files | identify licenses and extraction sources; preserve each device's calibration |
| camera HAL | existing M7 wrapper / proprietary camera stack | inventory source and binary provenance |

The publication draft does not contain the original ROM, firmware, NV, HAL,
patched library, ramdisk or tested boot image. Those inputs must be reviewed
before being accepted as Release assets.

The boot was inspected directly: bootstrap is a blocking `exec` in
`on post-fs-data`, not an independently running daemon. The fragment then sets
`wlan.driver.status=ok`; this property alone is not proof of success. Verify
helper exit behavior, the loaded module, wlan0 and actual network association.

## Device-specific data

The private test42 packer injects one device's `WCNSS_qcom_cfg.ini` and NV.
The private staging script also writes an ADB authorized key. Neither script
is imported here. Do not replace these with an arbitrary shared MAC or assume
all NV files are interchangeable.

Before packaging: determine the original-device MAC/calibration source and
extraction timing, validate firmware/model variants, then derive INI entries
from the receiving device. Reject missing/invalid device inputs. Never import
adb_keys, Wi-Fi passwords, app data, accounts or private recovery backups.

## Install and recovery design

- Assert m7cdug / verified device identity; do not remove the M7 assertion and
  call the result a supported package. Investigate Recovery identity differences
  before designing the exact checks.
- Inspect partition layout/sizes before any write. Use the verified p36/p38/p39/
  p40 layout only after matching the target device.
- Generate a clean system image from declared inputs, with labels and policy
  restored; never package a live `/system` dump with installed Google or user apps.
- Keep Google apps and the optional runtime debloat profile separate. Preserve
  sound/Bluetooth components. Do not alter animation settings as a speed tweak.
- Factory reset requires a clear installation step and explicit operator action;
  no automatic data deletion in the build script.
- Verify the complete ZIP from clean install and reboot; preserve rollback
  instructions and test Recovery access.

Replacing only boot on an arbitrary M7 installation is not a complete port.
