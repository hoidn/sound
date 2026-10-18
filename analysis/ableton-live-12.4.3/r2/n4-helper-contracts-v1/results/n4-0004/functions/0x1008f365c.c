
void FUN_1008f365c(long param_1,undefined8 *param_2)

{
  int iVar1;
  undefined8 uVar2;
  int *piVar3;
  undefined4 uVar4;
  int *piVar5;
  long lVar6;
  undefined1 auStack_38 [8];
  
  lVar6 = *(long *)(param_1 + 8);
  uVar2 = std::chrono::system_clock::now();
  FUN_103f3ffec(auStack_38,2,uVar2);
  iVar1 = FUN_103f3c8b8(auStack_38);
  if (iVar1 != 0) {
    uVar2 = FUN_103f39a78(auStack_38,"WebConnector: auto-update available: ");
    FUN_101432ff0(uVar2,param_2);
  }
  thunk_FUN_103f395e4(auStack_38);
  piVar5 = (int *)*param_2;
  if (piVar5 != (int *)0x0) {
    *piVar5 = *piVar5 + 1;
  }
  piVar3 = *(int **)(lVar6 + 0x38);
  if ((piVar3 != (int *)0x0) && (iVar1 = *piVar3, *piVar3 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
    piVar5 = (int *)*param_2;
  }
  *(int **)(lVar6 + 0x38) = piVar5;
  uVar4 = 1;
  if (*(char *)(param_1 + 0x10) == '\0') {
    uVar4 = 2;
  }
  FUN_1008e81f0(lVar6,uVar4);
  return;
}

