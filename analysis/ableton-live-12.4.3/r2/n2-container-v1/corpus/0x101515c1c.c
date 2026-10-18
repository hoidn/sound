
void FUN_101515c1c(void)

{
  int iVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  undefined **ppuVar4;
  undefined8 *puVar5;
  int *local_80;
  undefined8 *local_78;
  undefined8 *puStack_70;
  undefined **local_68;
  undefined8 uStack_60;
  int *local_58;
  undefined8 *local_50;
  undefined8 *puStack_48;
  undefined8 *local_40;
  undefined8 *puStack_38;
  
  local_40 = (undefined8 *)0x0;
  puStack_38 = (undefined8 *)0x0;
  iVar1 = FUN_1011b5354();
  if (iVar1 == 0) {
    puVar2 = (undefined8 *)FUN_1012d9850(0x20);
    puVar2[1] = 0;
    *puVar2 = 0;
    puVar2[3] = 0;
    puVar2[2] = 0;
    FUN_10128ed98();
    ppuVar4 = &PTR_thunk_FUN_10128edf8_106676608;
  }
  else {
    puVar2 = (undefined8 *)FUN_1012d9850(0x20);
    puVar2[1] = 0;
    *puVar2 = 0;
    puVar2[3] = 0;
    puVar2[2] = 0;
    FUN_10128ed98();
    ppuVar4 = &PTR_thunk_FUN_10128edf8_1066766c8;
  }
  puVar5 = puVar2 + 3;
  *puVar5 = ppuVar4 + 10;
  *puVar2 = ppuVar4;
  iVar1 = *(int *)(puVar2 + 1);
  *(int *)(puVar2 + 1) = iVar1 + 1;
  *(int *)(puVar2 + 1) = iVar1 + 2;
  uVar3 = DAT_106e0d200;
  local_78 = puVar2;
  puStack_70 = puVar5;
  local_40 = puVar2;
  puStack_38 = puVar5;
  FUN_101515508(&local_80);
  local_68 = &PTR_FUN_106675f58;
  uStack_60 = uVar3;
  local_58 = local_80;
  local_50 = puVar2;
  puStack_48 = puVar5;
  if (local_80 == (int *)0x0) {
    *(int *)(puVar2 + 1) = *(int *)(puVar2 + 1) + 1;
    iVar1 = *(int *)(puVar2 + 1) + -1;
    *(int *)(puVar2 + 1) = iVar1;
  }
  else {
    iVar1 = *local_80;
    *(int *)(puVar2 + 1) = *(int *)(puVar2 + 1) + 1;
    if (iVar1 == 0) {
      FUN_101449efc();
    }
    iVar1 = *(int *)(puVar2 + 1) + -1;
    *(int *)(puVar2 + 1) = iVar1;
  }
  if (iVar1 == 0) {
    FUN_10128eea0(puVar2);
  }
  uVar3 = FUN_101470ef4();
  FUN_101515ed8(&local_68,uVar3);
  local_68 = &PTR_FUN_106675f58;
  if ((local_50 != (undefined8 *)0x0) &&
     (iVar1 = *(int *)(local_50 + 1), *(int *)(local_50 + 1) = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_10128eea0();
  }
  if ((local_58 != (int *)0x0) && (iVar1 = *local_58, *local_58 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  iVar1 = *(int *)(puVar2 + 1);
  *(int *)(puVar2 + 1) = iVar1 + -1;
  if (iVar1 + -1 == 0) {
    FUN_10128eea0(puVar2);
  }
  return;
}

