
void FUN_1028f6664(long param_1)

{
  int iVar1;
  int iVar2;
  undefined8 *puVar3;
  long lVar4;
  long *plVar5;
  long lVar6;
  undefined8 uVar7;
  long *plVar8;
  long lVar9;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  
  plVar8 = *(long **)(param_1 + 0x430);
  puVar3 = (undefined8 *)(**(code **)(*plVar8 + 0x60))(plVar8);
  lVar4 = (**(code **)*puVar3)(puVar3,plVar8);
  lVar9 = *(long *)(lVar4 + 0x18);
  puVar3 = (undefined8 *)(**(code **)(*plVar8 + 0x60))(plVar8);
  (**(code **)*puVar3)(puVar3,plVar8);
  for (; lVar9 != lVar4; lVar9 = *(long *)(lVar9 + 0x18)) {
    plVar5 = (long *)(**(code **)(*plVar8 + 0x60))(plVar8);
    lVar6 = (**(code **)(*plVar5 + 0x20))(plVar5,plVar8,lVar9);
    uVar7 = FUN_1028abe68(*(undefined8 *)(lVar6 + 8));
    iVar1 = FUN_10155ede4();
    if (0 < iVar1) {
      iVar1 = 0;
      do {
        puVar3 = (undefined8 *)FUN_10155ee2c(uVar7,iVar1);
        lVar6 = FUN_1028da61c();
        if (lVar6 == 0) {
          FUN_1028db9b8(&local_80,puVar3,*(undefined8 *)(param_1 + 0x598));
          puVar3[3] = uStack_68;
          puVar3[2] = uStack_70;
          puVar3[5] = uStack_58;
          puVar3[4] = local_60;
          puVar3[1] = uStack_78;
          *puVar3 = local_80;
        }
        iVar1 = iVar1 + 1;
        iVar2 = FUN_10155ede4(uVar7);
      } while (iVar1 < iVar2);
    }
  }
  return;
}

