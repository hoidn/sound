
/* WARNING: Removing unreachable block (ram,0x000101516240) */
/* WARNING: Removing unreachable block (ram,0x000101516250) */
/* WARNING: Removing unreachable block (ram,0x0001015162ec) */
/* WARNING: Removing unreachable block (ram,0x0001015162fc) */

void FUN_101516204(undefined4 *param_1,undefined8 param_2)

{
  long *****ppppplVar1;
  long lVar2;
  long lVar3;
  long lVar4;
  long lVar5;
  uint uVar6;
  long ****pppplVar7;
  int iVar8;
  long *****ppppplVar9;
  long ****pppplVar10;
  long *plVar11;
  undefined8 uVar12;
  long lVar13;
  char *pcVar14;
  ulong uVar15;
  int *local_88;
  undefined4 local_80;
  long ****local_78;
  uint local_70;
  byte local_61;
  
  FUN_101463eb4(&local_78);
  pppplVar7 = local_78;
  (*(code *)(*local_78)[0x13])(local_78,param_2);
  (*(code *)(*local_78)[0x14])(local_78,0x17,1);
  (*(code *)(*local_78)[0xd])(local_78,1);
  ppppplVar9 = (long *****)FUN_1012d9850(0x60);
  FUN_10128ed98();
  *ppppplVar9 = (long ****)&PTR_thunk_FUN_101520a20_106676580;
  *(int *)(ppppplVar9 + 3) = 0;
  ppppplVar9[5] = (long ****)0x0;
  ppppplVar9[4] = (long ****)0x0;
  ppppplVar9[7] = (long ****)0x0;
  ppppplVar9[6] = (long ****)0x0;
  ppppplVar9[9] = (long ****)0x0;
  ppppplVar9[8] = (long ****)0x0;
  ((int *)((long)ppppplVar9 + 0x54))[0] = 0;
  ((int *)((long)ppppplVar9 + 0x54))[1] = 0;
  ((int *)((long)ppppplVar9 + 0x4c))[0] = 0;
  ((int *)((long)ppppplVar9 + 0x4c))[1] = 0;
  *(undefined2 *)((long)ppppplVar9 + 0x5c) = 1;
  *(int *)(ppppplVar9 + 1) = *(int *)(ppppplVar9 + 1) + 1;
  if (local_78 != (long ****)0x0) {
    *(int *)(local_78 + 1) = *(int *)(local_78 + 1) + 1;
  }
  pppplVar10 = ppppplVar9[10];
  local_78 = (long ****)ppppplVar9;
  if ((pppplVar10 != (long ****)0x0) &&
     (iVar8 = *(int *)(pppplVar10 + 1), *(int *)(pppplVar10 + 1) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  ppppplVar9[10] = pppplVar7;
  (*(code *)(*ppppplVar9)[7])(ppppplVar9,"<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
  *(int *)(ppppplVar9 + 3) = 1;
  FUN_101427680(&local_78,"AbletonSchema");
  FUN_1015170e0(ppppplVar9,&local_78);
  if (((long *****)local_78 != (long *****)0x0) &&
     (iVar8 = *(int *)local_78, *(int *)local_78 = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_101449efc();
  }
  (*(code *)(*ppppplVar9)[7])(ppppplVar9," ");
  (*(code *)(*ppppplVar9)[7])(ppppplVar9,"Version");
  FUN_1011bfe14(&local_78,5,"=%c");
  (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
  *(int *)(ppppplVar9 + 3) = 4;
  FUN_101520b2c(ppppplVar9,5);
  FUN_1011bfe14(&local_78,5,"%c");
  (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
  *(int *)(ppppplVar9 + 3) = 2;
  (*(code *)(*ppppplVar9)[7])(ppppplVar9," ");
  (*(code *)(*ppppplVar9)[7])(ppppplVar9,"TranslatorNumber");
  FUN_1011bfe14(&local_78,5,"=%c");
  (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
  *(int *)(ppppplVar9 + 3) = 4;
  FUN_101520b2c(ppppplVar9,*param_1);
  FUN_1011bfe14(&local_78,5,"%c");
  (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
  *(int *)(ppppplVar9 + 3) = 2;
  if (0 < (int)param_1[1]) {
    (*(code *)(*ppppplVar9)[7])(ppppplVar9," ");
    (*(code *)(*ppppplVar9)[7])(ppppplVar9,"ChangeCount");
    FUN_1011bfe14(&local_78,5,"=%c");
    (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
    *(int *)(ppppplVar9 + 3) = 4;
    FUN_101520b2c(ppppplVar9,param_1[1]);
    FUN_1011bfe14(&local_78,5,"%c");
    (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
    *(int *)(ppppplVar9 + 3) = 2;
  }
  lVar4 = *(long *)(param_1 + 4);
  for (lVar2 = *(long *)(param_1 + 2); lVar2 != lVar4; lVar2 = lVar2 + 0x38) {
    plVar11 = (long *)FUN_1014812dc(lVar2);
    if ((*plVar11 == 0) || ((*(uint *)(*plVar11 + 4) & 0xfffffffe) != 2)) {
      uVar12 = FUN_1014812dc(lVar2);
      FUN_1015170e0(ppppplVar9,uVar12);
      FUN_1014812d8(lVar2);
      uVar12 = FUN_10120e26c();
      FUN_101517404(ppppplVar9,"InternalName",uVar12);
    }
    else {
      FUN_1014812d8(lVar2);
      uVar12 = FUN_10120e26c();
      FUN_1015170e0(ppppplVar9,uVar12);
    }
    plVar11 = (long *)FUN_1014812d0(lVar2);
    lVar5 = plVar11[1];
    for (lVar3 = *plVar11; lVar3 != lVar5; lVar3 = lVar3 + 0x38) {
      plVar11 = (long *)FUN_1014810d0(lVar3);
      if ((*plVar11 == 0) || ((*(uint *)(*plVar11 + 4) & 0xfffffffe) != 2)) {
        uVar12 = FUN_1014810d0(lVar3);
      }
      else {
        uVar12 = FUN_1014810cc(lVar3);
      }
      FUN_1015170e0(ppppplVar9,uVar12);
      FUN_1014810d8(lVar3);
      uVar12 = FUN_10120e26c();
      FUN_101449838(&local_88);
      local_80 = 0;
      FUN_101522b50(&local_88,uVar12);
      (*(code *)(*ppppplVar9)[7])(ppppplVar9," ");
      (*(code *)(*ppppplVar9)[7])(ppppplVar9,"Class");
      FUN_1011bfe14(&local_78,5,"=%c");
      (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
      *(int *)(ppppplVar9 + 3) = 4;
      pppplVar10 = ppppplVar9[10];
      iVar8 = FUN_101208c60(&local_88);
      if (0 < iVar8) {
        uVar12 = FUN_101208db4(&local_88);
        lVar13 = FUN_101208db4(&local_88);
        iVar8 = FUN_101208c60(&local_88);
        FUN_103f484cc(&local_78,uVar12,lVar13 + (long)iVar8 * 2);
        ppppplVar1 = (long *****)local_78;
        uVar6 = local_70;
        if (-1 < (char)local_61) {
          ppppplVar1 = &local_78;
          uVar6 = (uint)local_61;
        }
        FUN_1014337f8(pppplVar10,ppppplVar1,uVar6);
        if ((char)local_61 < '\0') {
          operator_delete(local_78);
        }
      }
      FUN_1011bfe14(&local_78,5,"%c");
      (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
      *(int *)(ppppplVar9 + 3) = 2;
      if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0))
      {
        FUN_101449efc();
      }
      uVar12 = FUN_1014810e8(lVar3);
      (*(code *)(*ppppplVar9)[7])(ppppplVar9," ");
      (*(code *)(*ppppplVar9)[7])(ppppplVar9,"Type");
      FUN_1011bfe14(&local_78,5,"=%c");
      (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
      *(int *)(ppppplVar9 + 3) = 4;
      FUN_101520b2c(ppppplVar9,uVar12);
      FUN_1011bfe14(&local_78,5,"%c");
      (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
      *(int *)(ppppplVar9 + 3) = 2;
      iVar8 = FUN_1014810e8(lVar3);
      if (iVar8 == -3) {
        FUN_1014810e0(lVar3);
        uVar12 = FUN_10120e26c();
        FUN_101449838(&local_88);
        local_80 = 0;
        FUN_101522b50(&local_88,uVar12);
        (*(code *)(*ppppplVar9)[7])(ppppplVar9," ");
        (*(code *)(*ppppplVar9)[7])(ppppplVar9,"ArrayTranslator");
        FUN_1011bfe14(&local_78,5,"=%c");
        (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
        *(int *)(ppppplVar9 + 3) = 4;
        pppplVar10 = ppppplVar9[10];
        iVar8 = FUN_101208c60(&local_88);
        if (0 < iVar8) {
          uVar12 = FUN_101208db4(&local_88);
          lVar13 = FUN_101208db4(&local_88);
          iVar8 = FUN_101208c60(&local_88);
          FUN_103f484cc(&local_78,uVar12,lVar13 + (long)iVar8 * 2);
          ppppplVar1 = (long *****)local_78;
          uVar6 = local_70;
          if (-1 < (char)local_61) {
            ppppplVar1 = &local_78;
            uVar6 = (uint)local_61;
          }
          FUN_1014337f8(pppplVar10,ppppplVar1,uVar6);
          if ((char)local_61 < '\0') {
            operator_delete(local_78);
          }
        }
        FUN_1011bfe14(&local_78,5,"%c");
        (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
        *(int *)(ppppplVar9 + 3) = 2;
        if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)
           ) {
          FUN_101449efc();
        }
      }
      plVar11 = (long *)FUN_1014810d0(lVar3);
      if ((*plVar11 == 0) || ((*(uint *)(*plVar11 + 4) & 0xfffffffe) != 2)) {
        uVar12 = FUN_1014810cc(lVar3);
        FUN_101449838(&local_88);
        local_80 = 0;
        FUN_101522b50(&local_88,uVar12);
        (*(code *)(*ppppplVar9)[7])(ppppplVar9," ");
        (*(code *)(*ppppplVar9)[7])(ppppplVar9,"InternalName");
        FUN_1011bfe14(&local_78,5,"=%c");
        (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
        *(int *)(ppppplVar9 + 3) = 4;
        pppplVar10 = ppppplVar9[10];
        iVar8 = FUN_101208c60(&local_88);
        if (0 < iVar8) {
          uVar12 = FUN_101208db4(&local_88);
          lVar13 = FUN_101208db4(&local_88);
          iVar8 = FUN_101208c60(&local_88);
          FUN_103f484cc(&local_78,uVar12,lVar13 + (long)iVar8 * 2);
          ppppplVar1 = (long *****)local_78;
          uVar6 = local_70;
          if (-1 < (char)local_61) {
            ppppplVar1 = &local_78;
            uVar6 = (uint)local_61;
          }
          FUN_1014337f8(pppplVar10,ppppplVar1,uVar6);
          if ((char)local_61 < '\0') {
            operator_delete(local_78);
          }
        }
        FUN_1011bfe14(&local_78,5,"%c");
        (*(code *)(*ppppplVar9)[7])(ppppplVar9,&local_78);
        *(int *)(ppppplVar9 + 3) = 2;
        if ((local_88 != (int *)0x0) && (iVar8 = *local_88, *local_88 = iVar8 + -1, iVar8 + -1 == 0)
           ) {
          FUN_101449efc();
        }
      }
      *(int *)(ppppplVar9 + 0xb) = *(int *)(ppppplVar9 + 0xb) + -1;
      pppplVar10 = *ppppplVar9;
      if (*(int *)(ppppplVar9 + 3) == 2) {
        pcVar14 = " />";
      }
      else {
        (*(code *)pppplVar10[5])(ppppplVar9);
        (*(code *)(*ppppplVar9)[8])(ppppplVar9);
        (*(code *)(*ppppplVar9)[7])(ppppplVar9,"</");
        uVar15 = ((long)ppppplVar9[9] + (long)ppppplVar9[8]) - 1;
        (*(code *)(*ppppplVar9)[6])
                  (ppppplVar9,
                   *(long *)((long)ppppplVar9[5] + (uVar15 >> 6 & 0x3fffffffffffff8)) +
                   (uVar15 & 0x1ff) * 8);
        pppplVar10 = *ppppplVar9;
        pcVar14 = ">";
      }
      (*(code *)pppplVar10[7])(ppppplVar9,pcVar14);
      FUN_101462cec(ppppplVar9 + 4);
      iVar8 = 5;
      if (ppppplVar9[9] != (long ****)0x0) {
        iVar8 = 3;
      }
      *(int *)(ppppplVar9 + 3) = iVar8;
    }
    *(int *)(ppppplVar9 + 0xb) = *(int *)(ppppplVar9 + 0xb) + -1;
    pppplVar10 = *ppppplVar9;
    if (*(int *)(ppppplVar9 + 3) == 2) {
      pcVar14 = " />";
    }
    else {
      (*(code *)pppplVar10[5])(ppppplVar9);
      (*(code *)(*ppppplVar9)[8])(ppppplVar9);
      (*(code *)(*ppppplVar9)[7])(ppppplVar9,"</");
      uVar15 = ((long)ppppplVar9[9] + (long)ppppplVar9[8]) - 1;
      (*(code *)(*ppppplVar9)[6])
                (ppppplVar9,
                 *(long *)((long)ppppplVar9[5] + (uVar15 >> 6 & 0x3fffffffffffff8)) +
                 (uVar15 & 0x1ff) * 8);
      pppplVar10 = *ppppplVar9;
      pcVar14 = ">";
    }
    (*(code *)pppplVar10[7])(ppppplVar9,pcVar14);
    FUN_101462cec(ppppplVar9 + 4);
    iVar8 = 5;
    if (ppppplVar9[9] != (long ****)0x0) {
      iVar8 = 3;
    }
    *(int *)(ppppplVar9 + 3) = iVar8;
  }
  *(int *)(ppppplVar9 + 0xb) = *(int *)(ppppplVar9 + 0xb) + -1;
  pppplVar10 = *ppppplVar9;
  if (*(int *)(ppppplVar9 + 3) == 2) {
    pcVar14 = " />";
  }
  else {
    (*(code *)pppplVar10[5])(ppppplVar9);
    (*(code *)(*ppppplVar9)[8])(ppppplVar9);
    (*(code *)(*ppppplVar9)[7])(ppppplVar9,"</");
    uVar15 = ((long)ppppplVar9[9] + (long)ppppplVar9[8]) - 1;
    (*(code *)(*ppppplVar9)[6])
              (ppppplVar9,
               *(long *)((long)ppppplVar9[5] + (uVar15 >> 6 & 0x3fffffffffffff8)) +
               (uVar15 & 0x1ff) * 8);
    pppplVar10 = *ppppplVar9;
    pcVar14 = ">";
  }
  (*(code *)pppplVar10[7])(ppppplVar9,pcVar14);
  FUN_101462cec(ppppplVar9 + 4);
  iVar8 = 5;
  if (ppppplVar9[9] != (long ****)0x0) {
    iVar8 = 3;
  }
  *(int *)(ppppplVar9 + 3) = iVar8;
  (*(code *)(*ppppplVar9)[5])(ppppplVar9);
  *(int *)(ppppplVar9 + 3) = 0;
  (*(code *)(*pppplVar7)[0xe])();
  if (((ppppplVar9 != (long *****)0x0) &&
      ((*(code *)(*ppppplVar9)[3])(), ppppplVar9 != (long *****)0x0)) &&
     (iVar8 = *(int *)(ppppplVar9 + 1), *(int *)(ppppplVar9 + 1) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  if (((pppplVar7 != (long ****)0x0) && ((*(code *)(*pppplVar7)[3])(), pppplVar7 != (long ****)0x0))
     && (iVar8 = *(int *)(pppplVar7 + 1), *(int *)(pppplVar7 + 1) = iVar8 + -1, iVar8 + -1 == 0)) {
    FUN_10128eea0();
  }
  return;
}

