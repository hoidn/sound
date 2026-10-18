// 0x10189ee9c FUN_10189ee9c exported-with-warnings  sig: undefined FUN_10189ee9c()

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_10189ee9c(long param_1)

{
  int iVar1;
  undefined8 uVar2;
  uint extraout_w1;
  undefined8 local_40;
  undefined8 uStack_38;
  undefined8 uStack_30;
  undefined8 uStack_28;
  
  iVar1 = FUN_1011b59ec();
  if (iVar1 == 0) {
    uStack_38 = _UNK_105830ca0;
    local_40 = _DAT_105830c98;
    uStack_28 = _UNK_105830cb0;
    uStack_30 = _DAT_105830ca8;
    FUN_1011aeb80(&local_40);
    if ((extraout_w1 & 1) == 0) {
      iVar1 = FUN_1011c4750();
      if (iVar1 == 4) {
        uVar2 = FUN_1015645a0(*(undefined8 *)(param_1 + 0x30));
        return uVar2;
      }
      return 1;
    }
  }
  return 0;
}


