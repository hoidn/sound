// 0x1013f1be0 FUN_1013f1be0 state=exported role=real-time channel client id
// source chunk chunk-00893.jsonl; code_sha256=6f05f0fc3b2332a7b8665666dd3bc407cafbb781ab391f3c09c4d0aa57a0c64d

void FUN_1013f1be0(long param_1,long param_2)

{
  ulong uVar1;
  int iVar2;
  undefined8 uVar3;
  undefined1 auStack_28 [8];
  
  if (*(long *)(param_1 + 200) != 0) {
    FUN_1013f1a98(param_1);
  }
  uVar3 = std::chrono::system_clock::now();
  FUN_1003324b0(auStack_28,1,uVar3);
  iVar2 = FUN_10032ece8(auStack_28);
  if (iVar2 != 0) {
    uVar3 = FUN_10032bea8(auStack_28,"client id: ");
    FUN_10032cd88(uVar3,param_2);
  }
  thunk_FUN_10032ba14(auStack_28);
  (**(code **)(**(long **)(param_1 + 0x40) + 0x18))(*(long **)(param_1 + 0x40),1);
  uVar1 = *(ulong *)(param_2 + 8);
  if (-1 < (char)*(byte *)(param_2 + 0x17)) {
    uVar1 = (ulong)*(byte *)(param_2 + 0x17);
  }
  if (uVar1 != 0) {
    FUN_1013f1ca4(param_1,param_2);
  }
  return;
}

