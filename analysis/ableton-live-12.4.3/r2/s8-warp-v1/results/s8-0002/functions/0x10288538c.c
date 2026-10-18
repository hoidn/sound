
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10288538c(long param_1)

{
  undefined8 *puVar1;
  long lVar2;
  long *plVar3;
  long lVar4;
  long *plVar5;
  long lVar6;
  
  FUN_101486fa8();
  plVar5 = *(long **)(param_1 + 0x68);
  puVar1 = (undefined8 *)(**(code **)(*plVar5 + 0x60))(plVar5);
  lVar2 = (**(code **)*puVar1)(puVar1,plVar5);
  lVar6 = *(long *)(lVar2 + 0x18);
  while (lVar6 != lVar2) {
    while (lVar6 != 0) {
      plVar3 = (long *)(**(code **)(*plVar5 + 0x60))(plVar5);
      lVar4 = (**(code **)(*plVar3 + 0x20))(plVar3,plVar5,lVar6);
      FUN_102610134(*(undefined8 *)(lVar4 + 8),param_1 + 0x28);
      lVar6 = *(long *)(lVar6 + 0x18);
      if (lVar6 == lVar2) goto LAB_102885434;
    }
    FUN_102610134(0,param_1 + 0x28);
    lVar6 = _DAT_00000018;
  }
LAB_102885434:
  FUN_102884178(param_1);
  return;
}

