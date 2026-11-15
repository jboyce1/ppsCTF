---
layout: default
title: "A disk and a laboratory"
---

# A disk and a laboratory

A Wichita criminal investigation received a computer disk in 2005. This document
collection contains the front matter of a public laboratory report, but its case
records are missing from the visible directory.

Recover the missing records and identify the digital leads they describe.
Explain what those leads established and what still required corroboration.
This is a recovery investigation, not a hoax case. The material is non-graphic,
but concerns a violent-crime investigation.

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
