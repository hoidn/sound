---
id: RESEARCH-LIVE-API-DEVICE-RACK
type: research
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current public LOM index12.4.5 applicability U
---

# Public API device, rack and mixer source record

## Question and bounded ownership

Which direct members in the selected device/rack/mixer references have typed
source-backed roles without reconstructing inheritance, missing arguments or
numeric behavior? The [canonical draft](../specs/live-api-device-rack.md),
[full plan](full-live-specification-plan.md) and
[coverage design](full-live-specification-design.md) bound this partial F-05/F-08
work. The [API bridge](../specs/live-api-bridge-workflows.md) keeps generic object/
message/identity/observation/remote/init roles. SimplerDevice/View, Track and other
specialized classes remain excluded/separately owned. No new runtime or clean
implementation work occurred.

## Exact immutable selection and denominator

The requested11 names yield10 exact R1 entries; Chain.View is absent and not added.
The [denominator](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/denominator.json) lists each original direct member,
and the [ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/member-ledger.json) preserves its heading/type/access
and source spans. There are95 direct declarations (25children/53properties/
17functions), each linked to one requirement/case. Of these94 have bounded
source-backed roles and one, DrumPad.delete_all_chains, is heading-only semantic U.
Thus linked denominator95/95 and unlinked0 is a documentation map, not complete
semantics. All95 target members remain unclosed. Eight additional U obligations
produce103 requirements (94 D-current-public/9 U) and113 null-oracle future cases.
The global45-reference/588-direct-member inventory and inherited semantics are
not covered by these selected counts.

All315 text blocks in the10 selected references were read, including declaration
and canonical-path context. Source RackDevice inherits Device, RackDevice.View
inherits Device.View and DrumChain inherits Chain, but this packet does not flatten
or count inherited members. Sparse headings/access metadata remain exact declarations,
not behavior inferred from names. A printed scalar child type with a plural name
stays ambiguous. Missing argument lists are not empty lists; missing returns are
not void, success or no-output claims.

The original R1 inventory index declares Live12.4.5, later than12.4.3. Individual
current Max/reference versions are not matched. Local D-current-public denotes
publication text only. Source since11.0/12.3 contexts and every target availability,
default and behavior remain U. No current/public class guarantees runtime presence.

## Sources and locators

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/sources.json) preserves the exact reviewed R1 capture
records; retained_path points to the original immutable source, without recapture.
The mutable source-family page is navigation only, not an evidence pin. R1 manifest
seal is `67e24da58fb1d91d8c55659c65eb0779a3c3e8cc2424ddcf07915032d8637a73`;
all65 original payloads remain immutable. [Inventory pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/inventory-pins.json)
add the exact original source catalog, block catalog, parser, source-page snapshot,
entry and direct-member inventories. The pure reused parser is imported without
executing its guarded capture/write branch. [Pure member span extraction](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/derive.py)
records heading through next heading; it never fetches or writes a source.

### Device

[C74-LOM-DEVICE](https://docs.cycling74.com/apiref/lom/device/), final [https://docs.cycling74.com/apiref/lom/device/](https://docs.cycling74.com/apiref/lom/device/); captured `2026-10-19T22:11:38.160066+00:00`, 64772bytes, SHA-256 `9152de1814b341d479aafb198fea3a425657ea12db10bcd777d2ee5bd3432818`. Index declares Live12.4.5; target12.4.3 applicability U. [51 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json), 15 direct declarations.

### Device.View

[C74-LOM-DEVICE_VIEW](https://docs.cycling74.com/apiref/lom/device_view/), final [https://docs.cycling74.com/apiref/lom/device_view/](https://docs.cycling74.com/apiref/lom/device_view/); captured `2026-10-19T22:11:38.225549+00:00`, 45049bytes, SHA-256 `9d8612567da7ca7eeef3de78f17058c67f519e5adac7043b6fe3cafb09cb9f84`. Index declares Live12.4.5; target12.4.3 applicability U. [10 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json), 1 direct declarations.

### DeviceParameter

[C74-LOM-DEVICEPARAMETER](https://docs.cycling74.com/apiref/lom/deviceparameter/), final [https://docs.cycling74.com/apiref/lom/deviceparameter/](https://docs.cycling74.com/apiref/lom/deviceparameter/); captured `2026-10-19T22:11:38.579899+00:00`, 59750bytes, SHA-256 `f513d7dbd1dba0d142b5dbb97fa3feb591e452bec990e851cbfffca04836b510`. Index declares Live12.4.5; target12.4.3 applicability U. [48 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json), 15 direct declarations.

### MixerDevice

[C74-LOM-MIXERDEVICE](https://docs.cycling74.com/apiref/lom/mixerdevice/), final [https://docs.cycling74.com/apiref/lom/mixerdevice/](https://docs.cycling74.com/apiref/lom/mixerdevice/); captured `2026-10-19T22:11:45.170593+00:00`, 56468bytes, SHA-256 `da5bebace3b423ba58b801eaebdd8b24e88cf8af84ac24e9e7b4a374f16416eb`. Index declares Live12.4.5; target12.4.3 applicability U. [36 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json), 11 direct declarations.

### RackDevice

[C74-LOM-RACKDEVICE](https://docs.cycling74.com/apiref/lom/rackdevice/), final [https://docs.cycling74.com/apiref/lom/rackdevice/](https://docs.cycling74.com/apiref/lom/rackdevice/); captured `2026-10-19T22:11:45.581001+00:00`, 65883bytes, SHA-256 `140dc6c9bdf4e8f28f774521baa100bbec626098659d9254805c909643d0436b`. Index declares Live12.4.5; target12.4.3 applicability U. [59 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json), 21 direct declarations.

### RackDevice.View

[C74-LOM-RACKDEVICE_VIEW](https://docs.cycling74.com/apiref/lom/rackdevice_view/), final [https://docs.cycling74.com/apiref/lom/rackdevice_view/](https://docs.cycling74.com/apiref/lom/rackdevice_view/); captured `2026-10-19T22:11:45.559723+00:00`, 47047bytes, SHA-256 `f69977f9cdedc942b7743e319f125e4a3349c9db5c8ba0b4393922a1de59af9c`. Index declares Live12.4.5; target12.4.3 applicability U. [16 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json), 4 direct declarations.

### Chain

[C74-LOM-CHAIN](https://docs.cycling74.com/apiref/lom/chain/), final [https://docs.cycling74.com/apiref/lom/chain/](https://docs.cycling74.com/apiref/lom/chain/); captured `2026-10-19T22:11:36.879510+00:00`, 65732bytes, SHA-256 `e8c6c531d04016e6b5f70335ada7c3f49942019caa4a426417174d6ddff8285f`. Index declares Live12.4.5; target12.4.3 applicability U. [46 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json), 15 direct declarations.

### ChainMixerDevice

[C74-LOM-CHAINMIXERDEVICE](https://docs.cycling74.com/apiref/lom/chainmixerdevice/), final [https://docs.cycling74.com/apiref/lom/chainmixerdevice/](https://docs.cycling74.com/apiref/lom/chainmixerdevice/); captured `2026-10-19T22:11:37.271048+00:00`, 47506bytes, SHA-256 `20432e077704d66d437ff31becaddfdd9610b637e7a83e830852e0f633c75def`. Index declares Live12.4.5; target12.4.3 applicability U. [17 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json), 4 direct declarations.

### DrumChain

[C74-LOM-DRUMCHAIN](https://docs.cycling74.com/apiref/lom/drumchain/), final [https://docs.cycling74.com/apiref/lom/drumchain/](https://docs.cycling74.com/apiref/lom/drumchain/); captured `2026-10-19T22:11:38.985480+00:00`, 43203bytes, SHA-256 `b01611b4f99a9a48f3e2ff51c79d7824238c21a695981080919dec9b93045166`. Index declares Live12.4.5; target12.4.3 applicability U. [12 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json), 3 direct declarations.

### DrumPad

[C74-LOM-DRUMPAD](https://docs.cycling74.com/apiref/lom/drumpad/), final [https://docs.cycling74.com/apiref/lom/drumpad/](https://docs.cycling74.com/apiref/lom/drumpad/); captured `2026-10-19T22:11:39.076322+00:00`, 50905bytes, SHA-256 `1d782ca75dfb42e0c3c2a699881d07cec4a9f9a3181a9c6310b533e57e2de5a8`. Index declares Live12.4.5; target12.4.3 applicability U. [20 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json), 6 direct declarations.

## Interpretation and owner boundaries

[Device racks](../specs/device-racks.md), [bundled parameters](../specs/bundled-device-parameters.md),
[mixer values](../specs/mixer-values.md), [mix graph](../specs/mix-graph.md),
[Set structure](../specs/live-set-structure.md), [automation](../specs/automation-envelopes.md),
[automation workflows](../specs/automation-workflows.md), [mapping](../specs/midi-user-mapping.md),
[transport](../specs/transport-state.md), [projects](../specs/project-media-workflows.md)
and [hosting](../specs/max-for-live-hosting.md) retain existing file/native/numeric/UI
laws and open assumptions. API IDs/type codes/property domains do not rewrite
finite stored mixer enums, faders/gain/ramps, parameter values, mapping encoding,
REQ013, graph/voice/clock behavior or preset identity. AB/macro/variation labels
supply no private state architecture, probability distribution or mandatory change.
Declared latency samples/ms supplies no driver clock or compensation formula.

All API responses, callback/message/ID values, signal/timing/numeric and file/
persistence outcomes are null documentary oracles. Source claims are isolated from
target expected/comparison, which are null/U/unexecuted in every case. Conditional
capabilities and sparse/contradictory contexts need actual independently eligible
positive baselines. No own Set/patch/script/host, response/notification/audio trace,
controller or accepted ID is supplied. Absent capability cannot prove rejection,
no effect, silence or successful cleanup.

### Q-LADR-001 — Current reference versus target

The immutable inventory index declares12.4.5; exact12.4.3 and matching Max/platform/member availability remain U. Explicit since11.0/12.3 statements do not prove this target.

### Q-LADR-002 — Direct and inherited cardinality

RackDevice/RackDevice.View/DrumChain declare base-class inheritance in source context; the95-direct denominator is not flattened inheritance. Chain.View is absent from R1, not proved absent in Live. Chain.devices is printed Device and DrumPad.chains Chain despite plural names; cardinality remains unresolved.

### Q-LADR-003 — Chain mixer sends predicate

ChainMixerDevice.sends source says [in Audio Effect Racks and Instrument Racks only] For Drum Racks, otherwise empty. Preserve the exact source wording and determine eligibility/emptiness later; no repaired graph/predicate is adopted.

### Q-LADR-004 — Parameter domains and flags

DeviceParameter value/display_value/default/min/max and quantized/enabled/state/automation flags do not establish API-to-stored/native units, type widths, converters, precedence or numerical/no-audible-effect results. StringVector/unicode/long retain printed names only.

### Q-LADR-005 — Missing arguments returns and sparse declarations

Only six functions have explicit typed parameter declarations and two a typed return. Undocumented is not zero arguments/void. DrumPad.delete_all_chains is a heading only and semantic U; sparse capability/child headings do not justify behavior from their names.

### Q-LADR-006 — Mixer roots units and colors

Source master-track/API path naming is not silently changed to Main, nor are API enum codes equated to finite stored/native values. Samples/ms latency members supply no clock/conversion/compensation formula. RGB/nearest palette/MIDI note/choke descriptions give no new codec, distance metric or sound law.

### Q-LADR-007 — Insertion and compare predicates

12.3 insertion and AB compare support/error roles retain native-only/type-order/optional-index and can_compare_ab conditions. Complete acceptance, invalid-index/no-object outcomes, exact errors, return and transactions remain unknown.

### Q-LADR-008 — Macro variation and selection scope

Visible counts, mapped Macros, selected versus last-recalled variation and eligible randomization remain distinct. No seed/distribution/mandatory change, copied-value equality, count limit, default, no-selection or persistence law follows.

### Q-LADR-009 — Access history notification and lifecycle

Declared get/set/observe is documentary access, not accepted runtime proof. Mutation-time callbacks, override/remote/re-enable, Undo, save/reopen/editor moves, cancellation/concurrency, transport/rate, target/source/context loss and teardown remain ungraded with positive active context required.

## Finite proposals and freeze

[Fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/fixtures.json) require independently valid owned
initialized Live/Max/API patch/device/context and actual supported member/access,
positive same-context binding/readback/call/change before invalid/no-effect probes.
Active audible/remote tests add nonempty eligible source, nonzero base/depth/amount/
gain/send, enabled control/path, nonmuted wet/return/output and calibrated paired
positive baseline with explicit arm/monitor/receiver/clip/transport/record/automation.
Member-specific function proposals preserve documented parameters, conditions and
unknown arguments/returns. Cross-cutting probes cover invalid/capability, insertion/
compare, automation/remote/inactive, macro variation/random/pad copy, history/save/
cancel/concurrent mutation, transport/rates, context/source loss/recovery and teardown.
They create no call recipe, asynchronous cancel, rollback, schedule, latency or
numeric/signal law.

[Owner pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/owner-pins.json), [counts](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/counts.json),
[questions](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/questions.json), [manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/manifest-author-r1.json)
and canonical snapshots seal this partial author revision. The
[validator](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/validate.py) is read-only, run with `python -B`, prints
stdout only and never rewrites frozen reports. It checks original R1 payloads,
source/entry/member identity, spans/typed metadata, exact browser IDs, every case/
null/source relationship, snapshots, links and untracked-aware whitespace.
Integrity checks are not semantic review or runtime proof. Independent review and
exact-target evidence remain pending; root owns shared catalog/coverage/log updates.
No runtime/native/API/patch/example/hardware/account/service/install/implementation
or destructive file operation was performed. Amp/Cabinet blocker remains unchanged.
