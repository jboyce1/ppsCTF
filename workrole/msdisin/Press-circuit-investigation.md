---
layout: move
title: "The international press circuit"
---

# The international press circuit

A Soviet newspaper cartoon published in 1986 alleges a U.S. military origin for
AIDS. A reproduction of the published cartoon is present in this press collection.
The allegation is an artifact under examination, not health information.

<section class="move-card" aria-label="Press-circuit MOVE">
<dl>
<dt><span>M</span> Mission</dt><dd>Assess the sources behind the circulated military-origin allegation.</dd>
<dt><span>O</span> Objective</dt><dd>Recover missing records and examine the relationship between the public message and its circulation.</dd>
<dt><span>V</span> Verification</dt><dd>Display the recovered records and support a finding about the message&#x27;s sources and purpose.</dd>
<dt><span>E</span> Explain / Elaborate</dt><dd>Which findings come from contemporary records, and which from later analysis?</dd>
</dl>
</section>

## Tools

`grep`, `xxd`, `dd`, `sha256sum`, Scalpel; gzip extraction, read-only ext4 access, and image/PDF viewers.

## Evidence collection

Download: `press-circuit.img.gz` — a gzip-compressed, 64 MiB ext4 filesystem image,
without a partition table. The image contains PDFs and PNGs; other recoverable
formats may also be present.

```bash
wget https://raw.githubusercontent.com/jboyce1/ppsCTF/main/workrole/msdisin/challenges/investigations/press-circuit.img.gz
```

The drive and deletion history are simulated. Its contents are archival reproductions; no original historical storage device is represented.

Retain the source hash, recovery offsets, lengths, and recovered-file hashes
with a concise finding supported by the recovered exhibits.
