# HTC 802w ROM developer preview

This is an adapted package of Flyhalf205's Android 7.1.1 M7 build, with this
project's compiled kernel/Prima module and reviewed integration overlays. It
is not an official LineageOS build or a full Android source rebuild.

The original base is [Flyhalf205's 2017-01-21 M7 release](https://androidfilehost.com/?fid=673368273298925517),
MD5 `db369f61f537f04d8dd4d6c5fc6cf7f4`. Packaging dates do not indicate new
Android security patches. Preserve the upstream notices in the system image.

## Supported starting point

- HTC 802w / m7cdug, MID PN0771000, unlocked HBOOT; tested HBOOT 2.49.0000.
- TWRP 3.0.2-0 with its working device-specific kernel.
- Original 802w NV still present in `/system/etc/firmware/wlan/prima/`.
- Original WCNSS partition p18 intact, with the tested firmware version.

The installer checks MID/board, partition labels/sizes, firmware hashes, NV
format and factory MAC **before overwriting system**. Missing/unsupported inputs
abort installation. Do not use this package on 802d, 802t or single-SIM M7.

## Installation

1. Back up boot, system, data and cache with TWRP; copy the backup to a computer.
2. Download the ROM ZIP, supplied boot image, SHA256SUMS and release manifest
   from this project's Releases; verify SHA-256.
3. Enter TWRP. **Do not wipe system first**: the installer must preserve the
   receiving device's original NV. The WCNSS firmware is read from p18, not
   downloaded from the release or written back to the partition.
4. For a clean installation, factory-reset data/cache after backup, keeping
   internal storage. The installer itself never deletes userdata.
5. Install the ZIP in TWRP. This developer preview is unsigned; original upstream
   ZIP signatures were removed rather than left invalid. TWRP ZIP signature
   verification must be off to install this preview.
6. If Recovery cannot write boot on an S-ON device, flash the supplied boot via
   fastboot after the system install. Check `fastboot getvar product` is m7cdug:

   ```bash
   fastboot flash boot boot-m7cdug-preview.img
   fastboot reboot
   ```

7. First boot can take about two minutes because of the existing audio HAL
   initialization delays. Verify display/touch, Wi-Fi and camera before relying
   on the device. Audio/Bluetooth pairing, SIM/calls, video and long-term standby
   remain outside the current validation scope.

## Own-device identity and calibration

The package contains no phone NV, WCNSS firmware executables or trusted ADB keys.
It obtains the factory MAC from the receiving bootloader's `/proc/calibration`,
derives stable local secondary interface addresses, preserves that device's NV,
and copies its own verified WCNSS partition files into the new system.

If system was already erased, restore the original 802w system or the user's
own backup first. Do not substitute another phone's NV or a shared MAC.

Google apps, WeChat/WeCom APKs and personal data are not included. App
compatibility and optional runtime debloat are separate from ROM installation.

## Repack / audit

`scripts/extract_base_system.py` reconstructs a sparse raw ext4 image from the
pinned base ZIP. Use read-only `debugfs` to dump its original library:

```bash
python3 scripts/extract_base_system.py original-base.zip original-system.raw.img
debugfs -R 'dump -p /lib/libhardware_legacy.so libhardware_legacy.original.so' original-system.raw.img
```

`scripts/package_rom.py` validates the base MD5, original library SHA, exact
Broadcom-path transformation, boot kernel hash, same-build module/helper and
zero-address INI template. Supply the patched/verified boot ramdisk seed and
matching build outputs; recompiling kernel/modules requires repacking boot
with that same kernel. The tested boot's policy changes are documented in
`docs/android-integration.md`, and the kernel's complete source remains available.

```bash
python3 scripts/package_rom.py --base original-base.zip --boot matched-boot.img \
  --build-dir matched-build --legacy-lib libhardware_legacy.original.so \
  --output lineage-14.1-UNOFFICIAL-m7cdug-preview.zip
```

The system block data remain byte-identical to the declared public base. Only
declared overlays, boot and guarded installer logic are added. No live phone
system dump is used as the ROM source.

## Rollback

Return to the device-specific TWRP. In Mount, cancel "Mount system partition
read-only" (or swipe "Allow Modifications" when prompted), then restore the
user's own pre-install BSDC
backup. If boot cannot be restored by Recovery, flash the saved boot through
fastboot. The installer does not modify HBOOT, radio or the WCNSS partition.
