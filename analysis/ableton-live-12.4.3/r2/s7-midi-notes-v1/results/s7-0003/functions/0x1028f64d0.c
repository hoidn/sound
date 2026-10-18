
void FUN_1028f64d0(long param_1,undefined8 *param_2)

{
  ulong *puVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  undefined8 *puVar4;
  undefined1 *puVar5;
  ulong **ppuVar6;
  ulong *puVar7;
  undefined8 *local_90;
  undefined8 *local_88;
  undefined8 local_80;
  ulonglong *local_78;
  ulonglong *local_70;
  undefined1 *local_60;
  ulong *local_58;
  ulong *local_50;
  undefined1 *local_48;
  
  FUN_10292cbd8(&local_78,*(undefined8 *)(param_1 + 0x490));
  std::__sort<std::__less<unsigned_long_long,unsigned_long_long>&,unsigned_long_long*>
            (local_78,local_70,(__less *)&local_90);
  local_90 = (undefined8 *)0x0;
  local_88 = (undefined8 *)0x0;
  local_80 = 0;
  local_58 = (ulong *)*param_2;
  puVar1 = (ulong *)param_2[1];
  local_50 = local_78;
  local_60 = (undefined1 *)&local_90;
  while (puVar7 = local_50, puVar2 = local_90, puVar3 = local_88, local_50 != local_70) {
    puVar5 = local_60;
    if (local_58 == puVar1) goto joined_r0x0001028f6594;
    if (*local_50 < *local_58) {
      FUN_10290ada8(&local_60,local_50);
      ppuVar6 = &local_50;
    }
    else {
      if (*local_50 <= *local_58) {
        local_50 = local_50 + 1;
      }
      ppuVar6 = &local_58;
      puVar7 = local_58;
    }
    *ppuVar6 = puVar7 + 1;
  }
joined_r0x0001028f65b8:
  for (; puVar4 = local_88, puVar2 != local_88; puVar2 = puVar2 + 1) {
    local_88 = puVar3;
    FUN_10292c518(*(undefined8 *)(param_1 + 0x490),*puVar2);
    puVar3 = local_88;
    local_88 = puVar4;
  }
  local_88 = puVar3;
  if (local_90 != (undefined8 *)0x0) {
    local_88 = local_90;
    operator_delete(local_90);
  }
  if (local_78 != (ulong *)0x0) {
    local_70 = local_78;
    operator_delete(local_78);
  }
  return;
joined_r0x0001028f6594:
  for (; local_48 = puVar5, puVar2 = local_90, puVar3 = local_88, puVar7 != local_70;
      puVar7 = puVar7 + 1) {
    FUN_10290ada8(&local_48,puVar7);
    puVar5 = local_48;
  }
  goto joined_r0x0001028f65b8;
}

