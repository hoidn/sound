
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1028f5f74(long param_1)

{
  long lVar1;
  int iVar2;
  undefined8 *puVar3;
  long lVar4;
  long *plVar5;
  long lVar6;
  long *plVar7;
  long lVar8;
  undefined8 uVar9;
  undefined8 local_48;
  
  lVar1 = param_1 + 0x28;
  local_48 = 0;
  FUN_1028f46d0(lVar1,&local_48);
  plVar7 = *(long **)(param_1 + 0x430);
  puVar3 = (undefined8 *)(**(code **)(*plVar7 + 0x60))(plVar7);
  lVar4 = (**(code **)*puVar3)(puVar3,plVar7);
  lVar8 = *(long *)(lVar4 + 0x18);
  do {
    if (lVar8 == lVar4) {
      return;
    }
    while (lVar8 != 0) {
      plVar5 = (long *)(**(code **)(*plVar7 + 0x60))(plVar7);
      lVar6 = (**(code **)(*plVar5 + 0x20))(plVar5,plVar7,lVar8);
      uVar9 = *(undefined8 *)(lVar6 + 8);
      plVar5 = (long *)(**(code **)(*plVar7 + 0x60))(plVar7);
      lVar6 = (**(code **)(*plVar5 + 0x20))(plVar5,plVar7,lVar8);
      iVar2 = FUN_1028aca40(*(undefined8 *)(lVar6 + 8));
      *(undefined8 *)(lVar1 + (long)iVar2 * 8) = uVar9;
      lVar8 = *(long *)(lVar8 + 0x18);
      if (lVar8 == lVar4) {
        return;
      }
    }
    iVar2 = FUN_1028aca40(0);
    *(undefined8 *)(lVar1 + (long)iVar2 * 8) = 0;
    lVar8 = _DAT_00000018;
  } while( true );
}

