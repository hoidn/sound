// 0x10022142c FUN_10022142c state=exported role=nanomsg server open: nn_socket + nn_bind
// source chunk chunk-00094.jsonl; code_sha256=8cbfae13729737c1aa5b27d1aa22a54fd703ae2f63403fd9c123dfcd4c91b512

void FUN_10022142c(long *param_1)

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
  uVar3 = FUN_100a1c558(param_1[1],1,*(undefined4 *)((long)param_1 + 0x14));
  *(int *)(param_1 + 3) = (int)uVar3;
  if ((int)uVar3 != -1) {
    plVar4 = (long *)param_1[4];
    if (-1 < *(char *)((long)param_1 + 0x37)) {
      plVar4 = param_1 + 4;
    }
    iVar1 = FUN_100a1c570(param_1[1],uVar3,plVar4);
    *(int *)((long)param_1 + 0x1c) = iVar1;
    if (iVar1 != -1) {
      return;
    }
  }
  FUN_100221600(param_1);
  return;
}

