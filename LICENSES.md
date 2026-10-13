# Licenses and provenance

- Bundled kernel/ source: Linux GPL version 2, with individual file notices
  preserved. Prima has file-level ISC notices and declares Dual BSD/GPL as a
  module; consult each file rather than relabeling all code as MIT.
- Toolkit original Python scripts, WCNSS bootstrap, Dockerfile and original
  documentation: MIT, see LICENSES/MIT.txt. WCNSS bootstrap was authored for this port.
- Original Android ROM, hardware_legacy library, HTC / Qualcomm firmware and
  camera HAL: external inputs, not covered by this toolkit's MIT license and
  not included as Git source files. ROM Release assets retain the declared
  public base system and its vendor HAL; the new toolkit MIT license does not
  cover these components. Comprehensive vendor redistribution licensing has
  not been established. Preserve all upstream notices.
- GCC toolchain: external pinned dependency; its own COPYING / NOTICE files
  apply. It is not bundled with the toolkit.
- Upstream kernel history and author notices must remain intact. If kernel or
  WLAN module binaries are distributed, publish their corresponding complete
  source/configuration/build scripts at the same release and identify commits.

This file records the intended separation of materials; it does not relicense
upstream or proprietary components.

## Imported runtime configuration

The corrected public kernel/ tree imports Prima 3.2.3.22 and its CFG/INI files
from the reference commit `67da107c62e9eabd2d9275b5cad7049262c35310`, preserving
upstream notices and COPYING. The v0.1.0-source tag retained an earlier
experimental driver; see the correction in README.
These runtime configuration files are not compiled into zImage or wlan.ko.
They are not a tested 802w installation configuration; receiving devices need
their own configuration/MAC/calibration workflow implemented by the ROM installer.
Unchanged upstream example files and firmware for unrelated drivers remain part
of inherited kernel source/history under their original licensing; this preview
does not add the phone's factory WCNSS firmware, NV, HAL or backup.

## ROM packaging inputs

The adapted ROM retains Flyhalf205's original system image and notices, with
declared overlays. Original base MD5: db369f61f537f04d8dd4d6c5fc6cf7f4.
The helper/packager scripts are MIT; this grant does not relicense the original
ROM, ramdisk or vendor HAL. config/rom/WCNSS_cfg.dat is imported from the GPLv2
reference kernel repository at 67da107c62e9eabd2d9275b5cad7049262c35310; provenance
is in config/rom/sources.json. The INI template omits all device MAC values.
The receiving device supplies its own NV and WCNSS firmware at install time.
