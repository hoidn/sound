
void FUN_101488490(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined8 uVar1;
  undefined1 auStack_58 [8];
  undefined8 local_50;
  undefined *puStack_48;
  undefined8 local_40;
  undefined *puStack_38;
  
  uVar1 = FUN_10120e26c(param_2);
  local_40 = FUN_10120e26c(param_3);
  puStack_48 = PTR_format_custom<TString>_106509e70;
  puStack_38 = PTR_format_custom<TString>_106509e70;
  local_50 = uVar1;
  FUN_10143e88c(auStack_58,L"Wrong class found. Expected a \"{}\" or subclass, found a \"{}\"",0x3c,
                0xff,&local_50);
                    /* WARNING: Subroutine does not return */
  FUN_10148229c(param_1,auStack_58);
}

