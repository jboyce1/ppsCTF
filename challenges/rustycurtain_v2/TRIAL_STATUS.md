# Rusty Curtain v2 trial status

`rustycurtain_v2` is the staged copy. The original `rustycurtain` is intact.
Do not remove `_v2` until the classroom range trial passes.

## New deleted-file evidence

| Box | Flag prefix | Evidence file | Deleted JPEGs |
| --- | --- | --- | ---: |
| Ivan | `pps{1x2_...}` | `dead-drop.img.gz` | 1 |
| Tanya | `pps{2x2_...}` | `iron-curtain.img.gz` | 1 |
| Nikoli | `pps{2x3_...}` | `switchboard.img.gz` | 2 |
| Boris | `pps{3x3_...}` | `roswell-relay.img.gz` | 2 |
| Yuri | `pps{4x4_...}` | `vostok-telemetry.img.gz` | 3 |

The disk images contain deleted JPEGs that can be carved with the MsDisin
Part 7 method. Each box has one valid authorization code. Other pictures are
ordinary station copies. The code is not plain text in the disk image.

## Local checks

- All five disk images passed deletion, hash, JPEG, and Scalpel carving checks.
- All five ZIPs passed CRC and exact source comparison; transfer hashes are in
  `ZIP_SHA256SUMS.txt`.
- All six encrypted archives opened with their existing passwords and flag
  values. The three frequency ledgers match their books.
- Browser databases, sed keys, fedcount documents, and diff pairs passed local
  integrity and solution checks. Yuri's 12-character diff is reconstructable.
- Both deployers placed the evidence files and browser data at the intended
  paths on a repeat extraction test.
- The student ZIPs contain no walkthroughs, carving config, recovery folder,
  README, or process instructions. Instructor-only files stay in `instructor/`.

For another local check after edits, run these commands separately:

```bash
python3 verify_recovery.py
```

```bash
python3 instructor/test_challenges.py
```

The verification scripts accept an executable path for Scalpel or 7-Zip when
those tools are not on `PATH`. Rebuild the ZIPs after any source edit:

```bash
python3 package_boxes.py
```

## Range trial still needed

Follow `challenge_instructions.txt` on two clean Ubuntu targets, then use
`RANGE_TEST.md` from Kali. Confirm the services, logins, file transfers, and
flags before dropping `_v2`. Refresh and publish the classroom target list
only after the CYBER.ORG VMs have their assigned IPs. A live range test has
not yet been run.
