
void FUN_10146d168(undefined8 param_1,undefined8 param_2)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  long local_58;
  undefined1 auStack_50 [8];
  undefined8 local_48;
  undefined8 uStack_40;
  undefined8 local_38;
  
  if (DAT_106f4f5e0 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
    FUN_10148229c(DAT_106f4f5d8,param_2);
  }
  local_48 = 0;
  uStack_40 = 0;
  local_38 = 0;
  (**(code **)(*DAT_106f4f5e0 + 0x28))();
  uVar2 = FUN_10120e26c();
  FUN_10046f0dc(&local_48,0,uVar2);
  iVar1 = FUN_101471938(&local_48,DAT_106f4f5e0,param_1);
  if (iVar1 != 0) {
    uVar2 = FUN_1002e40c8(param_2,", path: ");
    FUN_101427680(&local_58,"/");
    if (local_58 == 0) {
      lVar3 = -1;
    }
    else {
      lVar3 = (long)(*(int *)(local_58 + 4) / 2 + -1);
    }
    FUN_1014267d8(auStack_50,&local_48,local_58 + 0x10,lVar3);
    FUN_10142da5c(uVar2,auStack_50);
    FUN_100234444(auStack_50);
    FUN_100234444(&local_58);
  }
  FUN_1002343c8(&local_48);
                    /* WARNING: Subroutine does not return */
  FUN_10148229c(DAT_106f4f5d8,param_2);
}

