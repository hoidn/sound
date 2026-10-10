---
id: HANDOFF-REPLACE
type: handoff
status: draft
updated: YYYY-MM-DD
access: handoff
---

# Handoff release manifest

## Release identity

Release ID, target version/platform, spec revisions, requirement IDs, prior
release, and scope of implementation authorization. State excluded/deferred
features and compatibility dimensions explicitly.

## Payload inventory

| Relative path | SHA-256 | Purpose | Provenance and review disposition |
| --- | --- | --- | --- |

List every payload file including scoped instructions, specs, fixtures, approved
public references, and any dependency-lock records. Record this manifest's hash
in the handoff catalog rather than inside itself.

## Approved inputs

Exact public-source versions and allowed fixtures. Specs and tests must be
intelligible without analyst source access. Document any limitations introduced
by sanitization and how they were resolved.

## Review record

Reviewer identity/role/date; findings; corrections; completeness review;
implementation-detail review; source/fixture sharing review; checksum and
self-contained-link checks; final pass/fail disposition. Blank fields are not
a completed review.

## Remaining uncertainty

Unresolved behavioral questions, required cases not covered, and explicit
blocking/deferred status. Do not turn missing information into an assertion.

## Changes and implementation entry point

Changes since the previous release, affected requirements and tests, migration
instructions, and the self-contained implementation starting page.
