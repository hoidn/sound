"""Apply the reviewer's text edits to the staged midi-config-v4 payload (reviewer, analyst side; run once).

  python3 -I -B apply_review_edits.py

Each edit replaces text that must occur exactly once. No case record, fixture or expected value is changed;
cases.json changes only its top-level status. REVIEW.md is written separately; finalize_manifest.py re-hashes.
"""
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / 'midi-config-v4'

EDITS = {
    'README.md': [
        ('# MIDI configuration interpretation and value transforms, release candidate 4',
         '# MIDI configuration interpretation and value transforms, release 4'),
        ('**Staged candidate: not reviewed and not released.** It is not an\n'
         'implementation input. Read [the contract](spec.md), [cases](cases.json),\n'
         '[role instructions](AGENTS.md) and [the draft manifest](manifest.json).',
         '**Reviewed local release.** Read [the contract](spec.md), [cases](cases.json),\n'
         '[role instructions](AGENTS.md), [the manifest](manifest.json) and\n'
         '[the review disposition](REVIEW.md). The stated partial scope is approved as a\n'
         'contract for a fresh, restricted implementation workspace. Such a workspace has\n'
         'not been provisioned by this release.'),
        ('When published, this release supersedes midi-config-v3 as a strict superset.\n'
         'midi-config-v3 stays immutable and valid for its narrower scope. Its 127 cases\n'
         'keep their IDs, records and fixture bytes, and no expected value is corrected;\n'
         '34 value cases are new, for 161 in total. [The manifest](manifest.json)\n'
         'records the relationship and the superseded manifest digest.',
         'This release supersedes midi-config-v3. It carries every midi-config-v3 case\n'
         'and clause and widens the scope, with two precision corrections to general\n'
         'value clauses (changes 5 and 7): a value reached by several relative messages\n'
         'in a row is compared within a tolerance that grows with their number, and a\n'
         'stepped target value very close to a half-integer has no expectation. No\n'
         'midi-config-v3 case is affected. Its 127 cases keep their IDs, records and\n'
         'fixture bytes, and no expected value is corrected; 34 value cases are new, for\n'
         '161 in total. midi-config-v3 stays immutable and valid for its own scope apart\n'
         'from those two corrections. [The manifest](manifest.json) records the\n'
         'relationship and the superseded manifest digest.'),
        ('   |max|)) instead of 1e-6. τ is 1e-6 for every midi-config-v3 case, so no\n'
         '   carried comparison changes.',
         '   |max|)) instead of 1e-6. τ is 1e-6 for every midi-config-v3 case, so no\n'
         '   carried comparison changes. Rounding adds up over relative messages in a\n'
         '   row on a parameter that is not stepped, so a value reached by *k* of them\n'
         '   is compared within *k* × τ. Each step of the carried relative cases is\n'
         '   exact in single precision, so their comparison is unchanged.'),
        ('   parameter. Every other target value of a stepped parameter is rounded as\n'
         '   before.',
         '   parameter. Every other target value of a stepped parameter is rounded as\n'
         '   before. A stepped parameter\'s value after a move has no expectation.'),
        ('   Added: results near a bound and Value Scaling moves outside the listed\n'
         '   cases, with the later values of their sequences, and anything that empties\n'
         '   the record of previous data values. The default choice stays excluded; the',
         '   Added: results near a bound, stepped target values near a half-integer and\n'
         '   Value Scaling moves outside the listed cases, with the later values of\n'
         '   their sequences, and anything that empties the record of previous data\n'
         '   values. The stepped exclusion narrows the midi-config-v3 rounding rule,\n'
         '   which gave such values an expectation; no midi-config-v3 case lies near a\n'
         '   half-integer. The default choice stays excluded; the'),
        ('   The contract states the assumptions that the value cases rest on.',
         '   The contract states the assumptions that the value cases rest on and the\n'
         '   parts of the original code that did not run.'),
        ('10. **Cases.** MIDI-CONFIG-128 to 161 are new value cases.\n'
         '11. **Unchanged.** Every other clause, case and fixture of midi-config-v3 is\n'
         '    carried unchanged, and nothing in midi-config-v3 is contradicted. The\n'
         '    sentences that left takeover unspecified now point to the new rules.',
         '10. **Comparison obligations.** A reference comparison selects each case\'s\n'
         '    choice by its entry\'s position and records the entry\'s wording, instead\n'
         '    of confirming that the `none` choice is the one under which takeover\n'
         '    never acts. The rule for a crossfader that reports another range now\n'
         '    also covers MIDI-CONFIG-150.\n'
         '11. **Cases.** MIDI-CONFIG-128 to 161 are new value cases.\n'
         '12. **Unchanged.** Every other clause, case and fixture of midi-config-v3 is\n'
         '    carried unchanged. Apart from the two precision corrections in changes 5\n'
         '    and 7, nothing in midi-config-v3 is contradicted or narrowed. The\n'
         '    sentences that left takeover unspecified now point to the new rules.'),
    ],
    'AGENTS.md': [
        ('This directory is a staged release candidate. Use it for implementation only\n'
         'after a separate review approves it and it is published as an immutable\n'
         'release. Even then, implementation requires a fresh, restricted implementation\n'
         'workspace containing only permitted materials. Do not begin clean\n'
         'implementation in an analyst checkout.',
         'This is a reviewed local release for its explicit partial scope. Application\n'
         'implementation requires a fresh, restricted implementation workspace containing\n'
         'only permitted materials. Publication of this package does not provision one.\n'
         'Do not begin clean implementation in an analyst checkout.'),
    ],
    'spec.md': [
        ('# MIDI configuration interpretation and value transforms — release candidate 4',
         '# MIDI configuration interpretation and value transforms — release 4'),
        ('SPEC-MIDI-USER-MAPPING revision 5. Release candidate: midi-config-v4, which\n'
         'supersedes midi-config-v3 as a strict superset when published\n'
         '([README](README.md#supersession)). Only the',
         'SPEC-MIDI-USER-MAPPING revision 5. Release: midi-config-v4, which\n'
         'supersedes midi-config-v3 ([README](README.md#supersession)). Only the'),
        ('**Status: staged candidate, not reviewed, not released.** It is not an\n'
         'implementation input until a separate review approves it and it is published.\n'
         'The clauses carried from midi-config-v3 keep the narrowing of the earlier\n'
         'releases\' reviews.',
         '**Status: reviewed local release.** A separate review approved the clauses\n'
         'below, recorded in [the review disposition](REVIEW.md). The clauses carried\n'
         'from midi-config-v3 keep the narrowing of the earlier releases\' reviews.\n'
         'Implementation requires a fresh, restricted implementation workspace.'),
        ('  returned the value last set on it, and the previous data value on each\n'
         '  controller number. Cases MIDI-CONFIG-128 to 161 carry it.',
         '  returned the value last set on it, and the previous data value on each\n'
         '  controller number. Two parts of that code did not run: a notification\n'
         '  that Pick-Up gives after it has decided a value, and the route that\n'
         '  applies a value later instead of at once; the run applied each value at\n'
         '  once. Cases MIDI-CONFIG-128 to 161 carry it.'),
        ('tolerance τ given under [value cases](#value-cases). Two kinds of result can\n'
         'lie farther from the exact rules than τ, so outside the cases that state them\n'
         'they have no expectation:',
         'tolerance τ given under [value cases](#value-cases). τ covers the rounding of\n'
         'one message. Over relative messages in a row on a parameter that is not\n'
         'stepped, that rounding can add up, so a value reached by *k* relative\n'
         'messages in a row is compared within *k* × τ. Three kinds of result can lie\n'
         'farther from the exact rules than that, so outside the cases that state them\n'
         'they have no expectation:'),
        ('  it; their expected values hold.\n'
         '- A Value Scaling move. The travelled fraction can magnify rounding beyond τ.\n'
         '  The moves in cases MIDI-CONFIG-129, 133, 137, 138, 143 to 145, 153, 155 and\n'
         '  161, all with a smaller bound of 0, lie within τ of the exact rule; their\n'
         '  expected values hold.',
         '  it; their expected values hold.\n'
         '- A target value *n* or *p* of a stepped parameter whose exact value lies\n'
         '  within 8τ of a half-integer. Rounding can give either adjacent whole\n'
         '  number. No case has one.\n'
         '- A Value Scaling move. The travelled fraction can magnify rounding far beyond\n'
         '  τ. The moves in cases MIDI-CONFIG-129, 133, 137, 138, 143 to 145, 153, 155\n'
         '  and 161, all with a smaller bound of 0, lie within τ of the exact rule;\n'
         '  their expected values hold. None of them is on a stepped parameter. A\n'
         '  stepped parameter takes only whole-number values, so its value after a\n'
         '  move has no expectation.'),
        ('τ covers the original\'s rounding and the one difference between its two\n'
         'builds (see [provenance](#what-the-contract-means)), except near a bound and\n'
         'for Value Scaling moves ([precision](#starting-state-order-and-precision)).',
         'τ covers the original\'s rounding of one message and the one difference\n'
         'between its two builds (see [provenance](#what-the-contract-means)). The\n'
         '[precision](#starting-state-order-and-precision) rules say where it does not:\n'
         'after relative messages in a row, near a bound, near a half-integer on a\n'
         'stepped parameter and for Value Scaling moves. Each step of the relative\n'
         'cases is exact in single precision, so τ holds for each of their values.'),
        ('outside [*lo*, *hi*]; a parameter that changes a value after it is set; the\n'
         'results near a bound and the Value Scaling moves described under\n'
         '[precision](#starting-state-order-and-precision), outside the cases listed\n'
         'there, and the later values of their sequences; another enabled assignment on',
         'outside [*lo*, *hi*]; a parameter that changes a value after it is set; the\n'
         'results near a bound, the stepped target values near a half-integer and the\n'
         'Value Scaling moves described under\n'
         '[precision](#starting-state-order-and-precision), outside the cases listed\n'
         'there, and the later values of their sequences; another enabled assignment on'),
    ],
    'cases.json': [
        ('"status": "candidate-unreviewed",', '"status": "released-reviewed",'),
    ],
}

for name, edits in EDITS.items():
    p = PKG / name
    text = p.read_text()
    for old, new in edits:
        assert text.count(old) == 1, (name, old[:70])
        text = text.replace(old, new)
    p.write_text(text)
    print(name, len(edits), 'edits')
