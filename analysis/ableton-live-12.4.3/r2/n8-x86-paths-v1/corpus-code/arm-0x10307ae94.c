// arm 0x10307ae94 FUN_10307ae94 state=exported-with-warnings chunk=chunk-02331.jsonl code_sha256=832b614871a58ba12372d486ef25a0b3b14047235a6e38c35aa862a5bce2e902

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10307ae94(undefined8 *param_1)

{
  ulong uVar1;
  int iVar2;
  undefined8 *puVar3;
  undefined8 uVar4;
  ulong extraout_x1;
  void *local_40;
  ulong uStack_38;
  undefined8 uStack_30;
  undefined8 uStack_28;
  
  uStack_38 = _UNK_1058c2a00;
  local_40 = _DAT_1058c29f8;
  uStack_28 = _UNK_1058c2a10;
  uStack_30 = _DAT_1058c2a08;
  FUN_1011aeb80(&local_40);
  if ((extraout_x1 & 1) == 0) {
    puVar3 = (undefined8 *)FUN_1012d9850(0x18);
    FUN_10128ed98();
    *puVar3 = &PTR_thunk_FUN_10128edf8_1068bcd10;
    uVar4 = std::chrono::system_clock::now();
    FUN_103f3ffec(&local_40,2,uVar4);
    iVar2 = FUN_103f3c8b8(&local_40);
    if (iVar2 != 0) {
      FUN_103f39a78(&local_40,"Audio2Midi: Use builtin MultiF0 lib");
    }
    thunk_FUN_103f395e4(&local_40);
    *(int *)(puVar3 + 1) = *(int *)(puVar3 + 1) + 1;
    *param_1 = puVar3;
    return;
  }
  FUN_10307a630(&local_40);
  uVar1 = uStack_38;
  if (-1 < (char)uStack_30._7_1_) {
    uVar1 = (ulong)uStack_30._7_1_;
  }
  if (uVar1 == 0) {
    *param_1 = 0;
    if (((uint)(int)(char)uStack_30._7_1_ >> 7 & 1) != 0) goto LAB_10307af84;
  }
  else {
    FUN_10307a96c(param_1,&local_40);
    if (uStack_30 < 0) {
LAB_10307af84:
      operator_delete(local_40);
      return;
    }
  }
  return;
}

