
void FUN_101472750(long *param_1,undefined8 param_2)

{
  long *plVar1;
  int iVar2;
  code *pcVar3;
  ulong uVar4;
  long lVar5;
  int *piVar6;
  long *plVar7;
  int aiStack_70 [2];
  undefined1 auStack_68 [8];
  int *local_60;
  undefined *puStack_58;
  undefined8 local_50;
  undefined *puStack_48;
  
  plVar1 = param_1 + 5;
  plVar7 = (long *)param_1[6];
  if (plVar7 == plVar1) {
LAB_101472834:
    if (plVar7 != plVar1) {
      lVar5 = *plVar7;
      plVar1 = (long *)plVar7[1];
      *(long **)(lVar5 + 8) = plVar1;
      *plVar1 = lVar5;
      param_1[7] = param_1[7] + -1;
      lVar5 = plVar7[4];
      if (lVar5 != 0) {
        iVar2 = *(int *)(lVar5 + 8) + -1;
        *(int *)(lVar5 + 8) = iVar2;
        if (iVar2 == 0) {
          FUN_10128eea0();
        }
      }
      piVar6 = (int *)plVar7[2];
      if (piVar6 != (int *)0x0) {
        iVar2 = *piVar6;
        *piVar6 = iVar2 + -1;
        if (iVar2 + -1 == 0) {
          FUN_101449efc();
        }
      }
      lVar5 = DAT_106f4f5f0;
      *plVar7 = *(long *)(DAT_106f4f5f0 + 0x648);
      *(long **)(lVar5 + 0x648) = plVar7;
      return;
    }
  }
  else {
    do {
      local_60 = (int *)plVar7[2];
      if (local_60 != (int *)0x0) {
        *local_60 = *local_60 + 1;
      }
      uVar4 = FUN_1014289f4(&local_60,param_2);
      if (local_60 != (int *)0x0) {
        iVar2 = *local_60;
        *local_60 = iVar2 + -1;
        if (iVar2 + -1 == 0) {
          FUN_101449efc();
        }
      }
      if ((uVar4 & 1) != 0) goto LAB_101472834;
      plVar7 = (long *)plVar7[1];
    } while (plVar7 != plVar1);
  }
  FUN_101427680(aiStack_70,param_2);
  (**(code **)(*param_1 + 0x28))(param_1);
  local_50 = FUN_10120e26c();
  puStack_58 = PTR_format_custom<TString>_106509e70;
  puStack_48 = PTR_format_custom<TString>_106509e70;
  local_60 = aiStack_70;
  FUN_10143e88c(auStack_68,L"Member \"{}\" of Class {} is missing",0x22,0xff,&local_60);
  FUN_10146d168(param_1,auStack_68);
                    /* WARNING: Does not return */
  pcVar3 = (code *)SoftwareBreakpoint(1,0x101472834);
  (*pcVar3)();
}

