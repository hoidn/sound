
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1031b625c(long param_1,undefined8 param_2,undefined4 param_3)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 *puVar3;
  undefined8 uVar4;
  
  uVar4 = *(undefined8 *)(param_1 + 0x508);
  puVar3 = (undefined8 *)FUN_1012d9850(0x30);
  FUN_10128ed98();
  *puVar3 = &PTR_thunk_FUN_10128edf8_1068ddff8;
  *(undefined4 *)(puVar3 + 3) = param_3;
  uVar2 = _DAT_10561dfd0;
  puVar3[5] = _UNK_10561dfd8;
  puVar3[4] = uVar2;
  *(int *)(puVar3 + 1) = *(int *)(puVar3 + 1) + 1;
  FUN_103192720(0,param_2,uVar4,"F1 To F2",puVar3,0,0);
  iVar1 = *(int *)(puVar3 + 1);
  *(int *)(puVar3 + 1) = iVar1 + -1;
  if (iVar1 + -1 == 0) {
    FUN_10128eea0(puVar3);
  }
  return;
}

