
void FUN_101472624(long *param_1,long *param_2,undefined8 *param_3)

{
  code *pcVar1;
  int iVar2;
  long *plVar3;
  undefined8 uVar4;
  int *piVar5;
  long lVar6;
  long *plVar7;
  undefined1 auStack_58 [8];
  undefined8 local_50;
  undefined *puStack_48;
  undefined8 *local_40;
  undefined *puStack_38;
  
  iVar2 = (**(code **)(*param_1 + 0x78))(param_1,param_3);
  if (iVar2 == 0) {
    plVar3 = (long *)FUN_101479028(DAT_106f4f5f0 + 0x640);
    *plVar3 = 0;
    plVar3[1] = 0;
    piVar5 = (int *)*param_3;
    plVar3[2] = (long)piVar5;
    if (piVar5 != (int *)0x0) {
      *piVar5 = *piVar5 + 1;
    }
    *(undefined4 *)(plVar3 + 3) = 0;
    plVar3[4] = (long)param_2;
    if (param_2 != (long *)0x0) {
      *(int *)(param_2 + 1) = (int)param_2[1] + 1;
    }
    plVar7 = param_1 + 5;
    lVar6 = *plVar7;
    *plVar3 = lVar6;
    plVar3[1] = (long)plVar7;
    *(long **)(lVar6 + 8) = plVar3;
    *plVar7 = (long)plVar3;
    param_1[7] = param_1[7] + 1;
    uVar4 = (**(code **)(*param_2 + 0x28))(param_2);
    FUN_101479ec4(&DAT_106f4f618,uVar4,uVar4);
    return;
  }
  (**(code **)(*param_1 + 0x28))(param_1);
  local_50 = FUN_10120e26c();
  puStack_48 = PTR_format_custom<TString>_106509e70;
  puStack_38 = PTR_format_custom<TString>_106509e70;
  local_40 = param_3;
  FUN_10143e88c(auStack_58,L"Class {} already has member {}",0x1e,0xff,&local_50);
  FUN_10146d168(param_1,auStack_58);
                    /* WARNING: Does not return */
  pcVar1 = (code *)SoftwareBreakpoint(1,0x10147273c);
  (*pcVar1)();
}

