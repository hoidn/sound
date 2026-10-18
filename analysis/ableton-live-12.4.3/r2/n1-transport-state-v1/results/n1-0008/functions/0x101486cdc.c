
void FUN_101486cdc(long *param_1,undefined8 param_2)

{
  long lVar1;
  uint uVar2;
  int iVar3;
  long lVar4;
  ulong uVar5;
  long *plVar6;
  long *plVar7;
  long lVar8;
  
  FUN_1011b5224();
  (**(code **)(*param_1 + 0xd8))(param_1);
  lVar4 = (**(code **)(*param_1 + 0x170))(param_1);
  lVar1 = lVar4 + 0x50;
  lVar8 = *(long *)(lVar4 + 0x68);
  if (lVar8 != lVar1) {
    do {
      if ((*(byte *)(lVar8 + 0x74) >> 2 & 1) != 0) {
        plVar7 = param_1;
        if (-1 < (int)*(uint *)(lVar8 + 0x30)) {
          plVar7 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar8 + 0x30));
        }
        uVar5 = (**(code **)(*param_1 + 0x150))(param_1,(long)plVar7 + (long)*(int *)(lVar8 + 0x38))
        ;
        if ((uVar5 & 1) == 0) {
          plVar7 = param_1;
          if (-1 < (int)*(uint *)(lVar8 + 0x30)) {
            plVar7 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar8 + 0x30));
          }
          FUN_10152205c(param_2,lVar8 + 0x40,(long)plVar7 + (long)*(int *)(lVar8 + 0x38),
                        lVar8 + 0x50);
        }
      }
      lVar8 = *(long *)(lVar8 + 0x18);
    } while (lVar8 != lVar1);
    lVar8 = *(long *)(lVar4 + 0x68);
  }
  do {
    if (lVar8 == lVar1) {
                    /* WARNING: Could not recover jumptable at 0x000101486f04. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(*param_1 + 0xe0))(param_1);
      return;
    }
    if ((*(byte *)(lVar8 + 0x74) & 6) == 0) {
      uVar5 = FUN_10120e310(lVar8 + 0x50);
      if ((uVar5 & 1) == 0) {
        plVar7 = param_1;
        if (-1 < (int)*(uint *)(lVar8 + 0x30)) {
          plVar7 = *(long **)((long)param_1 + (ulong)*(uint *)(lVar8 + 0x30));
        }
        uVar5 = (**(code **)(**(long **)((long)plVar7 + (long)*(int *)(lVar8 + 0x38) + 8) + 0x148))
                          ();
        if ((uVar5 & 1) != 0) goto LAB_101486dcc;
      }
      iVar3 = FUN_10120e310(lVar8 + 0x50);
      uVar2 = *(uint *)(lVar8 + 0x30);
      if (iVar3 == 0) {
        plVar7 = param_1;
        if (-1 < (int)uVar2) {
          plVar7 = *(long **)((long)param_1 + (ulong)uVar2);
        }
        uVar5 = (**(code **)(*param_1 + 0x150))
                          (param_1,*(undefined8 *)((long)plVar7 + (long)*(int *)(lVar8 + 0x38) + 8))
        ;
      }
      else {
        plVar7 = param_1;
        if (-1 < (int)uVar2) {
          plVar7 = *(long **)((long)param_1 + (ulong)uVar2);
        }
        uVar5 = (**(code **)(*param_1 + 0x150))(param_1,(long)plVar7 + (long)*(int *)(lVar8 + 0x38))
        ;
      }
      if ((uVar5 & 1) == 0) {
        plVar6 = (long *)(lVar8 + 0x48);
        plVar7 = plVar6;
        if ((*plVar6 != 0) &&
           (plVar7 = (long *)(lVar8 + 0x40), (*(uint *)(*plVar6 + 4) & 0xfffffffe) != 2)) {
          plVar7 = plVar6;
        }
        FUN_1015170e0(param_2,plVar7);
        iVar3 = FUN_10120e310(lVar8 + 0x50);
        uVar2 = *(uint *)(lVar8 + 0x30);
        if (iVar3 == 0) {
          plVar7 = param_1;
          if (-1 < (int)uVar2) {
            plVar7 = *(long **)((long)param_1 + (ulong)uVar2);
          }
          plVar7 = *(long **)((long)plVar7 + (long)*(int *)(lVar8 + 0x38) + 8);
          (**(code **)(*plVar7 + 0x138))(plVar7,param_2);
        }
        else {
          plVar7 = param_1;
          if (-1 < (int)uVar2) {
            plVar7 = *(long **)((long)param_1 + (ulong)uVar2);
          }
          FUN_101521750(param_2,(long)plVar7 + (long)*(int *)(lVar8 + 0x38),lVar8 + 0x50);
        }
        FUN_10151752c(param_2);
      }
    }
LAB_101486dcc:
    lVar8 = *(long *)(lVar8 + 0x18);
  } while( true );
}

