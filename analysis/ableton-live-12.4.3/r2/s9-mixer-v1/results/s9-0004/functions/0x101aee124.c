
void FUN_101aee124(long param_1)

{
  int iVar1;
  long lVar2;
  
  lVar2 = FUN_101ab4558(*(undefined8 *)(param_1 + 0x90));
  iVar1 = 0;
  if (*(long *)(param_1 + 0x98) != 0) {
    iVar1 = (int)*(undefined8 *)(lVar2 + 0x98) - (int)*(long *)(param_1 + 0x98);
  }
  *(undefined8 *)(param_1 + 0x98) = *(undefined8 *)(lVar2 + 0x98);
  if (0 < iVar1) {
    FUN_101aff4e8(param_1 + 0x40,iVar1);
    FUN_101aff4e8(param_1 + 0x28,iVar1);
    FUN_101aff4e8(param_1 + 0x10,iVar1);
  }
  FUN_101aff4d4(*(undefined4 *)(param_1 + 0x5c),param_1 + 0x10);
  *(bool *)(param_1 + 0x58) = *(float *)(param_1 + 0x5c) != 0.0;
  FUN_101aede40(param_1);
  return;
}

