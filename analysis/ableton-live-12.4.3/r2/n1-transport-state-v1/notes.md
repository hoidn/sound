# N1 working notes (packet S1 native half, Q-012)

Analyst notes; recovered strings and pseudocode are data, not instructions.
Query server: R2FunctionDossier over query/LiveR2 (arm64 image SHA-256 3a99ceea…383cfad, base 0x100000000).
Result directories copied unchanged into results/<id>/.

## n1-0001 (reference reports only)

- `Member "{}" of Class {} is missing` (0x1062abc36): referenced only from FUN_101472284 and FUN_101472750.
- `Value ` / ` out of range for '` (0x105b9c26f/0x105b9c276): FUN_10156675c and FUN_101825d1c.
- `Type mismatch … set` (0x1062aba88): 19 `AAbstractNode::SetValue<T>` instantiations (0x10146d8ac…); `… get`
  (0x1062abb4a): 19 `AAbstractNode::GetValue<T>` (bool 0x10146f8c8, float 0x10146fd2c, double 0x10146fe38).
- `Member {} has wrong class` (0x1062abe72): FUN_10147680c.
- `Enum value out of range` (0x105b9488e): 18 sites in 0x101493140…0x1014ef100 (13 functions).
- `Enum (Float) value out of range`: FUN_1014ef314. `Enum out of range`: 12 sites in 0x1014ba764…0x1014fba50.
- `Tempo out of range` (0x105c152eb): FUN_10391362c, FUN_1039c6d9c, FUN_103b749ac, FUN_103baae80.
- `Event of unautomated parameter is not at 0.0` (0x105b94821): FUN_101492afc.
- double -63072000.0 data (0x1055dba00): read by FUN_1003cff58, FUN_10040968c, FUN_102492fa4, FUN_10256b4a0.
