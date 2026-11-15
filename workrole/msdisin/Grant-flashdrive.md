---
layout: default
title: Ms. Disin — The City Point flash drive
---

# The City Point flash drive

A history exhibition has received a flash drive with a photograph said to show
General Ulysses S. Grant at City Point with his soldiers. The accompanying story
connects the photograph to his wartime headquarters. A curator wants your team
to check that interpretation before putting it on display.

The contributor says several reference scans were deleted before the drive was
sent. Recover the missing material, compare it with the proposed exhibition
photograph, and recommend a caption supported by the evidence.

**This is a fictional classroom investigation using real historical photographs.**
The flash drive, contributor, exhibition, and deletion story are invented.

## Receive and inspect the flash drive

**Step 1:** In the file manager, create a folder named `city-point-case`. Open it,
then right-click an empty area and open a terminal there. Keep this terminal in
that folder throughout the investigation.

**Step 2:** The manual investigation uses `grep`, `xxd`, `dd`, and `sha256sum`,
the tools used in our successful CYBER.ORG PNG recovery test. Scalpel is an
optional follow-up after you recover the pictures manually.

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
`city-point-case`.

**Step 7:** Attach the image to that folder. `-t ext2` selects the filesystem;
`loop` mounts the image file, and `ro` makes it read-only.

```bash
sudo mount -t ext2 -o loop,ro grant-flashdrive.img flashdrive
```

**Step 8:** Inspect the visible file names. Which file types are present?

```bash
ls flashdrive
```

**Step 9:** In the file manager, open `flashdrive`. Read `01_assignment.pdf`,
`02_city_point_context.pdf`, and `03_catalog_reference.pdf`. Open
`exhibition_photo.jpg`. All of these files remain on the drive; they were not
deleted. The PDFs contain the context you need inside the range.

Before searching for missing files, record:

- What does the proposed caption ask you to believe about the rider and soldiers?
- Why would Grant being at City Point be historically significant?
- Which visible details could you compare with other photographs?

**Step 10:** Close the viewer and any file-manager window inside `flashdrive`.
Detach the filesystem. If it is busy, close the remaining window or terminal
inside it and repeat this step.

```bash
sudo umount flashdrive
```

## Find the missing photographs in the bytes

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
not lengths. The bytes after the colon may look like strange characters.

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

The search used the first four signature bytes. Do all eight bytes match
`89 50 4e 47 0d 0a 1a 0a`? The offsets on the left of xxd's display
are hexadecimal; the numbers printed by your grep searches are decimal.
Keep your worksheet in decimal.

**Step 14:** Inspect the IEND candidate after that header. Replace IEND_OFFSET
with its decimal offset. `-l 8` reads the four letters and their four CRC bytes.

```bash
xxd -g 1 -s IEND_OFFSET -l 8 grant-flashdrive.img
```

Check for `49 45 4e 44 ae 42 60 82`. For these prepared, contiguous classroom
scans, pair each header with the first IEND after it, before the next header.
Inspect the remaining candidates with steps 13 and 14. Real files can have
misleading matches or fragmented data, so this pairing shortcut is not a general
guarantee. Reading the end of the entire filesystem image would not find the
end of a particular picture inside it.

## Calculate and recover

**Step 15:** Fill in one row per candidate. Calculate each length yourself with
paper or a calculator. The IEND offset points to the `I`. Add **eight** to include the four
letters and the four following CRC bytes:

```text
length = IEND offset + 8 - start offset
```

For an unrelated example, a start of 1,000 and an IEND at 3,460 give
`3,460 + 8 - 1,000 = 2,468 bytes`. Do not use those example numbers for this image.

| Candidate | Start offset (decimal) | IEND offset (decimal) | Calculated length in bytes |
| --- | --- | --- | --- |
| A | | | |
| B | | | |
| C | | | |

Explain why using the IEND offset alone as the length would be wrong. Which
candidate has the greatest length? Which has the lowest start offset?

**Step 16:** Recover candidate A manually. Replace START and LENGTH with your
calculated decimal values, without commas. `if` is the input image; `of` is a new
output file. `bs=1` counts in individual bytes, `skip` moves to the start, and
`count` copies exactly the length you calculated.

```bash
dd if=grant-flashdrive.img of=candidate-A.png bs=1 skip=START count=LENGTH
```

Check that dd's copied-byte count matches your calculated length.

**Step 17:** Open `candidate-A.png` in the file manager. Does it display completely?
Describe what you see. A picture viewer may tolerate a truncated file, so opening
it alone does not prove the byte count was correct. Record its hash and ask your
teacher to compare it with the original hash in the instructor key.

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

You can now complete the case report below using your manually recovered pictures.
Scalpel is a comparison, not a requirement for completing this investigation.

## Optional: apply your measurements to Scalpel

Scalpel's `-s` option skips a number of bytes before searching. Its configuration
sets the **maximum length of each recovered file**. Neither value is a duration
in seconds. Scalpel continues searching the rest of the image after the skip;
it has no exact-byte-count option corresponding to dd's `count`.

**Step 18a:** If Scalpel is missing, install it. Wait for installation to finish.

```bash
sudo apt install scalpel
```

**Step 18b:** Download the unfinished configuration. Wait for Wget to report success.

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/grant-flashdrive/grant-png.conf
```

**Step 19:** Open `grant-png.conf` in the file manager's text editor. Replace
`MAX_BYTES` on the `png` rule with the **greatest length** from your worksheet,
in decimal bytes without commas. Save the file. Leave the header and footer intact.

Why must the maximum fit the largest candidate, rather than just candidate A?
What might happen to a larger picture if you choose a smaller maximum?

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

Match all three Scalpel results to your manually recovered pictures by their hashes. Compare your worksheet
with the audit log's offsets and lengths. If the numbers or hashes disagree,
review the boundary calculations. For another Scalpel attempt, use a new output
folder name, such as `recovered2`.

**Step 23:** In your original `city-point-case` terminal, hash the evidence image
again. It should match the hash you recorded in step 5.

```bash
sha256sum grant-flashdrive.img
```

## Decide what the evidence supports

Reopen the drive read-only with step 7 if you need the visible PDFs and photograph
again; detach it with step 10 when finished.

Submit your worksheet and a short case report:

- Match each recovered photograph to a reference record in the catalog PDF.
  Describe the visual details that support each identification.
- Identify which parts of the exhibition photograph appear in the recovered
  photographs. Use specific features, not just a general resemblance.
- Explain whether the exhibition picture records one scene at one moment.
  Reconcile any conflicting dates, places, or descriptions.
- Write a corrected display caption. Separate the date of a photographed scene
  from the date of a later print or construction when the evidence supports that distinction.
- State what you can and cannot conclude about the deletion. Recovery alone
  does not establish a person's motive or make every caption accurate.

The teacher has the original file hashes to check your results. These classroom
images have been resized and re-encoded from archival reproductions; their hashes
will differ from the Library of Congress downloads.
