
void FUN_10307aa68(undefined8 *param_1,long *param_2)

{
  long lVar1;
  int iVar2;
  long *plVar3;
  undefined8 uVar4;
  long lVar5;
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  long local_68;
  long lStack_60;
  long *local_50;
  undefined1 auStack_48 [8];
  
  plVar3 = (long *)FUN_1012d9850(0x70);
  lVar5 = *param_2;
  lVar1 = param_2[1];
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  local_68 = lVar5;
  lStack_60 = lVar1;
  FUN_10128ed98(plVar3);
  *plVar3 = (long)&PTR_FUN_1068bcc60;
  plVar3[3] = lVar5;
  plVar3[4] = lVar1;
  local_68 = 0;
  lStack_60 = 0;
  plVar3[6] = 0;
  plVar3[5] = 0;
  plVar3[8] = 0;
  plVar3[7] = 0;
  plVar3[10] = 0;
  plVar3[9] = 0;
  plVar3[0xc] = 0;
  plVar3[0xb] = 0;
  plVar3[0xd] = 0;
  uVar4 = std::chrono::system_clock::now();
  FUN_103f3ffec(auStack_48,2,uVar4);
  iVar2 = FUN_103f3c8b8(auStack_48);
  if (iVar2 != 0) {
    FUN_103f39a78(auStack_48,"Audio2Midi: Use dynamic loaded MultiF0 lib");
  }
  thunk_FUN_103f395e4(auStack_48);
  *(int *)(plVar3 + 1) = (int)plVar3[1] + 1;
  local_50 = plVar3;
  lVar5 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_GetApiRevision");
  plVar3[5] = lVar5;
  iVar2 = (**(code **)(*plVar3 + 0x28))(plVar3);
  if (iVar2 == 10) {
    lVar5 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_GetDefaultParameters");
    plVar3[6] = lVar5;
    lVar5 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_RunMultiF0OnAudio");
    plVar3[7] = lVar5;
    lVar5 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_GetProgress");
    plVar3[8] = lVar5;
    lVar5 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_GetStatus");
    plVar3[9] = lVar5;
    lVar5 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_CancelProcess");
    plVar3[10] = lVar5;
    lVar5 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_GetMultiF0Result");
    plVar3[0xb] = lVar5;
    lVar5 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_FreeHandle");
    plVar3[0xc] = lVar5;
    lVar5 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_FreeMultiF0Result");
    plVar3[0xd] = lVar5;
    *param_1 = plVar3;
    return;
  }
  uVar4 = ___cxa_allocate_exception(0x30);
  FUN_101447188(&local_68,&DAT_106e0cc01,"API revision does not match. Loaded $1, expected $2.");
  (**(code **)(*plVar3 + 0x28))(plVar3);
  FUN_101430a10(auStack_48);
  FUN_101430a10(auStack_70,10);
  FUN_1011cb734(auStack_78);
  FUN_1011cb734(auStack_80);
  FUN_1011cb734(auStack_88);
  FUN_101242ce8(uVar4,&local_68,auStack_48,auStack_70,auStack_78,auStack_80,auStack_88);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar4,&PTR_vtable_106661270,FUN_10124335c);
}

