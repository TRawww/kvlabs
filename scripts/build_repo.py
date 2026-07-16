#!/usr/bin/env python3
import gzip, hashlib, subprocess, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEBS = ROOT / 'debs'

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def control(deb):
    try:
        out = subprocess.check_output(['dpkg-deb', '-f', str(deb)], text=True)
    except Exception as e:
        raise SystemExit(f'failed reading {deb}: {e}\nInstall dpkg-deb or build on a system with dpkg.')
    return out.strip()

entries = []
for deb in sorted(DEBS.glob('*.deb')):
    rel = deb.relative_to(ROOT).as_posix()
    meta = control(deb)
    if not meta.endswith('\n'):
        meta += '\n'
    meta += f'Filename: {rel}\nSize: {deb.stat().st_size}\nSHA256: {sha256(deb)}\n'
    entries.append(meta)

packages = '\n'.join(entries)
(ROOT / 'Packages').write_text(packages)
with gzip.open(ROOT / 'Packages.gz', 'wb', compresslevel=9) as gz:
    gz.write(packages.encode())

release = (
    'Origin: KVLabs\n'
    'Label: KVLabs\n'
    'Suite: stable\n'
    'Version: 1.0\n'
    'Codename: kvlabs\n'
    'Architectures: iphoneos-arm\n'
    'Components: main\n'
    'Description: KVLabs iOS jailbreak packages\n'
    f"Date: {time.strftime('%a, %d %b %Y %H:%M:%S %z')}\n"
)
(ROOT / 'Release').write_text(release)
print(f'wrote {len(entries)} package entries')
