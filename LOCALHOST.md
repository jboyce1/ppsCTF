# Preview ppsCTF and ppsCTF-move locally

These commands work on this computer, which already has Jekyll, the Minima theme, and Python 3 installed. Open a terminal and copy the block for the site you want to preview.

## ppsCTF-move (MOVE prototype)

```bash
cd /home/morgan/CyberTacticsForge/ppsCTF-move
jekyll build --destination /tmp/ppsctf-move-preview/ppsCTF-move && python3 -m http.server 4173 --bind 127.0.0.1 --directory /tmp/ppsctf-move-preview
```

Leave the terminal open, then open these addresses in your browser:

- Home: http://localhost:4173/ppsCTF-move/
- HashHound: http://localhost:4173/ppsCTF-move/classes/HashHound/HashHound.html
- SSHerlock: http://localhost:4173/ppsCTF-move/classes/SSHerlock/SSHerlock.html

## ppsCTF (original site)

```bash
cd /home/morgan/CyberTacticsForge/ppsCTF
jekyll build --destination /tmp/ppsctf-preview/ppsCTF && python3 -m http.server 4174 --bind 127.0.0.1 --directory /tmp/ppsctf-preview
```

Open http://localhost:4174/ppsCTF/ in your browser. You can run both sites at once in separate terminals to compare them.

## Stop, restart, and see edits

- Press **Ctrl+C** in the server terminal to stop it. Run the same command block again to restart it.
- After editing source files, stop the server, rerun the block to rebuild, and refresh the browser. If the browser shows an old version, press **Ctrl+Shift+R**.
- If you see `Address already in use`, that port already has a server running. Try opening the matching URL first. To use another port, change `4173` or `4174` in the command and browser address to the same unused number.
- Keep `/ppsCTF-move/` or `/ppsCTF/` in the browser address: each site's configured base path needs it for links and styling to work.
- Jekyll may print Sass deprecation warnings. A build that ends with `done` succeeded.

The generated previews live under `/tmp` and may disappear after a reboot. Running these commands recreates them. Previewing does not publish anything to GitHub.
