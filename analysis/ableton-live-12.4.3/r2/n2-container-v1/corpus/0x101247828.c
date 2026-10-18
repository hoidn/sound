
void FUN_101247828(long param_1)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  int *local_40;
  int *local_38;
  
  uVar2 = FUN_1049f8b64(*(undefined8 *)(param_1 + 0x18));
  lVar3 = FUN_1049f8f44();
  FUN_1011cb734(&local_40);
  if (lVar3 != 0) {
    FUN_101427680(&local_38,lVar3);
    FUN_10142da5c(&local_40,&local_38);
    if (local_38 != (int *)0x0) {
      iVar1 = *local_38;
      *local_38 = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_101449efc();
      }
    }
  }
  FUN_101247760(param_1,uVar2,&local_40);
  if (local_40 != (int *)0x0) {
    iVar1 = *local_40;
    *local_40 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  return;
}

