#!/usr/bin/env python3
"""Build a clean HTC 802w kernel, matching WLAN module and WCNSS bootstrap."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--kernel', type=Path, default=Path(__file__).resolve().parents[1]/'kernel')
    ap.add_argument('--toolchain', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--image', default='htc-kernel-builder:18.04')
    ap.add_argument('--jobs', type=int, default=3)
    a = ap.parse_args()
    kernel, tc, out = a.kernel.resolve(), a.toolchain.resolve(), a.output.resolve()
    kit = Path(__file__).resolve().parents[1]
    repo = Path(subprocess.check_output(['git','-C',str(kernel),'rev-parse','--show-toplevel'], text=True).strip()).resolve()
    if repo != kit or kernel != repo/'kernel':
        ap.error('Use the bundled kernel/ directory in a Git clone of this project')
    if out.exists() and any(out.iterdir()):
        ap.error('Output must be empty; existing results will not be overwritten')
    if not 1 <= a.jobs <= 8:
        ap.error('Jobs must be between 1 and 8')
    if not (tc/'bin/arm-linux-androideabi-gcc').is_file():
        ap.error('Missing toolchain GCC executable')
    if not (kernel/'arch/arm/configs/m7cdug_test44_defconfig').is_file():
        ap.error('Missing verified build configuration')
    expected = json.loads((kit/'sources.json').read_text())['toolchain']['commit']
    actual = subprocess.check_output(['git','-C',str(tc),'rev-parse','HEAD'], text=True).strip()
    if actual != expected:
        ap.error('Toolchain commit does not match sources.json')
    out.mkdir(parents=True, exist_ok=True)
    (out/'kernel').mkdir()
    shell = r'''set -euo pipefail
cp /repository/.git/index /output/source-index
export GIT_INDEX_FILE=/output/source-index
# Refresh container stat data without writing the read-only source Git index.
git -C /repository update-index --refresh
# Linux 3.4 setlocalversion expects the kernel at the Git root. Our kernel/ is
# nested, so supply the project revision explicitly without changing .config.
port_revision="$(git -C /repository rev-parse --short=8 HEAD)"
if ! git -C /repository diff-index --quiet HEAD --; then
  port_revision="${port_revision}-dirty"
fi
export LOCALVERSION="-g${port_revision}"
export ARCH=arm CROSS_COMPILE=/toolchain/bin/arm-linux-androideabi-
make -C /repository/kernel O=/output/kernel m7cdug_test44_defconfig
make -C /repository/kernel O=/output/kernel -j"$1" zImage modules
"${CROSS_COMPILE}strip" --strip-debug /output/kernel/drivers/staging/prima/wlan.ko
test "$(stat -c %s /output/kernel/drivers/staging/prima/wlan.ko)" -lt 8388608
"${CROSS_COMPILE}gcc" -marm -Os -fno-pic -fno-pie -fno-stack-protector \
  -nostdlib -nostartfiles -static -Wl,-e,_start -Wl,--build-id=none \
  /repository/src/wcnss-init.c -o /output/wcnss-init
"${CROSS_COMPILE}readelf" -h /output/wcnss-init
'''
    cmd = ['docker','run','--rm','--platform','linux/amd64',
           '--cpus',str(a.jobs),'--memory','3g',
           '-v',str(repo)+':/repository:ro','-v',str(tc)+':/toolchain:ro',
           '-v',str(out)+':/output',
           a.image,'bash','-lc',shell,'build',str(a.jobs)]
    with (out/'build.log').open('wb') as log:
        r = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
    if r.returncode:
        raise SystemExit('Build failed; inspect '+str(out/'build.log'))
    files = ['kernel/arch/arm/boot/zImage',
             'kernel/drivers/staging/prima/wlan.ko','kernel/.config','wcnss-init']
    hashes = {p:sha256(out/p) for p in files}
    (out/'SHA256SUMS').write_text(''.join(f'{h}  {p}\n' for p,h in hashes.items()))
    state = subprocess.check_output(['git','-C',str(kernel),'status','--porcelain'],text=True)
    meta = {
        'kernel_commit':subprocess.check_output(['git','-C',str(kernel),'rev-parse','HEAD'],text=True).strip(),
        'kernel_dirty':bool(state), 'toolchain_commit':actual,
        'kernel_release':(out/'kernel/include/config/kernel.release').read_text().strip(),
        'docker_image':a.image,
        'docker_image_id':subprocess.check_output(['docker','image','inspect',a.image,'--format','{{.Id}}'],text=True).strip(),
        'artifacts':hashes, 'device_validation':'pending',
    }
    (out/'build.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps(meta,indent=2))


if __name__ == '__main__':
    main()
