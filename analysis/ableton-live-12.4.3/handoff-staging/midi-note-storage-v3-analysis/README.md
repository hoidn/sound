# MIDI note storage v3 staging analysis

Unreviewed, unpublished candidate; no final handoff directory created.
The [candidate](../midi-note-storage-v3/README.md) carries the 72 v2 case
objects and gzip fixtures exactly, and adds six bounded local group-data
comparisons. [Traceability](traceability.json) and [input pins](input-pins.json)
retain the analyst provenance; they are not candidate payloads.

`python3 -I -B build.py check` runs data-only author checks and writes
[author-validation.json](author-validation.json). `build` creates only the
initial cases/fixtures in a nonexistent staging directory; it deliberately
refuses to overwrite a candidate. Hand-authored contract and metadata are
review inputs. No native collectors/builders or original binaries are imported
or executed. Only the inspected existing schema/structure helper is imported.
The helper is limited; exact reviewed fragment equality and dedicated shape
assertions also check the nested group NoteId attribute form.

The candidate manifest enumerates all 83 payload files (78 fixtures plus
five text/JSON files), excluding its own hash. Author validation records that
manifest identity. No approval, publication, compatibility pass or candidate
implementation is recorded. Independent review must approve the bounded
local/public separation before a separate final publication seal.
