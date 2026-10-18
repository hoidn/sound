
void FUN_101535e0c(long param_1)

{
  int iVar1;
  long *plVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  ulong uVar5;
  int *local_40;
  undefined1 auStack_38 [8];
  
  if (*(long *)(param_1 + 0x40) != 0) {
    return;
  }
  plVar2 = (long *)FUN_101482d44(param_1);
  if (plVar2 != (long *)0x0) {
    uVar3 = (**(code **)(*plVar2 + 0x170))();
    uVar4 = FUN_10153f74c();
    uVar5 = FUN_10147fd68(uVar3,uVar4);
    if ((uVar5 & 1) != 0) {
      uVar3 = FUN_1015439b4(plVar2,*(undefined4 *)(param_1 + 0x24));
      FUN_10145917c(param_1 + 0x28,uVar3);
      if (*(long *)(param_1 + 0x40) != 0) {
        return;
      }
      uVar3 = std::chrono::system_clock::now();
      FUN_103f3ffec(auStack_38,4,uVar3);
      iVar1 = FUN_103f3c8b8(auStack_38);
      if (iVar1 != 0) {
        uVar3 = FUN_103f39a78(auStack_38,"Invalid Pointee ID ");
        uVar3 = FUN_103f3b7b0(uVar3,*(undefined4 *)(param_1 + 0x24));
        uVar3 = FUN_103f39a78(uVar3," in APtr ");
        FUN_1014861d8(&local_40,param_1);
        FUN_101432ff0(uVar3,&local_40);
        if ((local_40 != (int *)0x0) && (iVar1 = *local_40, *local_40 = iVar1 + -1, iVar1 + -1 == 0)
           ) {
          FUN_101449efc();
        }
      }
      thunk_FUN_103f395e4(auStack_38);
      if (*(long *)(param_1 + 0x40) != 0) {
        return;
      }
      goto LAB_101535f58;
    }
  }
  uVar3 = std::chrono::system_clock::now();
  FUN_103f3ffec(auStack_38,4,uVar3);
  iVar1 = FUN_103f3c8b8(auStack_38);
  if (iVar1 != 0) {
    FUN_103f39a78(auStack_38,"Trying to access a pointee from outside the document.");
  }
  FUN_1054147dc(auStack_38);
LAB_101535f58:
  FUN_1054147b8();
                    /* WARNING: Subroutine does not return */
  FUN_10017b398();
}

