
void FUN_102778870(long param_1)

{
  int iVar1;
  uint uVar2;
  undefined1 auVar3 [16];
  undefined8 uVar4;
  undefined8 uVar5;
  
  uVar4 = *(undefined8 *)(param_1 + 0x68);
  uVar5 = *(undefined8 *)(param_1 + 0x78);
  iVar1 = FUN_1012132d8(ZEXT816(0),*(undefined8 *)(param_1 + 0x60),*(undefined8 *)(param_1 + 0x70),
                        0x3ff0000000000000);
  if ((iVar1 == 0) ||
     (uVar2 = FUN_1012132d8(ZEXT816(0),uVar4,uVar5,0x3ff0000000000000), (uVar2 & 1) == 0)) {
    auVar3 = NEON_fmov(0x3fe0000000000000,8);
    *(long *)(param_1 + 0x68) = auVar3._8_8_;
    *(long *)(param_1 + 0x60) = auVar3._0_8_;
    *(long *)(param_1 + 0x78) = auVar3._8_8_;
    *(long *)(param_1 + 0x70) = auVar3._0_8_;
  }
  return;
}

