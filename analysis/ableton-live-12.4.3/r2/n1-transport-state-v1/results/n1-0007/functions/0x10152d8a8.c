
void FUN_10152d8a8(long param_1)

{
  int iVar1;
  undefined8 uVar2;
  long lVar3;
  undefined4 uVar4;
  ulong uVar5;
  undefined8 *puVar6;
  long *plVar7;
  undefined8 uVar8;
  long *plVar9;
  int *local_50;
  long local_48;
  undefined4 uStack_40;
  undefined4 uStack_3c;
  undefined2 uStack_38;
  byte bStack_36;
  
  if (*(long *)(param_1 + 0x90) == 0) {
    return;
  }
  uVar5 = (*(long *)(param_1 + 0x90) + *(long *)(param_1 + 0x88)) - 1;
  puVar6 = (undefined8 *)
           (*(long *)(*(long *)(param_1 + 0x70) + (uVar5 / 0x66) * 8) + (uVar5 % 0x66) * 0x28);
  plVar7 = (long *)*puVar6;
  if (plVar7 != (long *)0x0) {
    *(int *)(plVar7 + 1) = (int)plVar7[1] + 1;
  }
  local_50 = (int *)puVar6[1];
  if (local_50 != (int *)0x0) {
    *local_50 = *local_50 + 1;
  }
  local_48 = puVar6[2];
  uStack_38 = (undefined2)((uint)*(undefined4 *)((long)puVar6 + 0x1f) >> 8);
  bStack_36 = (byte)((uint)*(undefined4 *)((long)puVar6 + 0x1f) >> 0x18);
  uStack_40 = (undefined4)puVar6[3];
  uStack_3c = (undefined4)((ulong)puVar6[3] >> 0x20);
  FUN_101533f94(param_1 + 0x68);
  if ((bStack_36 & 1) == 0) {
    if (local_48 != 0) {
      uVar8 = *(undefined8 *)(param_1 + 0xa8);
      FUN_1014812d8();
      uVar2 = FUN_10120e26c();
      FUN_101522fb8(uVar8,uVar2,local_48);
    }
    lVar3 = (**(code **)(**(long **)(param_1 + 0xd0) + 0x60))();
    if (lVar3 != 0) {
      (**(code **)(**(long **)(param_1 + 0xd0) + 0x70))();
      (**(code **)(**(long **)(param_1 + 0xd0) + 0x68))(*(long **)(param_1 + 0xd0),0);
      (**(code **)(*plVar7 + 0x28))();
      iVar1 = FUN_10120e264();
      if (iVar1 == 0x50) {
        FUN_10152dbe4(param_1);
      }
      else {
        FUN_10152df0c(param_1,plVar7);
      }
      (**(code **)(**(long **)(param_1 + 0xd0) + 0x70))();
      (**(code **)(**(long **)(param_1 + 0xd0) + 0x68))(*(long **)(param_1 + 0xd0),1);
      (**(code **)(**(long **)(param_1 + 0xd0) + 0xb0))();
    }
    if (*(long *)(param_1 + 0x90) == 0) {
      if (plVar7 != (long *)0x0) {
        *(int *)(plVar7 + 1) = (int)plVar7[1] + 1;
      }
      lVar3 = *(long *)(param_1 + 0xa0);
      if ((lVar3 != 0) &&
         (iVar1 = *(int *)(lVar3 + 8) + -1, *(int *)(lVar3 + 8) = iVar1, iVar1 == 0)) {
        FUN_10128eea0();
      }
      *(long **)(param_1 + 0xa0) = plVar7;
    }
    else {
      uVar5 = (*(long *)(param_1 + 0x90) + *(long *)(param_1 + 0x88)) - 1;
      puVar6 = (undefined8 *)
               (*(long *)(*(long *)(param_1 + 0x70) + (uVar5 / 0x66) * 8) + (uVar5 % 0x66) * 0x28);
      plVar9 = (long *)*puVar6;
      iVar1 = *(int *)(puVar6 + 3);
      if (iVar1 == -3) {
        uVar2 = (**(code **)(*plVar9 + 0xd0))(plVar9);
        uVar4 = 0x80000000;
      }
      else {
        if (iVar1 != -1) {
          if (iVar1 == 0) {
            (**(code **)(*plVar9 + 0xb8))(plVar9,plVar7,&local_50);
          }
          goto LAB_10152db14;
        }
        uVar2 = (**(code **)(*plVar9 + 0xd0))(plVar9);
        uVar4 = uStack_3c;
      }
      (**(code **)(*plVar9 + 0x120))(plVar9,plVar7,uVar2,uVar4);
    }
  }
LAB_10152db14:
  if ((local_50 != (int *)0x0) && (iVar1 = *local_50, *local_50 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_101449efc();
  }
  if ((plVar7 != (long *)0x0) &&
     (iVar1 = (int)plVar7[1] + -1, *(int *)(plVar7 + 1) = iVar1, iVar1 == 0)) {
    FUN_10128eea0();
  }
  return;
}

