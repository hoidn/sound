
void FUN_1002fe740(undefined8 param_1,char *param_2)

{
  ulong uVar1;
  undefined1 auStack_60 [8];
  undefined1 auStack_58 [8];
  undefined1 auStack_50 [8];
  undefined1 auStack_48 [8];
  undefined1 auStack_40 [8];
  undefined1 auStack_38 [24];
  
  if (*param_2 != '\x01') {
    return;
  }
  uVar1 = FUN_1011b5354();
  if ((uVar1 & 1) != 0) {
                    /* WARNING: Subroutine does not return */
    FUN_1011a68f8(0x2a);
  }
  FUN_10178ae84(auStack_38);
  FUN_1011cb734(auStack_40);
  FUN_1011cb734(auStack_48);
  FUN_1011cb734(auStack_50);
  FUN_1011cb734(auStack_58);
  FUN_1011cb734(auStack_60);
  FUN_101241d1c(auStack_38,auStack_40,auStack_48,auStack_50,auStack_58,auStack_60);
  FUN_100234444(auStack_60);
  FUN_100234444(auStack_58);
  FUN_100234444(auStack_50);
  FUN_100234444(auStack_48);
  FUN_100234444(auStack_40);
  FUN_100236a4c(auStack_38);
                    /* WARNING: Subroutine does not return */
  FUN_1011a68f8(0x2a);
}

