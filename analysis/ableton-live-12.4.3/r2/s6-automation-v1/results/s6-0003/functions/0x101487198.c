
void FUN_101487198(long *param_1,undefined8 param_2,undefined8 param_3)

{
  undefined8 *puVar1;
  long lVar2;
  long lVar3;
  long *plVar4;
  ulong uVar5;
  undefined8 uVar6;
  long lVar7;
  
  puVar1 = (undefined8 *)(**(code **)(*param_1 + 0x60))();
  lVar2 = (**(code **)*puVar1)(puVar1,param_1);
  for (lVar7 = *(long *)(lVar2 + 0x18); lVar7 != lVar2; lVar7 = *(long *)(lVar7 + 0x18)) {
    plVar4 = (long *)(**(code **)(*param_1 + 0x60))(param_1);
    (**(code **)(*plVar4 + 0x40))(plVar4,lVar7);
    uVar5 = FUN_10120e310();
    if ((uVar5 & 1) == 0) {
      if (lVar7 == 0) {
        uVar6 = 0;
      }
      else {
        plVar4 = (long *)(**(code **)(*param_1 + 0x60))(param_1);
        lVar3 = (**(code **)(*plVar4 + 0x20))(plVar4,param_1,lVar7);
        uVar6 = *(undefined8 *)(lVar3 + 8);
      }
      FUN_101487198(uVar6,param_2,param_3);
    }
  }
                    /* WARNING: Could not recover jumptable at 0x000101487280. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (**(code **)(*param_1 + 0x100))(param_1,param_2,param_3);
  return;
}

