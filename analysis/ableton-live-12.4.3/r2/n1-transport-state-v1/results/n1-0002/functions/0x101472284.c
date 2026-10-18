
long FUN_101472284(long *param_1,long *param_2)

{
  int iVar1;
  code *pcVar2;
  bool bVar3;
  int *piVar4;
  long lVar5;
  int *piVar6;
  long lVar7;
  short *psVar8;
  long *plVar9;
  undefined1 auStack_68 [8];
  long *local_60;
  undefined *puStack_58;
  undefined8 local_50;
  undefined *puStack_48;
  
  plVar9 = (long *)param_1[6];
  do {
    if (plVar9 == param_1 + 5) {
      (**(code **)(*param_1 + 0x28))(param_1);
      local_50 = FUN_10120e26c();
      puStack_58 = PTR_format_custom<TString>_106509e70;
      puStack_48 = PTR_format_custom<TString>_106509e70;
      local_60 = param_2;
      FUN_10143e88c(auStack_68,L"Member \"{}\" of Class {} is missing",0x22,0xff,&local_60);
      FUN_10146d168(param_1,auStack_68);
                    /* WARNING: Does not return */
      pcVar2 = (code *)SoftwareBreakpoint(1,0x1014723d0);
      (*pcVar2)();
    }
    piVar4 = (int *)plVar9[2];
    if (piVar4 == (int *)0x0) {
      lVar5 = -1;
      lVar7 = *param_2;
      if (lVar7 == 0) goto LAB_10147233c;
LAB_1014722e0:
      if (lVar5 == *(int *)(lVar7 + 4) / 2 + -1) goto LAB_1014722fc;
LAB_101472348:
      bVar3 = false;
    }
    else {
      *piVar4 = *piVar4 + 1;
      lVar5 = (long)(piVar4[1] / 2 + -1);
      lVar7 = *param_2;
      if (lVar7 != 0) goto LAB_1014722e0;
LAB_10147233c:
      if (lVar5 != -1) goto LAB_101472348;
LAB_1014722fc:
      if (lVar5 == 0) {
        bVar3 = true;
      }
      else {
        piVar6 = piVar4 + 4;
        psVar8 = (short *)(lVar7 + 0x10);
        do {
          lVar5 = lVar5 + -1;
          bVar3 = *psVar8 == (short)*piVar6;
          if (!bVar3) break;
          piVar6 = (int *)((long)piVar6 + 2);
          psVar8 = psVar8 + 1;
        } while (lVar5 != 0);
      }
    }
    if ((piVar4 != (int *)0x0) && (iVar1 = *piVar4, *piVar4 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_101449efc();
    }
    if (bVar3) {
      return plVar9[4];
    }
    plVar9 = (long *)plVar9[1];
  } while( true );
}

