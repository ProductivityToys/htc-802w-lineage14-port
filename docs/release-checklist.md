# Developer preview release checklist

Public project checklist. Remaining checks below define the limits of the developer preview.

## Source preview

- [x] Preserve complete kernel upstream history; correct the first snapshot's Prima source.
- [x] Record upstream/reference/toolchain commits and complete verified config.
- [x] Separate public toolkit from private logs, calibration and tested images.
- [x] Supply WCNSS bootstrap source and boot repacking tool.
- [x] Complete clean kernel + WLAN + helper build and record results.
- [x] Verify source archive content and hashes; keep build outputs outside Git.
- [x] Keep reference runtime CFG/INI; use a separate zero-MAC installer template.
- [x] Use zee / GitHub noreply attribution in ProductivityToys/htc-802w-lineage14-port.
- [x] Public repository URL fixed; v0.1.0-source historical tag retained with explicit Prima correction; redundant Release removed.

## Binary preview

- [ ] Review camera GPIO/regulator error cleanup and retest any changed code.
- [x] Correct Prima 3.2.3.22 source, strip debug info; verify same-release kernel/module on device.
- [ ] Inventory boot ramdisk, HAL, firmware and system components / licenses.
- [x] Provide guarded original-library patch and own-device firmware extraction.
- [ ] Reconstruct complete Android build manifest and ramdisk policy generation from source.
- [x] Extract receiving-device factory MAC/NV/firmware before system writes.
- [x] Assert board/MID, partition labels/sizes and firmware hashes before writes.
- [x] Test installation after clean data/cache; reflash final complete ZIP and verify.
- [x] Verify display/touch, Wi-Fi/DHCP/reconnect and front+rear JPEG; other HW remains untested.
- [x] Base system remains byte-identical to public original; private device blobs/keys excluded.
- [x] Prepare SHA256SUMS, source commit mapping, release notes and rollback guide.
- [x] Mark first ROM Unofficial / Developer Preview with exact supported model.

## GitHub workflow

Keep source in Git and large binaries in Releases. First prepare the exact local
repository, commits and artifacts; review them before creating public remotes
or uploading. A source-only preview may precede a ROM preview, with the remaining
binary work stated plainly. Never label the old test42 ZIP as the new test44 ROM.
