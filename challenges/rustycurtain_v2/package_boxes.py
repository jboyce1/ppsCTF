"""Build and verify the five box ZIPs from this v2 source tree.

Run only after verify_recovery.py passes. Original rustycurtain ZIPs are never
opened for writing. Instructor answer keys and build tools are not included.
"""

from pathlib import Path
import hashlib
import os
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parent
BOXES = ('ivan', 'tanya', 'nikoli', 'boris', 'yuri')


def package():
    with tempfile.TemporaryDirectory(prefix='ctf-boxes-', dir=ROOT) as temporary:
        temporary = Path(temporary)
        for box in BOXES:
            source = ROOT / box
            files = sorted(path for path in source.rglob('*') if path.is_file() and '__pycache__' not in path.parts)
            if not files:
                raise RuntimeError(f'{box}: no source files')
            archive = temporary / f'{box}.zip'
            with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as output:
                for path in files:
                    output.write(path, path.relative_to(ROOT).as_posix())
            with zipfile.ZipFile(archive) as check:
                if check.testzip() is not None:
                    raise RuntimeError(f'{box}: ZIP CRC failure')
                expected = {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in files}
                if set(check.namelist()) != set(expected):
                    raise RuntimeError(f'{box}: missing or extra ZIP members')
                for name, data in expected.items():
                    if check.read(name) != data:
                        raise RuntimeError(f'{box}: member bytes differ: {name}')
            print(f'PASS {box}: {len(files)} ZIP members match source')
        for box in BOXES:
            os.replace(temporary / f'{box}.zip', ROOT / f'{box}.zip')
    checksums = []
    for box in BOXES:
        archive = ROOT / f'{box}.zip'
        checksums.append(f"{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}")
    (ROOT / 'ZIP_SHA256SUMS.txt').write_text('\n'.join(checksums) + '\n')
    print('Updated only rustycurtain_v2 ZIPs.')


if __name__ == '__main__':
    package()
