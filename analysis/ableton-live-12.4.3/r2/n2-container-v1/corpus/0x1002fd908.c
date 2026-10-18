
ulong FUN_1002fd908(char *param_1,ulong param_2)

{
  char *pcVar1;
  uint uVar2;
  ulong uVar3;
  bool bVar4;
  bool bVar5;
  ulong uVar6;
  ulong uVar7;
  char *pcVar8;
  long lVar9;
  undefined1 auVar10 [12];
  uint local_24;
  
  if (param_2 != 0) {
    uVar6 = 0;
    do {
      if (param_1[uVar6] != ' ') goto LAB_1002fd93c;
      uVar6 = uVar6 + 1;
    } while (param_2 != uVar6);
    uVar6 = 0xffffffffffffffff;
LAB_1002fd93c:
    uVar7 = 0;
    lVar9 = -1;
    pcVar8 = param_1;
    do {
      pcVar8 = pcVar8 + -1;
      if (param_2 == uVar7) {
        return 0;
      }
      lVar9 = lVar9 + 1;
      uVar7 = uVar7 + 1;
    } while (pcVar8[param_2] == ' ');
    if ((uVar6 != 0xffffffffffffffff) && (uVar7 = param_2 - lVar9, uVar7 != 0)) {
      pcVar8 = param_1 + uVar6;
      if (*pcVar8 == '+') {
        uVar6 = uVar6 + 1;
      }
      if (param_2 < uVar6) {
                    /* WARNING: Subroutine does not return */
        FUN_100277278("string_view::substr");
      }
      uVar3 = param_2 - uVar6;
      if (uVar7 <= param_2 - uVar6) {
        uVar3 = uVar7;
      }
      if (((param_2 != uVar6) && (uVar3 < 0x40)) &&
         ((pcVar1 = param_1 + uVar6, *pcVar8 != '+' || (*pcVar1 != '-')))) {
        while (-1 < *param_1) {
          param_1 = param_1 + 1;
          param_2 = param_2 - 1;
          if (param_2 == 0) {
            pcVar8 = pcVar1 + uVar3;
            local_24 = 0;
            auVar10 = FUN_1002fda78(pcVar1,pcVar8,&local_24);
            bVar4 = auVar10._8_4_ != 0;
            bVar5 = pcVar8 != auVar10._0_8_;
            uVar2 = local_24 & 0xffffff00;
            local_24 = local_24 & 0xff;
            if (bVar4 || bVar5) {
              uVar2 = 0;
              local_24 = 0;
            }
            uVar6 = 0x100000000;
            if (bVar4 || bVar5) {
              uVar6 = 0;
            }
            return uVar6 | (uVar2 | local_24);
          }
        }
      }
    }
  }
  return 0;
}

