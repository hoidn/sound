
void FUN_101488ec0(undefined8 param_1)

{
  undefined8 uVar1;
  undefined1 auStack_58 [8];
  undefined1 auStack_50 [8];
  undefined1 auStack_48 [8];
  undefined1 auStack_40 [8];
  undefined1 auStack_38 [8];
  
  uVar1 = ___cxa_allocate_exception(0x30);
  FUN_1014335f8(auStack_38,param_1);
  FUN_1011cb734(auStack_40);
  FUN_1011cb734(auStack_48);
  FUN_1011cb734(auStack_50);
  FUN_1011cb734(auStack_58);
  FUN_101242ce8(uVar1,&DAT_106f4f720,auStack_38,auStack_40,auStack_48,auStack_50,auStack_58);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar1,&PTR_vtable_106661270,FUN_10124335c);
}

