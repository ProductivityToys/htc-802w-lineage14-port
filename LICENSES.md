# Licenses and provenance

- Bundled kernel/ source: Linux GPL version 2, with individual file notices
  preserved. Prima has file-level ISC notices and declares Dual BSD/GPL as a
  module; consult each file rather than relabeling all code as MIT.
- Toolkit original Python scripts, WCNSS bootstrap, Dockerfile and original
  documentation: MIT, see LICENSE. WCNSS bootstrap was authored for this port.
- Original Android ROM, hardware_legacy library, HTC / Qualcomm firmware and
  camera HAL: external inputs, not covered by this toolkit's MIT license and
  not included in this repository. Availability elsewhere does not establish
  permission to redistribute; inventory and review before any binary ROM release.
- GCC toolchain: external pinned dependency; its own COPYING / NOTICE files
  apply. It is not bundled with the toolkit.
- Upstream kernel history and author notices must remain intact. If kernel or
  WLAN module binaries are distributed, publish their corresponding complete
  source/configuration/build scripts at the same release and identify commits.

This file records the intended separation of materials; it does not relicense
upstream or proprietary components.

## Imported runtime configuration

The public kernel/ tree keeps the original LineageOS base CFG/INI files from
`cb121ea9e86cd51e814cb50048fd64544e672bcc`, with upstream notices and COPYING
preserved. Untraced experimental replacements are excluded from this preview.
These runtime configuration files are not compiled into zImage or wlan.ko.
They are not a tested 802w installation configuration; receiving devices need
their own reviewed configuration/MAC/calibration workflow before a binary ROM.
Unchanged upstream example files and firmware for unrelated drivers remain part
of inherited kernel source/history under their original licensing; this preview
does not add the phone's factory WCNSS firmware, NV, HAL or backup.
