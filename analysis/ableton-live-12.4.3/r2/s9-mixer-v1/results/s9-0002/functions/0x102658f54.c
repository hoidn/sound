
long FUN_102658f54(long param_1)

{
  undefined *puVar1;
  undefined8 uVar2;
  int iVar3;
  undefined8 *puVar4;
  long *plVar5;
  undefined8 uVar6;
  undefined4 uVar7;
  undefined *local_70;
  long lStack_68;
  int *local_60;
  undefined4 local_58;
  undefined1 local_52;
  undefined1 local_51;
  
  puVar4 = (undefined8 *)FUN_101573bcc();
  *puVar4 = &PTR_FUN_1067efa58;
  FUN_1015643d8(&local_70);
  FUN_10150b1cc(puVar4 + 10,local_70);
  if (local_70 != (undefined *)0x0) {
    iVar3 = *(int *)(local_70 + 8);
    *(int *)(local_70 + 8) = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x50) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_70);
  FUN_10150b1cc(param_1 + 0x68,local_70);
  if (local_70 != (undefined *)0x0) {
    iVar3 = *(int *)(local_70 + 8);
    *(int *)(local_70 + 8) = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x68) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_1015643d8(&local_70);
  FUN_10150b1cc(param_1 + 0x80,local_70);
  if (local_70 != (undefined *)0x0) {
    iVar3 = *(int *)(local_70 + 8);
    *(int *)(local_70 + 8) = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x80) = &PTR_thunk_FUN_10150b2b4_10658fdd8;
  FUN_10156915c(&local_70);
  FUN_10150b1cc(param_1 + 0x98,local_70);
  if (local_70 != (undefined *)0x0) {
    iVar3 = *(int *)(local_70 + 8);
    *(int *)(local_70 + 8) = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0x98) = &PTR_thunk_FUN_10150b2b4_10658fd48;
  FUN_1026f06b4(&local_70);
  FUN_10150b1cc(param_1 + 0xb0,local_70);
  if (local_70 != (undefined *)0x0) {
    iVar3 = *(int *)(local_70 + 8);
    *(int *)(local_70 + 8) = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_10128eea0();
    }
  }
  *(undefined ***)(param_1 + 0xb0) = &PTR_thunk_FUN_10150b2b4_1067ace00;
  FUN_101486414(param_1);
  if (((DAT_10700c320 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_10700c320), iVar3 != 0)) {
    local_70 = (undefined *)CONCAT44(local_70._4_4_,3);
    local_51 = 1;
    local_52 = 1;
    local_58 = 1;
    FUN_1023e06fc(&DAT_10700c318,&local_70,&local_51,&local_52,&local_58);
    ___cxa_atexit(FUN_1023e0784,&DAT_10700c318,0x100000000);
    ___cxa_guard_release(&DAT_10700c320);
  }
  uVar6 = *(undefined8 *)(param_1 + 0xb8);
  if (((DAT_10700c368 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_10700c368), iVar3 != 0)) {
    FUN_1026605c8();
    ___cxa_atexit(FUN_1026606cc,&DAT_10700c360,0x100000000);
    ___cxa_guard_release(&DAT_10700c368);
  }
  uVar7 = (**(code **)(*DAT_10700c360 + 0x30))(0,0,0x3f800000);
  if (((DAT_10700c368 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_10700c368), iVar3 != 0)) {
    FUN_1026605c8();
    ___cxa_atexit(FUN_1026606cc,&DAT_10700c360,0x100000000);
    ___cxa_guard_release(&DAT_10700c368);
  }
  plVar5 = DAT_10700c360;
  uVar2 = DAT_10700c318;
  FUN_101427680(&local_60,"Send");
  FUN_1026f0b58(0,0x3f800000,uVar7,uVar6,0,plVar5,uVar2,&local_60,0);
  if (local_60 != (int *)0x0) {
    iVar3 = *local_60;
    *local_60 = iVar3 + -1;
    if (iVar3 + -1 == 0) {
      FUN_101449efc();
    }
  }
  FUN_1026faab4(*(undefined8 *)(param_1 + 0xb8));
  plVar5 = (long *)FUN_1026f96b0(*(undefined8 *)(param_1 + 0xb8));
  (**(code **)(*plVar5 + 0x240))();
  local_70 = PTR_CallMemberFunc<&ASendHolder::OnIsEnabledByUserChanged>_10652a790;
  lStack_68 = param_1;
  FUN_101564728(*(undefined8 *)(param_1 + 0x58),1,&local_70);
  local_70 = PTR_CallMemberFunc<&ASendHolder::OnDisabledByRoutingChanged>_10652a798;
  lStack_68 = param_1;
  FUN_101564728(*(undefined8 *)(param_1 + 0x70),0,&local_70);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x70),1);
  puVar1 = PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  local_70 = PTR__lambda___1__ARemoteable__TRemoteableUpdate__106551c78;
  lStack_68 = 0;
  FUN_101564728(*(undefined8 *)(param_1 + 0x88),1,&local_70);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0x88),1);
  FUN_101573c14(param_1,*(undefined8 *)(param_1 + 0x88));
  local_70 = puVar1;
  lStack_68 = 0;
  FUN_10156934c(*(undefined8 *)(param_1 + 0xa0),0,&local_70);
  FUN_10155baa4(*(undefined8 *)(param_1 + 0xa0),1);
  return param_1;
}

