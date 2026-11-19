# CyberCartographer v2 challenge trial

This is a staged working copy of `challenges/rustycurtain`. The original folder
and its five ZIPs are intact. The v2 deployers read ZIPs beside the scripts,
so the staged trial can be tested before any rename or publication.

## New deleted-file challenges

| Box | Flag prefix | Theme | Deleted JPEGs |
| --- | --- | --- | ---: |
| Ivan | `pps{1x2_...}` | Anonymous FTP dead drop | 1 |
| Tanya | `pps{2x2_...}` | Iron Curtain field note | 1 |
| Nikoli | `pps{2x3_...}` | High-port FTP switchboard | 2, including a decoy |
| Boris | `pps{3x3_...}` | Roswell relay | 2, including a decoy |
| Yuri | `pps{4x4_...}` | Vostok telemetry | 3, including two decoys |

Each box ZIP contains `recovery/recovery.img.gz`, `scalpel-jpg.conf`, and a
box-specific `0ReadMe.txt`. The disk image is an ext2 filesystem with deleted
JPEGs. The flag is printed in one recovered picture; it is not present as
plain text in the disk bytes. Students use the same Scalpel JPEG rule and
recovery method taught in MsDisin Part 7. No hex-only bonus is included.

## Local checks completed on November 19, 2026

- Scalpel 1.60 recovered the expected 1/1/2/2/3 deleted pictures byte for byte.
  The image hashes, deletion state, JPEG decoding, and flag prefixes passed.
- All five rebuilt outer ZIPs passed CRC and matched their source folders.
  Their transfer hashes are saved in `ZIP_SHA256SUMS.txt`.
- All six password-protected inner ZIPs opened and passed CRC with 7-Zip 23.01.
  Boris's spacerace archive and hint were repaired in v2; its original copy is
  preserved under `rustycurtain`.
- The three spacerace frequency hints match their source books. The three
  sedsearch keys reveal their intended clues, and all three fedcount puzzles
  contain six replacement phrases with distinct counts.
- All three browser SQLite databases passed `PRAGMA integrity_check` and have a
  distinct most-visited site.
- All three diff text pairs have equal line counts and actual differences.
  Yuri's old 12-character flag had only 11 visible changes; v2 now has all 12
  recoverable characters. Its generator is kept in `instructor/`.
- Non-root extraction tests confirmed the deployers place all five recovery
  folders at the intended FTP/Desktop paths, including on a repeat run,
  without extra nesting.

Run the same local checks after any edit to a box folder. From this directory,
run one command and inspect its result before the next:

```bash
python3 verify_recovery.py
```

```bash
python3 instructor/test_challenges.py
```

If `scalpel` or `7z` is unavailable on the instructor computer, supply its
executable path as the last argument. The checks do not configure host services.
To rebuild box ZIPs after a source edit, run:

```bash
python3 package_boxes.py
```

## Range trial still needed

1. Follow `challenge_instructions.txt` to clone `rustycurtain_v2` on two clean
   assigned Ubuntu range VMs. Keep `instructor/` and its answer keys local.
2. On the first VM, run the first deployer:

   ```bash
   sudo python3 deploy_rustycurtain_1.py
   ```

3. On the second VM, open a terminal in its challenge folder, then run the second
   deployer:

   ```bash
   sudo python3 deploy_rustycurtain_2.py
   ```

4. From a separate Kali VM, use the existing CyberCartographer scanning and
   login steps to verify the assigned IPs, standard and high ports, and all
   five accounts. Download or copy each recovery image using its box readme.
   Expand it, carve it with Scalpel, open the pictures, and compare the flags
   with the private `instructor/recovery-answer-key.json`.
5. Complete the existing sedsearch, spacerace, browser, fedcount, and diff
   challenges from the student side on the range. Record failures before
   replacing `rustycurtain` or dropping `_v2`.

Local checks establish artifact consistency. They do not prove the range VMs
will install services, accept logins, or permit FTP/SCP transfers. Keep this
v2 copy and the original until the range trial passes.
