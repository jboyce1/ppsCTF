---
layout: move
title: "The observatory dispatch"
---

# The observatory dispatch

A series circulated in 1835 attributes extraordinary lunar observations to
Sir John Herschel's observatory at the Cape of Good Hope. The visible documents
are nineteenth-century reprints of the claimed discoveries.

<section class="move-card" aria-label="Lunar-dispatch MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Assess the authority behind the circulated lunar discoveries.</dd>
<dt><span>O</span> Objective</dt><dd>Recover missing publication records and assess the account&#x27;s authorship and claimed source.</dd>
<dt><span>V</span> Verification</dt><dd>Display the recovered records and answer who stands behind the account, using the publication evidence.</dd>
<dt><span>E</span> Explain / Elaborate</dt><dd>How do the original claim and later publication records differ?</dd>
</dl>
</section>

## Tools

`grep`, `xxd`, `dd`, `sha256sum`, Scalpel; gzip extraction, read-only ext4 access, and image/PDF viewers.

## Evidence collection

Download: `lunar-dispatch.img.gz` — a gzip-compressed, 64 MiB ext4 filesystem image,
without a partition table. The image contains PDFs and PNGs; other recoverable
formats may also be present.

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/investigations/lunar-dispatch.img.gz
```

The drive and deletion history are simulated. Its contents are archival reproductions; no original historical storage device is represented.

Retain the source hash, recovery offsets, lengths, and recovered-file hashes
with a concise finding supported by the recovered exhibits.
