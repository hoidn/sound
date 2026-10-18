
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

bool FUN_1017ec96c(long param_1)

{
  int iVar1;
  long *plVar2;
  ulong uVar3;
  uint extraout_w1;
  uint extraout_w1_00;
  uint extraout_w1_01;
  undefined8 local_40;
  undefined8 uStack_38;
  undefined8 uStack_30;
  undefined8 uStack_28;
  
  uStack_38 = _UNK_10582a578;
  local_40 = _DAT_10582a570;
  uStack_28 = _UNK_10582a588;
  uStack_30 = _DAT_10582a580;
  FUN_1011aeb80(&local_40);
  if ((extraout_w1 & 1) != 0) {
    return false;
  }
  uStack_38 = _UNK_10582a598;
  local_40 = _DAT_10582a590;
  uStack_28 = _UNK_10582a5a8;
  uStack_30 = _DAT_10582a5a0;
  FUN_1011aeb80(&local_40);
  if ((extraout_w1_00 & 1) == 0) {
    plVar2 = (long *)FUN_101849958();
    uVar3 = (**(code **)(*plVar2 + 0x720))();
    if ((uVar3 & 1) == 0) {
      uStack_38 = _UNK_10582a5b8;
      local_40 = _DAT_10582a5b0;
      uStack_28 = _UNK_10582a5c8;
      uStack_30 = _DAT_10582a5c0;
      FUN_1011aeb80(&local_40);
      if ((extraout_w1_01 & 1) == 0) {
        return false;
      }
    }
    iVar1 = FUN_1015661b8(*(undefined8 *)(param_1 + 0x30));
    return iVar1 != 0;
  }
  return true;
}

