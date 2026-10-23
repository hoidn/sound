# Direct public API member mappings — companion R7

This companion reconciles the unchanged original 45-entry/588-direct-declaration
inventory with five independently reviewed partial API member packets. The current
source index explicitly names Live12.4.5; target12.4.3 remains U. This is routing
and evidence identity, not a new semantic API review or complete typed contract.

[Summary](summary.json) records 587 direct documentary roles, one heading-only
semantic-U member, one separately identified zero-member root entry,626 globally
distinct requirements and702 packet-qualified proposed cases. There are only539
unqualified case labels: dropping the packet/revision path would conflate163
cases from two families. Both requirement references and case references retain
an exact repository-relative JSON path and array-index pointer. Every actual
member documentary/target oracle is null/U/unexecuted; zero members/entries are
semantically complete. Bridge workflows are a separate overlapping owner and
are excluded from these counts.

[Entries](entry-mappings.json) and [members](member-mappings.json) retain original
inventory records unchanged alongside their new owner/reference mappings.
[Requirements](requirement-index.json) includes U groups and the extra root role,
not only direct-member clauses. [Cases](case-index.json) includes every member,
source-branch and unresolved case, preserving kind, requirement links and null
flags. A list of case links is not full branch or acceptance completeness.
[Input pins](input-pins.json) records all five current author manifests/payloads,
their approved reviews and the original inventory R1 manifest/all65 payloads.
Original source/frozen packet bytes are never rewritten.

Run the readonly check from repository root:

```sh
python -B analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r7-api-member-mappings/derive.py --check
```

It reconstructs exact member/entry sets and all JSON pointers, verifies source/
packet/review hashes and dispositions, requirement uniqueness and qualified-case
uniqueness, null guards and manifest payloads. Without `--check`, author output
is refused once a manifest exists. It imports or executes no original source,
Max example, controller module, API, candidate, application or hardware operation.

The [coverage design](../../../../../wiki/research/full-live-specification-design.md)
and [inventory](../../../../../wiki/research/full-live-coverage-inventory.md)
retain completion gates. Inheritance/aliases/root closure, full schemas and
arguments/results, error/event/lifecycle and actual target processing remain
unresolved. A heading-only DrumPad.delete_all_chains is mapped as explicitly U,
never inferred from its name. Missing source behavior is unknown, not a pass.
Independent review of this companion is pending; source/member semantic approvals
remain limited to the five named partial packets and their exact revisions.
