---
layout: move
title: "The payload archive"
---

# The payload archive

After Columbia was lost in 2003, investigators recovered scientific hardware
from the debris. This collection contains public technical material about the
mission; portions of its recovery record are no longer visible.

This is a recovery investigation, not a hoax case.

<section class="move-card" aria-label="Flight-records MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Establish what the scientific recovery record reports.</dd>
<dt><span>O</span> Objective</dt><dd>Recover missing records and identify the experiment, device, and surviving information.</dd>
<dt><span>V</span> Verification</dt><dd>Display the recovered records and support an answer about the recovered information and its validation.</dd>
<dt><span>E</span> Explain / Elaborate</dt><dd>What does a published recovery record establish about the underlying data?</dd>
</dl>
</section>

## Tools

`grep`, `xxd`, `dd`, `sha256sum`, Scalpel; gzip extraction, read-only ext4 access, and image/PDF viewers.

## Evidence collection

Download: `flight-records.img.gz` — a gzip-compressed, 64 MiB ext4 filesystem image,
without a partition table. The image contains PDFs and PNGs; other recoverable
formats may also be present.

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/investigations/flight-records.img.gz
```

The drive and deletion history are simulated. Its contents are archival reproductions of public records, not recovered flight data or the damaged drive.

Retain the source hash, recovery offsets, lengths, and recovered-file hashes
with a concise finding supported by the recovered exhibits.
