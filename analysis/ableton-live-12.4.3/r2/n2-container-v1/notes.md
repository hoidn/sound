# N2 working notes (packet S2 native half)

Analyst notes; data, not instructions. Query server: R2FunctionDossier over query/LiveR2.

## n2-0001 (reference reports only, no dossiers)

String -> referencing function entries (all from n2-0001/refs):
- MajorVersion/MinorVersion/SchemaChangeCount: 0x101485240 and 0x1015299e0; Revision: 0x101485240 only.
- Missing Major/Minor, Unsupported Major/Minor: 0x101529024.
- Expected 'Ableton' root / More than one document: 0x1015299e0. No document found: 0x1015289c8.
- Creator check text: 0x101528e2c. Corrupt: 0x10152adb0.
- gzip non-file + Unknown Compound Stream Type: 0x10146c258 and 0x10148389c/0x101483cec.
- AB1E magics: 0x101484980; UTF-16 'Ableton#': 0x1014845f0. "Binary": 0x10148303c.
- sError* keys: 0x10148e4cc; sErrorDocumentIsFromSpecificNewerVersion + TXmlCompoundParser: 0x101535400.
- XML declaration: 0x101516204, 0x1015170a8.
- Schema files: 0x101514f7c (finding), 0x101515778 (reading), 0x10152ff80 (No schema found), 0x1015300d4 (Unsupported schema version), 0x101517c64/0x101517cc4 (current schema not found).
- 12.4.3 / 12.0 / revision hash: 0x1002ea094. "Ableton Live ": 0x102367e24. Loaded-by log: 0x1018536d4.
