
undefined8 FUN_1028f5640(long param_1)

{
  ulong uVar1;
  undefined8 *puVar2;
  long lVar3;
  long *plVar4;
  long lVar5;
  undefined8 uVar6;
  long *plVar7;
  long lVar8;
  long lVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  
  uVar1 = FUN_10156da34(*(undefined8 *)(param_1 + 0x4a8));
  if ((uVar1 & 1) == 0) {
    plVar7 = *(long **)(param_1 + 0x4a8);
    puVar2 = (undefined8 *)(**(code **)(*plVar7 + 0x60))(plVar7);
    lVar3 = (**(code **)*puVar2)(puVar2,plVar7);
    lVar8 = *(long *)(lVar3 + 0x18);
    puVar2 = (undefined8 *)(**(code **)(*plVar7 + 0x60))(plVar7);
    (**(code **)*puVar2)(puVar2,plVar7);
    if (lVar8 != lVar3) {
      lVar9 = 0;
      do {
        plVar4 = (long *)(**(code **)(*plVar7 + 0x60))(plVar7);
        lVar5 = (**(code **)(*plVar4 + 0x20))(plVar4,plVar7,lVar8);
        uVar11 = *(undefined8 *)(lVar5 + 8);
        lVar5 = FUN_102926940(uVar11);
        if (lVar5 == 0) {
          return 0;
        }
        lVar5 = FUN_102926940(uVar11);
        if (lVar5 <= lVar9) {
          return 0;
        }
        uVar10 = *(undefined8 *)(param_1 + 0x5b0);
        uVar6 = FUN_102926940(uVar11);
        uVar6 = FUN_102920ecc(uVar10,uVar6);
        if ((int)uVar6 == 0) {
          return uVar6;
        }
        FUN_1028f5770(param_1,uVar11);
        lVar9 = FUN_102926940(uVar11);
        lVar8 = *(long *)(lVar8 + 0x18);
      } while (lVar8 != lVar3);
    }
  }
  return 1;
}

