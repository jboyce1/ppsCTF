# MOVE lesson trial

The existing repository hosts both lesson versions. No separate repository is needed.

Trial pages:
- /ppsCTF/classes/HashHound/HashHound-move.html
- /ppsCTF/classes/SSHerlock/SSHerlock-move.html

Original pages remain available:
- /ppsCTF/classes/HashHound/HashHound.html
- /ppsCTF/classes/SSHerlock/SSHerlock.html

Each trial page links to its original. Homepage and season schedule links currently select the trial pages. To make the originals the default again, remove `-move` from the HashHound and SSHerlock lesson links in `index.md` and `_data/season.json`, then commit and push those two files. This preserves the corrected meeting times. The MOVE layout navigation is in `_layouts/move.html`.

Edit the alternate Markdown files in the same directories as the originals. Their layout, styling, and Copy buttons are in `_layouts/move.html`, `assets/css/move.css`, and `assets/js/move.js`. Keep required files, tool names, and target prerequisites above the collapsed Mission Support blocks.

See LOCALHOST.md for local build and preview commands. The separate ppsCTF-move folder remains a local prototype; public trial pages use the ppsCTF base path.
