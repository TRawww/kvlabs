#!/usr/bin/env python3
import gzip, hashlib, io, lzma, tarfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEBS = ROOT / 'debs'

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def _ar_members(path):
    data = path.read_bytes()
    if not data.startswith(b'!<arch>\n'):
        raise ValueError(f'{path} is not an ar/deb archive')
    pos = 8
    while pos + 60 <= len(data):
        header = data[pos:pos+60]
        pos += 60
        name = header[:16].decode('utf-8', 'replace').strip().rstrip('/')
        size = int(header[48:58].decode().strip())
        payload = data[pos:pos+size]
        pos += size + (size % 2)
        yield name, payload

def control(deb):
    control_payload = None
    control_name = None
    for name, payload in _ar_members(deb):
        if name.startswith('control.tar'):
            control_name = name
            control_payload = payload
            break
    if control_payload is None:
        raise SystemExit(f'failed reading {deb}: missing control.tar member')
    if control_name.endswith('.xz'):
        control_payload = lzma.decompress(control_payload)
        mode = 'r:'
    elif control_name.endswith('.gz'):
        mode = 'r:gz'
    else:
        mode = 'r:'
    with tarfile.open(fileobj=io.BytesIO(control_payload), mode=mode) as tf:
        try:
            f = tf.extractfile('./control') or tf.extractfile('control')
        except KeyError:
            f = None
        if f is None:
            raise SystemExit(f'failed reading {deb}: control file not found')
        return f.read().decode('utf-8').strip()

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
