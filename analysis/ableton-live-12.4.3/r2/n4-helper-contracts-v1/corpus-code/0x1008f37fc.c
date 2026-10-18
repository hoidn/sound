// 0x1008f37fc FUN_1008f37fc exported  sig: undefined FUN_1008f37fc()

void FUN_1008f37fc(long param_1)

{
  int iVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined1 auStack_28 [8];
  
  uVar3 = *(undefined8 *)(param_1 + 8);
  uVar2 = std::chrono::system_clock::now();
  FUN_103f3ffec(auStack_28,2,uVar2);
  iVar1 = FUN_103f3c8b8(auStack_28);
  if (iVar1 != 0) {
    FUN_103f39a78(auStack_28,"WebConnector: auto-update needs to run vcredist.exe");
  }
  thunk_FUN_103f395e4(auStack_28);
  FUN_1008e81f0(uVar3,3);
  return;
}


