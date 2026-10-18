
void FUN_1030e4c94(long param_1)

{
  undefined *puVar1;
  int iVar2;
  undefined8 uVar3;
  long lVar4;
  undefined8 uVar5;
  long *plVar6;
  int *local_50;
  long lStack_48;
  int *local_40;
  int *local_38;
  
  FUN_10319285c(*(undefined8 *)(param_1 + 0x598),"Filter On/Off",0,0);
  uVar3 = (**(code **)(**(long **)(param_1 + 0x598) + 0x278))();
  FUN_1024874ac(param_1,uVar3);
  if (((DAT_107027038 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107027038), iVar2 != 0)) {
    lVar4 = FUN_1012d9850(0x50);
    FUN_101576354(0x42480000,0x468ca000,0x3f800000,0x3dcccccd);
    DAT_107027030 = lVar4;
    if (lVar4 != 0) {
      *(int *)(lVar4 + 8) = *(int *)(lVar4 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107027030,0x100000000);
    ___cxa_guard_release(&DAT_107027038);
  }
  lVar4 = DAT_107027030;
  uVar5 = *(undefined8 *)(param_1 + 0x5b0);
  uVar3 = FUN_101435cb8();
  FUN_101427680(&local_38,"Filter Mid Freq");
  FUN_1026f0b58(0,0x3f800000,0x447a0000,uVar5,param_1,lVar4,uVar3,&local_38,2);
  if (local_38 != (int *)0x0) {
    iVar2 = *local_38;
    *local_38 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  plVar6 = *(long **)(param_1 + 0x5b0);
  FUN_101427680(&local_50,"Mid Freq");
  (**(code **)(*plVar6 + 0x298))(plVar6,&local_50);
  if (local_50 != (int *)0x0) {
    iVar2 = *local_50;
    *local_50 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  if (((DAT_107027048 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_107027048), iVar2 != 0)) {
    lVar4 = FUN_1012d9850(0x38);
    FUN_101575868(0x3f000000,0x41100000,0x3f800000,0x3dcccccd);
    DAT_107027040 = lVar4;
    if (lVar4 != 0) {
      *(int *)(lVar4 + 8) = *(int *)(lVar4 + 8) + 1;
    }
    ___cxa_atexit(FUN_1002483c0,&DAT_107027040,0x100000000);
    ___cxa_guard_release(&DAT_107027048);
  }
  lVar4 = DAT_107027040;
  uVar5 = *(undefined8 *)(param_1 + 0x5c8);
  uVar3 = FUN_1014380fc();
  FUN_101427680(&local_40,"Filter Width");
  FUN_1026f0b58(0x3f000000,0x41100000,0x40800000,uVar5,param_1,lVar4,uVar3,&local_40,2);
  if (local_40 != (int *)0x0) {
    iVar2 = *local_40;
    *local_40 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  plVar6 = *(long **)(param_1 + 0x5c8);
  FUN_101427680(&local_50,"Width");
  (**(code **)(*plVar6 + 0x298))(plVar6,&local_50);
  if (local_50 != (int *)0x0) {
    iVar2 = *local_50;
    *local_50 = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_101449efc();
    }
  }
  puVar1 = PTR_CallMemberFunc<&ACorpus::FilterCoeffGetterCallback>_106535020;
  local_50 = (int *)PTR_CallMemberFunc<&ACorpus::FilterCoeffGetterCallback>_106535020;
  lStack_48 = param_1;
  FUN_102953ab4(*(undefined8 *)(param_1 + 0x688),0,&local_50);
  local_50 = (int *)puVar1;
  lStack_48 = param_1;
  FUN_102953ab4(*(undefined8 *)(param_1 + 0x690),1,&local_50);
  local_50 = (int *)
             PTR_CallMemberFunc<&(ACorpus::FilterCascadeCountGetterCallback()const)>_106536350;
  lStack_48 = param_1;
  FUN_102953514(*(undefined8 *)(param_1 + 0x698),&local_50);
  FUN_102953520(*(undefined8 *)(param_1 + 0x698),*(undefined8 *)(param_1 + 0x688));
  FUN_102953520(*(undefined8 *)(param_1 + 0x698),*(undefined8 *)(param_1 + 0x690));
  uVar5 = *(undefined8 *)(param_1 + 0x698);
  uVar3 = (**(code **)(**(long **)(param_1 + 0x5b0) + 0x278))();
  FUN_102953070(uVar5,uVar3);
  uVar5 = *(undefined8 *)(param_1 + 0x698);
  uVar3 = (**(code **)(**(long **)(param_1 + 0x5c8) + 0x278))();
  FUN_102953070(uVar5,uVar3);
  return;
}

