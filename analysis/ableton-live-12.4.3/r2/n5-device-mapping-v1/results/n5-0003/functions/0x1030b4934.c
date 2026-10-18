
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

long FUN_1030b4934(long param_1)

{
  int iVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  int *local_a8;
  int *local_a0;
  int *local_98;
  long local_90;
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  undefined1 auStack_68 [8];
  undefined1 auStack_60 [8];
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_1064f8818;
  puVar2 = (undefined8 *)FUN_103197678();
  *puVar2 = &PTR_FUN_1068bff78;
  puVar2[10] = &PTR_FUN_1068c0550;
  puVar2[0xb] = &PTR_FUN_1068c0588;
  puVar2[0x37] = &PTR_FUN_1068c0600;
  FUN_1026eece0(&local_90);
  FUN_10150b1cc(param_1 + 0x248,local_90);
  if (local_90 != 0) {
    iVar1 = *(int *)(local_90 + 8) + -1;
    *(int *)(local_90 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x248) = &PTR_thunk_FUN_10150b2b4_1068001d0;
  FUN_1026f06b4(&local_90);
  FUN_10150b1cc(param_1 + 0x260,local_90);
  if (local_90 != 0) {
    iVar1 = *(int *)(local_90 + 8) + -1;
    *(int *)(local_90 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x260) = &PTR_thunk_FUN_10150b2b4_1067ace00;
  FUN_1026f06b4(&local_90);
  FUN_10150b1cc(param_1 + 0x278,local_90);
  if (local_90 != 0) {
    iVar1 = *(int *)(local_90 + 8) + -1;
    *(int *)(local_90 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x278) = &PTR_thunk_FUN_10150b2b4_1067ace00;
  FUN_1026f06b4(&local_90);
  FUN_10150b1cc(param_1 + 0x290,local_90);
  if (local_90 != 0) {
    iVar1 = *(int *)(local_90 + 8) + -1;
    *(int *)(local_90 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x290) = &PTR_thunk_FUN_10150b2b4_1067ace00;
  FUN_1026f06b4(&local_90);
  FUN_10150b1cc(param_1 + 0x2a8,local_90);
  if (local_90 != 0) {
    iVar1 = *(int *)(local_90 + 8) + -1;
    *(int *)(local_90 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x2a8) = &PTR_thunk_FUN_10150b2b4_1067ace00;
  FUN_1026f06b4(&local_90);
  FUN_10150b1cc(param_1 + 0x2c0,local_90);
  if (local_90 != 0) {
    iVar1 = *(int *)(local_90 + 8) + -1;
    *(int *)(local_90 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x2c0) = &PTR_thunk_FUN_10150b2b4_1067ace00;
  FUN_1026f06b4(&local_90);
  FUN_10150b1cc(param_1 + 0x2d8,local_90);
  if (local_90 != 0) {
    iVar1 = *(int *)(local_90 + 8) + -1;
    *(int *)(local_90 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x2d8) = &PTR_thunk_FUN_10150b2b4_1067ace00;
  FUN_1026ebbc4(&local_90);
  FUN_10150b1cc(param_1 + 0x2f0,local_90);
  if (local_90 != 0) {
    iVar1 = *(int *)(local_90 + 8) + -1;
    *(int *)(local_90 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x2f0) = &PTR_thunk_FUN_10150b2b4_1067b50c8;
  FUN_1026f06b4(&local_90);
  FUN_10150b1cc(param_1 + 0x308,local_90);
  if (local_90 != 0) {
    iVar1 = *(int *)(local_90 + 8) + -1;
    *(int *)(local_90 + 8) = iVar1;
    if (iVar1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x308) = &PTR_thunk_FUN_10150b2b4_1067ace00;
  FUN_101486414(param_1);
  uVar3 = *(undefined8 *)(param_1 + 0xd0);
  FUN_101427680(&local_98,"Amp");
  FUN_10156fa68(uVar3,&local_98);
  if (local_98 != (int *)0x0) {
    iVar1 = *local_98;
    *local_98 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_1023a147c(param_1);
  if (((DAT_107026c98 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_107026c98), iVar1 != 0)) {
    FUN_101427680(&local_90,"Clean");
    FUN_101427680(auStack_88,"Boost");
    FUN_101427680(auStack_80,"Blues");
    FUN_101427680(auStack_78,"Rock");
    FUN_101427680(auStack_70,"Lead");
    FUN_101427680(auStack_68,"Heavy");
    FUN_101427680(auStack_60,"Bass");
    FUN_1002c29cc(&DAT_107026dc0,&local_90,7);
    FUN_100234444(auStack_60);
    FUN_100234444(auStack_68);
    FUN_100234444(auStack_70);
    FUN_100234444(auStack_78);
    FUN_100234444(auStack_80);
    FUN_100234444(auStack_88);
    FUN_100234444(&local_90);
    ___cxa_atexit(FUN_1002343c8,&DAT_107026dc0,0x100000000);
    ___cxa_guard_release(&DAT_107026c98);
  }
  if (DAT_106e78588 == 0) {
    if (DAT_106e78580 != (undefined8 *)0x0) {
      if (DAT_106e7858c == '\x01') {
        FUN_101a24778(DAT_106e78580,0);
      }
      DAT_106e78580 = (undefined8 *)0x0;
      DAT_106e78588 = 0;
    }
    puVar2 = operator_new__(0x1c);
    uVar3 = _DAT_1058c6a70;
    DAT_106e78588 = 7;
    DAT_106e7858c = '\x01';
    DAT_106e78580 = puVar2;
    puVar2[1] = _UNK_1058c6a78;
    *puVar2 = uVar3;
    puVar2[2] = DAT_1055102d0;
    *(undefined4 *)(puVar2 + 3) = 6;
  }
  uVar3 = *(undefined8 *)(param_1 + 0x250);
  FUN_101427680(&local_a0,"Amp Type");
  FUN_1026ef060(uVar3,2,&DAT_107026dc0,&local_a0,1);
  if (local_a0 != (int *)0x0) {
    iVar1 = *local_a0;
    *local_a0 = iVar1 + -1;
    if (iVar1 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_103197a6c(0x40a00000,param_1,*(undefined8 *)(param_1 + 0x268),"Bass");
  FUN_103197a6c(0x40a00000,param_1,*(undefined8 *)(param_1 + 0x280),"Middle");
  FUN_103197a6c(0x40a00000,param_1,*(undefined8 *)(param_1 + 0x298),"Treble");
  FUN_103197a6c(0x40a00000,param_1,*(undefined8 *)(param_1 + 0x2b0),"Presence");
  FUN_103197a6c(0x40a00000,param_1,*(undefined8 *)(param_1 + 0x2c8),"Input Gain");
  FUN_103197a6c(0x41100000,param_1,*(undefined8 *)(param_1 + 0x2e0),"Volume");
  FUN_103197bf8(param_1,*(undefined8 *)(param_1 + 0x310));
  uVar4 = *(undefined8 *)(param_1 + 0x2f8);
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
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_58) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

