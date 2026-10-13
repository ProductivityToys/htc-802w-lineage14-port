# HTC 802w / m7cdug — Android 7.1 kernel port

Unofficial community port based on LineageOS `cm-14.1` commit
`cb121ea9e86cd51e814cb50048fd64544e672bcc`, with board-level reference code
from zcop/android_kernel_htc_m7c `cm-13.0` commit
`67da107c62e9eabd2d9275b5cad7049262c35310`.

## Tested baseline

The test44 kernel has been tested on one HTC 802w / m7cdug device with Android
7.1.1: display, touch, Wi-Fi auto-connect, front/rear camera preview and JPEG
capture work. SELinux remains Enforcing. Calls, dual SIM, Bluetooth pairing,
audio playback, video recording and long-term stability are not certified.
Do not assume support for 802d, 802t or single-SIM M7 variants.

The kernel/ directory contains the complete current kernel code, including Prima
3.2.3.22, and preserves upstream Git history and copyright notices. See COPYING
and individual files for applicable licenses; the kernel is GPL version 2.

## Build configuration

`arch/arm/configs/m7cdug_test44_defconfig` is the complete configuration copied
from the successful test44 build. The older `m7cdug_defconfig` is retained for
history and must not be substituted for the verified configuration.

Use Android GCC 4.9 from:

```
https://android.googlesource.com/platform/prebuilts/gcc/linux-x86/arm/arm-linux-androideabi-4.9
commit 0390252b6bcc6217966ade31d07f8b12f6f78f89
```

The repository root contains the Dockerfile, build
script, boot repacker, provenance and release checklist. Compile zImage and
wlan.ko together. A new Git commit changes the kernel release string, so a new
kernel must not be paired with the old test42/test44 WLAN module without checking
its ABI and vermagic.

## Ported areas

- M7C board registration, machine type, GSBI2 base and GSBI4 I2C pin selection.
- China panel initialization, PM8921 MPP8 backlight and MPP9/10 LCD power.
- WCNSS GPIO64–68, flashlight GPIO60, 48 MHz XO path, LVS1 RF I/O supply.
- Prima 3.2.3.22 integration and GCC 4.9 build adjustments.
- M7C camera power sequences and RAW_INT0 GPIO58.

Android-side integration is also required: firmware/configuration, WCNSS
bootstrap service, SELinux labeling/policy and hardware_legacy firmware-path
adjustment. This kernel alone does not turn an arbitrary M7 ROM into an 802w ROM.

## Release state

This is a local source snapshot prepared for publication, not an official
LineageOS release. The tested binary was built before this snapshot commit;
freshly built binaries still need device validation. Camera error cleanup paths
inherited from the reference board need review before a broader binary release.
An unused diagnostic header is preserved to keep the working source snapshot
complete; it is not included by the active WCNSS drivers.

The root README is the user entry point. Releases in the same GitHub repository
will contain source previews and future validated ROM downloads. Runtime CFG/INI
are original upstream defaults; untraced experimental replacements are excluded.
Kernel/module code and verified config are retained.
