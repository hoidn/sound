
void FUN_102565a48(long *param_1,double param_2,long *param_3,long param_4)

{
  undefined8 *puVar1;
  long lVar2;
  long lVar3;
  long lVar4;
  long *plVar5;
  undefined8 uVar6;
  long lVar7;
  double dVar8;
  long local_98;
  long lStack_90;
  long *local_88;
  long *local_80;
  long local_78;
  long lStack_70;
  long *local_68;
  double local_60;
  double local_58;
  
  local_80 = param_3;
  puVar1 = (undefined8 *)(**(code **)(*param_3 + 0x60))();
  lVar2 = (**(code **)*puVar1)(puVar1,param_3);
  local_78 = lVar2;
  local_68 = param_3;
  local_60 = param_2;
  puVar1 = (undefined8 *)(**(code **)(*param_3 + 0x60))(param_3);
  lVar3 = (**(code **)*puVar1)(puVar1,param_3);
  local_98 = lVar3;
  local_88 = param_3;
  puVar1 = (undefined8 *)(**(code **)(*param_3 + 0x60))(param_3);
  lVar4 = (**(code **)*puVar1)(puVar1,param_3);
  lVar7 = *(long *)(lVar4 + 0x18);
  if (lVar7 != lVar4) {
    plVar5 = (long *)(**(code **)(*param_3 + 0x60))(param_3);
    lVar4 = (**(code **)(*plVar5 + 0x20))(plVar5,param_3,lVar7);
    if (*(double *)(*(long *)(lVar4 + 8) + 0x50) < param_2) {
      lVar7 = *(long *)(lVar2 + 0x18);
      lStack_70 = lVar7;
      plVar5 = (long *)(**(code **)(*param_3 + 0x60))(param_3);
      lVar4 = (**(code **)(*plVar5 + 0x20))(plVar5,param_3,lVar7);
      if ((*(double *)(*(long *)(lVar4 + 8) + 0x50) == -63072000.0) &&
         (lVar7 != *(long *)(lVar2 + 0x20))) {
        lVar7 = *(long *)(lVar7 + 0x18);
      }
      plVar5 = (long *)(**(code **)(*param_3 + 0x60))(param_3);
      lVar2 = (**(code **)(*plVar5 + 0x20))(plVar5,param_3,lVar7);
      dVar8 = *(double *)(*(long *)(lVar2 + 8) + 0x50);
      lVar3 = *(long *)(lVar3 + 0x20);
      lStack_90 = lVar3;
      local_58 = dVar8;
      plVar5 = (long *)(**(code **)(*param_3 + 0x60))(param_3);
      lVar2 = (**(code **)(*plVar5 + 0x20))(plVar5,param_3,lVar3);
      if (ABS(*(double *)(*(long *)(lVar2 + 8) + 0x50) - param_2) < ABS(dVar8 - param_2)) {
        plVar5 = (long *)(**(code **)(*param_3 + 0x60))(param_3);
        lVar2 = (**(code **)(*plVar5 + 0x20))(plVar5,param_3,lVar3);
        dVar8 = *(double *)(*(long *)(lVar2 + 8) + 0x50);
        lStack_70 = lStack_90;
        local_78 = local_98;
        local_68 = local_88;
        local_58 = dVar8;
      }
      if (param_4 != 0) {
        plVar5 = (long *)(**(code **)(*param_3 + 0x60))(param_3);
        uVar6 = (**(code **)(*plVar5 + 0x28))(plVar5,param_4);
        FUN_10144a090(&local_98,uVar6);
        lVar2 = lStack_90;
        plVar5 = (long *)(**(code **)(*local_88 + 0x60))();
        lVar3 = (**(code **)(*plVar5 + 0x20))(plVar5,local_88,lVar2);
        lVar2 = lStack_90;
        if (ABS(*(double *)(*(long *)(lVar3 + 8) + 0x50) - param_2) < ABS(dVar8 - param_2)) {
          plVar5 = (long *)(**(code **)(*local_88 + 0x60))();
          lVar2 = (**(code **)(*plVar5 + 0x20))(plVar5,local_88,lVar2);
          local_58 = *(double *)(*(long *)(lVar2 + 8) + 0x50);
          lStack_70 = lStack_90;
          local_78 = local_98;
          local_68 = local_88;
        }
      }
      FUN_1025669d8(&local_80);
      param_1[1] = lStack_70;
      *param_1 = local_78;
      param_1[2] = (long)local_68;
      return;
    }
  }
  param_1[2] = (long)local_88;
  param_1[1] = lVar3;
  *param_1 = local_98;
  return;
}

