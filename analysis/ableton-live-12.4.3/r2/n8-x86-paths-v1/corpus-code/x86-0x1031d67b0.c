// x86 0x1031d67b0 FUN_1031d67b0 state=exported-with-warnings chunk=chunk-02323.jsonl code_sha256=e65f4b9cb2933e35dfed28d5886e73153e302007f0f45b303ff8014bda4cd1b0

undefined8 * FUN_1031d67b0(undefined8 *param_1,long *param_2)

{
  long lVar1;
  char cVar2;
  int iVar3;
  long *plVar4;
  undefined8 uVar5;
  long lVar6;
  undefined1 local_38 [8];
  
  plVar4 = (long *)FUN_1012bdaa0(0x70);
  lVar6 = *param_2;
  lVar1 = param_2[1];
  if (lVar1 != 0) {
    LOCK();
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
    UNLOCK();
  }
  FUN_1012715b0(plVar4);
  *plVar4 = (long)&PTR_FUN_106e026b8;
  plVar4[3] = lVar6;
  plVar4[4] = lVar1;
  plVar4[0xb] = 0;
  plVar4[0xc] = 0;
  plVar4[9] = 0;
  plVar4[10] = 0;
  plVar4[7] = 0;
  plVar4[8] = 0;
  plVar4[5] = 0;
  plVar4[6] = 0;
  plVar4[0xd] = 0;
  uVar5 = std::chrono::system_clock::now();
  FUN_10410fff0(local_38,2,uVar5);
  cVar2 = FUN_10410c530(local_38);
  if (cVar2 != '\0') {
    FUN_104108bf0(local_38,"Audio2Midi: Use dynamic loaded MultiF0 lib");
  }
  FUN_104108a10(local_38);
  *(int *)(plVar4 + 1) = (int)plVar4[1] + 1;
  lVar6 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_GetApiRevision");
  plVar4[5] = lVar6;
  iVar3 = (**(code **)(*plVar4 + 0x28))(plVar4);
  if (iVar3 == 10) {
    lVar6 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_GetDefaultParameters");
    plVar4[6] = lVar6;
    lVar6 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_RunMultiF0OnAudio");
    plVar4[7] = lVar6;
    lVar6 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_GetProgress");
    plVar4[8] = lVar6;
    lVar6 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_GetStatus");
    plVar4[9] = lVar6;
    lVar6 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_CancelProcess");
    plVar4[10] = lVar6;
    lVar6 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_GetMultiF0Result");
    plVar4[0xb] = lVar6;
    lVar6 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_FreeHandle");
    plVar4[0xc] = lVar6;
    lVar6 = (**(code **)(*(long *)*param_2 + 0x20))((long *)*param_2,"mf0p_FreeMultiF0Result");
    plVar4[0xd] = lVar6;
    *param_1 = plVar4;
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___cxa_allocate_exception(0x30);
}

