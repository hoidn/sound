
void FUN_1026787f0(long param_1)

{
  ulong uVar1;
  undefined8 *puVar2;
  long lVar3;
  undefined8 uVar4;
  long *plVar5;
  long *plVar6;
  long lVar7;
  undefined8 local_38;
  
  plVar6 = *(long **)(param_1 + 0x620);
  uVar1 = FUN_101467280(plVar6);
  if ((uVar1 & 1) == 0) {
    puVar2 = (undefined8 *)(**(code **)(*plVar6 + 0x60))(plVar6);
    lVar3 = (**(code **)*puVar2)(puVar2,plVar6);
    lVar7 = *(long *)(lVar3 + 0x18);
    if (lVar7 != 0 && lVar7 != lVar3) {
      plVar5 = (long *)(**(code **)(*plVar6 + 0x60))(plVar6);
      lVar3 = (**(code **)(*plVar5 + 0x20))(plVar5,plVar6,lVar7);
      uVar4 = *(undefined8 *)(lVar3 + 8);
      goto LAB_102678878;
    }
  }
  uVar4 = 0;
LAB_102678878:
  local_38 = FUN_1026e3698(uVar4);
  uVar4 = FUN_1015661b8(*(undefined8 *)(*(long *)(param_1 + 8) + 0x388));
  FUN_101aaae44(&local_38,uVar4);
  return;
}

