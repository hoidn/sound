# ARM64 class and vtable structure recovery

Author data recovery for packet 1a under plan revision 4/design revision 11.
Independent review and the combined packet seal belong to Root. These files
recover a component-level metadata inventory; they grade no application outcome.

`class-recovery.py --build` is the new stdlib-only analyst reader. It hashes the
pinned 149,711,904-byte original ARM64 image, reuses the fully inspected pure
Mach-O `require`/`span`/`header` definitions from the existing function-start
reader, and checks its 53 load commands/6,944 load-command bytes. It interprets
the normal dyld binding stream without applying bindings. The inspected owned
`tools/xexec/xexec.c` is source context for unsigned64 offset arithmetic; its
loader, imports and calling code are never run or imported. No Ghidra, native
decoder, original instruction/function, compiler, harness or tool process ran.

The selected recovery predicates and output roles are:

- `class-rtti.jsonl`: 28,017 file-backed records with a normal binding to one
  of the `__cxxabiv1` class/si/vmi type-info vtable imports, addend 16 and a
  bounded printable literal referenced name. There are 25,101 distinct literal
  encodings. 13,140 pointers are direct; 14,877 use an explicitly qualified
  bit63-cleared candidate interpretation. Raw pointer words, literal name/NUL
  bytes, file offsets and binding-opcode locators remain alongside that label.
  This is not a demangler or proof of global RTTI ABI/runtime class identity.
- `class-tables.jsonl`: 25,485 address-point candidates structurally validated
  against a nonpositive offset-to-top header, the selected RTTI record and a
  nonempty executable-section pointer prefix. 20,759 have zero offset-to-top;
  4,726 have negative offsets. Only aligned `__DATA_CONST,__const` and
  `__DATA,__const` headers with offset-to-top in [-2^32,0] are selected. The
  address point is header+16 under this explicit layout interpretation.
  There are 458,796 executable-prefix slot values; 458,576 also match an exact
  internal exported-function entry. Other executable addresses remain weaker
  candidates. These relations do not attach a method to every caller.
- Slot scanning stops at the first non-executable-section target or 128 slots.
  24,070 prefixes stop at a non-executable value and 1,415 reach the cap. Null,
  imported, alternative-layout and longer tables can be truncated or omitted.
  Neither stop proves native table extent, exhaustive methods or all paths.
- `class-legacy-validation.jsonl`: every one of the old export's 80 rows and
  2,191 slot-like values is checked. 55 address points satisfy the new recovery
  predicate; 25 stay legacy candidates outside it. Nine old slot-like values
  are not executable-section targets. Eight are imported RTTI pseudo-addresses
  whose raw file word is 0x10; one is a DATA address. This is a concrete reason
  to avoid treating the old heuristic slot list as complete dispatch evidence.
- `class-stores.jsonl`: 53,635 lexical decompiled assignment candidates from
  418,417 retained C records. Quotes, exact JSONL row hashes, code hashes and
  line locators are retained. `literal_store_candidate_count` counts these
  lexical rows, not proved constructor stores. Bodies were not all semantically
  read; receiver/object identity, ABI, lifetime and source-to-native alignment
  must be checked before indirect-site attachment. Warnings remain attached.

`class-inputs.json` pins the eight method/source providers and all 4,185 scanned
decomp chunks. The three governing documents are captured as-of, not mutable
future gates. The normal binding stream contains 41,401 records at 41,401 unique
locations; zero duplicates are asserted before building the keyed RTTI census.
Only selected normal binds participate. Weak/private/stripped and unsupported
layouts remain unaccounted for, not globally absent.

`class-check.py --check` is read-only: it verifies pins, all recovered raw
headers/name bytes/slot pointers, counts, current data identities and unchanged
watches. Only the fully read pure analyst LEB/bind/fixture definitions are
compiled for owned synthetic controls. Seven positive and eight rejection
controls include signed64 endpoints/overflows, a valid-symbol out-of-range
binding, truncated ULEB and unsigned backward offset wrapping. Four executable
classification controls distinguish code, actual legacy DATA, the external
pseudo-address and an unaligned code address. No supplied old main is run.

The three initial parser stops are retained in `class-failure-attempt-*`.
The first hypothesized zero-fill cause was withdrawn after the virtual-bound
version also failed. The diagnostic third stop exposed a dyld unsigned64 offset
wrap (2^64+48912 before normalization), handled with explicit modulo arithmetic
and a fixture. The first two unsealed method snapshots were already retained;
later refinements use concise correction records. Prefreeze review also fixed
the ineffective bounds fixture, added uniqueness/signed overflow guards and
renamed the lexical count. Unsealed generated data was regenerated under the
final method; no frozen source/provider or earlier packet was changed.

For the T1 message boundary, table row 9532 names literal
`18OSendThreadMessage`: address point `0x106756188`, type-info `0x1067562d8`,
slots 0/8/0x10 to `0x101ab786c`/`0x101ab787c`/`0x101ab7898`.
This only supplies structural method membership. The separate `indirect-*`
workstream owns any exact-PC/receiver/slot proof and resolved-site count; these
class records alone add **zero** resolved sites. All behavior, route, execution,
completion and compatibility gates remain unchanged.
