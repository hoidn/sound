// 0x1011aeb80 FUN_1011aeb80 exported  sig: undefined FUN_1011aeb80()

undefined1  [16] FUN_1011aeb80(int *param_1)

{
  long lVar1;
  long lVar2;
  long lVar3;
  ushort uVar4;
  undefined1 auVar5 [16];
  
  if (DAT_106f29802 != '\x01') {
    return ZEXT816(0);
  }
  if ((DAT_106f29820 & 1) == 0) {
    FUN_10540fd1c();
  }
  if (DAT_106f29860 == 0) {
    return ZEXT816(0);
  }
  if ((DAT_106f29820 & 1) == 0) {
    FUN_10540fd64();
    lVar1 = *(long *)(DAT_106f29858 + 0x10);
    lVar3 = *(long *)(DAT_106f29858 + 0x18);
    lVar2 = lVar3;
    if (lVar3 == lVar1) goto LAB_1011aec50;
  }
  else {
    lVar1 = *(long *)(DAT_106f29858 + 0x10);
    lVar3 = *(long *)(DAT_106f29858 + 0x18);
    lVar2 = lVar3;
    if (lVar3 == lVar1) goto LAB_1011aec50;
  }
  do {
    uVar4 = NEON_uminv(CONCAT26(-(ushort)((int)((ulong)*(undefined8 *)(lVar3 + -0x38) >> 0x20) ==
                                         (int)((ulong)*(undefined8 *)(param_1 + 6) >> 0x20)),
                                CONCAT24(-(ushort)((int)*(undefined8 *)(lVar3 + -0x38) ==
                                                  (int)*(undefined8 *)(param_1 + 6)),
                                         CONCAT22(-(ushort)((int)((ulong)*(undefined8 *)
                                                                          (lVar3 + -0x40) >> 0x20)
                                                           == (int)((ulong)*(undefined8 *)
                                                                            (param_1 + 4) >> 0x20)),
                                                  -(ushort)((int)*(undefined8 *)(lVar3 + -0x40) ==
                                                           (int)*(undefined8 *)(param_1 + 4))))),2);
    if ((((uVar4 & 1) != 0) &&
        ((*(int *)(lVar3 + -0x44) == param_1[3] && *(int *)(lVar3 + -0x48) == param_1[2]) &&
         *(int *)(lVar3 + -0x4c) == param_1[1])) &&
       (lVar2 = lVar3, *(int *)(lVar3 + -0x50) == *param_1)) break;
    lVar3 = lVar3 + -0x68;
    lVar2 = lVar1;
  } while (lVar3 != lVar1);
LAB_1011aec50:
  lVar3 = lVar2 + -0x68;
  if (lVar2 == lVar1) {
    lVar3 = 0;
  }
  auVar5[8] = lVar2 != lVar1;
  auVar5._0_8_ = lVar3;
  auVar5._9_7_ = 0;
  return auVar5;
}


