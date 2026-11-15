---
layout: move
title: "A disk and a laboratory"
---

# A disk and a laboratory

A Wichita criminal investigation received a computer disk in 2005. This document
collection contains the front matter of a public laboratory report, but its case
records are missing from the visible directory.

This is a recovery investigation, not a hoax case. The material is non-graphic,
but concerns a violent-crime investigation.

<section class="move-card" aria-label="Disk-lead MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Establish the digital leads described in the Wichita case record.</dd>
<dt><span>O</span> Objective</dt><dd>Recover the missing laboratory account and assess the leads it reports.</dd>
<dt><span>V</span> Verification</dt><dd>Display the recovered account and identify its digital leads and their need for corroboration.</dd>
<dt><span>E</span> Explain / Elaborate</dt><dd>What is the difference between a lead and a corroborated identification?</dd>
</dl>
</section>

## Tools

`grep`, `xxd`, `dd`, `sha256sum`, Scalpel; gzip extraction, read-only ext4 access, and image/PDF viewers.

## Evidence collection

Download: `disk-lead.img.gz` — a gzip-compressed, 64 MiB ext4 filesystem image,
without a partition table. The image contains PDFs and PNGs; other recoverable
formats may also be present.

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/investigations/disk-lead.img.gz
```

The drive and deletion history are simulated. Its contents are archival reproductions of public records, not the original seized disk.

Retain the source hash, recovery offsets, lengths, and recovered-file hashes
with a concise finding supported by the recovered exhibits.
