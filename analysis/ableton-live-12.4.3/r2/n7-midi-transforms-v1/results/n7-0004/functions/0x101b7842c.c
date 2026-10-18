
byte FUN_101b7842c(long param_1,int *param_2)

{
  int iVar1;
  uint uVar2;
  byte bVar3;
  long lVar4;
  code *pcVar5;
  byte bVar6;
  undefined8 uVar7;
  ulong uVar8;
  float fVar9;
  float fVar10;
  
  iVar1 = *param_2;
  if (iVar1 == 3) {
    uVar2 = param_2[6];
    if (uVar2 == 0xfffffffe) {
      lVar4 = *(long *)(param_1 + (long)param_2[5] * 8 + 8);
      if ((lVar4 != 0) && (lVar4 = *(long *)(lVar4 + 0x1828), lVar4 != 0)) {
        do {
          while (fVar10 = (float)param_2[7], fVar9 = (float)FUN_1011afe48(), fVar10 == fVar9) {
            uVar7 = FUN_1011afbc0(param_2[6]);
            (**(code **)(lVar4 + 0x20))(uVar7,param_2[8],*(undefined8 *)(lVar4 + 0x18));
            lVar4 = *(long *)(lVar4 + 8);
            if (lVar4 == 0) goto LAB_101b78588;
          }
          (**(code **)(lVar4 + 0x20))(param_2[7],param_2[8],*(undefined8 *)(lVar4 + 0x18));
          lVar4 = *(long *)(lVar4 + 8);
        } while (lVar4 != 0);
LAB_101b78588:
        bVar6 = 1;
        goto LAB_101b785c4;
      }
    }
    else if (((uVar2 < 0x80) && (lVar4 = *(long *)(param_1 + (long)param_2[5] * 8 + 8), lVar4 != 0))
            && (lVar4 = *(long *)(lVar4 + (ulong)uVar2 * 0x18 + 0xc10), lVar4 != 0)) {
      bVar6 = 1;
      do {
        fVar10 = (float)param_2[7];
        fVar9 = (float)FUN_1011afe48();
        if (fVar10 == fVar9) {
          uVar8 = FUN_1011afbc0(param_2[6]);
          pcVar5 = *(code **)(lVar4 + 0x20);
          if (pcVar5 == (code *)0x0) goto LAB_101b78668;
LAB_101b7862c:
          (*pcVar5)(uVar8,*(undefined8 *)(lVar4 + 0x18),*(undefined4 *)(lVar4 + 0x30));
        }
        else {
          uVar8 = (ulong)(uint)param_2[7];
          pcVar5 = *(code **)(lVar4 + 0x20);
          if (pcVar5 != (code *)0x0) goto LAB_101b7862c;
LAB_101b78668:
          if (*(code **)(lVar4 + 0x28) != (code *)0x0) {
            (**(code **)(lVar4 + 0x28))
                      (uVar8,param_2[8],*(undefined8 *)(lVar4 + 0x18),*(undefined4 *)(lVar4 + 0x30))
            ;
          }
        }
        bVar6 = bVar6 & *(byte *)(lVar4 + 0x34);
        lVar4 = *(long *)(lVar4 + 8);
      } while (lVar4 != 0);
      goto LAB_101b785c4;
    }
  }
  else if (iVar1 == 2) {
    lVar4 = *(long *)(param_1 + (long)param_2[5] * 8 + 8);
    if ((lVar4 != 0) && (lVar4 = *(long *)(lVar4 + (long)param_2[8] * 0x18 + 0x10), lVar4 != 0)) {
      bVar6 = 1;
      do {
        (**(code **)(lVar4 + 0x20))(0,*(undefined8 *)(lVar4 + 0x18),1);
        bVar6 = bVar6 & *(byte *)(lVar4 + 0x29);
        lVar4 = *(long *)(lVar4 + 8);
      } while (lVar4 != 0);
      goto LAB_101b785c4;
    }
  }
  else if (((iVar1 == 1) && (lVar4 = *(long *)(param_1 + (long)param_2[5] * 8 + 8), lVar4 != 0)) &&
          (lVar4 = *(long *)(lVar4 + (long)param_2[8] * 0x18 + 0x10), lVar4 != 0)) {
    fVar9 = (float)param_2[9];
    bVar6 = 1;
    do {
      fVar10 = fVar9 / 127.0;
      if (*(char *)(lVar4 + 0x28) == '\0') {
        fVar10 = fVar9;
      }
      (**(code **)(lVar4 + 0x20))(fVar10,*(undefined8 *)(lVar4 + 0x18),fVar9 == 0.0);
      bVar6 = bVar6 & *(byte *)(lVar4 + 0x29);
      lVar4 = *(long *)(lVar4 + 8);
    } while (lVar4 != 0);
    goto LAB_101b785c4;
  }
  bVar6 = 0;
LAB_101b785c4:
  if (0 < *(int *)(param_1 + 0xe8)) {
    lVar4 = 0;
    do {
      bVar3 = FUN_101b78930(*(undefined8 *)(*(long *)(param_1 + 0xe0) + lVar4 * 8),param_2);
      bVar6 = bVar6 | bVar3;
      lVar4 = lVar4 + 1;
    } while (lVar4 < *(int *)(param_1 + 0xe8));
  }
  if ((bVar6 & 1) != 0) {
    FUN_101a45218();
    FUN_101a4f6a4();
  }
  return bVar6 & 1;
}

