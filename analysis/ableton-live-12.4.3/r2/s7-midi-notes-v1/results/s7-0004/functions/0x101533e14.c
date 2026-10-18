
undefined1  [16] FUN_101533e14(char *param_1,ulong param_2)

{
  char *pcVar1;
  ulong uVar2;
  bool bVar3;
  bool bVar4;
  ulong uVar5;
  ulong uVar6;
  long lVar7;
  char *pcVar8;
  undefined1 auVar9 [16];
  undefined1 auVar10 [12];
  ulong local_28;
  
  if (param_2 != 0) {
    uVar6 = 0;
    do {
      if (param_1[uVar6] != ' ') goto LAB_101533e48;
      uVar6 = uVar6 + 1;
    } while (param_2 != uVar6);
    uVar6 = 0xffffffffffffffff;
LAB_101533e48:
    uVar5 = 0;
    lVar7 = -1;
    pcVar8 = param_1;
    do {
      pcVar8 = pcVar8 + -1;
      if (param_2 == uVar5) goto LAB_101533eec;
      lVar7 = lVar7 + 1;
      uVar5 = uVar5 + 1;
    } while (pcVar8[param_2] == ' ');
    if (uVar6 == 0xffffffffffffffff) {
LAB_101533f70:
      return ZEXT816(0);
    }
    uVar5 = param_2 - lVar7;
    if (uVar5 != 0) {
      pcVar8 = param_1 + uVar6;
      if (*pcVar8 == '+') {
        uVar6 = uVar6 + 1;
      }
      if (param_2 < uVar6) {
                    /* WARNING: Subroutine does not return */
        FUN_100277278("string_view::substr");
      }
      uVar2 = param_2 - uVar6;
      if (uVar5 <= param_2 - uVar6) {
        uVar2 = uVar5;
      }
      if (param_2 == uVar6) goto LAB_101533f70;
      if ((uVar2 < 0x40) && ((pcVar1 = param_1 + uVar6, *pcVar8 != '+' || (*pcVar1 != '-')))) {
        while (-1 < *param_1) {
          param_1 = param_1 + 1;
          param_2 = param_2 - 1;
          if (param_2 == 0) {
            pcVar8 = pcVar1 + uVar2;
            local_28 = 0;
            auVar10 = FUN_101524d8c(pcVar1,pcVar8,&local_28);
            bVar3 = auVar10._8_4_ == 0;
            bVar4 = pcVar8 == auVar10._0_8_;
            uVar6 = local_28 & 0xffffffffffffff00;
            local_28 = local_28 & 0xff;
            if (!bVar3 || !bVar4) {
              uVar6 = 0;
              local_28 = 0;
            }
            auVar9._0_8_ = local_28 | uVar6;
            auVar9[8] = bVar3 && bVar4;
            auVar9._9_7_ = 0;
            return auVar9;
          }
        }
      }
    }
  }
LAB_101533eec:
  return ZEXT816(0);
}

