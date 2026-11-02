# Pre-push validation

Validation includes the latest 25 commits already published on `origin/main`.
The schedule and newer lesson content were incorporated before testing.

| Check | Result |
| --- | --- |
| Source links and migration inventory | 243 references, 232 source-to-destination entries, 11 redirects; pass |
| Real Jekyll build | Jekyll 4.3.2 with Minima; checkout and exact staged-tree builds pass |
| Complete website reference scan | 33 HTML files scanned; all 236 references into workrole and legacy pages resolve |
| Copyable download commands | All 49 rendered commands parse in Bash; all 40 distinct download targets are present in the commit |
| Legacy section bookmarks | All 485 pre-migration IDs retained, including 21 compatibility anchors for changed command headings |
| Rendered website links and anchors | 23 pages, 283 local references; no missing files or anchors |
| Existing schedule tests | All 6 Node tests pass |
| Firefox offline game behavior | All 15 local HTML files display correctly; exactly one flag per practice, matching its MD5 |
| Firefox homepage and redirects | Updated navigation works; all 22 original/MOVE legacy URLs, with and without .html, preserve query strings and fragments |
| Archive integrity | 26 ZIP/DOCX containers including nested ZIPs, 2,762 entries, 1 TAR archive; readable members pass CRC/read checks |
| Password-protected archive entries | 3 existing encrypted entries retained; plaintext content was not tested without challenge passwords |
| SQLite integrity | All 3 databases pass read-only `PRAGMA integrity_check` |
| Python challenge syntax | All 34 challenge scripts parse; setup/payload scripts were not executed |
| Migration preservation | All 225 tracked source files accounted for; 122 binary sources checked, with only the approved Fun New Game ZIP replacements changed |
| Staged publication scope | New and removed paths staged together; unrelated calendar PDF excluded |
| Fun New Game consistency | Both website editions and bundled READMEs agree with the actual target file hashes; deterministic rebuild verified |

Ruby/Jekyll dependencies were extracted into a temporary runtime for the build;
no system packages were installed. Firefox tests used a temporary headless
profile and extracted copies of the game files. Three encrypted ZIP entries
remain part of their existing password challenges.

These checks validate the checkout and built site. GitHub raw-download paths
become live after the commit is pushed, and GitHub Pages still needs to finish
its deployment. Previously shared raw-file URLs cannot be covered by website
redirects; use the migration inventory to replace those external references.
