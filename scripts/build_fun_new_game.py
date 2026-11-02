#!/usr/bin/env python3
"""Rebuild the offline beginner MD5 exercises and their published target hashes."""
import hashlib
import io
import re
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['FUNNEWGAME.html', 'funnewGAME.html', 'funNEWgame.html', 'FuNeWgAmE.html', 'FUNnewGAME.html']
# Sealed display messages; no literal flags in the builder or student files.
SEALED = [[['bM+EuuYyB3BQviQ94kMzVRQXUDN5ECLGEpw7oQ8Ke4I=', 'iKJG2KQSJYUdihaYAVMXfw==', 'JKJbHBS4O0MoyLZ8', 'hnSxprXDZt5Bo/oIOdFA1VR/5nD5kWOln3QmrEGBf4VKykd6aYaR/hexGq+7OwZGyFJn39/d3L9Z0/6o9SnvNE/t2ElkqKeS5cWvGRvF5SIyRPmUZOjOwaz+s/dApZTA'], ['v2uvK5Dhhkra9IxuN14K0uH+8tKmblkoaLQHwn08MLk=', 'awT7jPwfQVLwxImTOm+STA==', 'sKwJ7LoD18NBZUPZ', 'g/MUpRIsTMIqIejIzMckPXj0tl41bsDOYHz66VGFN6N6a8Js+2wN0wh3yVyScQQQqc6j/+Z/aFsoTUw0M7odAn++PtAuIPFxiIvYpzSj1CXmDAPlszabxMfFS4/lPOcN'], ['0kQWDGsVyAzQ4CXrT/nxskPO5w3qZvUhdyst6hO7tU4=', 'dWKWR3qXx2LrjxWTG0YIBw==', 'DwloU/BvUBCV9fN7', '88Llf1gHrXKLw2ZNQWVJ8DaNUUHFwHgCn/4JJXsBOp8pLoly3zr6ey5VwHSncpvUYocyX6/nppFcGpjMwsAQxua+mUk4SSZrs3P8H5STVljUrZGCJLxA2nv33RZAmw7k'], ['ma3DfoyrZL7kCwterjBDQdY9MqArhURC1yrEhjTTFVs=', 'wdx0zKMRXwD4eE83l1xRZw==', 'oO09s22Di45S5/2a', 'wbAEA7iuGTAeFLf6aOXolAymTGreHLC6jKB+/6fqVq0HhYC/+t9EcLruTyIPtlNqZjMBq5eP9hrCa5mXy+JeZ9bXINLaPXECgr/2FHEiqbaXqSHdwtuAhZZUxRtaX4AZ'], ['Uioca9ujMsLnnP71CCWa0qc4ZlextdPTnn1mLB1NG7M=', '9Spd4pxdZZO7KzVn44cm0A==', '4qBmn1qDq/kdqULq', 'k69LWq3NCVquxrkbgUg3heLEXe5Vqadhy7d114gRd6sPvEmr/6I8K2bVvZ7Zaz5aXtyDnDu+ljzFCyBIzKd+IYOvjxj7EQuK3/sox+QN8fhVvJXGE2R4fq5/tUAS4JkV']], [['Ij+wWPnrrrbyc/viAWww5WpJlayvYvrfqyTyFoh9qzY=', 'ziW+BTwUTxpQeGpMY2opgg==', '5nGbWuk34FXR5NLj', 'QRxPjj/yQCXEkoGyHRWdJ/E3KLlI0WjKv2j5ZRdRANdCmKYLqc3ib7uBlc8Mr3yW3n55zxiM7DpDJ2ZxKKmdFHSwZYacoVFaTHKGjuNH99C/rdnYDpWZNdciijvKmVEB'], ['JQVsPh73wE1OSbW4fJAs3ZzWp61oWKIsqaPBOlRA8dM=', 'TklZ0lTYfIve0Oxw/tfGyA==', 'xAlMmgoN3m6WZNIt', 'afuiichhQdFRgM2Gjw0RxKErVAlG8yHdLkJHh6xgGjxfw9j1ZENiM9NnOIYG5KO6TtENkFDLpiEEXQyX150ZdMsj+UN/2vzNKMI1jKK7d8yeTBmMJzrIgHDa3IKa+c8O'], ['nzRijIrGuuqIvNnb+118S8zPgd/9jAn2zOmWxqPFA1w=', 'ACbbaUSOPVud8PO4V+MjHA==', 'ir4HE9fmIkAoxZzW', 'yqIoUCkwRltLjdKeiE84MpbwMbS1ZzCS/Unj5x2MvH2dqMvA4RT4/7KVNWtvxe20U06ko8/z+AIMhvztEW2OG3iXVlAXadxdgIInKn4u2sE8HAQQNLNa7Zst14ws7Q0i'], ['WoJQIVQsFCDFUXFP5IIXA/GQgjMYKFTgvIqOyFcUqbg=', 'TZndpSTTKzM9oyiQaNnXkQ==', 'LD/q7UlFGNVuGZ71', 'n4X/84c7xA3E1rJxj5qn0QYhp2cTWIRU/ICKKC7EjxbgMbEz7uUwPPyekRjHj7w+IV7fktheWbL7CCkgmh2H37gWRKox3quszvGVqr9xqe3PHuq1lmWnKlzzzPq8eWZL'], ['7PcvP7oETutFCNvbwraG7d8+3eGtXNc5Apjf7OxSRIQ=', 'pstiRnfrS5CngwTzIcI7dg==', 'DyLOuYmW2Ab0xRcG', '2pZaNHotglfLJmjUBJUP5PDClQ174qH/lj2tIAO440SsZqE6HrLt2WBg1VzjHogs+gcKw1titKIHsskdWYwAypwgawthsbuSSsmASI3fSa+7fbfDgJqLkmP7T+IkJz3P']], [['he+Jlz3xTGi2U+o2pVPhvJcF18r9LcyXEU2CXAQBVrM=', 'GugRgOmi3E7BqeuZT31AvQ==', 'q+WYieevp+bO0vcn', 'XyGTBlsflAD7UYDosPDc3Af7N4vbnM0/Y0oBxYc2Q1t6T7ndELIprvBuPJBIKikjolE8W0oECiWdKcCysaxon0q3QEIadxyb70hLcu1IvGDMJneqnw7dBKybYQMTEvEi'], ['C9MowDUC+Ia1deaAJL7RSqoldRv7KnD/fQm5ALgH4hQ=', 'hU5sOtOhQV7IQ5EJUWD4sg==', 'kbZwIC1V1IrIl93y', 'kpzVAhMMYhpZlr7OnhmLZwllEdWcRvTGaikomBp5mVqGszMeN6MfhZPJZ/uv2HLFCyc7riSdleEuZg54zgyBIEa/JskBQi437b9qJe3SreFCONtxNaplmX/OZ0yDxpeI'], ['jv8ShwY7nN5McX1f3yEjT2E91bMiZWpPVLvmmjCfFH4=', 'QVku9+GnpftUF1poFqJgjw==', 'xt9uyZcrOOliHdfs', '4Zma0t3tlEwEK3+0Rl6pdA3ZKTr6xZAmg0270piG8pC0w7VdpzRp0TC2xh4lDiZGnG6bgEbAjSTUu9F8o3csqcruw4BPHxnm+ShPLtgvtTkWqZMWcJ4m0x9BbIYHTEiR'], ['ndg18NnR1Ng1kCdjqDLTrKCH3N7vS4NSWsvb/CDpmTs=', 'ptjSiWYQSubtk0bUEBOOOg==', 'U74Um/pEfH5M54Af', '+p927XaQQ2OQRDH0hST5LWkaKGJGFUU0vYpzyqZG966Y0l6LsADamzmLJuHW8Cuk/vvHvOwyMhDp40D4ZayhoKw5Y3fOuSiz2NbWruTbql08S66RbTfwWBv0InAEHPvn'], ['7vsP7AyitKB8J2f6QJ9eKT6RoYek6HIvkF1JJMvFCOE=', 'B8PXm76mA/quVzdPBtcs8A==', 'lTxJQfGrzH7Q98xK', 'gD0TUJhQUOp/apZgC5wvfEKPJcfhePigrmZKEokQwc6pOWG4Qb6bAoGUU+jLUfpGjZYytvHzj2A5NXIQhI0fv3i36w5ipCCzwtAZNFQD6/GxpcxSm8rAt/5UYDL0oVSn']]]
WINNERS = [2, 0, 3]


def archive(entries):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in entries.items():
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data)
    return output.getvalue()


def build():
    targets = []
    bundles = {}
    for number, (messages, winner) in enumerate(zip(SEALED, WINNERS), 1):
        folder = f'1 Fun New Game (practice {number})'
        entries = {}
        for index, name in enumerate(NAMES):
            # All candidates use the same renderer and padded ciphertext length.
            seed, salt, nonce, payload = messages[index]
            content = f'''<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fun New Game</title>
<style>body {{ font: 24px sans-serif; margin: 3rem; }} pre {{ white-space: pre-wrap; }}</style>
<h1>Fun New Game</h1>
<pre id="result">Opening game...</pre>
<noscript>Enable JavaScript in your browser to show the result.</noscript>
<script>
(async () => {{
  const bytes = value => Uint8Array.from(atob(value), c => c.charCodeAt(0));
  try {{
    const material = await crypto.subtle.importKey(
      'raw', bytes('{seed}'), 'PBKDF2', false, ['deriveKey']);
    const key = await crypto.subtle.deriveKey(
      {{name: 'PBKDF2', salt: bytes('{salt}'), iterations: 180000, hash: 'SHA-256'}},
      material, {{name: 'AES-GCM', length: 256}}, false, ['decrypt']);
    const result = await crypto.subtle.decrypt(
      {{name: 'AES-GCM', iv: bytes('{nonce}')}}, key, bytes('{payload}'));
    document.getElementById('result').textContent = new TextDecoder().decode(result).trim();
  }} catch {{
    document.getElementById('result').textContent =
      'Please open this file in a current Firefox or Chrome browser with JavaScript enabled.';
  }}
}})();
</script>
</html>
'''.encode()
            entries[f'{folder}/{name}'] = content
        target = hashlib.md5(entries[f'{folder}/{NAMES[winner]}']).hexdigest()
        targets.append(target)
        entries[f'{folder}/1 README.txt'] = f'''Fun New Game - Practice {number}

Target MD5: {target}

1. Open this extracted folder in the file manager.
2. Right-click an empty space and choose Open Terminal Here.
3. Type ls and press Enter to list the files.
4. Type md5sum FUNNEWGAME.html and press Enter.
5. Compare the 32-character hash with the target above.
6. Repeat with each of the other .html filenames, one at a time.
   Capital letters matter. Use the exact filename shown by ls.
7. Once you have checked all five files, return to the file manager.
8. Double-click ONLY the .html file whose hash matches the target.
   It opens in your web browser and shows your flag.

No sudo is needed. Do not edit or open the game files before checking
their hashes. Record each filename and hash as you go.
'''.encode()
        data = archive(entries)
        bundles[f'Fun New Game Practice/{folder}.zip'] = data
        path = ROOT / 'workrole/hashhound/challenges/Fun New Game Practice' / f'{folder}.zip'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (ROOT / 'workrole/hashhound/challenges/Fun New Game Practice.zip').write_bytes(archive(bundles))
    page = ROOT / 'workrole/hashhound/HashHound.md'
    text = page.read_text()
    start = text.index('## **Walkthrough**')
    end = text.index('\n---\n\n# Part 2:', start)
    walkthrough = '''## **Walkthrough**

These practices use five HTML game files. Double-clicking one opens it in your
web browser. First, use the terminal to find the file you should open.

If you downloaded an earlier version, download it again and extract it in a new,
empty folder before starting.

1. Extract `hashhound_practice1.zip` in your file manager (right-click, then **Extract Here**).
2. Open the extracted `1 Fun New Game (practice 1)` folder.
3. Right-click an empty space in that folder and choose **Open Terminal Here**.
4. Type `ls` and press Enter to see the filenames.
5. Type `md5sum FUNNEWGAME.html` and press Enter. You do not need `sudo`.
6. Compare the 32-character hash at the start of the output with the target for your practice below.
7. Repeat `md5sum` for each of the other four HTML files, **one file at a time**.
   Capital letters matter: type each filename exactly as `ls` shows it.
   Write down each filename and its hash.
8. After checking all five files, return to the file manager and **double-click only
   the file with the matching hash**. Your browser will display the flag.

| Practice | Target MD5 |
| --- | --- |
'''
    walkthrough += ''.join(f'| {n} | `{target}` |\n' for n, target in enumerate(targets, 1))
    walkthrough += '''
For practices 2 and 3, extract that practice's ZIP and follow the same steps in
its own folder. Each practice has a different target. The `1 README.txt` inside
each folder also gives that practice's target and instructions.

Leave the HTML files unchanged and unopened until you finish comparing their hashes.
No programs need installing; the game works offline in your browser.

'''
    page.write_text(text[:start] + walkthrough + text[end:])
    # Repair the broken closing backtick on the third download command.
    page.write_text(page.read_text().replace('practice%203\\).zip\n`', 'practice%203\\).zip`'))
    # The homepage also links to the MOVE edition; keep its guided activity in sync.
    move_page = ROOT / 'workrole/hashhound/HashHound-move.md'
    if move_page.exists():
        move_text = move_page.read_text()
        help_start = move_text.index('## **Walkthrough**')
        help_end = move_text.index('</details>', help_start)
        move_text = move_text[:help_start] + walkthrough + move_text[help_end:]
        move_text = re.sub(
            r'(<dt><span>O</span> Objective</dt><dd>).*?(</dd>)',
            r'\1Manually calculate the MD5 of each of the five HTML files, compare with your practice target below, then double-click only the matching file.\2',
            move_text, count=1)
        table = 'If you downloaded an earlier version, download it again and extract it in a new, empty folder before starting.\n\n| Practice | Target MD5 |\n| --- | --- |\n'
        table += ''.join(f'| {n} | `{target}` |\n' for n, target in enumerate(targets, 1))
        # Replace the visible target table, or add it before the first download.
        table_start = move_text.find('<!-- fun-new-game-targets -->')
        if table_start != -1:
            table_end = move_text.index('<!-- /fun-new-game-targets -->', table_start) + len('<!-- /fun-new-game-targets -->')
            move_text = move_text[:table_start] + '<!-- fun-new-game-targets -->\n' + table + '<!-- /fun-new-game-targets -->' + move_text[table_end:]
        else:
            download_start = move_text.index('[Download hashhound_practice1.zip]')
            move_text = move_text[:download_start] + '<!-- fun-new-game-targets -->\n' + table + '<!-- /fun-new-game-targets -->\n\n' + move_text[download_start:]
        move_page.write_text(move_text)
    return targets


if __name__ == '__main__':
    for number, target in enumerate(build(), 1):
        print(f'Practice {number}: {target}')
