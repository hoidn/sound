
void FUN_10069f714(undefined8 param_1)

{
  undefined8 uVar1;
  undefined8 *puVar2;
  undefined7 local_48;
  char cStack_41;
  char acStack_40 [7];
  undefined1 local_39;
  char local_31;
  
  local_31 = '\x0f';
  local_48 = s_Logging_options_100a4ea42._0_7_;
  cStack_41 = s_Logging_options_100a4ea42[7];
  acStack_40 = (char  [7])s_Logging_options_100a4ea42._8_7_;
  local_39 = 0;
  FUN_10015f6fc(param_1,&local_48,DAT_1009aa3f0,DAT_1009aa3f0 >> 1);
  if (local_31 < '\0') {
    operator_delete((void *)CONCAT17(cStack_41,local_48));
  }
  uVar1 = FUN_10015fa30(param_1);
  local_48 = (undefined7)uVar1;
  cStack_41 = (char)((ulong)uVar1 >> 0x38);
  puVar2 = operator_new(0x98);
  *puVar2 = &PTR_FUN_100b43d50;
  puVar2[1] = &PTR_FUN_100b43dc0;
  puVar2[0xf] = 0;
  puVar2[3] = 0;
  puVar2[2] = 0;
  puVar2[5] = 0;
  puVar2[4] = 0;
  puVar2[7] = 0;
  puVar2[6] = 0;
  puVar2[9] = 0;
  puVar2[8] = 0;
  puVar2[0xb] = 0;
  puVar2[10] = 0;
  puVar2[0xd] = 0;
  puVar2[0xc] = 0;
  *(undefined8 *)((long)puVar2 + 0x6d) = 0;
  uVar1 = FUN_10015f490(&local_48,"log.level",puVar2,
                        "Sets the log-level.  Possible values are: debug, info, warn, error, off");
  puVar2 = operator_new(0x98);
  *puVar2 = &PTR_FUN_100b43d50;
  puVar2[1] = &PTR_FUN_100b43dc0;
  puVar2[0xf] = 0;
  puVar2[3] = 0;
  puVar2[2] = 0;
  puVar2[5] = 0;
  puVar2[4] = 0;
  puVar2[7] = 0;
  puVar2[6] = 0;
  puVar2[9] = 0;
  puVar2[8] = 0;
  puVar2[0xb] = 0;
  puVar2[10] = 0;
  puVar2[0xd] = 0;
  puVar2[0xc] = 0;
  *(undefined8 *)((long)puVar2 + 0x6d) = 0;
  FUN_10015f490(uVar1,"log.categories",puVar2,"Configuration of additional logging categories");
  return;
}

