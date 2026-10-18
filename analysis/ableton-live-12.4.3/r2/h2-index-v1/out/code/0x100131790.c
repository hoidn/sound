// 0x100131790 FUN_100131790 state=exported body_bytes=488 warnings=0 chunk=chunk-00052.jsonl

void FUN_100131790(undefined8 param_1)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined8 *puVar3;
  void *local_90;
  char acStack_88 [8];
  undefined8 local_80;
  undefined8 local_28;
  
  local_80 = CONCAT17(0x10,(undefined7)local_80);
  acStack_88 = (char  [8])s_AppIndex_options_100c1d0ce._8_8_;
  local_90 = (void *)s_AppIndex_options_100c1d0ce._0_8_;
  local_80 = local_80 & 0xffffffffffffff00;
  FUN_100190f90(param_1,&local_90,DAT_100ba1ad8,DAT_100ba1ad8 >> 1);
  if ((long)local_80 < 0) {
    operator_delete(local_90);
  }
  local_28 = FUN_1001912c4(param_1);
  uVar1 = FUN_100196dd4();
  uVar1 = FUN_100190d24(&local_28,"slave,l",uVar1,"Slave mode");
  uVar2 = FUN_100196dd4();
  uVar1 = FUN_100190d24(uVar1,"standalone,s",uVar2,"Stand-alone mode");
  uVar2 = FUN_100196dd4();
  uVar1 = FUN_100190d24(uVar1,"os-notifications,t",uVar2,"Test OS notifications");
  puVar3 = operator_new(0x98);
  *puVar3 = &PTR_FUN_100d87d18;
  puVar3[1] = &PTR_FUN_100d87d88;
  puVar3[0xf] = 0;
  puVar3[3] = 0;
  puVar3[2] = 0;
  puVar3[5] = 0;
  puVar3[4] = 0;
  puVar3[7] = 0;
  puVar3[6] = 0;
  puVar3[9] = 0;
  puVar3[8] = 0;
  puVar3[0xb] = 0;
  puVar3[10] = 0;
  puVar3[0xd] = 0;
  puVar3[0xc] = 0;
  *(undefined8 *)((long)puVar3 + 0x6d) = 0;
  local_90 = (void *)0x0;
  acStack_88[0] = '\0';
  acStack_88[1] = '\0';
  acStack_88[2] = '\0';
  acStack_88[3] = '\0';
  acStack_88[4] = '\0';
  acStack_88[5] = '\0';
  acStack_88[6] = '\0';
  acStack_88[7] = '\0';
  local_80 = 0;
  uVar2 = FUN_100147058(puVar3,&local_90);
  uVar1 = FUN_100190d24(uVar1,"libconfig,L",uVar2,"Path to library configuration file");
  uVar2 = FUN_100196dd4();
  uVar1 = FUN_100190d24(uVar1,"dump-config-files",uVar2,
                        "Dump empty configurations files into the current folder");
  puVar3 = operator_new(0x98);
  *puVar3 = &PTR_FUN_100d87ee8;
  puVar3[1] = &PTR_FUN_100d87f58;
  puVar3[0xf] = 0;
  puVar3[3] = 0;
  puVar3[2] = 0;
  puVar3[5] = 0;
  puVar3[4] = 0;
  puVar3[7] = 0;
  puVar3[6] = 0;
  puVar3[9] = 0;
  puVar3[8] = 0;
  puVar3[0xb] = 0;
  puVar3[10] = 0;
  puVar3[0xd] = 0;
  puVar3[0xc] = 0;
  *(undefined8 *)((long)puVar3 + 0x6d) = 0;
  FUN_100190d24(uVar1,"options-file",puVar3,"File containing additional options");
  if ((long)local_80 < 0) {
    operator_delete(local_90);
  }
  FUN_1001af854(&local_90,0);
  FUN_100190ffc(param_1,&local_90);
  FUN_10014b72c(&local_90);
  return;
}

