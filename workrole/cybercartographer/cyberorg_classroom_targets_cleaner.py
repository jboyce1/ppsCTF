#!/usr/bin/env python3
"""Extract unique IPv4 addresses from the instructor's pasted VM inventory."""
import ipaddress
from pathlib import Path
import re
import sys

CLASS = Path(__file__).resolve().parent
SOURCE = CLASS / 'cyberorg_classroom_targets_dirty.txt'
OUTPUT = CLASS / 'cyberorg_classroom_targets.txt'


def extract_addresses(text):
    addresses = []
    seen = set()
    for match in re.finditer(r'(?<![\w.:])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![\w.]|:\w*:)', text):
        try:
            address = str(ipaddress.IPv4Address(match.group()))
        except ipaddress.AddressValueError:
            continue
        if address not in seen:
            seen.add(address)
            addresses.append(address)
    return sorted(addresses, key=ipaddress.IPv4Address)


def main():
    try:
        addresses = extract_addresses(SOURCE.read_text(encoding='utf-8-sig'))
        if not addresses:
            print('No valid IPv4 addresses found; existing output was left unchanged.', file=sys.stderr)
            return 1
        OUTPUT.write_text('\n'.join(addresses) + '\n', encoding='utf-8')
    except OSError as error:
        print(f'Could not clean target list: {error}', file=sys.stderr)
        return 1
    print(f'Saved {len(addresses)} unique IPv4 addresses to {OUTPUT.name}.')
    print('Updated cyberorg_classroom_targets.txt. This does not check whether VMs are up.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
