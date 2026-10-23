
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

ulong FUN_00003820(long param_1,long *param_2,uint param_3,char param_4,undefined1 *param_5)

{
  float fVar1;
  float fVar2;
  long lVar3;
  long lVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  double dVar10;
  double dVar11;
  ulong uVar12;
  double dVar13;
  
  *param_5 = 0;
  if (*(long *)(param_1 + 8) == 0) {
    uVar12 = 0;
  }
  else {
    func_0x0000eb70((float)*(int *)(*(long *)(param_1 + 8) + 0x14),param_1 + 0xe0030,param_3);
    if (param_4 == '\0') {
      *(undefined8 *)(param_1 + 0xe0068) = 0x317e0;
      *(undefined8 *)(param_1 + 0xe0070) = 0x317e0;
    }
    else {
      uVar5 = *(undefined4 *)((long)param_2 + 4);
      lVar3 = param_2[1];
      uVar6 = *(undefined4 *)((long)param_2 + 0xc);
      *(int *)(param_1 + 0xe0068) = (int)*param_2;
      *(undefined4 *)(param_1 + 0xe006c) = uVar5;
      *(int *)(param_1 + 0xe0070) = (int)lVar3;
      *(undefined4 *)(param_1 + 0xe0074) = uVar6;
    }
    (**(code **)(**(long **)(param_1 + 8) + 0x20))
              (*(long **)(param_1 + 8),*(undefined8 *)(param_1 + 0xe0028),param_2,param_3,
               param_1 + 0xe0060,2);
    dVar11 = _DAT_0002e208;
    dVar10 = _DAT_0002e200;
    fVar9 = _DAT_0002e1d4;
    fVar8 = _DAT_0002e1d0;
    fVar7 = _DAT_0002e1b4;
    if (0 < (int)param_3) {
      lVar3 = *param_2;
      lVar4 = param_2[1];
      uVar12 = 0;
      do {
        fVar1 = *(float *)(lVar3 + uVar12 * 4);
        dVar13 = (double)fVar1;
        if ((((dVar13 < dVar10) || (fVar2 = *(float *)(lVar4 + uVar12 * 4), fVar8 < fVar2)) ||
            (dVar11 < dVar13)) || (fVar2 < fVar9)) {
          *param_5 = 1;
        }
        *(float *)(lVar3 + uVar12 * 4) = fVar1 * fVar7;
        *(float *)(lVar4 + uVar12 * 4) = *(float *)(lVar4 + uVar12 * 4) * fVar7;
        uVar12 = uVar12 + 1;
      } while (param_3 != uVar12);
    }
    uVar12 = CONCAT71((int7)((ulong)param_5 >> 8),1);
    if (*(char *)(param_1 + 0xe0484) != '\0') {
      (**(code **)(**(long **)(param_1 + 8) + 0xd0))
                (*(long **)(param_1 + 8),*(undefined4 *)(param_1 + 0xe0078),
                 *(undefined4 *)(param_1 + 0xe007c),*(undefined4 *)(param_1 + 0xe0488));
      *(undefined1 *)(param_1 + 0xe0484) = 0;
    }
  }
  return uVar12 & 0xffffffff;
}

