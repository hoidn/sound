// 0x1008f3940 FUN_1008f3940 exported  sig: undefined FUN_1008f3940()

void FUN_1008f3940(long param_1)

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
    FUN_103f39a78(auStack_28,"WebConnector: auto-update ready");
  }
  thunk_FUN_103f395e4(auStack_28);
  FUN_1008e81f0(uVar3,5);
  return;
}


