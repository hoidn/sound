
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 * FUN_1031d6b30(undefined8 *param_1)

{
  char cVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  ulong extraout_RDX;
  uint local_38;
  undefined4 uStack_34;
  undefined4 uStack_30;
  undefined4 uStack_2c;
  void *local_28;
  undefined8 uStack_20;
  
  local_28 = _DAT_105e2c7c8;
  uStack_20 = _UNK_105e2c7d0;
  local_38 = _DAT_105e2c7b8;
  uStack_34 = _UNK_105e2c7bc;
  uStack_30 = _UNK_105e2c7c0;
  uStack_2c = _UNK_105e2c7c4;
  FUN_101188890(&local_38);
  if ((extraout_RDX & 1) == 0) {
    puVar2 = (undefined8 *)FUN_1012bdaa0(0x18);
    FUN_1012715b0(puVar2);
    *puVar2 = &PTR_FUN_106e02768;
    uVar3 = std::chrono::system_clock::now();
    FUN_10410fff0(&local_38,2,uVar3);
    cVar1 = FUN_10410c530(&local_38);
    if (cVar1 != '\0') {
      FUN_104108bf0(&local_38,"Audio2Midi: Use builtin MultiF0 lib");
    }
    FUN_104108a10(&local_38);
    *(int *)(puVar2 + 1) = *(int *)(puVar2 + 1) + 1;
    *param_1 = puVar2;
    return param_1;
  }
  FUN_1031d6330(&local_38);
  if ((local_38 & 1) == 0) {
    if ((byte)local_38 >> 1 != 0) goto LAB_1031d6b86;
  }
  else if (CONCAT44(uStack_2c,uStack_30) != 0) {
LAB_1031d6b86:
    FUN_1031d66b0(param_1,&local_38);
    goto joined_r0x0001031d6b9a;
  }
  *param_1 = 0;
joined_r0x0001031d6b9a:
  if ((local_38 & 1) != 0) {
    operator_delete(local_28);
  }
  return param_1;
}

