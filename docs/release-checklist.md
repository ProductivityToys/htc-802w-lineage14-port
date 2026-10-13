# Developer preview release checklist

Source preview checklist for the merged public project. Binary ROM work remains below.

## Source preview

- [x] Preserve complete kernel upstream history and test44 working source.
- [x] Record upstream/reference/toolchain commits and complete verified config.
- [x] Separate public toolkit from private logs, calibration and tested images.
- [x] Supply WCNSS bootstrap source and boot repacking tool.
- [x] Complete clean kernel + WLAN + helper build and record results.
- [x] Verify source archive content and hashes; keep build outputs outside Git.
- [x] Keep original upstream runtime CFG/INI; exclude untraced experimental replacements.
- [x] Use zee / GitHub noreply attribution in ProductivityToys/htc-802w-lineage14-port.
- [x] Public repository URL fixed; release tag v0.1.0-source is prepared for publication.

## Binary preview

- [ ] Review camera GPIO/regulator error cleanup and retest any changed code.
- [ ] Match kernel and WLAN vermagic; verify freshly built binaries on device.
- [ ] Inventory boot ramdisk, HAL, firmware and system components / licenses.
- [ ] Provide reproducible Android-side patches and firmware extraction.
- [ ] Handle each device's own MAC / calibration without leaking the test device.
- [ ] Assert device/partition identity in the installer.
- [ ] Build ROM including camera changes, then test a full clean installation.
- [ ] Verify display/touch/Wi-Fi/front+rear JPEG after reboot; document untested HW.
- [ ] Inspect for ADB keys, Wi-Fi credentials, accounts, app data and signing keys.
- [ ] Attach SHA256SUMS, source commit mapping, release notes and rollback guide.
- [ ] Mark first build Unofficial / Developer Preview with exact supported model.

## GitHub workflow

Keep source in Git and large binaries in Releases. First prepare the exact local
repository, commits and artifacts; review them before creating public remotes
or uploading. A source-only preview may precede a ROM preview, with the remaining
binary work stated plainly. Never label the old test42 ZIP as the new test44 ROM.
