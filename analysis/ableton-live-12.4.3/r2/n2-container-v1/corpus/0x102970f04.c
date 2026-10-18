
/* WARNING: Removing unreachable block (ram,0x000102970fcc) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_102970f04(long param_1)

{
  int iVar1;
  ulong uVar2;
  long *plVar3;
  undefined8 uVar4;
  ulong extraout_x1;
  void *local_88 [2];
  char local_71;
  void *local_70 [2];
  char local_59;
  void *local_58 [2];
  char local_41;
  undefined8 local_40;
  undefined8 uStack_38;
  undefined8 uStack_30;
  undefined8 uStack_28;
  
  iVar1 = FUN_1011b59ec();
  if (iVar1 != 1) {
    FUN_101747a10();
    uVar2 = FUN_101747db8();
    if ((uVar2 & 1) == 0) {
      uStack_38 = _UNK_10589a5b4;
      local_40 = _DAT_10589a5ac;
      uStack_28 = _UNK_10589a5c4;
      uStack_30 = _DAT_10589a5bc;
      FUN_1011aeb80(&local_40);
      if ((((extraout_x1 & 1) == 0) && (iVar1 = FUN_1011b59ec(), iVar1 != 2)) &&
         ((*(byte *)(param_1 + 0x1d9) & 1) == 0)) {
        plVar3 = (long *)FUN_101849958();
        uVar4 = (**(code **)(*plVar3 + 0x718))();
        if ((int)uVar4 == 0) {
          return uVar4;
        }
        FUN_1011db880(local_70);
        local_40 = 0x7972617262694c;
        uStack_30 = CONCAT17(7,(undefined7)uStack_30);
        FUN_101284b54(local_88,&local_40,10);
        FUN_100241e54(local_58,local_70,local_88);
        if (local_71 < '\0') {
          operator_delete(local_88[0]);
        }
        if (local_59 < '\0') {
          operator_delete(local_70[0]);
        }
        uVar4 = FUN_102971090(param_1,local_58);
        if (-1 < local_41) {
          return uVar4;
        }
        operator_delete(local_58[0]);
        return uVar4;
      }
    }
  }
  return 0;
}

