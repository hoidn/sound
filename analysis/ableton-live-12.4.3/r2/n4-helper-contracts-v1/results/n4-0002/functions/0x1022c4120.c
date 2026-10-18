
void FUN_1022c4120(long *param_1)

{
  int iVar1;
  ulong uVar2;
  undefined8 uVar3;
  long *plVar4;
  
  uVar2 = (**(code **)(*param_1 + 0x10))();
  if ((uVar2 & 1) != 0) {
    return;
  }
  *(undefined4 *)(param_1 + 7) = 0;
  if (*(char *)((long)param_1 + 0x57) < '\0') {
    param_1[9] = 0;
    plVar4 = (long *)param_1[8];
  }
  else {
    plVar4 = param_1 + 8;
    *(undefined1 *)((long)param_1 + 0x57) = 0;
  }
  *(undefined1 *)plVar4 = 0;
  uVar3 = FUN_1009032c0(param_1[1],1,*(undefined4 *)((long)param_1 + 0x14));
  *(int *)(param_1 + 3) = (int)uVar3;
  if ((int)uVar3 != -1) {
    plVar4 = (long *)param_1[4];
    if (-1 < *(char *)((long)param_1 + 0x37)) {
      plVar4 = param_1 + 4;
    }
    iVar1 = FUN_1009032cc(param_1[1],uVar3,plVar4);
    *(int *)((long)param_1 + 0x1c) = iVar1;
    if (iVar1 != -1) {
      return;
    }
  }
  FUN_1022c42f4(param_1);
  return;
}

