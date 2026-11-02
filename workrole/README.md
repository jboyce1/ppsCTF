# Workroles

Each workrole owns its learning page, images, and challenge files:

```text
workrole/<title>/
  <WorkroleTitle>.md
  images/
  challenges/
```

Use lowercase directory names. Keep exercises, practice ZIPs, setup scripts,
wordlists, packet captures, and supporting downloads under `challenges/`.
Keep screenshots and banners under `images/`. Image files that are challenge
inputs stay with their exercise under `challenges/`.

- [SSHerlock](./ssherlock/SSHerlock.md)
- [HashHound](./hashhound/HashHound.md)
- [CyberCartographer](./cybercartographer/CyberCartographer.md)
- [MsDisin](./msdisin/MsDisin.md)
- [LANgeist](./langeist/LANgeist.md)
- [MALchemist](./malchemist/MALchemist.md)
- [Portalord](./portalord/Portalord.md)
- [8ball](./8ball/8ball.md)
- [Cyberus](./cyberus/cyberus.md)

Run `python3 scripts/check_workrole_links.py` from the repository root after
moving files or changing links. Rebuild Fun New Game with
`python3 scripts/build_fun_new_game.py`; it updates the practice ZIPs and website
target hashes together in their canonical location.

Tournament/event scenarios remain in the repository's top-level `challenges/`.
See [migration details](../docs/workrole-migration.md) for old URLs and compatibility.
