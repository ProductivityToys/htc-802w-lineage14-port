#!/sbin/sh
# SPDX-License-Identifier: MIT
# Validate hardware and preserve receiving-device inputs before system writes.
set -eu
PATH=/sbin:/system/bin:/system/xbin
export PATH
WORK=/tmp/m7c-device
FW=/tmp/m7c-firmware
CONFIG=/tmp/m7c-installer
fail() { echo "m7cdug: $*" >&2; exit 1; }

grep -q 'androidboot.mid=PN0771000' /proc/cmdline || fail 'Wrong MID'
grep -q 'board_m7cdug\.' /proc/cmdline || fail 'Wrong board'
[ "$(cat /sys/class/block/mmcblk0p36/size)" = 32768 ] || fail 'Wrong boot layout'
[ "$(cat /sys/class/block/mmcblk0p18/size)" = 10240 ] || fail 'Wrong WCNSS layout'
[ "$(cat /sys/class/block/mmcblk0p38/size)" -ge 3801080 ] || fail 'System too small'
grep -q '^mmcblk0p18:.*"wcnss"' /proc/emmc || fail 'Missing WCNSS partition label'
grep -q '^mmcblk0p36:.*"boot"' /proc/emmc || fail 'Missing boot partition label'
grep -q '^mmcblk0p38:.*"system"' /proc/emmc || fail 'Missing system partition label'

MAC=$(sed -n 's/^macaddr=//p' /proc/calibration | tr -d '\r:' | tr a-f A-F)
[ "${#MAC}" -eq 12 ] || fail 'No unique factory MAC'
case "$MAC" in *[!0-9A-F]*|000000000000|FFFFFFFFFFFF|000AF58989FF) fail 'Invalid factory MAC';; esac
FIRST=$(printf '%s' "$MAC" | cut -c1-2)
[ "$((0x$FIRST & 1))" -eq 0 ] || fail 'Multicast factory MAC'

NV=/system/etc/firmware/wlan/prima/WCNSS_qcom_wlan_nv.bin
[ -f "$NV" ] || fail 'Own stock NV missing; restore original 802w system first'
[ "$(wc -c < "$NV" | tr -d ' ')" = 29776 ] || fail 'Unsupported NV layout'
mkdir -p "$WORK/etc/firmware/wlan/prima" "$FW"
cp "$NV" "$WORK/etc/firmware/wlan/prima/WCNSS_qcom_wlan_nv.bin"
mount -t vfat -o ro /dev/block/mmcblk0p18 "$FW" || fail 'Cannot read own WCNSS firmware'
trap 'umount "$FW" 2>/dev/null || true' EXIT HUP INT TERM
(cd "$FW" && sha256sum -c "$CONFIG/firmware-SHA256SUMS" >/dev/null) || fail 'Unsupported firmware version'
for name in wcnss.mdt wcnss.b00 wcnss.b01 wcnss.b02 wcnss.b04 wcnss.b05; do
    cp "$FW/$name" "$WORK/etc/firmware/$name"
done

# Stable per-device/per-persona locally administered secondary addresses.
derive() {
    VALUE=$(printf '%s:%s' "$MAC" "$1" | sha256sum | cut -c1-12 | tr a-f A-F)
    BYTE=$(printf '%s' "$VALUE" | cut -c1-2)
    PREFIX=$(printf '%02X' "$(( (0x$BYTE | 2) & 254 ))")
    printf '%s%s' "$PREFIX" "$(printf '%s' "$VALUE" | cut -c3-12)"
}
M1=$(derive 1); M2=$(derive 2); M3=$(derive 3); AP=$(derive ap)
[ "$(printf '%s\n' "$MAC" "$M1" "$M2" "$M3" "$AP" | sort -u | wc -l | tr -d ' ')" = 5 ] || fail 'Derived MAC collision'
INI="$WORK/etc/firmware/wlan/prima/WCNSS_qcom_cfg.ini"
sed -e "s/^Intf0MacAddress=.*/Intf0MacAddress=$MAC/" \
    -e "s/^Intf1MacAddress=.*/Intf1MacAddress=$M1/" \
    -e "s/^Intf2MacAddress=.*/Intf2MacAddress=$M2/" \
    -e "s/^Intf3MacAddress=.*/Intf3MacAddress=$M3/" \
    -e "s/^gAPMacAddr=.*/gAPMacAddr=$AP/" \
    "$CONFIG/WCNSS_qcom_cfg.template.ini" > "$INI"
[ "$(grep -c '^Intf[0-3]MacAddress=' "$INI")" = 4 ] || fail 'Bad INI template'
echo 'm7cdug: hardware, own firmware/NV and factory MAC prepared'
