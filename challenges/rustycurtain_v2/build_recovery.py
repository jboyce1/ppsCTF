"""Instructor builder for the five box-specific deleted JPEG challenges.

Run from this folder with: python3 build_recovery.py
Requires Pillow, mkfs.ext2, and debugfs. Refuses to replace existing recovery
folders. The answer key is local and must stay out of student ZIPs.
"""

import gzip
import hashlib
import json
from pathlib import Path
import secrets
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
SPECS = {
    'ivan':   {'box': 1, 'difficulty': 2, 'theme': 'dead_drop', 'title': 'IVAN / DEAD DROP',
               'lead': 'The first FTP handoff vanished.', 'decoys': 0, 'color': '#1e5260', 'location': 'ftp'},
    'tanya':  {'box': 2, 'difficulty': 2, 'theme': 'iron_curtain', 'title': 'TANYA / IRON CURTAIN',
               'lead': 'A field note was erased.', 'decoys': 0, 'color': '#6e3d2e', 'location': 'Desktop'},
    'nikoli': {'box': 2, 'difficulty': 3, 'theme': 'switchboard', 'title': 'NIKOLI / SWITCHBOARD',
               'lead': 'One relay order is a decoy.', 'decoys': 1, 'color': '#31566b', 'location': 'ftp'},
    'boris':  {'box': 3, 'difficulty': 3, 'theme': 'roswell_relay', 'title': 'BORIS / ROSWELL RELAY',
               'lead': 'One report was planted.', 'decoys': 1, 'color': '#3d4b54', 'location': 'Desktop'},
    'yuri':   {'box': 4, 'difficulty': 4, 'theme': 'vostok_telemetry', 'title': 'YURI / VOSTOK TELEMETRY',
               'lead': 'Two telemetry sheets mislead.', 'decoys': 2, 'color': '#1a3357', 'location': 'Desktop'},
}


def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def digest(data):
    return hashlib.sha256(data).hexdigest()


def card(path, spec, flag=None, decoy_number=None):
    image = Image.new('RGB', (800, 400), '#eee8d9')
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 285, 399), fill=spec['color'])
    draw.line((48, 285, 130, 190, 230, 230), fill='#cbd9d7', width=4)
    for x, y in ((48, 285), (130, 190), (230, 230)):
        draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill='#f2d48a')
    title_font = ImageFont.truetype(FONT, 23)
    body_font = ImageFont.truetype(FONT, 17)
    flag_font = ImageFont.truetype(FONT, 16)
    draw.text((310, 58), spec['title'], font=title_font, fill='#202020')
    draw.text((310, 115), spec['lead'], font=body_font, fill='#303030')
    if flag:
        draw.text((310, 193), 'RECOVERED ROUTE FLAG', font=body_font, fill='#303030')
        draw.text((310, 233), flag, font=flag_font, fill='#101010')
    else:
        draw.text((310, 193), f'DECOY SHEET {decoy_number}', font=body_font, fill='#303030')
        draw.text((310, 233), 'No route flag on this sheet.', font=body_font, fill='#303030')
    image.save(path, 'JPEG', quality=75, optimize=True)


def build_one(name, spec, scratch):
    folder = ROOT / name / spec['location'] / 'recovery'
    folder.mkdir(parents=True, exist_ok=False)
    flag = f"pps{{{spec['box']}x{spec['difficulty']}_{spec['theme']}_{secrets.token_hex(3)}}}"
    cards = []
    for number in range(1, spec['decoys'] + 1):
        path = scratch / f'{name}-decoy-{number}.jpg'
        card(path, spec, decoy_number=number)
        cards.append(path)
    real = scratch / f'{name}-route.jpg'
    card(real, spec, flag=flag)
    cards.append(real)

    image = scratch / f'{name}-recovery.img'
    with image.open('xb') as stream:
        stream.truncate(8 * 1024 * 1024)
    run('mkfs.ext2', '-q', '-F', '-b', '4096', '-L', f'CTF_{name.upper()}', str(image))
    hashes = {}
    for path in cards:
        run('debugfs', '-w', '-R', f'write {path} /{path.name}', str(image))
        listing = run('debugfs', '-R', 'ls -l /', str(image))
        if path.name not in listing:
            raise RuntimeError(f'{name}: write failed for {path.name}')
        hashes[path.name] = digest(path.read_bytes())
    for path in cards:
        run('debugfs', '-w', '-R', f'rm /{path.name}', str(image))
    listing = run('debugfs', '-R', 'ls -l /', str(image))
    if any(path.name in listing for path in cards):
        raise RuntimeError(f'{name}: deletion failed')
    raw = image.read_bytes()
    archive = folder / 'recovery.img.gz'
    with archive.open('xb') as destination, gzip.GzipFile(filename='', mode='wb', fileobj=destination, mtime=0) as packed:
        packed.write(raw)
    return {'box_value': spec['box'], 'difficulty_value': spec['difficulty'],
            'theme': spec['theme'], 'flag': flag, 'image_sha256': digest(raw),
            'archive_sha256': digest(archive.read_bytes()), 'deleted_jpeg_sha256': hashes}


def main():
    for name, spec in SPECS.items():
        folder = ROOT / name / spec['location'] / 'recovery'
        if folder.exists():
            raise RuntimeError(f'{folder} already exists; no files were replaced')
    key = {}
    with tempfile.TemporaryDirectory(prefix='ctf-recovery-build-') as temporary:
        for name, spec in SPECS.items():
            key[name] = build_one(name, spec, Path(temporary))
    private = ROOT / 'instructor'
    private.mkdir(exist_ok=True)
    answer_key = private / 'recovery-answer-key.json'
    with answer_key.open('x') as stream:
        json.dump(key, stream, indent=2)
        stream.write('\n')
    print('Built five box-specific deleted-file images.')
    print('Keep instructor/recovery-answer-key.json private and out of all ZIPs.')


if __name__ == '__main__':
    main()
