---
id: SRC-C-LIBRARY-STRING-CONTRACTS
type: source
status: current
updated: 2026-10-20
access: analysis
---

# C library string contracts

Two retained official publications document the destination-pointer return of `strncpy`. They supply a conditional public-library premise for the Utility investigation, not evidence of the library implementation or arguments used by a running Live instance.

## Provenance

- Apple Developer Documentation Archive: [archived `STRCPY(3)` manual](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/strncpy.3.html), BSD footer dated August 9, 2001; its standards section cites ISO/IEC 9899:1990 (C90). The archive wrapper identifies iOS Manual Pages and the manual identifies Mac OS X/BSD. This is not a current macOS library guarantee. The [retained HTML](../../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-strncpy-public-contract/apple-strncpy.html) was captured at `2026-10-20T12:21:46.571114+00:00`, HTTP 200, 15,903 bytes, SHA-256 `1934a21f07a64fc07c3e6a8449beed5fb97876dc6d137d2e359d7d71beb97162`.
- The Open Group / IEEE: [Base Specifications Issue 8, IEEE Std 1003.1-2024, `strncpy`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/strncpy.html). The [retained HTML](../../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-strncpy-public-contract/posix-strncpy-response.html) was captured at `2026-10-20T12:21:46.883403+00:00`, HTTP 200, 8,400 bytes, SHA-256 `a51caa92afc5dbb9ae86bcc9d6ebae6ced1e6ab8539dad997298afa07a347e4c`.

Both are full HTML captures retained for analysis. Capture URLs, response headers and UTC timestamps are in [sources.json](../../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-strncpy-public-contract/sources.json). Browser requests for POSIX returned 403; a separate ordinary direct HTTPS request to the official 2024 URL returned the retained Issue 8 HTML with HTTP 200. No authentication or proxy bypass is claimed. Images and linked destinations were not inspected. The original author read both pages' visible text; this source-page reconciliation inspected the eight exact retained locators below and the reviewed packet, without claiming a fresh full-page read.

The [immutable packet manifest](../../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-strncpy-public-contract/manifest.json) has SHA-256 `21b1a2b2496832db8dea63b8f5a0bfbd8637fb291bd9f7abd482a7010ad1d9b1`. Its historical pending-review labels describe the author freeze. The subsequent [independent review](../../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/utility-strncpy-public-contract-review.json) approves the captured public return premise and conditional composition only; SHA-256 `48a957b9713b65c0a9cd17151bcae7688aee3c458ce4d1abe2b132a854c14153`.

## Findings

Exact raw-span hashes and source-specific locations are retained in [claims.json](../../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-strncpy-public-contract/claims.json), `/locators/0`–`/locators/7`.

| Claim | Evidence label | Exact source locator | Limits |
| --- | --- | --- | --- |
| Both publications specify that `strncpy` returns its destination pointer. | Observed: public documentation | Apple HTML lines 117–119, RETURN VALUES; POSIX HTML line 64, RETURN VALUE; locators 0 and 6 | Function-specific contract; no actual loader binding, invocation or implementation conformance proved. |
| Copying is bounded by the supplied count; a short source is padded, and a source reaching the bound need not yield a terminated destination. | Observed: public documentation | Apple lines 113–115; POSIX lines 48–54; locators 1 and 5 | No application buffer validity or malformed-input behavior established. |
| POSIX requires destination space for the count and disallows overlap; overlapping copying is undefined. | Observed: public documentation | POSIX lines 48–54 and 79–80; locators 5 and 7 | No current source/destination allocation, lifetime or disjointness proved. |
| The versions are archived BSD/C90 and POSIX Issue 8/2024, respectively. | Observed: publication identity | Apple lines 163–164 and 171; POSIX lines 25–27; locators 2–4 | The 2026 capture date does not update the publication version or establish Live 12.4.3 applicability. |
| For the separately retained count 255, sufficient validity premises are writable destination storage for all 255 bytes; readable source through its first NUL inclusive if encountered within the bound, otherwise at least 255 readable bytes; and disjoint copying objects. | Inferred: conditional composition | `claims.json` `/validity_inference`, grounded in the DESCRIPTION and APPLICATION USAGE locators | NUL within 255 bytes is not required. These are premises, not observations of the current buffers or a new invalid-input contract. |

## Reconciliation

The [Utility research owner](../device-audio-utilities.md) retains the import association and conditional builder-return investigation. If the actual call is a conforming `strncpy` invocation, its arguments are valid and the applicable ABI holds, its normal returned pointer is the incoming destination. Combining that premise with the separately reviewed appended-entry identity and return-register survival supports a conditional helper-return association. It does not independently prove those other premises; the [packet input pins](../../../analysis/ableton-live-12.4.3/full-spec-v1/depth-utility-strncpy-public-contract/input-pins.json) identify their immutable evidence.

Actual target library/version, loader binding, ABI, argument validity, normal completion, runtime entry identity and public Mute delivery remain unknown. No library implementation, example, source function or original executable was run for this source page. The existing 38 Utility application outcomes remain U/unexecuted; no normative ID, case, grade or behavior coverage is added. This source record qualifies the external return premise only and does not replace the Utility owner or change historical evidence.

## Related pages

- [Research index](../index.md)
- [Audio utilities research](../device-audio-utilities.md)
- [Utility specification](../../specs/device-utility.md)
