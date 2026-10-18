
void FUN_101b65b68(long param_1,long param_2)

{
  long lVar1;
  int iVar2;
  int iVar3;
  float fVar4;
  undefined4 uVar5;
  float fVar6;
  
  iVar2 = *(int *)(param_2 + 0x14);
  iVar3 = *(int *)(param_2 + 0x18);
  fVar6 = *(float *)(param_2 + 0x1c);
  fVar4 = (float)FUN_1011afe48();
  if (fVar6 == fVar4) {
    uVar5 = FUN_1011afbc0(*(undefined4 *)(param_2 + 0x18));
  }
  else {
    uVar5 = *(undefined4 *)(param_2 + 0x1c);
  }
  if (iVar3 + 2U < 0x83) {
    lVar1 = param_1 + (long)iVar2 * 0x218 + (ulong)(iVar3 + 2) * 4;
    fVar4 = *(float *)(lVar1 + 0x20ba0);
    *(undefined4 *)(lVar1 + 0x20ba0) = uVar5;
    if (*(float *)(param_2 + 0x20) == fVar4) {
      return;
    }
  }
  else {
    fVar4 = -129.0;
    if (*(float *)(param_2 + 0x20) == -129.0) {
      return;
    }
  }
  *(float *)(param_2 + 0x20) = fVar4;
  return;
}

