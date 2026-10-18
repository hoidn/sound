
void FUN_1025d9d14(long param_1)

{
  long *plVar1;
  long lVar2;
  long *plVar3;
  int iVar4;
  long *plVar5;
  undefined4 *puVar6;
  undefined4 uVar7;
  ulong uVar8;
  
  plVar1 = (long *)(param_1 + 0x38);
  plVar5 = *(long **)(param_1 + 0x40);
  if (plVar5 != plVar1) {
    do {
      if ((long *)plVar5[4] == (long *)0x0) {
        uVar7 = 2;
      }
      else {
        iVar4 = (**(code **)(*(long *)plVar5[4] + 0x40))();
        uVar7 = 1;
        if (iVar4 == 0) {
          uVar7 = 2;
        }
      }
      FUN_1025dca28(plVar5[5],uVar7);
      puVar6 = (undefined4 *)plVar5[5];
      iVar4 = puVar6[2];
      puVar6[2] = iVar4 + 1000U;
      if ((*(char *)(puVar6 + 0x12) == '\x01') &&
         (uVar8 = *(ulong *)(puVar6 + 0x10), (uint)uVar8 <= iVar4 + 1000U)) {
        uVar7 = *puVar6;
        FUN_1025e4da0(puVar6,uVar8 >> 0x20);
        FUN_1025e8da8(*(undefined8 *)(puVar6 + 0xc),uVar7,*puVar6,uVar8 & 0xffffffff | 0x100000000);
      }
      plVar5 = (long *)plVar5[1];
    } while (plVar5 != plVar1);
    plVar5 = *(long **)(param_1 + 0x40);
  }
  do {
    if (plVar5 == plVar1) {
      return;
    }
    while (*(uint *)plVar5[5] < 0xb && (1 << (ulong)(*(uint *)plVar5[5] & 0x1f) & 0x670U) != 0) {
      lVar2 = *plVar5;
      plVar3 = (long *)plVar5[1];
      *(long **)(lVar2 + 8) = plVar3;
      *plVar3 = lVar2;
      *(long *)(param_1 + 0x48) = *(long *)(param_1 + 0x48) + -1;
      (**(code **)plVar5[2])();
      operator_delete(plVar5);
      plVar5 = plVar3;
      if (plVar3 == plVar1) {
        return;
      }
    }
    plVar5 = (long *)plVar5[1];
  } while( true );
}

