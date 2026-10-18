
void FUN_101528c84(long param_1)

{
  undefined8 uVar1;
  undefined1 auStack_58 [8];
  undefined1 auStack_50 [8];
  undefined1 auStack_48 [8];
  undefined1 auStack_40 [8];
  long local_38;
  
  FUN_101528e2c(&local_38);
  if ((local_38 != 0) && ((*(uint *)(local_38 + 4) & 0xfffffffe) == 2)) {
                    /* WARNING: Subroutine does not return */
    FUN_101488ec0(*(undefined8 *)(param_1 + 0x18));
  }
  uVar1 = ___cxa_allocate_exception(0x30);
  FUN_1014335f8(auStack_40,*(undefined8 *)(param_1 + 0x18));
  FUN_1011cb734(auStack_48);
  FUN_1011cb734(auStack_50);
  FUN_1011cb734(auStack_58);
  FUN_101242ce8(uVar1,&DAT_106f50538,auStack_40,&local_38,auStack_48,auStack_50,auStack_58);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar1,&PTR_vtable_106661270,FUN_10124335c);
}

