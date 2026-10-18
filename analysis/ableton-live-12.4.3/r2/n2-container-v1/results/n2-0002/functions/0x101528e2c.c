
void FUN_101528e2c(undefined8 param_1,long param_2)

{
  int iVar1;
  undefined8 uVar2;
  int *local_50 [2];
  char local_39;
  undefined1 auStack_38 [8];
  
  iVar1 = FUN_101429854(param_2 + 0x48,param_2 + 0x50);
  if (iVar1 != 0) {
    if (*(long *)(param_2 + 0x50) == 0) {
      iVar1 = -1;
    }
    else {
      iVar1 = *(int *)(*(long *)(param_2 + 0x50) + 4) / 2 + -1;
    }
    FUN_10142881c(local_50,param_2 + 0x48,iVar1,0x3fffffff);
    FUN_1014300e0(param_1,local_50,&PTR_u__10666fa18);
    if (local_50[0] != (int *)0x0) {
      iVar1 = *local_50[0];
      *local_50[0] = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_101449efc();
      }
    }
    return;
  }
  std::chrono::system_clock::now();
  FUN_103f40190(auStack_38);
  iVar1 = FUN_103f3c8b8(auStack_38);
  if (iVar1 != 0) {
    uVar2 = FUN_103f39a78(auStack_38,"The document hasn\'t been created by \"");
    FUN_1014320f0(local_50,param_2 + 0x50);
    uVar2 = FUN_103f3a958(uVar2,local_50);
    FUN_103f3baec(uVar2,0x22);
    if (local_39 < '\0') {
      operator_delete(local_50[0]);
    }
  }
  thunk_FUN_103f395e4(auStack_38);
  FUN_1011cb734(param_1);
  return;
}

