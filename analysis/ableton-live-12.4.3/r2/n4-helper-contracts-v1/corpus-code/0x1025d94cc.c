// 0x1025d94cc FUN_1025d94cc exported  sig: undefined FUN_1025d94cc()

undefined * FUN_1025d94cc(undefined *param_1,long *param_2,long param_3)

{
  int iVar1;
  undefined8 *puVar2;
  long *plVar3;
  long lVar4;
  undefined *local_60;
  undefined *puStack_58;
  
  puVar2 = (undefined8 *)FUN_10128ed98();
  *puVar2 = &PTR_thunk_FUN_1025d9a5c_1067e2c20;
  plVar3 = (long *)(param_3 + 0x18);
  lVar4 = *plVar3;
  if (lVar4 == 0) {
    plVar3 = (long *)(param_1 + 0x30);
  }
  else {
    if (lVar4 == param_3) {
      *(undefined8 **)(param_1 + 0x30) = puVar2 + 3;
      (**(code **)(*(long *)*plVar3 + 0x18))((long *)*plVar3,puVar2 + 3);
      goto LAB_1025d9548;
    }
    *(long *)(param_1 + 0x30) = lVar4;
  }
  *plVar3 = 0;
LAB_1025d9548:
  *(undefined8 *)(param_1 + 0x60) = 0;
  *(undefined8 *)(param_1 + 0x68) = 0;
  *(undefined8 *)(param_1 + 0x58) = 0;
  *(undefined8 *)(param_1 + 0x80) = 0;
  *(undefined8 *)(param_1 + 0x88) = 0;
  *(undefined8 *)(param_1 + 0x78) = 0;
  lVar4 = *param_2;
  *(long *)(param_1 + 0x90) = lVar4;
  *(undefined **)(param_1 + 0x38) = param_1 + 0x38;
  *(undefined **)(param_1 + 0x40) = param_1 + 0x38;
  *(undefined8 *)(param_1 + 0x48) = 0;
  *(undefined ***)(param_1 + 0x50) = &PTR_FUN_1067e3578;
  *(undefined ***)(param_1 + 0x70) = &PTR_FUN_1067e35b8;
  if (lVar4 != 0) {
    *(int *)(lVar4 + 8) = *(int *)(lVar4 + 8) + 1;
  }
  param_1[0x98] = 0;
  *(undefined8 *)(param_1 + 0xa0) = 0;
  *(int *)(param_1 + 8) = *(int *)(param_1 + 8) + 1;
  if (DAT_10700bab0 < DAT_10700bab8) {
    *DAT_10700bab0 = (long)param_1;
    DAT_10700bab0 = DAT_10700bab0 + 1;
  }
  else {
    local_60 = param_1;
    DAT_10700bab0 = (long *)FUN_1025e3fdc(&DAT_10700baa8,&local_60);
    if (local_60 != (undefined *)0x0) {
      iVar1 = *(int *)(local_60 + 8);
      *(int *)(local_60 + 8) = iVar1 + -1;
      if (iVar1 + -1 == 0) {
        FUN_10128eea0();
      }
    }
  }
  local_60 = PTR_CallMemberFunc<&TProcessController::OnTimer>_10652f088;
  puStack_58 = param_1;
  FUN_101447d84(1000,&local_60,"TProcessController");
  return param_1;
}


