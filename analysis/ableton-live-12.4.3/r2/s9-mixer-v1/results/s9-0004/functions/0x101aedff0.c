
void FUN_101aedff0(float param_1,long param_2)

{
  long lVar1;
  long lVar2;
  undefined8 uVar3;
  int iVar4;
  double dVar5;
  float local_48;
  int local_44;
  
  lVar1 = FUN_101ab4558(*(undefined8 *)(param_2 + 0x90));
  iVar4 = 0;
  if (*(long *)(param_2 + 0x98) != 0) {
    iVar4 = (int)*(undefined8 *)(lVar1 + 0x98) - (int)*(long *)(param_2 + 0x98);
  }
  *(undefined8 *)(param_2 + 0x98) = *(undefined8 *)(lVar1 + 0x98);
  if (0 < iVar4) {
    FUN_101aff4e8(param_2 + 0x40,iVar4);
    FUN_101aff4e8(param_2 + 0x28,iVar4);
    FUN_101aff4e8(param_2 + 0x10,iVar4);
  }
  FUN_101ab4558(*(undefined8 *)(param_2 + 0x90));
  dVar5 = (double)FUN_101ab05e8(0x3f60624dd2f1a9fc);
  lVar1 = FUN_101ab4558(*(undefined8 *)(param_2 + 0x90));
  iVar4 = (int)(dVar5 * *(double *)(lVar1 + 0x28));
  local_48 = 1.0 - param_1;
  *(float *)(param_2 + 0x5c) = local_48;
  local_44 = iVar4;
  FUN_101aff3f8(param_2 + 0x10,&local_48);
  *(undefined1 *)(param_2 + 0x58) = 1;
  lVar2 = *(long *)(param_2 + 0xa0);
  uVar3 = *(undefined8 *)(param_2 + 0x90);
  lVar1 = *(long *)(lVar2 + 0x38);
  if (lVar1 != 0) {
    *(undefined8 *)(lVar2 + 0x38) = 0;
    if (*(char *)(lVar2 + 0x40) == '\x01') {
      FUN_101ab1bb0();
    }
    else {
      FUN_101ab1980(lVar1,lVar2);
    }
  }
  *(int *)(lVar2 + 0x20) = iVar4;
  *(undefined1 *)(lVar2 + 0x40) = 0;
  FUN_101ab1648(uVar3,lVar2);
  *(undefined8 *)(lVar2 + 0x38) = uVar3;
  FUN_101aede40(param_2);
  return;
}

