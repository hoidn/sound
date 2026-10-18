
void FUN_10152b77c(long param_1,undefined8 *param_2,int *param_3,undefined8 *param_4)

{
  char *pcVar1;
  int iVar2;
  int iVar3;
  char *pcVar4;
  size_t sVar5;
  size_t sVar6;
  undefined8 *puVar7;
  ulong uVar8;
  undefined8 uVar9;
  int *piVar10;
  long lVar11;
  char *pcVar12;
  char *pcVar13;
  long lVar14;
  long *plVar15;
  long lVar16;
  int local_cc;
  undefined1 auStack_c0 [8];
  undefined1 auStack_b8 [8];
  undefined1 auStack_b0 [8];
  undefined1 auStack_a8 [8];
  undefined1 auStack_a0 [8];
  int *local_98 [3];
  char *local_80;
  int local_78;
  char *local_70;
  int local_68;
  
  pcVar4 = (char *)FUN_101489054();
  if (*param_3 < 1) {
    local_cc = -0x80000000;
  }
  else {
    lVar16 = 0;
    lVar14 = 0;
    pcVar1 = "";
    if (pcVar4 != (char *)0x0) {
      pcVar1 = pcVar4;
    }
    local_cc = -0x80000000;
    do {
      lVar11 = *(long *)(param_3 + 2);
      pcVar12 = *(char **)(lVar11 + lVar16);
      pcVar4 = "";
      if (pcVar12 != (char *)0x0) {
        pcVar4 = pcVar12;
      }
      sVar5 = _strlen(pcVar4);
      pcVar13 = (char *)((undefined8 *)(lVar11 + lVar16))[1];
      pcVar12 = "";
      if (pcVar13 != (char *)0x0) {
        pcVar12 = pcVar13;
      }
      sVar6 = _strlen(pcVar12);
      iVar2 = (int)sVar5;
      iVar3 = (int)sVar6;
      local_80 = pcVar4;
      local_78 = iVar2;
      local_70 = pcVar12;
      local_68 = iVar3;
      if ((param_4 == (undefined8 *)0x0) || ((*(byte *)(param_1 + 0x61) & 1) == 0)) {
LAB_10152b88c:
        puVar7 = (undefined8 *)FUN_1014812d0(param_2[2]);
        FUN_10152a28c(local_98,&local_80);
        lVar11 = FUN_10152ac0c(*puVar7,puVar7[1],local_98);
        if (local_98[0] != (int *)0x0) {
          iVar3 = *local_98[0];
          *local_98[0] = iVar3 + -1;
          if (iVar3 + -1 == 0) {
            FUN_101449efc();
          }
        }
        if ((*(char *)(param_1 + 200) == '\x01') && (puVar7[1] == lVar11)) {
          iVar3 = *(int *)(param_1 + 0x40);
          iVar2 = FUN_1015147cc(*(undefined8 *)(param_1 + 0xb0));
          if (iVar3 == iVar2) {
            uVar9 = ___cxa_allocate_exception(0x30);
            FUN_101447188(local_98,&DAT_106e0cc01,"Unknown attribute \'$1\'");
            FUN_10152a28c(auStack_a0,&local_80);
            FUN_1011cb734(auStack_a8);
            FUN_1011cb734(auStack_b0);
            FUN_1011cb734(auStack_b8);
            FUN_1011cb734(auStack_c0);
            FUN_101242ce8(uVar9,local_98,auStack_a0,auStack_a8,auStack_b0,auStack_b8,auStack_c0);
                    /* WARNING: Subroutine does not return */
            ___cxa_throw(uVar9,&PTR_vtable_106661270,FUN_10124335c);
          }
        }
        else {
          FUN_1014810d8(lVar11);
          uVar8 = FUN_10120e324();
          if ((uVar8 & 1) == 0) {
            uVar9 = ___cxa_allocate_exception(0x30);
            FUN_101447188(local_98,&DAT_106e0cc01,"Attribute value for non-base type: \'$1\'");
            FUN_101432520(auStack_a0,local_80,local_78);
            FUN_1011cb734(auStack_a8);
            FUN_1011cb734(auStack_b0);
            FUN_1011cb734(auStack_b8);
            FUN_1011cb734(auStack_c0);
            FUN_101242ce8(uVar9,local_98,auStack_a0,auStack_a8,auStack_b0,auStack_b8,auStack_c0);
                    /* WARNING: Subroutine does not return */
            ___cxa_throw(uVar9,&PTR_vtable_106661270,FUN_10124335c);
          }
          uVar9 = FUN_1014810d8(lVar11);
          piVar10 = (int *)FUN_10146cf50(0x30);
          thunk_FUN_101475120(piVar10,uVar9);
          if (piVar10 != (int *)0x0) {
            piVar10[2] = piVar10[2] + 1;
          }
          local_98[0] = piVar10;
          FUN_10152bfb8(piVar10,&local_70);
          plVar15 = (long *)*param_2;
          uVar9 = FUN_1014810cc(lVar11);
          (**(code **)(*plVar15 + 0xb8))(plVar15,piVar10,uVar9);
          if (piVar10 != (int *)0x0) {
            iVar3 = piVar10[2];
            piVar10[2] = iVar3 + -1;
            if (iVar3 + -1 == 0) {
              FUN_10128eea0(piVar10);
            }
          }
        }
      }
      else {
        sVar5 = _strlen(pcVar1);
        if ((iVar2 != (int)sVar5) || (iVar2 = _memcmp(pcVar4,pcVar1,(long)(int)sVar5), iVar2 != 0))
        goto LAB_10152b88c;
        uVar8 = FUN_1002fd908(pcVar12,(long)iVar3);
        local_cc = (int)uVar8;
        if ((uVar8 & 0x100000000) == 0) {
          local_cc = 0;
        }
        if ((local_cc < 0) || ((uVar8 & 0x100000000) == 0)) {
          uVar9 = ___cxa_allocate_exception(0x30);
          FUN_101447188(local_98,&DAT_106e0cc01,"Illegal value for \'Id\' attribute");
          FUN_1011cb734(auStack_a0);
          FUN_1011cb734(auStack_a8);
          FUN_1011cb734(auStack_b0);
          FUN_1011cb734(auStack_b8);
          FUN_1011cb734(auStack_c0);
          FUN_101242ce8(uVar9,local_98,auStack_a0,auStack_a8,auStack_b0,auStack_b8,auStack_c0);
                    /* WARNING: Subroutine does not return */
          ___cxa_throw(uVar9,&PTR_vtable_106661270,FUN_10124335c);
        }
      }
      lVar14 = lVar14 + 1;
      lVar16 = lVar16 + 0x10;
    } while (lVar14 < *param_3);
  }
  if (param_4 != (undefined8 *)0x0) {
    if (*(int *)(param_1 + 0xbc) < 5) {
      iVar3 = (**(code **)(*(long *)*param_4 + 0xd0))();
      if (iVar3 == 0) {
        *(bool *)(param_4 + 4) = local_cc != -0x80000000;
      }
      else if ((bool)*(char *)(param_4 + 4) != (local_cc != -0x80000000)) {
        uVar9 = ___cxa_allocate_exception(0x30);
        FUN_101427680(local_98,"Some list members have Ids, others don\'t.");
        FUN_10144672c(&local_80,&DAT_106e0cc01,local_98);
        FUN_1011cb734(auStack_a0);
        FUN_1011cb734(auStack_a8);
        FUN_1011cb734(auStack_b0);
        FUN_1011cb734(auStack_b8);
        FUN_1011cb734(auStack_c0);
        FUN_101242ce8(uVar9,&local_80,auStack_a0,auStack_a8,auStack_b0,auStack_b8,auStack_c0);
                    /* WARNING: Subroutine does not return */
        ___cxa_throw(uVar9,&PTR_vtable_106661270,FUN_10124335c);
      }
    }
    else if ((*(char *)(param_1 + 0x61) == '\x01') && (local_cc == -0x80000000)) {
      uVar9 = ___cxa_allocate_exception(0x30);
      FUN_101427680(local_98,"Not all list members have Ids.");
      FUN_10144672c(&local_80,&DAT_106e0cc01,local_98);
      FUN_1011cb734(auStack_a0);
      FUN_1011cb734(auStack_a8);
      FUN_1011cb734(auStack_b0);
      FUN_1011cb734(auStack_b8);
      FUN_1011cb734(auStack_c0);
      FUN_101242ce8(uVar9,&local_80,auStack_a0,auStack_a8,auStack_b0,auStack_b8,auStack_c0);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(uVar9,&PTR_vtable_106661270,FUN_10124335c);
    }
    *(int *)((long)param_2 + 0x1c) = local_cc;
  }
  return;
}

