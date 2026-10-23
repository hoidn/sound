## Finite local checksum cases for REQ-LIVE-SET-STRUCTURE-008

**X — enumerated supplied-buffer scope only.** The
[complete initial-zero one-byte catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-live-set-structure-r3-finite-crc-v1/catalog.json)
records all 256 byte values at length 1 with a fresh zeroed four-byte CRC seed/output
buffer. The selected checksum result is the low 16 bits of that buffer interpreted
little-endian after the original x86_64 step `0x101191310`. The 253 new draft cases
[LSS-CRC-001–LSS-CRC-253](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-live-set-structure-r3-finite-crc-v1/new-cases.json)
use the exact native CRC16 expectations in that catalog, from the existing
polynomial `0x8005`, MSB-first, initial-zero, no-reflection, no-final-xor rule frozen
before the new calls. These expectations were not fitted to the results. The
three previously observed bytes `00`, `b7` and `ff` retain their historical summary
references and receive no new case IDs or process receipts.

The four raw output bytes and saved RAX/RDX/XMM carriers are retained provenance.
The upper 16 output bits and RAX are not the CRC16 criterion. Each new case's
portable expected value and portable comparator remain **NULL**; no ARM or Apple
execution equivalence, portable full-word criterion or candidate grade is selected.
The local observations do not establish actual file reading, sample matching,
Open/Save, public receiver or state/lifecycle delivery, other seeds, longer inputs
or chunk histories. The existing REQ-008 clauses, their evidence scope, general
static rules and unresolved application joins remain unchanged.

The catalog and case rows cite the independently approved actual review through
`approved_review_join`; the review pin and batch identity are recorded in this
owner packet's manifest. This finite annex extends the draft only. The preceding
40-row case table and all 34 cases and fixtures of `live-set-structure-v1` remain
unchanged; no handoff release, released comparator, grade or site credit changes.
The 256 input values are one local finite class, not a required-outcome denominator
or family/product completion.

