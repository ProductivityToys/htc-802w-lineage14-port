#!/usr/bin/env python3
"""Decode this project's pinned full block OTA to a sparse raw ext4 image."""
import argparse
import hashlib
from pathlib import Path
import zipfile


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('base', type=Path)
    ap.add_argument('output', type=Path)
    a = ap.parse_args()
    if a.output.exists():
        ap.error('Output exists')
    h = hashlib.md5()
    with a.base.open('rb') as f:
        for b in iter(lambda: f.read(4*1024*1024), b''):
            h.update(b)
    if h.hexdigest() != 'db369f61f537f04d8dd4d6c5fc6cf7f4':
        ap.error('Wrong original ROM')
    with zipfile.ZipFile(a.base) as z:
        lines = z.read('system.transfer.list').decode().splitlines()
        if lines[0] != '4':
            ap.error('Unsupported transfer version')
        commands = []
        for line in lines[4:]:
            op, values = line.split()
            if op not in ['new', 'erase', 'zero']:
                ap.error('Expected full OTA, not an incremental update')
            nums = [int(n) for n in values.split(',')]
            if nums[0] != len(nums)-1 or nums[0] % 2:
                ap.error('Invalid range count')
            pairs = list(zip(nums[1::2], nums[2::2]))
            if any(s < 0 or s >= e for s, e in pairs):
                ap.error('Invalid range bounds')
            commands.append((op, pairs))
        total = max(e for _, pairs in commands for _, e in pairs)*4096
        a.output.parent.mkdir(parents=True, exist_ok=True)
        with a.output.open('wb') as out, z.open('system.new.dat') as data:
            out.truncate(total)
            for op, pairs in commands:
                if op != 'new':
                    continue
                for start, end in pairs:
                    out.seek(start*4096)
                    remaining = (end-start)*4096
                    while remaining:
                        chunk = data.read(min(4*1024*1024, remaining))
                        if not chunk:
                            raise ValueError('Truncated system.new.dat')
                        out.write(chunk)
                        remaining -= len(chunk)
            if data.read(1):
                raise ValueError('Unused system.new.dat bytes')
    print('Decoded raw image bytes:', total)


if __name__ == '__main__':
    main()
