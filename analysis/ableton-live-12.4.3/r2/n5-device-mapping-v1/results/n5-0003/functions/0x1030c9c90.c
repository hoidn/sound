
long FUN_1030c9c90(long param_1)

{
  int iVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  int *local_a8;
  int *local_a0;
  int *local_98;
  int *local_90;
  int *local_88;
  int *local_80;
  int *local_78;
  long local_70;
  undefined1 auStack_68 [8];
  undefined1 auStack_60 [8];
  undefined1 auStack_58 [8];
  undefined1 auStack_50 [8];
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_1064f8818;
  puVar2 = (undefined8 *)FUN_103197678();
  *puVar2 = &PTR_FUN_1068c2718;
  puVar2[10] = &PTR_FUN_1068c2cf0;
  puVar2[0xb] = &PTR_FUN_1068c2d28;
  puVar2[0x37] = &PTR_FUN_1068c2da0;
  FUN_1026eece0(&local_70);
  FUN_10150b1cc(param_1 + 0x248,local_70);
  if (local_70 != 0) {
    iVar1 = *(int *)(local_70 + 8) + -1;
    *(int *)(local_70 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x248) = &PTR_thunk_FUN_10150b2b4_1068001d0;
  FUN_1026ebbc4(&local_70);
  FUN_10150b1cc(param_1 + 0x260,local_70);
  if (local_70 != 0) {
    iVar1 = *(int *)(local_70 + 8) + -1;
    *(int *)(local_70 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x260) = &PTR_thunk_FUN_10150b2b4_1067b50c8;
  FUN_1026eece0(&local_70);
  FUN_10150b1cc(param_1 + 0x278,local_70);
  if (local_70 != 0) {
    iVar1 = *(int *)(local_70 + 8) + -1;
    *(int *)(local_70 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x278) = &PTR_thunk_FUN_10150b2b4_1068001d0;
  FUN_1026ebbc4(&local_70);
  FUN_10150b1cc(param_1 + 0x290,local_70);
  if (local_70 != 0) {
    iVar1 = *(int *)(local_70 + 8) + -1;
    *(int *)(local_70 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x290) = &PTR_thunk_FUN_10150b2b4_1067b50c8;
  FUN_1026f06b4(&local_70);
  FUN_10150b1cc(param_1 + 0x2a8,local_70);
  if (local_70 != 0) {
    iVar1 = *(int *)(local_70 + 8) + -1;
    *(int *)(local_70 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x2a8) = &PTR_thunk_FUN_10150b2b4_1067ace00;
  FUN_101486414(param_1);
  uVar3 = *(undefined8 *)(param_1 + 0xd0);
  FUN_101427680(&local_78,"Cabinet");
  FUN_10156fa68(uVar3,&local_78);
  if (local_78 != (int *)0x0) {
    iVar1 = *local_78;
    *local_78 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_1023a147c(param_1);
  if (((DAT_107026e70 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107026e70), iVar1 != 0)) {
    FUN_101427680(&local_70,"1x12");
    FUN_101427680(auStack_68,"2x12");
    FUN_101427680(auStack_60,"4x12");
    FUN_101427680(auStack_58,"4x10");
    FUN_101427680(auStack_50,"4x10 Bass");
    FUN_1002c29cc(&DAT_107027128,&local_70,5);
    FUN_100234444(auStack_50);
    FUN_100234444(auStack_58);
    FUN_100234444(auStack_60);
    FUN_100234444(auStack_68);
    FUN_100234444(&local_70);
    ___cxa_atexit(FUN_1002343c8,&DAT_107027128,0x100000000);
    ___cxa_guard_release(&DAT_107026e70);
  }
  uVar3 = *(undefined8 *)(param_1 + 0x250);
  FUN_101427680(&local_80,"Cabinet Type");
  FUN_1026ef060(uVar3,0,&DAT_107027128,&local_80,1);
  if (local_80 != (int *)0x0) {
    iVar1 = *local_80;
    *local_80 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar3 = *(undefined8 *)(param_1 + 0x268);
  FUN_101427680(&local_88,"Microphone Type");
  FUN_101427680(&local_90,"Dynamic");
  FUN_101427680(&local_98,"Condenser");
  FUN_102a43394(&local_70,&local_90,&local_98);
  FUN_1026ec1cc(uVar3,0,&local_88,local_70);
  if (local_70 != 0) {
    iVar1 = *(int *)(local_70 + 8) + -1;
    *(int *)(local_70 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  if (local_98 != (int *)0x0) {
    iVar1 = *local_98;
    *local_98 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_90 != (int *)0x0) {
    iVar1 = *local_90;
    *local_90 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (local_88 != (int *)0x0) {
    iVar1 = *local_88;
    *local_88 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (((DAT_107026e78 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107026e78), iVar1 != 0)) {
    FUN_101427680(&local_70,"Near On-Axis");
    FUN_101427680(auStack_68,"Near Off-Axis");
    FUN_101427680(auStack_60,"Far");
    FUN_1002c29cc(&DAT_107027140,&local_70,3);
    FUN_100234444(auStack_60);
    FUN_100234444(auStack_68);
    FUN_100234444(&local_70);
    ___cxa_atexit(FUN_1002343c8,&DAT_107027140,0x100000000);
    ___cxa_guard_release(&DAT_107026e78);
  }
  uVar3 = *(undefined8 *)(param_1 + 0x280);
  FUN_101427680(&local_a0,"Microphone Position");
  FUN_1026ef060(uVar3,0,&DAT_107027140,&local_a0,1);
  if (local_a0 != (int *)0x0) {
    iVar1 = *local_a0;
    *local_a0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  uVar4 = *(undefined8 *)(param_1 + 0x298);
  FUN_101427680(&local_a8,"Dual Mono");
  uVar3 = FUN_10143b884();
  FUN_1026ec1cc(uVar4,0,&local_a8,uVar3);
  if (local_a8 != (int *)0x0) {
    iVar1 = *local_a8;
    *local_a8 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_103197bf8(param_1,*(undefined8 *)(param_1 + 0x2b0));
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_48) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

