
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1028e2af4(long *param_1)

{
  undefined8 uVar1;
  undefined8 uVar2;
  long lVar3;
  undefined8 *puVar4;
  
  lVar3 = FUN_1012d9734(0x60);
  puVar4 = (undefined8 *)FUN_1014826c4();
  *puVar4 = &PTR_thunk_FUN_10128edf8_1068256e0;
  puVar4[5] = &PTR_FUN_106825898;
  uVar2 = _UNK_10561dfb8;
  uVar1 = _DAT_10561dfb0;
  puVar4[7] = &DAT_7fefffffffffffff;
  puVar4[6] = &DAT_7fefffffffffffff;
  puVar4[9] = uVar2;
  puVar4[8] = uVar1;
  *(undefined1 *)(puVar4 + 10) = 1;
  puVar4[0xb] = 0;
  FUN_101486414();
  *param_1 = lVar3;
  *(int *)(lVar3 + 8) = *(int *)(lVar3 + 8) + 1;
  FUN_101482718(lVar3);
  return;
}

