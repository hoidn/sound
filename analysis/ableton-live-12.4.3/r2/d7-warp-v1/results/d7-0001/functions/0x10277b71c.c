
void FUN_10277b71c(undefined8 param_1,long *param_2)

{
  undefined8 uVar1;
  undefined8 *puVar2;
  long lVar3;
  long *plVar4;
  long lVar5;
  long lVar6;
  int iVar7;
  
  uVar1 = FUN_10156d4c8(param_2);
  FUN_101b39cc4(param_1,uVar1);
  puVar2 = (undefined8 *)(**(code **)(*param_2 + 0x60))(param_2);
  lVar3 = (**(code **)*puVar2)(puVar2,param_2);
  lVar6 = *(long *)(lVar3 + 0x18);
  if (lVar6 != lVar3) {
    iVar7 = 0;
    do {
      if (lVar6 == 0) {
        FUN_10261026c(0);
        FUN_101b39d74(param_1,iVar7);
        uVar1 = 0;
      }
      else {
        plVar4 = (long *)(**(code **)(*param_2 + 0x60))(param_2);
        lVar5 = (**(code **)(*plVar4 + 0x20))(plVar4,param_2,lVar6);
        FUN_10261026c(*(undefined8 *)(lVar5 + 8));
        FUN_101b39d74(param_1,iVar7);
        plVar4 = (long *)(**(code **)(*param_2 + 0x60))(param_2);
        lVar5 = (**(code **)(*plVar4 + 0x20))(plVar4,param_2,lVar6);
        uVar1 = *(undefined8 *)(lVar5 + 8);
      }
      FUN_102610264(uVar1);
      FUN_101b39d80(param_1,iVar7);
      iVar7 = iVar7 + 1;
      lVar6 = *(long *)(lVar6 + 0x18);
    } while (lVar6 != lVar3);
  }
  return;
}

