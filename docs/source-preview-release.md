# HTC 802w Android 7.1 — source preview

This release shares the kernel port and build tools behind the tested HTC 802w
Android 7.1.1 system. It is unofficial and intended for developers and testers.

## What has worked on the test device

- Display, touch and full Android startup.
- Wi-Fi automatic loading, network association and DHCP; HTTPS browsing.
- Front/rear camera preview and JPEG capture with the test44 kernel.
- SELinux Enforcing.

## Contents

- Complete kernel source with upstream history retained under kernel/.
- Pinned compiler reference and verified test44 configuration.
- Clean-build script for kernel, matching Prima WLAN module and WCNSS bootstrap.
- Boot repacking tool and Android integration/release checklist.

Source archives and SHA256SUMS identify the local preparation snapshots. The public project is https://github.com/ProductivityToys/htc-802w-lineage14-port;
source previews and future validated ROM downloads share its Releases page.

## Limitations

Only m7cdug / HTC 802w was tested. Audio, Bluetooth pairing, SIM/calls, video
recording and long-term stability have not been fully verified. New builds from
the source snapshot require separate device validation.

There is no complete public ROM in this source preview. The old assembled test42
ZIP contains device-specific data and has not passed a full clean-install test;
it must not be offered as a generic release. Android-side policy/ramdisk/library
patching and firmware extraction still need a reproducible public workflow.

Google apps, WeChat/WeCom packages, user data and private calibration backups
are not supplied. App compatibility is separate from the Android port.
