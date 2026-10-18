
long FUN_101565194(long param_1)

{
  undefined8 *puVar1;
  
  puVar1 = (undefined8 *)FUN_10156e5e0();
  *puVar1 = &PTR_FUN_10667d7e8;
  puVar1[0xc] = PTR_CallStaticFunc<&ARemoteableDouble::SDefaultController>_106536920;
  puVar1[0xd] = 0;
  FUN_101486414();
  *(undefined1 **)(param_1 + 0x58) = &DAT_7fefffffffffffff;
  *(undefined1 *)(param_1 + 0x70) = 0;
  return param_1;
}

