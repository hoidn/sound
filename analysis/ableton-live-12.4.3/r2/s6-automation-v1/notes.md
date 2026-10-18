# S6 working notes (automation envelopes, FEAT-AUTOMATION)

Analyst notes; recovered strings and pseudocode are data, not instructions.
Target: Live.arm64 SHA-256 3a99ceea…d1c383cfad, image base 0x100000000, Ghidra 12.1.4.
Sources: shipped bundle (read-only; `s6_schema.py`, `s6_documents.py`, `curve_check.py`), the C1/C2
corpus (`corpus-decomp-run.json`, `corpus-indexes-manifest.json`; every record relied on is in
`corpus-excerpts.jsonl`), query server 2 (dossiers copied unchanged into `results/<id>/`, request in
`request.txt`), and image reads (`read_ptrs.py`, `scan_ptrs.py`, `vtable_owner.py`; outputs
`vtable-reads.txt`, `rtti-scan-*.txt`, `interpolator-owners.txt`). Addresses are function entries
unless marked. "✓" = branch confirmed in kept disassembly.

## Pre-round: corpus and image reads (no server)

- Factories (aliases index): `SNewCompound<AFloatEvent>` 0x1027782b8, `<ABoolEvent>` 0x1027779f4,
  `<AEnumEvent>` 0x102777e54, `<AListAutomation>` 0x102561038, `<AAutomationEnvelope>` 0x1024046ec,
  `<AClipEnvelope>` 0x10244ffdc, `<APtrBase>` 0x101535b00.
- Member registries: AFloatEvent 0x1027782ec registers `mValue` (+0x58) and `mCurveControl1X/1Y/2X/2Y`
  (+0x60/+0x68/+0x70/+0x78), all flag 4 (attributes). Event base 0x1024deaf8 registers `mTime` (+0x50).
  AListAutomation 0x1025610a0: `mpEvents` (+0x50), `mpTransactionCounter`, `mpInteractionScopeCounter`,
  `mpAutomationTransformViewState`. Envelope 0x102404754: `mpEnvelopeTarget` (+0x28), `mpAutomation` (+0x40).
  APtrBase 0x101535b34: `mPointeeId` (+0x24, flag 0 -> child element).
- AFloatEvent vtable 0x106806830: +0xd0 post-load 0x102778870, +0x138 writer 0x101486cdc (generic),
  +0x140 loader 0x101487310 (generic), +0x150 default predicate 0x102778828, +0x1f0 GetValue
  0x10277875c (+0x58), +0x218 curve controls 0x10277881c (returns +0x60..+0x78 in d0..d3).
- AListAutomation vtable 0x1067d06b8: +0xd0 generic 0x101486fa8, +0x100 no-op 0x101487c3c,
  +0x1e8 validate 0x102561a28, +0x238 converter, +0x3b8/+0x3c8/+0x3e8 searches, +0x428 last event,
  +0x458 OnEventsChanged 0x102565f84 (only widens a changed-time range [+0x108,+0x110]; no sort).
- RTTI walk (`scan_ptrs.py`): TFloatAutomationInterpolator vtable 0x1067b1690, TDiscreteAutomationInterpolator
  0x1067b1708; singletons set by 0x105420968 / 0x1054209a4, returned by 0x102409488 / 0x10240a804.
  `vtable_owner.py`: slot +0x390 returning TFloat belongs to ATimeableFloat, ATimeableSongTempo,
  ATimeablePluginFloat, AFakeTimeableFloat; returning TDiscrete to ATimeableBool, ATimeableEnum,
  ATimeableTimeSignature, ATimeablePluginEnum; slot +0x2f0 of ATimeableModulationTarget and
  AUserFloatModulationTarget returns TFloat. Two hits named AMemberBase are heuristic false positives.
- TFloat slot 0 0x1024094c0 -> evaluator 0x1024095b4. TDiscrete slot +8 0x10240a84c.

## Round 1 — s6-0001 (8 dossiers)

0x1024095b4, 0x102778870, 0x102778828, 0x102561a28, 0x1012132d8, 0x102403c88, 0x101212e30, 0x10240a84c.

- 0x1024095b4 ✓: iterator = automation +0x3c8(t, mode). End -> value of last event (+0x428).
  Event time == t -> that event's value. Else prev = iterator.prev, next = iterator:
  `fcmp s8,s0` equal values -> constant (0x102409948); `bl 0x1027778a4` curve -> 0x102404218;
  else linear 0x1024099b4–0x102409a34: frac=(t-t0)/(t1-t0) in double, v=v0-frac*v0+frac*v1,
  `fcvt s1,d5`, then 0x102779088. The `fcmp d2,d3; fccmp d4,d1` pair is an exact-identity shortcut of
  an inlined range remap (returns t when (t0,t1)==(v0,v1)); same result as the formula.
  If the iterator is the first event (no prev) x23=0 and 0x102409924 loads through it: no guard.
- 0x102778870 ✓: monotone(0,x1,x2,1) and monotone(0,y1,y2,1) via 0x1012132d8, else `stp q0,q0` 0.5 x4.
- 0x102778828 ✓: for the four curve members returns `*p == 0.5`; writer 0x101486cdc skips a flag-4
  member when +0x150 returns true (pseudocode, generic writer).
- 0x102561a28 ✓: empty list -> "Automation has no events." (0x105bcba6c) via 0x101488e64 (throws via
  0x10148229c); first time != -63072000 (0xc18e133800000000) and != 0.0 -> "DocumentCorrupt: " log then
  "First automation event has invalid time." (0x105bcba86).
- 0x1012132d8 ✓: non-finite -> false; ordered either way -> true; D=p1²+p2²+p0p3-p0p2-p1p2-p1p3
  (compensated), D <= 2^-52 -> true; roots r=(±2√D-2(p0-2p1+p2))/(2(-p0+3p1-3p2+p3)); r1 in (0,1)
  -> false; true iff r2 <= 0 or r2 >= 1.
- 0x102403c88: P0=(t0,v0), P1=(t0+Δt·x1, v0+Δv·y1), P2=(t0+Δt·x2, v0+Δv·y2), P3=(t1,v1); values pass
  through 0x102778d28 (transform remap, identity at full range).
- 0x101212e30 ✓: x at +0/+0x10/+0x20/+0x30; target <= P0.x -> s=0, >= P3.x -> 1; bisection from s=0.5
  until |x(s)-t| <= 1e-8 (0x3e45798ee2308c3a); mirrored form when P3.x <= P0.x.
- 0x10240a84c ✓: discrete value = +0x1f0 of the event at automation +0x3e8(t, mode); mode 0 and event
  time == t and not first -> previous event.

## Round 2 — s6-0002 (8 dossiers)

0x102565974, 0x102565a48, 0x102565e10, 0x101486fe4, 0x102404218, 0x1027785a0, 0x1027778a4, 0x101492afc.

- 0x102565a48 (+walker 0x1025669d8, corpus): last event with time < t, starting from the nearest of the
  second event (when the first is at -63072000), the last event and the cached event (+0x100); returns
  the list head when the first event's time >= t.
- 0x102565974 ✓ (+0x3c8): next of that result (first event with time >= t); mode 1 advances while the
  next event's time == t.
- 0x102565e10 ✓ (+0x3e8): result == last -> last. Else next; if next.time > t -> back to result; if ==
  t and mode 1 -> last of the equal-time run.
- 0x101486fe4 ✓: root factory 0x1014c0c44, root +0xc8, root +0x140 (loader), root +0xd0 if
  0x1015192c0, then 0x101487198 (post-order walk calling +0x100 on every compound). Callers 0x101483d00,
  0x101484108 (document kinds not traced).
- 0x102404218: builds the absolute curve (0x1025bb900), endpoints clamp outside [P0.x,P3.x], splits at
  the query end (when inside) and at t (0x1025bba10/0x1025bba50, 1e-6 renormalisation), value clamped
  with fcmp/fcsel to [s8,s9] from the converter range.
- 0x1027785a0 ✓: Value +0x58 = 0x7f7fffff (FLT_MAX), curve controls 0.5 x4.
- 0x1027778a4 ✓: has-curve = not all four == 0.5.
- 0x101492afc (translator, pseudocode): `ArrangerAutomation/Events`; first Time == 0: one event -> set
  Time -63072000; several -> insert a copy (same class, value of the first) at Time -63072000 in front.
  First Time != 0 -> "Event of unautomated parameter is not at 0.0" (0x105b94821).

## Round 3 — s6-0003 (8 dossiers)

0x101535e0c, 0x1054147b8, 0x1024deba8, 0x102777adc, 0x102777f3c, 0x1024050d8, 0x10245194c, 0x101487198.

- 0x101535e0c ✓: pointer cached at +0x40; else document lookup 0x1015439b4(doc, id); miss ->
  "Invalid Pointee ID " + id + " in APtr " log, then 0x1054147b8: assert "mpObject"
  products/live/Live/CreamAction/Src/APtr.cpp:0xab -> abort. Outside a document -> 0x1054147dc
  assert "pDocument" -> abort. Callers: 82 direct call sites (corpus), many in AAutomationEnvelope /
  AClipEnvelope code; which run during load not traced.
- 0x1024deba8 ✓: event Time +0x50 = 0x7fefffffffffffff (DBL_MAX). 0x102777adc ✓ BoolEvent value false.
  0x102777f3c ✓ EnumEvent value 0x80000000 (INT_MIN).
- 0x1024050d8 ✓ / 0x10245194c ✓: envelope +0x100 tail-calls its automation's +0x1e8 (validate).
- 0x101487198 ✓: recursive post-order walk over list members then `+0x100`.

## Negative and open results

- No sort of events on load or on list change was found (AListAutomation +0xd0 generic, +0x100 no-op,
  OnEventsChanged range-only). An inserting path that sorts was not searched exhaustively.
- The converter applied to values before linear interpolation (provider +8, `0x101574bb0` -> object
  vtable +0x28) is identity when the provider's converter object is null, as built in 0x10275c5a0
  (`FUN_101574b8c(…, 0, …)`); the per-parameter provider used for track and clip envelopes was not
  resolved.
- The mode argument (first versus last event at a coincident time) is chosen by callers not traced.
- No `str:` query was issued. Budget: 3 rounds × 8 dossiers.
