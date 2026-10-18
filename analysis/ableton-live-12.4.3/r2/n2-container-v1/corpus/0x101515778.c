
void FUN_101515778(undefined8 param_1)

{
  long *plVar1;
  long *plVar2;
  int iVar3;
  void *pvVar4;
  long *plVar5;
  undefined8 uVar6;
  long lVar7;
  long *plVar8;
  long local_a0;
  long *local_98;
  long *local_90;
  int local_80 [2];
  undefined8 local_78;
  long *local_70;
  long *local_68 [2];
  char local_51;
  long **local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_1064f8818;
  local_80[0] = 0;
  local_78 = std::system_category();
  FUN_10127b18c(local_68,DAT_105800d30,DAT_105800d38);
  FUN_103e718dc(&local_98,param_1,0x40,local_68,local_80);
  if (local_50 == local_68) {
    lVar7 = 0x20;
  }
  else {
    plVar5 = local_98;
    plVar1 = local_98;
    plVar8 = local_90;
    if (local_50 == (long **)0x0) goto joined_r0x000101515814;
    lVar7 = 0x28;
  }
  (**(code **)((long)*local_50 + lVar7))();
  plVar5 = local_98;
  plVar1 = local_98;
  plVar8 = local_90;
joined_r0x000101515814:
  for (; plVar2 = local_90, local_98 = plVar1, plVar5 != local_90; plVar5 = plVar5 + 1) {
    local_68[0] = (long *)0x0;
    local_90 = plVar8;
    FUN_101463eb4(&local_70);
    if ((local_68[0] != (long *)0x0) &&
       (iVar3 = (int)local_68[0][1] + -1, *(int *)(local_68[0] + 1) = iVar3, iVar3 == 0)) {
      FUN_10128eea0();
    }
    plVar1 = local_70;
    local_68[0] = local_70;
    uVar6 = FUN_103e7c174(plVar5);
    (**(code **)(*plVar1 + 0x98))(plVar1,uVar6);
    (**(code **)(*local_68[0] + 0xa0))(local_68[0],0x17,1);
    (**(code **)(*local_68[0] + 0x68))(local_68[0],0);
    FUN_101514b14(&local_a0,local_68[0]);
    lVar7 = local_a0;
    local_a0 = 0;
    if (lVar7 != 0) {
      pvVar4 = (void *)FUN_10148dbd4();
      operator_delete(pvVar4);
    }
    (**(code **)(*local_68[0] + 0x70))();
    if (((local_68[0] != (long *)0x0) &&
        ((**(code **)(*local_68[0] + 0x18))(), local_68[0] != (long *)0x0)) &&
       (iVar3 = (int)local_68[0][1] + -1, *(int *)(local_68[0] + 1) = iVar3, iVar3 == 0)) {
      FUN_10128eea0();
    }
    plVar1 = local_98;
    plVar8 = local_90;
    local_90 = plVar2;
  }
  if (plVar1 != (long *)0x0) {
    if (plVar8 == plVar1) {
      operator_delete(plVar1);
    }
    else {
      do {
        plVar8 = plVar8 + -1;
        plVar5 = (long *)*plVar8;
        *plVar8 = 0;
        if (plVar5 != (long *)0x0) {
          (**(code **)(*plVar5 + 8))();
        }
      } while (plVar8 != plVar1);
      operator_delete(local_98);
    }
  }
  if (local_80[0] != 0) {
    uVar6 = std::chrono::system_clock::now();
    FUN_103f3ffec(&local_98,4,uVar6);
    iVar3 = FUN_103f3c8b8(&local_98);
    if (iVar3 != 0) {
      uVar6 = FUN_103f39a78(&local_98,"Live: Reading schema files failed: ");
      std::error_code::message();
      FUN_103f3a958(uVar6,local_68);
      if (local_51 < '\0') {
        operator_delete(local_68[0]);
      }
    }
    thunk_FUN_103f395e4(&local_98);
  }
  if (*(long *)PTR____stack_chk_guard_1064f8818 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

