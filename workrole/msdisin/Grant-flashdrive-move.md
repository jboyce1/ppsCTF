---
layout: move
title: City Point — Digital forensic examination
---


# City Point: digital forensic examination

A history exhibition has received a flash drive with a photograph said to show
General Ulysses S. Grant at City Point with his soldiers. The accompanying story
connects the photograph to his wartime headquarters. A curator wants your team
to check that interpretation before putting it on display.


<section class="move-card" aria-label="City Point MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Assess the photograph proposed for the exhibition.</dd>
<dt><span>O</span> Objective</dt><dd>Recover missing photographic material and assess the proposed caption.</dd>
<dt><span>V</span> Verification</dt><dd>Display the recovered photographs and support a caption finding with specific visual evidence.</dd>
<dt><span>E</span> Explain / Elaborate</dt><dd>What does the recovered material establish, and what cannot be inferred about the deletion?</dd>
</dl>
</section>

## Tools and downloads

`grep`, `xxd`, `dd`, `sha256sum`, Scalpel; gzip extraction, read-only ext2 access, and image/PDF viewers.

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/grant-flashdrive/grant-flashdrive.img.gz
```

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/grant-flashdrive/grant-png.conf
```

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/carving/dd-cheatsheet.txt
```

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/carving/scalpel-cheatsheet.txt
```

<details class="move-help" markdown="1">
<summary>City Point examination walkthrough</summary>

## Evidence intake and initial examination

**Step 1:** In the file manager, create a folder named `city-point-case`. Open it,
then right-click an empty area and open a terminal there. Keep this terminal in
that folder throughout the investigation.

**Step 2:** The manual investigation uses `grep`, `xxd`, `dd`, and `sha256sum`
to locate, extract, and verify file content. Scalpel provides an optional
comparison after manual recovery.

**Step 3:** Download the flash-drive filesystem. Wait for Wget to report success.
This is a 16 MiB ext2 filesystem image, not a complete operating system.

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/grant-flashdrive/grant-flashdrive.img.gz
```

**Step 4:** Decompress the filesystem. Wait for the prompt to return.

```bash
gunzip grant-flashdrive.img.gz
```

**Step 5:** Record the image's hash in your case notes. You will check it again
at the end to confirm that your investigation did not change the evidence.

```bash
sha256sum grant-flashdrive.img
```

**Step 6:** In the file manager, create an empty folder named `flashdrive` inside
`city-point-case`. This is your mount point: an ordinary empty directory
alongside `grant-flashdrive.img`. If the case folder is on your Desktop, its path
is `~/Desktop/city-point-case/flashdrive`. Keep the terminal in `city-point-case`.

**Step 7:** Attach the image to that folder. `-t ext2` selects the filesystem;
`loop` mounts the image file, and `ro` makes it read-only.

```bash
sudo mount -t ext2 -o loop,ro grant-flashdrive.img flashdrive
```

**Step 8:** Inspect the visible file names. Record the file names and types in your examination notes.

```bash
ls flashdrive
```

**Step 9:** In the file manager, open `flashdrive`. Examine `Grant_City_Point.jpg`
and the two newspaper PDFs: `western-democrat_1864-06-21_p2.pdf` and
`western-democrat_1864-07-05_p2.pdf`. These are unaltered scans from *The Western
Democrat*, Charlotte, North Carolina, preserved as downloaded from DigitalNC.
They are Confederate-aligned contemporary reporting; distinguish reported claims
from independently established facts.

Record the photograph's caption, visible inscriptions, and features you can
compare with other images. Note the newspapers' dates and relevant references
to Grant, Petersburg, and City Point. The articles provide period context; they
do not authenticate the photograph.

**Step 10:** Close the viewer and any file-manager window inside `flashdrive`.
Detach the filesystem. If it is busy, close the remaining window or terminal
inside it and repeat this step.

```bash
sudo umount flashdrive
```

## Locate file signatures

A PNG begins with the eight bytes `89 50 4E 47 0D 0A 1A 0A`. Its last chunk
contains `IEND`, followed by four CRC bytes. We will find those boundaries and
calculate exactly how many bytes to copy. The visible exhibition photograph is
a JPEG, so it will not appear in this PNG search.

**Step 11:** Search the entire image for candidate PNG beginnings.
`LC_ALL=C` makes the search operate on bytes; `-a` treats the image as searchable
text, `-o` prints matches only, `-b` prints byte offsets, and `-F` searches for an
exact byte sequence. Bash's `$'...'` notation turns `\xNN` into a byte.

```bash
LC_ALL=C grep -aobF $'\x89PNG' grant-flashdrive.img
```

Record the decimal number before each colon. Those are candidate **start offsets**,
not lengths. Nonprinting bytes after the colon may render as unfamiliar characters; the
decimal offset is the value to retain.

**Step 12:** Search for the IEND chunk type. Record each decimal offset.

```bash
LC_ALL=C grep -aobF 'IEND' grant-flashdrive.img
```

These offsets point to the `I` in `IEND`, not to the end of the file.
A signature match is a candidate, not proof of a complete file.

**Step 13:** Inspect the first candidate header. Replace START with a decimal
start offset from your results. `-g 1` groups individual bytes, `-s` selects where
to start, and `-l 16` displays sixteen bytes.

```bash
xxd -g 1 -s START -l 16 grant-flashdrive.img
```

The search used the first four signature bytes. Confirm that the full eight-byte
signature is `89 50 4e 47 0d 0a 1a 0a`. The offsets on the left of xxd's display
are hexadecimal; the numbers printed by your grep searches are decimal.
Record offsets in decimal in your examination notes.

**Step 14:** Inspect the IEND candidate after that header. Replace IEND_OFFSET
with its decimal offset. `-l 8` reads the four letters and their four CRC bytes.

```bash
xxd -g 1 -s IEND_OFFSET -l 8 grant-flashdrive.img
```

Confirm `49 45 4e 44 ae 42 60 82`. For a contiguous PNG, an IEND after a valid
header is a candidate boundary.
Check that it precedes the next header and validate the extracted file.
Inspect the remaining candidates with steps 13 and 14. Real files can have
misleading matches or fragmented data, so this pairing shortcut is not a general
guarantee. Reading the end of the entire filesystem image would not find the
end of a particular picture inside it.

## Determine boundaries and extract files

**Step 15:** Record each candidate's start offset, IEND offset, and calculated
length in your examination notes. Keep values in decimal. The IEND offset points
to the `I`. Add **eight** to include the four letters and the four following CRC bytes:

```text
length = IEND offset + 8 - start offset
```

For an unrelated example, a start of 1,000 and an IEND at 3,460 give
`3,460 + 8 - 1,000 = 2,468 bytes`. Use the offsets you observed in this image
for your actual extraction. Record the largest calculated length and the lowest
start offset for the later Scalpel comparison.

**Step 16:** Recover candidate A manually. Replace START and LENGTH with your
calculated decimal values, without commas. `if` is the input image; `of` is a new
output file. `bs=1` counts in individual bytes, `skip` moves to the start, and
`count` copies exactly the length you calculated.

```bash
dd if=grant-flashdrive.img of=candidate-A.png bs=1 skip=START count=LENGTH
```

Check that dd's copied-byte count matches your calculated length.

**Step 17:** Open `candidate-A.png` in the file manager. Document its contents
and any visible decoding errors or missing image areas. A picture viewer may tolerate a truncated file, so opening
it alone does not prove the byte count was correct. Record its hash and compare it
with the reference hash supplied for the examination, if available. Retain the
hash in your case record so each recovered exhibit can be identified later.

```bash
sha256sum candidate-A.png
```

**Step 17b:** Recover candidate B. Use B's start and calculated length; leave the
output filename different so you preserve candidate A.

```bash
dd if=grant-flashdrive.img of=candidate-B.png bs=1 skip=START count=LENGTH
```

Open the result, then record and verify its hash before continuing.

```bash
sha256sum candidate-B.png
```

**Step 17c:** Recover candidate C with C's start and calculated length.

```bash
dd if=grant-flashdrive.img of=candidate-C.png bs=1 skip=START count=LENGTH
```

Open the result, then record and verify its hash.

```bash
sha256sum candidate-C.png
```

The manual extractions are ready for analysis and reporting. The following
Scalpel pass provides a second extraction method for comparison.

## Optional: corroborate extraction with Scalpel

Scalpel's `-s` option skips a number of bytes before searching. Its configuration
sets the **maximum length of each recovered file**. Neither value is a duration
in seconds. Scalpel continues searching the rest of the image after the skip;
it has no exact-byte-count option corresponding to dd's `count`.

**Step 18a:** If Scalpel is missing, install it. Wait for installation to finish.

```bash
sudo apt install scalpel
```

**Step 18b:** Download the PNG signature configuration template. Wait for Wget to report success.

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/grant-flashdrive/grant-png.conf
```

**Step 19:** Open `grant-png.conf` in the file manager's text editor. Replace
`MAX_BYTES` on the `png` rule with the **greatest length** from your examination notes,
in decimal bytes without commas. Save the file. Leave the header and footer intact.

The maximum must accommodate the largest candidate. A smaller maximum may
truncate a larger file or prevent complete recovery.

**Step 20:** Read your saved rule. Check that it contains your calculated number
instead of `MAX_BYTES`.

```bash
cat grant-png.conf
```

**Step 21:** Run Scalpel. Replace FIRST_START with the **lowest start offset** from
your header search, without commas. `-c` selects your rule, `-s` skips the bytes
before that offset, and `-o` selects a new output folder. Wait for completion.

```bash
scalpel -c grant-png.conf -s FIRST_START -o recovered grant-flashdrive.img
```

**Step 22:** Open `recovered` in the file manager. Inspect `audit.txt` and the
PNG subfolder. Open each recovered picture. Open a terminal in that PNG
subfolder and record the hashes.

```bash
sha256sum *.png
```

Match the Scalpel results to the manual extractions by their hashes. Compare your examination notes
with the audit log's offsets and lengths. If the numbers or hashes disagree,
review the boundary calculations. For another Scalpel attempt, use a new output
folder name, such as `recovered2`.

**Step 23:** In your original `city-point-case` terminal, hash the evidence image
again. It should match the hash you recorded in step 5.

```bash
sha256sum grant-flashdrive.img
```

## Report findings and limitations

Reopen the drive read-only with step 7 if you need the visible PDFs and photograph
again; detach it with step 10 when finished.

Prepare a finding for the curator, supported by the recovered exhibits:

- Identify the parts of the submitted photograph that also appear in recovered
  images. Describe specific matching features and retain the corresponding hashes.
- Assess whether the photograph records one scene at one moment. Distinguish
  observations from interpretations, and reconcile conflicting inscriptions,
  dates, or locations where the evidence allows.
- Recommend a display caption supported by your findings. Distinguish a source
  scene's date from a later print or construction date when you can establish them.
- State the limits of the examination. Recovery does not establish who deleted
  a file, when it was deleted, or why. A newspaper report does not independently
  authenticate a photograph.

Retain the source-image hash, extraction offsets and lengths, recovered-file
hashes, and relevant audit output with your case record. The photographic files
are resized archival reproductions; their hashes differ from the original archive
files. The newspaper PDFs retain the archival download bytes.

</details>
