#!/usr/bin/env python3
"""Extract unique IPv4 addresses from the instructor's pasted VM inventory."""
import ipaddress
from pathlib import Path
import re
import sys
import webbrowser

CLASS = Path(__file__).resolve().parent
SOURCE = CLASS / 'cyberorg_classroom_targets_dirty.txt'
OUTPUT = CLASS / 'cyberorg_classroom_targets.txt'
EDIT_URL = 'https://github.com/jboyce1/ppsCTF/edit/main/workrole/cybercartographer/cyberorg_classroom_targets.txt'


def prompt_publish():
    try:
        answer = input('Open GitHub to publish this list? [y/N] ').strip().lower()
    except (EOFError, KeyboardInterrupt):
        print('\nSaved locally; nothing published.')
        return
    if answer not in ('y', 'yes'):
        print('Saved locally; nothing published.')
        return
    print(f'In VS Code, open {OUTPUT.name}, select all (Ctrl+A), and copy (Ctrl+C).')
    print('In the GitHub file editor, replace the contents with your paste, then click Commit changes.')
    print(f'GitHub editor: {EDIT_URL}')
    try:
        if not webbrowser.open(EDIT_URL):
            print('Open the GitHub editor link above in your browser.')
    except webbrowser.Error:
        print('Open the GitHub editor link above in your browser.')


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
    status = main()
    if status == 0:
        prompt_publish()
    raise SystemExit(status)
