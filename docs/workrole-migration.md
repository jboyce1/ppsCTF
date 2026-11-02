# Workrole directory migration

All nine former `classes/<Title>/` directories and the HashHound/SSHerlock
folders formerly under `workroles/` now live under singular `workrole/<title>/`.
Titles in directory names are lowercase; existing learning-page filenames retain
their spelling. Pages live directly under the workrole, images in `images/`,
and practice files, downloads, instructor setup files, and supporting documents
in `challenges/`. Subfolders within challenges preserve exercise groupings,
including image files that are themselves challenge inputs (8ball and BasicTrojan).

The complete source-to-destination inventory is in
[workrole-paths.json](./workrole-paths.json). Seven byte-identical duplicates
were consolidated; no conflicting copies were discarded. The standalone
CyberTactics archive outside this repository was not imported or modified.

The 25 newer published commits were incorporated before pre-push validation,
preserving their schedule and SSHerlock additions. Both HashHound lesson
editions now use the repaired Fun New Game instructions and generated targets.

Navigation, the homepage schedule, image references, PDF links, GitHub download
commands, setup instructions, and the Fun New Game builder use the new locations.
Existing broken CyberCartographer download filenames and MsDisin practice ZIP
paths were repaired. 8ball wordlist URLs now use `main` instead of a historical
revision. Cyberus uses an existing process screenshot and no longer references
the absent listener screenshot; its listener command remains.

## Old URLs

The eleven old website page URLs (nine original lessons and two MOVE editions)
have compatibility pages in
`_legacy_workrole_redirects/`, explicitly included in `_config.yml`. They use
the `redirect` layout to send visitors to the new page while retaining query
strings and section fragments when JavaScript is available. Canonical links,
a meta refresh, and a clickable fallback are provided.

These redirects cover GitHub Pages HTML pages. GitHub raw files, GitHub repository
file links, and direct asset downloads cannot be redirected by Jekyll. Links in
this repository are updated; previously shared download URLs outside the
repository need to be replaced using the inventory. New download URLs will
become available when the migration is committed and pushed to `main`.

## Validation

Run from the repository root:

```sh
python3 scripts/check_workrole_links.py
python3 scripts/build_fun_new_game.py
python3 scripts/check_workrole_links.py
node --test scripts/schedule.test.cjs
jekyll build --destination /tmp/ppsctf-site --disable-disk-cache
python3 scripts/check_built_workrole_links.py /tmp/ppsctf-site
git diff --check
```

The link checker resolves workrole website links, images, relative PDF links,
GitHub raw downloads, migration destinations, and redirect destinations against
the checkout. It also rejects obsolete directory references in active content.
It does not request external services or perform a Jekyll build. The separate
built-site checker validates rendered HTML links and section anchors after the
Jekyll build. See [pre-push results](./workrole-validation.md).

For publication, review the complete migration as one change, including the
new files and removal of old paths. Publish these together so pages and downloads
switch locations in the same deployment.
