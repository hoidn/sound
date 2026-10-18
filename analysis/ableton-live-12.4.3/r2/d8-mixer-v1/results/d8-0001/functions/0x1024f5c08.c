
void FUN_1024f5c08(long param_1,long *param_2)

{
  char *pcVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  long *plVar5;
  undefined1 auStack_78 [24];
  char *local_60;
  undefined1 local_58;
  char *local_48;
  
  FUN_102322ba0();
  uVar3 = (**(code **)(*param_2 + 0x170))(param_2);
  uVar4 = FUN_10265993c();
  iVar2 = FUN_10147fd68(uVar3,uVar4);
  if (iVar2 != 0) {
    param_2 = (long *)FUN_102659688(param_2);
  }
  if ((DAT_10700a970 & 1) == 0) {
    FUN_105421d34();
  }
  local_48 = (char *)0x0;
  FUN_102324308(&local_60);
  pcVar1 = local_60;
  local_48 = local_60;
  uVar3 = (**(code **)(*param_2 + 0x328))(param_2);
  uVar3 = FUN_10232444c(local_60,&DAT_10700aa88,uVar3);
  FUN_1023490d0(param_1,uVar3);
  local_60 = "InClearBang";
  local_58 = 0;
  FUN_102321f5c(*(undefined8 *)(param_1 + 0x80),pcVar1,&local_60,0);
  local_60 = "In";
  local_58 = 0;
  FUN_102321e6c(*(undefined8 *)(param_1 + 0x88),pcVar1,&local_60,0);
  FUN_102322110(pcVar1,*(undefined8 *)(param_1 + 0xa0),4);
  (**(code **)(**(long **)(param_1 + 0x90) + 0x28))(*(long **)(param_1 + 0x90),param_2);
  plVar5 = *(long **)(param_1 + 0x88);
  uVar3 = (**(code **)(*param_2 + 0x328))(param_2);
  FUN_1026faba8(&local_60,param_2);
  FUN_1026f96b0(param_2);
  FUN_1024dd6f8(auStack_78);
  (**(code **)(*plVar5 + 0x280))(plVar5,1,uVar3,&local_60,auStack_78);
  (**(code **)(**(long **)(param_1 + 0x88) + 0xb8))(*(long **)(param_1 + 0x88),param_2);
  (**(code **)(**(long **)(param_1 + 0x88) + 0x2a8))(*(long **)(param_1 + 0x88),pcVar1);
  FUN_1026fac44(param_2,*(undefined8 *)(param_1 + 0x98));
  uVar4 = *(undefined8 *)(param_1 + 0x98);
  uVar3 = FUN_1026f96b0(param_2);
  FUN_1026f40b8(uVar4,uVar3);
  if (pcVar1 != (char *)0x0) {
    iVar2 = *(int *)(pcVar1 + 8);
    *(int *)(pcVar1 + 8) = iVar2 + -1;
    if (iVar2 + -1 == 0) {
      FUN_10128eea0(pcVar1);
    }
  }
  return;
}

