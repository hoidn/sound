// x86 0x101188890 FUN_101188890 state=exported chunk=chunk-00674.jsonl code_sha256=dc2371f60f85da3d202a84655c643152f7a36469f10aafa303546529f44c59fd

undefined1  [16] FUN_101188890(int *param_1)

{
  undefined1 (*pauVar1) [16];
  int *piVar2;
  int *piVar3;
  int iVar4;
  long lVar5;
  long lVar6;
  long lVar7;
  uint uVar8;
  undefined1 auVar9 [16];
  undefined1 auVar10 [16];
  
  if (DAT_1073bb210 != '\x01') {
    return ZEXT816(0);
  }
  if (DAT_1073bb260 == '\0') {
    FUN_10595f670();
  }
  if (DAT_1073bb258 == 0) {
    return ZEXT816(0);
  }
  if (DAT_1073bb260 == '\0') {
    FUN_10595f6d0();
  }
  lVar5 = *(long *)(DAT_1073bb250 + 0x10);
  lVar7 = *(long *)(DAT_1073bb250 + 0x18);
  if (lVar7 != lVar5) {
    pauVar1 = (undefined1 (*) [16])(param_1 + 4);
    piVar2 = param_1 + 2;
    iVar4 = *param_1;
    piVar3 = param_1 + 1;
    do {
      if (*(undefined1 (*) [16])(lVar7 + -0x40) == *pauVar1) {
        auVar9._0_4_ = -(uint)((int)*(undefined8 *)(lVar7 + -0x48) == (int)*(undefined8 *)piVar2);
        auVar9._4_4_ = -(uint)((int)((ulong)*(undefined8 *)(lVar7 + -0x48) >> 0x20) ==
                              (int)((ulong)*(undefined8 *)piVar2 >> 0x20));
        auVar9._8_4_ = 0xffffffff;
        auVar9._12_4_ = 0xffffffff;
        auVar9 = pmovsxdq(auVar9,auVar9);
        uVar8 = movmskpd((int)param_1,auVar9);
        param_1 = (int *)(ulong)uVar8;
        if (((((byte)((byte)uVar8 >> 1) != 0) && ((uVar8 & 1) != 0)) &&
            (*(int *)(lVar7 + -0x4c) == *piVar3)) && (*(int *)(lVar7 + -0x50) == iVar4)) break;
      }
      lVar7 = lVar7 + -0x68;
    } while (lVar7 != lVar5);
  }
  auVar10._9_7_ = (undefined7)((ulong)lVar7 >> 8);
  auVar10[8] = lVar7 != lVar5;
  lVar6 = 0;
  if (lVar7 != lVar5) {
    lVar6 = lVar7 + -0x68;
  }
  auVar10._0_8_ = lVar6;
  return auVar10;
}

