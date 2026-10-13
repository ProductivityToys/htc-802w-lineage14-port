#!/usr/bin/env python3
"""Package the declared M7 base with an 802w boot/module and own-device provisioning."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zipfile

BASE_MD5 = 'db369f61f537f04d8dd4d6c5fc6cf7f4'
LEGACY_SHA = '6afebba8ee627b8e44dd833c39474a0ba789be69654ce3e10d64c84c48d13e7a'
OLD_PATH = b'/sys/module/bcmdhd/parameters/firmware_path'


def hash_file(path, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with path.open('rb') as f:
        for data in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ['base', 'boot', 'build-dir', 'legacy-lib', 'output']:
        ap.add_argument('--' + name, required=True, type=Path)
    a = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    if a.output.exists():
        ap.error('Output exists; preserve it or select a new path')
    if hash_file(a.base, 'md5') != BASE_MD5:
        ap.error('Original base ZIP does not match the declared Flyhalf205 release')
    legacy = a.legacy_lib.read_bytes()
    if hashlib.sha256(legacy).hexdigest() != LEGACY_SHA or legacy.count(OLD_PATH) != 1:
        ap.error('Unexpected original hardware_legacy library')
    replacement = b'/dev/null' + b'\0' * (len(OLD_PATH) - len(b'/dev/null'))
    patched = legacy.replace(OLD_PATH, replacement)
    if hashlib.sha256(patched).hexdigest() != '4ab05e4f944e932d76985e33279dd12df75256d815df6c0d0c5709fb58dae0df':
        ap.error('Library transformation did not reproduce the verified patch')
    build = json.loads((a.build_dir/'build.json').read_text())
    module = a.build_dir/'kernel/drivers/staging/prima/wlan.ko'
    helper = a.build_dir/'wcnss-init'
    if hash_file(module) != build['artifacts']['kernel/drivers/staging/prima/wlan.ko']:
        ap.error('Module differs from build manifest')
    if module.stat().st_size >= 8*1024*1024:
        ap.error('Module exceeds bootstrap buffer; strip debugging information first')
    vermagic = [x.decode() for x in module.read_bytes().split(b'\0') if x.startswith(b'vermagic=')]
    if len(vermagic) != 1 or vermagic[0].split()[0] != 'vermagic=' + build['kernel_release']:
        ap.error('Module release mismatch')
    if hash_file(helper) != build['artifacts']['wcnss-init']:
        ap.error('Bootstrap differs from build manifest')
    boot = a.boot.read_bytes()
    if boot[:8] != b'ANDROID!' or len(boot) > 16*1024*1024:
        ap.error('Invalid/oversized boot image')
    kernel_size = struct.unpack_from('<I', boot, 8)[0]
    page = struct.unpack_from('<I', boot, 36)[0]
    if page != 2048 or hashlib.sha256(boot[page:page+kernel_size]).hexdigest() != build['artifacts']['kernel/arch/arm/boot/zImage']:
        ap.error('Boot kernel does not match the same-build WLAN module')
    template = (root/'config/rom/WCNSS_qcom_cfg.template.ini').read_text()
    for key in ['Intf0MacAddress', 'Intf1MacAddress', 'Intf2MacAddress', 'Intf3MacAddress', 'gAPMacAddr']:
        if template.count(key+'=000000000000') != 1:
            ap.error('INI contains an address or missing key')

    script = '''ui_print("HTC 802w / m7cdug Android 7.1.1 developer preview");
ui_print("Preserving this device's own Wi-Fi identity, NV and firmware...");
ifelse(is_mounted("/system"), unmount("/system"));
package_extract_dir("m7c-installer", "/tmp/m7c-installer");
set_metadata_recursive("/tmp/m7c-installer", "uid", 0, "gid", 0, "dmode", 0755, "fmode", 0644);
set_metadata("/tmp/m7c-installer/prepare.sh", "mode", 0755);
set_metadata("/tmp/m7c-installer/restore-inputs.sh", "mode", 0755);
mount("ext4", "EMMC", "/dev/block/mmcblk0p38", "/system", "");
run_program("/tmp/m7c-installer/prepare.sh") == "0" || abort("Wrong device or missing/unsupported original Wi-Fi inputs. System was not overwritten.");
unmount("/system");
show_progress(0.750000, 0);
block_image_update("/dev/block/mmcblk0p38", package_extract_file("system.transfer.list"), "system.new.dat", "system.patch.dat") || abort("System write failed.");
mount("ext4", "EMMC", "/dev/block/mmcblk0p38", "/system", "");
package_extract_dir("m7c-overrides", "/system");
run_program("/tmp/m7c-installer/restore-inputs.sh") == "0" || abort("Device input restore failed.");
set_metadata("/system/bin/wcnss-init", "uid", 0, "gid", 0, "mode", 0755, "selabel", "u:object_r:init_exec:s0");
set_metadata("/system/lib/modules/wlan.ko", "uid", 0, "gid", 0, "mode", 0644, "selabel", "u:object_r:system_file:s0");
set_metadata("/system/lib/libhardware_legacy.so", "uid", 0, "gid", 0, "mode", 0644, "selabel", "u:object_r:system_file:s0");
set_metadata_recursive("/system/etc/firmware", "uid", 0, "gid", 0, "dmode", 0755, "fmode", 0644, "selabel", "u:object_r:system_file:s0");
unmount("/system");
show_progress(0.050000, 5);
package_extract_file("boot.img", "/dev/block/mmcblk0p36") || abort("Boot write failed. Flash supplied boot.img via fastboot.");
set_progress(1.000000);
ui_print("Installed. No userdata wipe was performed.");
'''
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(a.base) as source, zipfile.ZipFile(a.output, 'w', zipfile.ZIP_DEFLATED, compresslevel=1) as dest:
        for info in source.infolist():
            name = info.filename
            if name in ['boot.img', 'META-INF/com/google/android/updater-script', 'META-INF/com/android/metadata']:
                continue
            if name.startswith('META-INF/') and (name in ['META-INF/MANIFEST.MF', 'META-INF/CERT.SF', 'META-INF/CERT.RSA']):
                continue  # Do not carry invalid signatures from a modified upstream ZIP.
            with source.open(info) as src, dest.open(info, 'w') as dst:
                for chunk in iter(lambda: src.read(4*1024*1024), b''):
                    dst.write(chunk)
        dest.writestr('META-INF/com/google/android/updater-script', script)
        dest.writestr('META-INF/com/android/metadata', 'ota-required-cache=0\nota-type=BLOCK\npre-device=m7cdug\n')
        dest.writestr('boot.img', boot)
        dest.writestr('m7c-overrides/lib/libhardware_legacy.so', patched)
        dest.write(module, 'm7c-overrides/lib/modules/wlan.ko')
        dest.write(helper, 'm7c-overrides/bin/wcnss-init')
        dest.write(root/'config/rom/WCNSS_cfg.dat', 'm7c-overrides/etc/firmware/wlan/prima/WCNSS_cfg.dat')
        for src, name in [('scripts/recovery-prepare.sh', 'prepare.sh'),
                          ('scripts/recovery-restore-inputs.sh', 'restore-inputs.sh'),
                          ('config/rom/WCNSS_qcom_cfg.template.ini', 'WCNSS_qcom_cfg.template.ini'),
                          ('config/rom/firmware-SHA256SUMS', 'firmware-SHA256SUMS')]:
            dest.write(root/src, 'm7c-installer/'+name)
    meta = {'filename':a.output.name, 'size':a.output.stat().st_size, 'sha256':hash_file(a.output),
            'base_md5':BASE_MD5, 'kernel_build_commit':build['kernel_commit'],
            'kernel_release':build['kernel_release'], 'boot_sha256':hash_file(a.boot),
            'device_inputs':'Own ATAG MAC, original NV and original p18 firmware; not bundled',
            'signature':'unsigned developer preview; upstream ZIP signatures removed',
            'verification':'pending'}
    a.output.with_suffix('.json').write_text(json.dumps(meta, indent=2)+'\n')
    print(json.dumps(meta, indent=2))


if __name__ == '__main__':
    main()
