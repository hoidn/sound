
void FUN_1015299e0(long *param_1,undefined8 *param_2,undefined4 *param_3)

{
  byte bVar1;
  int iVar2;
  undefined4 uVar3;
  undefined8 *puVar4;
  long lVar5;
  int **ppiVar6;
  undefined8 uVar7;
  ulong uVar8;
  long lVar9;
  long lVar10;
  undefined1 auStack_88 [8];
  undefined1 auStack_80 [8];
  undefined1 auStack_78 [8];
  undefined1 auStack_70 [8];
  int *local_68;
  int **local_60;
  undefined *puStack_58;
  
  FUN_1011b5224();
  if (param_1[0x12] != 0) {
    uVar8 = (param_1[0x12] + param_1[0x11]) - 1;
    lVar9 = *(long *)(param_1[0xe] + (uVar8 / 0x66) * 8) + (uVar8 % 0x66) * 0x28;
    if (*(char *)(lVar9 + 0x22) == '\x01') {
      lVar9 = FUN_101532de0(param_1 + 0xd);
      *(undefined8 *)(lVar9 + 0x10) = 0;
      *(undefined4 *)(lVar9 + 0x1c) = 0x80000000;
      *(undefined2 *)(lVar9 + 0x20) = 0;
      *(undefined1 *)(lVar9 + 0x22) = 1;
      return;
    }
    iVar2 = *(int *)(lVar9 + 0x18);
    if (iVar2 == -3) {
      FUN_10152a28c(&local_60,param_2);
      FUN_10152a570(param_1,&local_60,param_3,0);
      if (local_60 == (int **)0x0) {
        return;
      }
      iVar2 = *(int *)local_60;
      *(int *)local_60 = iVar2 + -1;
      if (iVar2 + -1 != 0) {
        return;
      }
      FUN_101449efc();
      return;
    }
    if (iVar2 != -1) {
      if (iVar2 == -4) {
        uVar7 = ___cxa_allocate_exception(0x30);
        FUN_101447188(&local_60,&DAT_106e0cc01,"Base types can\'t have children");
        FUN_1011cb734(&local_68);
        FUN_1011cb734(auStack_70);
        FUN_1011cb734(auStack_78);
        FUN_1011cb734(auStack_80);
        FUN_1011cb734(auStack_88);
        FUN_101242ce8(uVar7,&local_60,&local_68,auStack_70,auStack_78,auStack_80,auStack_88);
                    /* WARNING: Subroutine does not return */
        ___cxa_throw(uVar7,&PTR_vtable_106661270,FUN_10124335c);
      }
      FUN_10152a28c(&local_60,param_2);
      FUN_10152957c(&local_68,&local_60);
      if ((local_60 != (int **)0x0) &&
         (iVar2 = *(int *)local_60, *(int *)local_60 = iVar2 + -1, iVar2 + -1 == 0)) {
        FUN_101449efc();
      }
      uVar8 = (param_1[0x12] + param_1[0x11]) - 1;
      puVar4 = (undefined8 *)
               FUN_1014812d0(*(undefined8 *)
                              (*(long *)(param_1[0xe] + (uVar8 / 0x66) * 8) + (uVar8 % 0x66) * 0x28
                              + 0x10));
      lVar9 = FUN_10152ac0c(*puVar4,puVar4[1],&local_68);
      if ((((char)param_1[0x19] == '\x01') && (puVar4[1] == lVar9)) &&
         (lVar5 = param_1[8], iVar2 = FUN_1015147cc(param_1[0x16]), (int)lVar5 == iVar2)) {
        local_60 = &local_68;
        puStack_58 = PTR_format_custom<TString>_106509e70;
        FUN_10143e88c(auStack_70,L"Unexpected node \'{}\'",0x14,0xf,&local_60);
        FUN_101453aac(&local_60,auStack_70);
        FUN_1014528e4(&local_60);
        FUN_100234444(&local_60);
        FUN_100234444(auStack_70);
      }
      lVar5 = FUN_101532de0(param_1 + 0xd);
      *(undefined8 *)(lVar5 + 0x10) = 0;
      *(undefined4 *)(lVar5 + 0x1c) = 0x80000000;
      *(undefined2 *)(lVar5 + 0x20) = 0;
      lVar10 = puVar4[1];
      *(bool *)(lVar5 + 0x22) = lVar10 == lVar9;
      if (lVar10 != lVar9) {
        FUN_10152adb0(param_1,lVar5,lVar9,param_3);
      }
      if (local_68 == (int *)0x0) {
        return;
      }
      iVar2 = *local_68;
      *local_68 = iVar2 + -1;
      if (iVar2 + -1 != 0) {
        return;
      }
      FUN_101449efc();
      return;
    }
    FUN_10152a28c(&local_60,param_2);
    uVar8 = (param_1[0x12] + param_1[0x11]) - 1;
    FUN_10152a570(param_1,&local_60,param_3,
                  *(long *)(param_1[0xe] + (uVar8 / 0x66) * 8) + (uVar8 % 0x66) * 0x28);
    if (local_60 == (int **)0x0) {
      return;
    }
    iVar2 = *(int *)local_60;
    *(int *)local_60 = iVar2 + -1;
    if (iVar2 + -1 != 0) {
      return;
    }
    FUN_101449efc();
    return;
  }
  if ((char)param_1[0x13] != '\x01') {
    if ((*(int *)(param_2 + 1) != 7) ||
       (*(int *)*param_2 != 0x656c6241 || *(int *)((long)*param_2 + 3) != 0x6e6f7465)) {
      uVar7 = ___cxa_allocate_exception(0x30);
      FUN_101447188(&local_60,&DAT_106e0cc01,"Expected \'Ableton\' root node, got \'$1\' instead");
      FUN_101432520(&local_68,*param_2,*(undefined4 *)(param_2 + 1));
      FUN_1011cb734(auStack_70);
      FUN_1011cb734(auStack_78);
      FUN_1011cb734(auStack_80);
      FUN_1011cb734(auStack_88);
      FUN_101242ce8(uVar7,&local_60,&local_68,auStack_70,auStack_78,auStack_80,auStack_88);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(uVar7,&PTR_vtable_106661270,FUN_10124335c);
    }
    uVar3 = FUN_10152a900(*param_3,*(undefined8 *)(param_3 + 2),"MajorVersion");
    *(undefined4 *)((long)param_1 + 0xbc) = uVar3;
    FUN_1011cb734(&local_68);
    FUN_10152ab04(&local_60,*param_3,*(undefined8 *)(param_3 + 2),"MinorVersion",local_68);
    ppiVar6 = (int **)param_1[0x18];
    param_1[0x18] = (long)local_60;
    local_60 = ppiVar6;
    if ((ppiVar6 != (int **)0x0) &&
       (iVar2 = *(int *)ppiVar6, *(int *)ppiVar6 = iVar2 + -1, iVar2 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((local_68 != (int *)0x0) && (iVar2 = *local_68, *local_68 = iVar2 + -1, iVar2 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((char)param_1[0x17] == '\x01') {
      (**(code **)(*param_1 + 0x50))(param_1);
      return;
    }
    uVar3 = FUN_10152a900(*param_3,*(undefined8 *)(param_3 + 2),"SchemaChangeCount");
    *(undefined4 *)(param_1 + 8) = uVar3;
    FUN_1011cb734(&local_68);
    FUN_10152ab04(&local_60,*param_3,*(undefined8 *)(param_3 + 2),"Creator",local_68);
    ppiVar6 = (int **)param_1[9];
    param_1[9] = (long)local_60;
    local_60 = ppiVar6;
    if ((ppiVar6 != (int **)0x0) &&
       (iVar2 = *(int *)ppiVar6, *(int *)ppiVar6 = iVar2 + -1, iVar2 + -1 == 0)) {
      FUN_101449efc();
    }
    if ((local_68 != (int *)0x0) && (iVar2 = *local_68, *local_68 = iVar2 + -1, iVar2 + -1 == 0)) {
      FUN_101449efc();
    }
    *(undefined1 *)(param_1 + 0x13) = 1;
    return;
  }
  if (param_1[0x14] != 0) {
    uVar7 = ___cxa_allocate_exception(0x30);
    FUN_101447188(&local_60,&DAT_106e0cc01,"More than one document in one stream");
    FUN_1011cb734(&local_68);
    FUN_1011cb734(auStack_70);
    FUN_1011cb734(auStack_78);
    FUN_1011cb734(auStack_80);
    FUN_1011cb734(auStack_88);
    FUN_101242ce8(uVar7,&local_60,&local_68,auStack_70,auStack_78,auStack_80,auStack_88);
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar7,&PTR_vtable_106661270,FUN_10124335c);
  }
  FUN_10152a28c(&local_60,param_2);
  lVar9 = FUN_10147fcc0(&local_60);
  if (lVar9 == 0) {
    *(undefined1 *)(param_1 + 0x19) = 1;
    *(undefined1 *)((long)param_1 + 0x61) = 1;
  }
  else {
    bVar1 = FUN_10147fdbc();
    *(byte *)(param_1 + 0x19) = bVar1;
    *(byte *)((long)param_1 + 0x61) = bVar1;
    if ((bVar1 & 1) == 0) goto LAB_101529e8c;
  }
  FUN_101529024(param_1);
LAB_101529e8c:
  FUN_10152a570(param_1,&local_60,param_3,0);
  if ((local_60 != (int **)0x0) &&
     (iVar2 = *(int *)local_60, *(int *)local_60 = iVar2 + -1, iVar2 + -1 == 0)) {
    FUN_101449efc();
  }
  return;
}

