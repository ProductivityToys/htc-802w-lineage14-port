#!/usr/bin/env python3
"""Replace a kernel in the verified HTC boot v0 image and update its SHA-1 ID."""

import hashlib
import json
from pathlib import Path
import struct
import sys


def repack(original, kernel_path, output):
    source = Path(original).read_bytes()
    kernel = Path(kernel_path).read_bytes()
    if source[:8] != b"ANDROID!":
        raise ValueError("Not an Android boot image")
    old_kernel_size, _, ramdisk_size, _, second_size, _, _, page, dt_size, _ = (
        struct.unpack_from("<10I", source, 8)
    )
    if page != 2048 or second_size or dt_size:
        raise ValueError("Requires the verified 2048-byte-page, kernel+ramdisk layout")
    ramdisk_offset = page * (1 + (old_kernel_size + page - 1) // page)
    ramdisk = source[ramdisk_offset:ramdisk_offset + ramdisk_size]
    if not kernel or len(ramdisk) != ramdisk_size:
        raise ValueError("Empty kernel or truncated ramdisk")
    header = bytearray(source[:page])
    struct.pack_into("<I", header, 8, len(kernel))
    image_id = hashlib.sha1(
        kernel + struct.pack("<I", len(kernel))
        + ramdisk + struct.pack("<I", len(ramdisk))
        + struct.pack("<I", 0)
    ).digest()
    header[576:608] = image_id + b"\0" * 12

    def padded(data):
        return data + b"\0" * (-len(data) % page)

    image = bytes(header) + padded(kernel) + padded(ramdisk)
    if len(image) > 16 * 1024 * 1024:
        raise ValueError("Image exceeds the 16 MiB boot partition")
    if Path(output).resolve() in {Path(original).resolve(), Path(kernel_path).resolve()}:
        raise ValueError("Output must not overwrite an input")
    Path(output).write_bytes(image)
    print(json.dumps({
        "size": len(image),
        "sha256": hashlib.sha256(image).hexdigest(),
        "ramdisk_sha256": hashlib.sha256(ramdisk).hexdigest(),
    }, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: repack_camera_boot.py original_boot.img zImage output.img")
    repack(*sys.argv[1:])
