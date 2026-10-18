
void FUN_101825d1c(undefined8 *param_1)

{
  long *plVar1;
  undefined4 uVar2;
  int *piVar3;
  int iVar4;
  int iVar5;
  undefined8 uVar6;
  int *local_b0;
  undefined1 local_a8;
  undefined7 uStack_a7;
  char local_90;
  undefined1 auStack_88 [56];
  char local_50;
  int *local_48;
  int *local_40;
  
  plVar1 = (long *)param_1[1];
  iVar5 = *(int *)*param_1;
  if (iVar5 == -1) {
                    /* WARNING: Could not recover jumptable at 0x000101825e44. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x5f0))(plVar1,0,0);
    return;
  }
  iVar4 = FUN_101826568(plVar1);
  if ((-1 < iVar5) && (iVar5 < iVar4)) {
    local_a8 = 0;
    local_90 = '\0';
    FUN_10172c2dc(auStack_88,plVar1,&local_a8);
    if ((local_90 == '\x01') &&
       ((piVar3 = (int *)CONCAT71(uStack_a7,local_a8), piVar3 != (int *)0x0 &&
        (iVar5 = *piVar3, *piVar3 = iVar5 + -1, iVar5 + -1 == 0)))) {
      FUN_101449efc();
    }
    uVar2 = *(undefined4 *)*param_1;
    FUN_10172b93c(&local_48,plVar1);
    for (piVar3 = local_48; piVar3 != local_40; piVar3 = piVar3 + 2) {
      (**(code **)(**(long **)piVar3 + 0x228))(*(long **)piVar3,uVar2);
    }
    if (local_48 != (int *)0x0) {
      operator_delete(local_48);
    }
    FUN_10172c504(plVar1,auStack_88);
    if (local_50 == '\x01') {
      thunk_FUN_101557acc(auStack_88);
    }
    return;
  }
  uVar6 = std::chrono::system_clock::now();
  FUN_103f3ffec(auStack_88,4,uVar6);
  iVar5 = FUN_103f3c8b8(auStack_88);
  if (iVar5 != 0) {
    uVar6 = FUN_103f39a78(auStack_88,"Value ");
    uVar6 = FUN_103f3b7b0(uVar6,*(undefined4 *)*param_1);
    uVar6 = FUN_103f39a78(uVar6," out of range for \'");
    FUN_1017928cc(plVar1);
    FUN_101447580(&local_48);
    uVar6 = FUN_101432ff0(uVar6,&local_48);
    uVar6 = FUN_103f39a78(uVar6,"\' (");
    FUN_1014861d8(&local_b0,plVar1);
    uVar6 = FUN_101432ff0(uVar6,&local_b0);
    FUN_103f39a78(uVar6,")");
    if ((local_b0 != (int *)0x0) && (iVar5 = *local_b0, *local_b0 = iVar5 + -1, iVar5 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((local_48 != (int *)0x0) && (iVar5 = *local_48, *local_48 = iVar5 + -1, iVar5 + -1 == 0)) {
      FUN_101449efc();
    }
  }
  thunk_FUN_103f395e4(auStack_88);
  return;
}

