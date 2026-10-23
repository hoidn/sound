# Synthesis source audit R2: two Operator associations

This additive source-only correction addresses [SIA-REVIEW-001](../reviews/synthesis-instruments-source-audit-review.json).
The original six R1 audit files, original seal, all88 input pins including81
owner/history files, source capture and current owner oracles remain unchanged.
[Response](response-r2.json) holds25 literal field replacements for the logical
current view; no whole catalog or archive is duplicated.

Operator B149 / INS:B630 / SIA-A394 is Filter Drive before the filter, not
frequency tracking or envelope timing. B150 / INS:B631 / SIA-A395 is continuous
Morph position, not Shaper Drive or waveshaper wet bypass. Both now associate
with existing OP015 and existing G25. OP015 actually invokes named Morph snaps
and inspects Drive eligibility; actual eligible Filter Drive changes and
continuous Morph changes remain documented-but-unexercised/U. The G25 productive
NONEMPTY main/filter baseline and future action text are unchanged. OP017 remains
a true distinct shaper/Drive/wet100-to0 history for B151–B153; B058/B059 retain
the true snap-versus-continuous distinction. No gain, curve, coefficient, timing
or audio identity law is added.

Six manual plan fields, eight derived forward fields, eight reverse-link fields,
one G25 membership field and two derived disposition counts change. The latter
move B150 from documentary-context-U to mixed-subset/gap:359→360 mixed and97→96
context-U. These are routing dispositions, not behavioral completion or evidence
grades. All567 contexts/112 resources/37 proposals/8 questions,109 requirements
and154 cases stay in scope; zero IDs/cases/adoption/coverage/completion are added.
All new documentary and actual outcomes remain null/U/unexecuted.

The full R1 review freshly read all selected contexts and owner records. Its
reviewer authors this narrow correction, so independent Root focused review is
pending AS OF AUTHOR FREEZE. This successor is not owner adoption or reference
execution. The historical README/check.py describe R1; current entrypoint is:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/synthesis-instruments-source-audit/check-r2.py --check
```

The new checker uses only its own fixed literal reconstruction, restores the
known affected records to prove all other values exact, validates25 delta
pointers, all immutable input pins and original seal, and rejects11 mutations.
Retained positive contexts include OP015 snaps and OP017 distinct Shaper Drive.
No old checker/author/import/AST/main/parser, replay, source recapture, archive
or preset decode, native/application/UI/audio/MIDI/Max/hardware/network/install/
configuration action runs. New checker definitions alone were inspected and
selected in the temporary author script to construct the literal response;
no old analyst or vendor code was selected. No future livecanonical gate exists.
There is no write mode or mutable validation report; manifest-r2.json seals the
three additive payloads.
