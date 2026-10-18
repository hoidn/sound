// 0x100150ab8 FUN_100150ab8 state=exported body_bytes=160 warnings=0 chunk=chunk-00056.jsonl

void FUN_100150ab8(long param_1)

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
  FUN_10073cd34(auStack_40,2,&local_38,uVar2);
  if (local_21 < '\0') {
    operator_delete((void *)CONCAT44(uStack_34,local_38));
  }
  iVar1 = FUN_1007396c0(auStack_40);
  if (iVar1 != 0) {
    FUN_100736880(auStack_40,"Shutdown request from Live");
  }
  thunk_FUN_1007363ec(auStack_40);
  **(undefined1 **)(param_1 + 8) = 1;
  return;
}

