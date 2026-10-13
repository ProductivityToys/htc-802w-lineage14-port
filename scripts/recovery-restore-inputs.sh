#!/sbin/sh
# SPDX-License-Identifier: MIT
set -eu
PATH=/sbin:/system/bin:/system/xbin
export PATH
[ -s /tmp/m7c-device/etc/firmware/wlan/prima/WCNSS_qcom_wlan_nv.bin ]
[ -s /tmp/m7c-device/etc/firmware/wlan/prima/WCNSS_qcom_cfg.ini ]
cp -R /tmp/m7c-device/etc/firmware/. /system/etc/firmware/
chown 0:0 /system/etc/firmware/wcnss.* /system/etc/firmware/wlan/prima/WCNSS_qcom_cfg.ini /system/etc/firmware/wlan/prima/WCNSS_qcom_wlan_nv.bin
chmod 644 /system/etc/firmware/wcnss.* /system/etc/firmware/wlan/prima/WCNSS_qcom_cfg.ini /system/etc/firmware/wlan/prima/WCNSS_qcom_wlan_nv.bin
echo 'm7cdug: own device inputs restored'
