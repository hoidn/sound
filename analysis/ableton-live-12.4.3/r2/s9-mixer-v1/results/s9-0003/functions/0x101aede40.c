
void FUN_101aede40(long param_1)

{
  float *pfVar1;
  char cVar2;
  undefined8 uVar3;
  long lVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  ulong uVar9;
  
  uVar3 = FUN_101aff570(*(undefined4 *)(param_1 + 0x50),*(undefined4 *)(param_1 + 0x38));
  uVar3 = FUN_101aff570(uVar3,*(undefined4 *)(param_1 + 0x20));
  if (*(char *)(param_1 + 0x58) == '\x01') {
    cVar2 = "\x01\x01\x01\x01\x01\x01"[*(int *)(param_1 + 8)];
    fVar5 = (float)FUN_101aff494(param_1 + 0x40,uVar3);
    if (cVar2 == '\x01') {
      fVar6 = (float)FUN_101ac3bac(1);
      lVar4 = *(long *)(param_1 + 0x88);
      fVar5 = (float)FUN_101aff494(param_1 + 0x28,uVar3);
      fVar7 = (float)FUN_101aff494(param_1 + 0x10,uVar3);
      fVar7 = (fVar5 * fVar7 - *(float *)(lVar4 + 0x20)) * *(float *)(lVar4 + 0x24);
      fVar5 = (float)*(int *)(lVar4 + 0x18);
      if (fVar7 <= (float)*(int *)(lVar4 + 0x18)) {
        fVar5 = fVar7;
      }
      fVar8 = 0.0;
      if (0.0 <= fVar7) {
        fVar8 = fVar5;
      }
      pfVar1 = (float *)(*(long *)(lVar4 + 8) + (long)(int)fVar8 * 4);
      fVar5 = *pfVar1;
      fVar6 = fVar6 * (fVar5 + (pfVar1[1] - fVar5) * (fVar8 - (float)(int)fVar8));
      goto LAB_101aedfb4;
    }
    lVar4 = *(long *)(param_1 + 0x88);
    fVar7 = (float)FUN_101aff494(param_1 + 0x28,uVar3);
    fVar6 = (float)FUN_101aff494(param_1 + 0x10,uVar3);
    fVar6 = (fVar7 * fVar6 - *(float *)(lVar4 + 0x20)) * *(float *)(lVar4 + 0x24);
    fVar7 = (float)*(int *)(lVar4 + 0x18);
    if (fVar6 <= (float)*(int *)(lVar4 + 0x18)) {
      fVar7 = fVar6;
    }
    fVar8 = 0.0;
    if (0.0 <= fVar6) {
      fVar8 = fVar7;
    }
    pfVar1 = (float *)(*(long *)(lVar4 + 8) + (long)(int)fVar8 * 4);
    fVar7 = *pfVar1;
    uVar9 = (ulong)(uint)(fVar5 * (fVar7 + (pfVar1[1] - fVar7) * (fVar8 - (float)(int)fVar8)));
  }
  else {
    uVar9 = FUN_101aff494(param_1 + 0x40,uVar3);
  }
  fVar6 = (float)FUN_101ac3bac(uVar9,1);
LAB_101aedfb4:
  if (fVar6 <= 0.00032) {
    fVar6 = 0.0;
  }
  *(float *)(param_1 + 0x80) = fVar6;
  *(int *)(param_1 + 0x84) = (int)uVar3;
  FUN_101b05314(param_1 + 0x60,(float *)(param_1 + 0x80));
  return;
}

