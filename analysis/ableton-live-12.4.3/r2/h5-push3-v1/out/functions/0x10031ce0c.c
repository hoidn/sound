// 0x10031ce0c FUN_10031ce0c state=exported-with-warnings role=temp_directory_path
// source chunk chunk-00137.jsonl; code_sha256=61b7072aff69daba25197b12fd221ee75a9f6ead81a5c9fc126674a09fed8fb7

void FUN_10031ce0c(undefined8 param_1)

{
  system_error *psVar1;
  undefined1 auStack_58 [24];
  int local_40;
  undefined4 uStack_3c;
  undefined8 local_38;
  
  local_40 = 0;
  local_38 = std::system_category();
  FUN_100328f34(param_1,&local_40);
  if (local_40 == 0) {
    return;
  }
  psVar1 = (system_error *)___cxa_allocate_exception(0x50);
  FUN_10017f204(auStack_58,"temp_directory_path() failed");
  std::system_error::system_error(psVar1,CONCAT44(uStack_3c,local_40),local_38,auStack_58);
  *(undefined ***)psVar1 = &PTR_FUN_101bd2bd8;
  *(undefined8 *)(psVar1 + 0x28) = 0;
  *(undefined8 *)(psVar1 + 0x20) = 0;
  *(undefined8 *)(psVar1 + 0x38) = 0;
  *(undefined8 *)(psVar1 + 0x30) = 0;
  *(undefined8 *)(psVar1 + 0x48) = 0;
  *(undefined8 *)(psVar1 + 0x40) = 0;
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(psVar1,&PTR_vtable_101bd2bb0,FUN_1001cf04c);
}

