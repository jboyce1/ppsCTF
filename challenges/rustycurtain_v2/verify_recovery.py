"""Verify every box's deleted-file challenge without changing the originals.

Usage: python3 verify_recovery.py [SCALPEL_BINARY]
Requires the local instructor/recovery-answer-key.json from build_recovery.py.
"""

import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image


ROOT = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify(scalpel):
    key = json.loads((ROOT / 'instructor/recovery-answer-key.json').read_text())
    with tempfile.TemporaryDirectory(prefix='ctf-recovery-check-') as tmp:
        tmp = Path(tmp)
        for box, entry in key.items():
            place = 'ftp' if box in {'ivan', 'nikoli'} else 'Desktop'
            folder = ROOT / box / place / 'recovery'
            archive = folder / 'recovery.img.gz'
            packed = archive.read_bytes()
            assert digest(packed) == entry['archive_sha256'], box
            raw = gzip.decompress(packed)
            assert len(raw) == 8 * 1024 * 1024, box
            assert digest(raw) == entry['image_sha256'], box
            assert entry['flag'].encode() not in raw, f'{box}: flag readable without carving'
            image = tmp / f'{box}.img'
            image.write_bytes(raw)
            listing = subprocess.run(['debugfs', '-R', 'ls -l /', str(image)],
                                     check=True, capture_output=True, text=True).stdout
            assert all(name not in listing for name in entry['deleted_jpeg_sha256']), box
            recovered = tmp / f'{box}-recovered'
            subprocess.run([scalpel, '-c', str(folder / 'scalpel-jpg.conf'),
                            '-o', str(recovered), str(image)], check=True, capture_output=True)
            pictures = list(recovered.rglob('*.jpg'))
            actual = sorted(digest(p.read_bytes()) for p in pictures)
            expected = sorted(entry['deleted_jpeg_sha256'].values())
            assert actual == expected, (box, actual, expected)
            for path in pictures:
                with Image.open(path) as opened:
                    opened.verify()
            assert entry['flag'].startswith(f"pps{{{entry['box_value']}x{entry['difficulty_value']}_"), box
            print(f"PASS {box}: {len(pictures)} deleted JPEG(s), exact bytes, {entry['box_value']}x{entry['difficulty_value']} flag")


if __name__ == '__main__':
    verify(sys.argv[1] if len(sys.argv) > 1 else 'scalpel')
