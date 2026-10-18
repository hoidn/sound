// 0x100140bac FUN_100140bac state=exported body_bytes=712 warnings=0 chunk=chunk-00052.jsonl

void FUN_100140bac(long param_1,undefined1 *param_2,long param_3,long param_4,long param_5)

{
  int iVar1;
  long *plVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  undefined1 auStack_68 [8];
  undefined1 *local_60;
  long lStack_58;
  undefined8 local_50;
  long local_48;
  
  if (param_2 != (undefined1 *)0x0) {
    *(int *)(param_2 + 8) = *(int *)(param_2 + 8) + 1;
  }
  if (param_3 != 0) {
    *(int *)(param_3 + 8) = *(int *)(param_3 + 8) + 1;
  }
  if (param_4 != 0) {
    *(int *)(param_4 + 8) = *(int *)(param_4 + 8) + 1;
  }
  if (param_5 != 0) {
    *(int *)(param_5 + 8) = *(int *)(param_5 + 8) + 1;
  }
  local_60 = param_2;
  lStack_58 = param_3;
  local_50 = param_4;
  local_48 = param_5;
  plVar2 = operator_new(0x30);
  plVar2[2] = (long)param_2;
  plVar2[3] = param_3;
  plVar2[4] = param_4;
  plVar2[5] = param_5;
  lStack_58 = 0;
  local_60 = (undefined1 *)0x0;
  local_48 = 0;
  local_50._0_7_ = 0;
  local_50._7_1_ = 0;
  puVar4 = *(undefined8 **)(param_1 + 0x100);
  *plVar2 = param_1 + 0xf8;
  plVar2[1] = (long)puVar4;
  *puVar4 = plVar2;
  *(long **)(param_1 + 0x100) = plVar2;
  *(long *)(param_1 + 0x108) = *(long *)(param_1 + 0x108) + 1;
  FUN_10015720c(&local_60);
  if (param_2 != (undefined1 *)0x0) {
    local_50._7_1_ = '\a';
    local_60 = &DAT_72656e6e616353;
    uVar3 = std::chrono::system_clock::now();
    FUN_10073cd34(auStack_68,1,&local_60,uVar3);
    if (local_50._7_1_ < '\0') {
      operator_delete(local_60);
    }
    iVar1 = FUN_1007396c0(auStack_68);
    if (iVar1 != 0) {
      uVar3 = FUN_100736880(auStack_68,"Push change detection task (Id: ");
      uVar3 = FUN_1007385b8(uVar3,*(undefined4 *)(param_2 + 0xd0));
      FUN_100736880(uVar3,")");
    }
    thunk_FUN_1007363ec(auStack_68);
  }
  if (param_3 != 0) {
    local_50._7_1_ = '\a';
    local_60 = &DAT_72656e6e616353;
    uVar3 = std::chrono::system_clock::now();
    FUN_10073cd34(auStack_68,1,&local_60,uVar3);
    if (local_50._7_1_ < '\0') {
      operator_delete(local_60);
    }
    iVar1 = FUN_1007396c0(auStack_68);
    if (iVar1 != 0) {
      uVar3 = FUN_100736880(auStack_68,"Push extraction task (Id: ");
      uVar3 = FUN_1007385b8(uVar3,*(undefined4 *)(param_3 + 0x18));
      FUN_100736880(uVar3,")");
    }
    thunk_FUN_1007363ec(auStack_68);
  }
  if (param_4 != 0) {
    local_50._7_1_ = '\a';
    local_60 = &DAT_72656e6e616353;
    uVar3 = std::chrono::system_clock::now();
    FUN_10073cd34(auStack_68,1,&local_60,uVar3);
    if (local_50._7_1_ < '\0') {
      operator_delete(local_60);
    }
    iVar1 = FUN_1007396c0(auStack_68);
    if (iVar1 != 0) {
      FUN_100736880(auStack_68,"Push xmp import task");
    }
    thunk_FUN_1007363ec(auStack_68);
  }
  if (param_5 != 0) {
    local_50._7_1_ = '\a';
    local_60 = &DAT_72656e6e616353;
    uVar3 = std::chrono::system_clock::now();
    FUN_10073cd34(auStack_68,1,&local_60,uVar3);
    if (local_50._7_1_ < '\0') {
      operator_delete(local_60);
    }
    iVar1 = FUN_1007396c0(auStack_68);
    if (iVar1 != 0) {
      FUN_100736880(auStack_68,"Push remove task");
    }
    thunk_FUN_1007363ec(auStack_68);
  }
  return;
}

