// 0x10014ddfc FUN_10014ddfc state=exported body_bytes=756 warnings=0 chunk=chunk-00055.jsonl

void FUN_10014ddfc(long param_1)

{
  int iVar1;
  undefined8 uVar2;
  undefined1 auStack_40 [8];
  undefined4 local_38;
  undefined4 uStack_34;
  char local_21;
  
  local_21 = '\a';
  local_38 = 0x6e616353;
  uStack_34 = 0x72656e;
  uVar2 = std::chrono::system_clock::now();
  FUN_10073cd34(auStack_40,1,&local_38,uVar2);
  if (local_21 < '\0') {
    operator_delete((void *)CONCAT44(uStack_34,local_38));
  }
  iVar1 = FUN_1007396c0(auStack_40);
  if (iVar1 != 0) {
    uVar2 = FUN_100736880(auStack_40,"  IPC Channel:     ");
    FUN_1004525f4(uVar2,param_1 + 0x30);
  }
  thunk_FUN_1007363ec(auStack_40);
  local_21 = '\a';
  local_38 = 0x6e616353;
  uStack_34 = 0x72656e;
  uVar2 = std::chrono::system_clock::now();
  FUN_10073cd34(auStack_40,1,&local_38,uVar2);
  if (local_21 < '\0') {
    operator_delete((void *)CONCAT44(uStack_34,local_38));
  }
  iVar1 = FUN_1007396c0(auStack_40);
  if (iVar1 != 0) {
    uVar2 = FUN_100736880(auStack_40,"  DB:              ");
    FUN_10013a004(uVar2,param_1);
  }
  thunk_FUN_1007363ec(auStack_40);
  local_21 = '\a';
  local_38 = 0x6e616353;
  uStack_34 = 0x72656e;
  uVar2 = std::chrono::system_clock::now();
  FUN_10073cd34(auStack_40,1,&local_38,uVar2);
  if (local_21 < '\0') {
    operator_delete((void *)CONCAT44(uStack_34,local_38));
  }
  iVar1 = FUN_1007396c0(auStack_40);
  if (iVar1 != 0) {
    uVar2 = FUN_100736880(auStack_40,"  Parent pid:      ");
    FUN_1004525f4(uVar2,param_1 + 0x50);
  }
  thunk_FUN_1007363ec(auStack_40);
  local_21 = '\a';
  local_38 = 0x6e616353;
  uStack_34 = 0x72656e;
  uVar2 = std::chrono::system_clock::now();
  FUN_10073cd34(auStack_40,1,&local_38,uVar2);
  if (local_21 < '\0') {
    operator_delete((void *)CONCAT44(uStack_34,local_38));
  }
  iVar1 = FUN_1007396c0(auStack_40);
  if (iVar1 != 0) {
    uVar2 = FUN_100736880(auStack_40,"  Usage data file: ");
    FUN_10013a004(uVar2,param_1 + 0x38);
  }
  thunk_FUN_1007363ec(auStack_40);
  local_21 = '\a';
  local_38 = 0x6e616353;
  uStack_34 = 0x72656e;
  uVar2 = std::chrono::system_clock::now();
  FUN_10073cd34(auStack_40,1,&local_38,uVar2);
  if (local_21 < '\0') {
    operator_delete((void *)CONCAT44(uStack_34,local_38));
  }
  iVar1 = FUN_1007396c0(auStack_40);
  if (iVar1 != 0) {
    uVar2 = FUN_100736880(auStack_40,"  Os Event Flags:  ");
    FUN_1004525f4(uVar2,param_1 + 0x68);
  }
  thunk_FUN_1007363ec(auStack_40);
  local_21 = '\a';
  local_38 = 0x6e616353;
  uStack_34 = 0x72656e;
  uVar2 = std::chrono::system_clock::now();
  FUN_10073cd34(auStack_40,1,&local_38,uVar2);
  if (local_21 < '\0') {
    operator_delete((void *)CONCAT44(uStack_34,local_38));
  }
  iVar1 = FUN_1007396c0(auStack_40);
  if (iVar1 != 0) {
    uVar2 = FUN_100736880(auStack_40,"  Filerefmap:      ");
    FUN_10013a004(uVar2,param_1 + 0x18);
  }
  thunk_FUN_1007363ec(auStack_40);
  return;
}

