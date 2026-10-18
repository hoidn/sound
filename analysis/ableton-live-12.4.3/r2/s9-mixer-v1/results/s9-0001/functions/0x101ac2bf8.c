
void FUN_101ac2bf8(long param_1)

{
  bool bVar1;
  float *pfVar2;
  ulong uVar3;
  float *pfVar4;
  float fVar5;
  float fVar6;
  float fVar7;
  float fVar8;
  int iVar9;
  float fVar10;
  
  if (*(long *)(param_1 + 0x20) != 0) {
    if (*(char *)(param_1 + 0x2c) == '\x01') {
      thunk_FUN_101aa0360(*(long *)(param_1 + 0x20),(long)*(int *)(param_1 + 0x28) << 2);
    }
    *(undefined8 *)(param_1 + 0x20) = 0;
    *(undefined4 *)(param_1 + 0x28) = 0;
  }
  pfVar2 = (float *)thunk_FUN_101aa0314(0x194);
  *(float **)(param_1 + 0x20) = pfVar2;
  *(undefined4 *)(param_1 + 0x28) = 0x65;
  *(undefined1 *)(param_1 + 0x2c) = 1;
  iVar9 = *(int *)(param_1 + 8);
  if (iVar9 < 3) {
    fVar7 = 0.4;
    fVar5 = 0.0;
    if (iVar9 != 2) {
      fVar5 = 3.4028235e+38;
      fVar7 = 3.4028235e+38;
    }
    fVar8 = 0.4;
    fVar10 = 0.04;
    if (iVar9 != 1) {
      fVar8 = fVar7;
      fVar10 = fVar5;
    }
    bVar1 = iVar9 == 0;
  }
  else {
    if (iVar9 - 4U < 2) {
      fVar7 = (float)(*(int *)(param_1 + 0x44) - *(int *)(param_1 + 0x40)) / 101.0;
      fVar5 = 0.0;
      goto LAB_101ac2d14;
    }
    fVar8 = 0.6;
    fVar10 = 0.015;
    if (iVar9 != 6) {
      fVar10 = 3.4028235e+38;
      fVar8 = 3.4028235e+38;
    }
    bVar1 = iVar9 == 3;
  }
  fVar7 = 0.4;
  fVar5 = 0.04;
  if (!bVar1) {
    fVar7 = fVar8;
    fVar5 = fVar10;
  }
LAB_101ac2d14:
  fVar8 = (float)*(int *)(param_1 + 0x44);
  uVar3 = 0x65;
  pfVar4 = pfVar2;
  do {
    fVar10 = 0.0;
    if (0.0001 <= ABS(fVar8)) {
      fVar10 = fVar8;
    }
    *pfVar4 = fVar10;
    fVar8 = fVar10 - fVar7;
    uVar3 = uVar3 - 1;
    pfVar4 = pfVar4 + 1;
  } while (0x29 < uVar3);
  fVar10 = 0.0;
  if (0.0001 <= ABS(fVar8)) {
    fVar10 = fVar8;
  }
  pfVar2[0x3c] = fVar10;
  fVar7 = fVar5 + fVar7;
  fVar8 = 0.0;
  if (0.0001 <= ABS(fVar10 - fVar7)) {
    fVar8 = fVar10 - fVar7;
  }
  pfVar2[0x3d] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar10 = 0.0;
  fVar6 = fVar10;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar6 = fVar8 - fVar7;
  }
  pfVar2[0x3e] = fVar6;
  fVar7 = fVar5 + fVar7;
  fVar8 = fVar10;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar8 = fVar6 - fVar7;
  }
  pfVar2[0x3f] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar6 = fVar10;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar6 = fVar8 - fVar7;
  }
  pfVar2[0x40] = fVar6;
  fVar7 = fVar5 + fVar7;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar10 = fVar6 - fVar7;
  }
  pfVar2[0x41] = fVar10;
  fVar7 = fVar5 + fVar7;
  fVar8 = 0.0;
  fVar6 = fVar8;
  if (0.0001 <= ABS(fVar10 - fVar7)) {
    fVar6 = fVar10 - fVar7;
  }
  pfVar2[0x42] = fVar6;
  fVar7 = fVar5 + fVar7;
  fVar10 = fVar8;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar10 = fVar6 - fVar7;
  }
  pfVar2[0x43] = fVar10;
  fVar7 = fVar5 + fVar7;
  fVar6 = fVar8;
  if (0.0001 <= ABS(fVar10 - fVar7)) {
    fVar6 = fVar10 - fVar7;
  }
  pfVar2[0x44] = fVar6;
  fVar7 = fVar5 + fVar7;
  fVar10 = fVar8;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar10 = fVar6 - fVar7;
  }
  pfVar2[0x45] = fVar10;
  fVar7 = fVar5 + fVar7;
  fVar6 = fVar8;
  if (0.0001 <= ABS(fVar10 - fVar7)) {
    fVar6 = fVar10 - fVar7;
  }
  pfVar2[0x46] = fVar6;
  fVar7 = fVar5 + fVar7;
  fVar10 = fVar8;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar10 = fVar6 - fVar7;
  }
  pfVar2[0x47] = fVar10;
  fVar7 = fVar5 + fVar7;
  fVar6 = fVar8;
  if (0.0001 <= ABS(fVar10 - fVar7)) {
    fVar6 = fVar10 - fVar7;
  }
  pfVar2[0x48] = fVar6;
  fVar7 = fVar5 + fVar7;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar8 = fVar6 - fVar7;
  }
  pfVar2[0x49] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar10 = 0.0;
  fVar6 = fVar10;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar6 = fVar8 - fVar7;
  }
  pfVar2[0x4a] = fVar6;
  fVar7 = fVar5 + fVar7;
  fVar8 = fVar10;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar8 = fVar6 - fVar7;
  }
  pfVar2[0x4b] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar6 = fVar10;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar6 = fVar8 - fVar7;
  }
  pfVar2[0x4c] = fVar6;
  fVar7 = fVar5 + fVar7;
  fVar8 = fVar10;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar8 = fVar6 - fVar7;
  }
  pfVar2[0x4d] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar6 = fVar10;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar6 = fVar8 - fVar7;
  }
  pfVar2[0x4e] = fVar6;
  fVar7 = fVar5 + fVar7;
  fVar8 = fVar10;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar8 = fVar6 - fVar7;
  }
  pfVar2[0x4f] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar6 = fVar10;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar6 = fVar8 - fVar7;
  }
  pfVar2[0x50] = fVar6;
  fVar7 = fVar5 + fVar7;
  fVar8 = fVar10;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar8 = fVar6 - fVar7;
  }
  pfVar2[0x51] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar6 = fVar10;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar6 = fVar8 - fVar7;
  }
  pfVar2[0x52] = fVar6;
  fVar7 = fVar5 + fVar7;
  fVar8 = fVar10;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar8 = fVar6 - fVar7;
  }
  pfVar2[0x53] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar6 = fVar10;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar6 = fVar8 - fVar7;
  }
  pfVar2[0x54] = fVar6;
  fVar7 = fVar5 + fVar7;
  fVar8 = fVar10;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar8 = fVar6 - fVar7;
  }
  pfVar2[0x55] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar6 = fVar10;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar6 = fVar8 - fVar7;
  }
  pfVar2[0x56] = fVar6;
  fVar7 = fVar5 + fVar7;
  fVar8 = fVar10;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar8 = fVar6 - fVar7;
  }
  pfVar2[0x57] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar6 = fVar10;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar6 = fVar8 - fVar7;
  }
  pfVar2[0x58] = fVar6;
  fVar7 = fVar5 + fVar7;
  if (0.0001 <= ABS(fVar6 - fVar7)) {
    fVar10 = fVar6 - fVar7;
  }
  pfVar2[0x59] = fVar10;
  fVar7 = fVar5 + fVar7;
  fVar6 = 0.0;
  fVar8 = fVar6;
  if (0.0001 <= ABS(fVar10 - fVar7)) {
    fVar8 = fVar10 - fVar7;
  }
  pfVar2[0x5a] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar10 = fVar6;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar10 = fVar8 - fVar7;
  }
  pfVar2[0x5b] = fVar10;
  fVar7 = fVar5 + fVar7;
  fVar8 = fVar6;
  if (0.0001 <= ABS(fVar10 - fVar7)) {
    fVar8 = fVar10 - fVar7;
  }
  pfVar2[0x5c] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar10 = fVar6;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar10 = fVar8 - fVar7;
  }
  pfVar2[0x5d] = fVar10;
  fVar7 = fVar5 + fVar7;
  fVar8 = fVar6;
  if (0.0001 <= ABS(fVar10 - fVar7)) {
    fVar8 = fVar10 - fVar7;
  }
  pfVar2[0x5e] = fVar8;
  fVar7 = fVar5 + fVar7;
  fVar10 = fVar6;
  if (0.0001 <= ABS(fVar8 - fVar7)) {
    fVar10 = fVar8 - fVar7;
  }
  pfVar2[0x5f] = fVar10;
  fVar7 = fVar5 + fVar7;
  fVar8 = fVar6;
  if (0.0001 <= ABS(fVar10 - fVar7)) {
    fVar8 = fVar10 - fVar7;
  }
  pfVar2[0x60] = fVar8;
  fVar5 = fVar5 + fVar7;
  iVar9 = *(int *)(param_1 + 0x40);
  fVar10 = (((float)iVar9 - (fVar8 - fVar5)) + fVar5 * 3.0) / 6.0;
  fVar7 = fVar6;
  if (0.0001 <= ABS(fVar8 - fVar5)) {
    fVar7 = fVar8 - fVar5;
  }
  pfVar2[0x61] = fVar7;
  fVar5 = fVar5 - fVar10;
  fVar8 = fVar6;
  if (0.0001 <= ABS(fVar7 - fVar5)) {
    fVar8 = fVar7 - fVar5;
  }
  pfVar2[0x62] = fVar8;
  fVar8 = fVar8 + (fVar10 - fVar5);
  if (0.0001 <= ABS(fVar8)) {
    fVar6 = fVar8;
  }
  pfVar2[99] = fVar6;
  pfVar2[100] = (float)iVar9;
  return;
}

