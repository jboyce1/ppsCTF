# Hamhunt v2 notes

The active test package is `challenges/hamhunt_v2/`. It intentionally contains
exactly five files: one Python installer, three ZIP assets, and the text guide.
The guide starts with download/deploy commands and includes unpublished-file
transfer instructions, reset instructions, the teaching progression, a proposed
30-point playtest rubric, and verified answer checks.

The installer sets the Ubuntu administrator password to `hamhunt` after SSH
configuration succeeds and prints it in the successful deployment summary.
The three challenge accounts have no supplementary groups. A managed final
sudoers block explicitly denies them sudo, including any inherited local grants,
while preserving Ubuntu's administrator permission. Specific command-permission
queries verify denials; a successful general policy listing is not treated as
an unrestricted sudo grant.
Download only `deploy_hamhunt_v2.py` and run it with sudo. It automatically
creates a private cache, downloads the three ZIPs and guide, validates them,
and deploys. It can also use adjacent local ZIPs for unpublished testing.
`--check` reads local assets only; `--reset` restores a previous run.

Validation completed locally:

- ZIP checksums, path validation and CRC reads for all three packages.
- Exactly one result for each of nine hash-selection/comparison exercises.
- Final message decrypted and repacked for standard Unzip; original message and
  password preserved. Standard Unzip successfully decrypts the working ZIP.
- Real OpenSSH parser test of the account-scoped Match block with an earlier
  global password-authentication denial; only the lab/admin accounts are enabled.
- SSH configuration generation is idempotent.
- Sandboxed deployment/reset test: direct Desktop placement, removal of old
  keys/history, group removal, password-setting order and summary output.
- Simulated SSH validation failure restores the original configuration bytes.
- Non-root deployment is rejected.
- Real sudo policy evaluation in an isolated filesystem: an inherited ALL grant
  initially permits Leroy; the managed final deny blocks all three challenge
  accounts as root and Ubuntu while retaining Ubuntu's root access.
- A denied account's general sudo listing can still exit zero; checks now query
  specific command permissions instead. Shared rules are retained, not deleted.
- Sudoers syntax, idempotence and preservation of administrator rules verified.
- Script-only bootstrap downloads all four supporting files into a private cache;
  matching cached assets are reused and adjacent assets support unpublished tests.
- A bad download fails its checksum and removes its temporary file before deployment.
- Guide hash answers compared against actual ZIP contents and download/setup
  command syntax checked with Bash.

No real workstation accounts, passwords or services were changed. Full live
Ubuntu/Kali playthroughs remain required before an event. The original
`challenges/hamhunt/` remains unchanged.

Earlier planning notes and original reference snapshots remain in the local
workspace at `docs/hamhunt_v2/planning/`; they are not included in the published
test package. Those copied scripts are historical, not deployment instructions.
