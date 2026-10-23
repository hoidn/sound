# Pickup step: unchanged-driver capability

**Source-only design record; no capture script or execution selected.**

The existing driver can express the event-free same-instance boundary: process
8192 frames, send one parameter command, process the next8192 frames. Keep the
same inputFILE open so its cursor continues, and the same outFILE already appends
a contiguous result. No new scheduler, harness, loader or export is needed.

[Capability and exact source spans](capability.json) distinguish this structural
support from actual response. The driver retains the devicehandle but replaces
hostbuffers perprocess; a future control must use the same segmentation. The
local eventposition resets perprocess while the staticqueue persists, so this
shape is restricted to an event-free modal history. Transport stays at its
configured position, and inputflag is reinitialized before every CalcA.

The existing4000-frame pickup movement claim remains unrendered. Productive
left/right ringing, actual stepresponse, unaffectedchannel accuracy and any
smoothing law need separately selected captures and reviewed measurements.
No vector, stepvalue, script, collector, criterion, capture or newexpectation is
authorized here. Source/binary pins are data identity checks, not runtime proof.
