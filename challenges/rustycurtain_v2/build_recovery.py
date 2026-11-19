"""Instructor builder for the five box-specific deleted JPEG challenges.

Run from this folder with: python3 build_recovery.py
Requires Pillow, mkfs.ext2, and debugfs. Refuses to replace existing images.
The answer key is local and must stay out of student ZIPs.
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
               'lead': 'Night dispatch / Station One', 'decoys': 0, 'color': '#1e5260', 'location': 'ftp', 'artifact': 'dead-drop.img.gz'},
    'tanya':  {'box': 2, 'difficulty': 2, 'theme': 'iron_curtain', 'title': 'TANYA / IRON CURTAIN',
               'lead': 'Field office / Northern circuit', 'decoys': 0, 'color': '#6e3d2e', 'location': 'Desktop', 'artifact': 'iron-curtain.img.gz'},
    'nikoli': {'box': 2, 'difficulty': 3, 'theme': 'switchboard', 'title': 'NIKOLI / SWITCHBOARD',
               'lead': 'Switchboard / Line assignments', 'decoys': 1, 'color': '#31566b', 'location': 'ftp', 'artifact': 'switchboard.img.gz'},
    'boris':  {'box': 3, 'difficulty': 3, 'theme': 'roswell_relay', 'title': 'BORIS / ROSWELL RELAY',
               'lead': 'Roswell relay / Field dispatch', 'decoys': 1, 'color': '#3d4b54', 'location': 'Desktop', 'artifact': 'roswell-relay.img.gz'},
    'yuri':   {'box': 4, 'difficulty': 4, 'theme': 'vostok_telemetry', 'title': 'YURI / VOSTOK TELEMETRY',
               'lead': 'Vostok telemetry / Control desk', 'decoys': 2, 'color': '#1a3357', 'location': 'Desktop', 'artifact': 'vostok-telemetry.img.gz'},
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
        draw.text((310, 193), 'Authorization code', font=body_font, fill='#303030')
        draw.text((310, 233), flag, font=flag_font, fill='#101010')
    else:
        draw.text((310, 193), f'Station copy {decoy_number}', font=body_font, fill='#303030')
        draw.text((310, 233), 'Relay status: awaiting clearance', font=body_font, fill='#303030')
    image.save(path, 'JPEG', quality=75, optimize=True)


def build_one(name, spec, scratch, flag):
    folder = ROOT / name / spec['location']
    cards = []
    for number in range(1, spec['decoys'] + 1):
        path = scratch / f'{name}-station-{number}.jpg'
        card(path, spec, decoy_number=number)
        cards.append(path)
    real = scratch / f'{name}-dispatch.jpg'
    card(real, spec, flag=flag)
    cards.append(real)

    image = scratch / f'{name}-recovery.img'
    with image.open('xb') as stream:
        stream.truncate(8 * 1024 * 1024)
    run('mkfs.ext2', '-q', '-F', '-b', '4096', '-L', f'{name.upper()}_LOG', str(image))
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
    archive = folder / spec['artifact']
    with archive.open('xb') as destination, gzip.GzipFile(filename='', mode='wb', fileobj=destination, mtime=0) as packed:
        packed.write(raw)
    return {'box_value': spec['box'], 'difficulty_value': spec['difficulty'],
            'theme': spec['theme'], 'artifact': str(archive.relative_to(ROOT)), 'flag': flag, 'image_sha256': digest(raw),
            'archive_sha256': digest(archive.read_bytes()), 'deleted_jpeg_sha256': hashes}


def main():
    for name, spec in SPECS.items():
        archive = ROOT / name / spec['location'] / spec['artifact']
        if archive.exists():
            raise RuntimeError(f'{archive} already exists; no files were replaced')
    key = {}
    previous_key = ROOT / 'instructor/previous-recovery-answer-key.json'
    previous = json.loads(previous_key.read_text()) if previous_key.exists() else {}
    with tempfile.TemporaryDirectory(prefix='ctf-recovery-build-') as temporary:
        for name, spec in SPECS.items():
            flag = previous[name]['flag'] if name in previous else f"pps{{{spec['box']}x{spec['difficulty']}_{spec['theme']}_{secrets.token_hex(3)}}}"
            key[name] = build_one(name, spec, Path(temporary), flag)
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
