---
layout: move
title: "Cottingley: the beck photographs"
---

# Cottingley: the beck photographs

A photographic account describes small winged figures beside a beck in Yorkshire.
Its published photographs were offered as evidence that the figures were real.
The supplied collection contains a photograph and pages from the published account.

<section class="move-card" aria-label="Cottingley MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Assess the photographic account of the figures beside the beck.</dd>
<dt><span>O</span> Objective</dt><dd>Recover deleted material and compare it with the published photograph.</dd>
<dt><span>V</span> Verification</dt><dd>Display the recovered material and support a finding with specific visual and publication evidence.</dd>
<dt><span>E</span> Explain / Elaborate</dt><dd>What does the comparison establish about the published claim?</dd>
</dl>
</section>

## Tools

`grep`, `xxd`, `dd`, `sha256sum`, Scalpel; gzip extraction, read-only ext4 access, and image/PDF viewers.

## Evidence collection

Download: `cottingley.img.gz` — a gzip-compressed, 64 MiB ext4 filesystem image,
without a partition table. The image contains PDFs and PNGs; other recoverable
formats may also be present.

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/investigations/cottingley.img.gz
```

The drive and deletion history are simulated. Its contents are archival reproductions; no original historical storage device is represented.

Retain the source hash, recovery offsets, lengths, and recovered-file hashes
with a concise finding supported by the recovered exhibits.
