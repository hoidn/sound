
void FUN_1014338b0(long param_1,int param_2,int param_3)

{
  int iVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  long lVar4;
  
  puVar2 = (undefined8 *)FUN_1012d9850(0xa8);
  iVar1 = 6;
  if (param_3 != -1) {
    iVar1 = param_3;
  }
  FUN_10128ed98();
  *puVar2 = &PTR_FUN_10666fa38;
  puVar2[0x14] = param_1;
  uVar3 = FUN_1012d9624((long)param_2,1);
  puVar2[3] = uVar3;
  *(int *)(puVar2 + 4) = param_2;
  *(undefined4 *)((long)puVar2 + 0x24) = 0;
  *(bool *)(puVar2 + 5) = iVar1 != 0;
  if (iVar1 != 0) {
    puVar2[0xe] = 0;
    puVar2[0xf] = 0;
    puVar2[0x10] = 0;
    iVar1 = FUN_1011995c0(puVar2 + 6,iVar1,8,0x1f,9,0,"1.3.1",0x70);
    if (iVar1 == -4) {
                    /* WARNING: Subroutine does not return */
      FUN_1011b50a8();
    }
  }
  *(int *)(puVar2 + 1) = *(int *)(puVar2 + 1) + 1;
  lVar4 = *(long *)(param_1 + 0x20);
  if (lVar4 != 0) {
    iVar1 = *(int *)(lVar4 + 8) + -1;
    *(int *)(lVar4 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
      *(undefined8 **)(param_1 + 0x20) = puVar2;
      return;
    }
  }
  *(undefined8 **)(param_1 + 0x20) = puVar2;
  return;
}

