---
layout: default
title: "The payload archive"
---

# The payload archive

After Columbia was lost in 2003, investigators recovered scientific hardware
from the debris. This collection contains public technical material about the
mission; portions of its recovery record are no longer visible.

Recover deleted files and establish which experiment and storage device the
records describe, what information survived, and how the reported results were
validated. This is a recovery investigation, not a hoax case.

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
