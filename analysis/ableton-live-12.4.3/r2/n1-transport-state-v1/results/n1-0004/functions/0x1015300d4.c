
void FUN_1015300d4(long param_1,long *param_2,int *param_3)

{
  char *pcVar1;
  int *piVar2;
  char *pcVar3;
  int iVar4;
  int iVar5;
  size_t sVar6;
  size_t sVar7;
  ulong uVar8;
  void *pvVar9;
  ulong uVar10;
  undefined8 uVar11;
  long *plVar12;
  long *plVar13;
  int *piVar14;
  char *pcVar15;
  long lVar16;
  long lVar17;
  long *plVar18;
  long lVar19;
  undefined8 *puVar20;
  int *local_100;
  int *local_f8;
  undefined1 auStack_f0 [8];
  undefined1 auStack_e8 [8];
  undefined1 auStack_e0 [8];
  int *local_d8;
  undefined1 auStack_d0 [8];
  int *local_c8;
  int *local_c0;
  undefined1 auStack_b8 [8];
  int *local_b0 [3];
  long *local_98;
  int local_90;
  undefined4 uStack_8c;
  long *local_88;
  int local_80;
  int *local_78;
  int *local_70;
  int *local_68;
  
  if (*(long *)(param_1 + 0x38) != 0) {
    if (*(long *)(param_1 + 0x40) != 0) {
      uVar11 = ___cxa_allocate_exception(0x30);
      FUN_101447188(&local_98,&DAT_106e0cc01,"Illegal schema structure");
      FUN_1011cb734(local_b0);
      FUN_1011cb734(&local_c8);
      FUN_1011cb734(&local_68);
      FUN_1011cb734(&local_70);
      FUN_1011cb734(&local_78);
      FUN_101242ce8(uVar11,&local_98,local_b0,&local_c8,&local_68,&local_70,&local_78);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
    }
    plVar18 = (long *)(param_1 + 0x48);
    if (*plVar18 == 0) {
      FUN_1011cb734(&local_c8);
      FUN_10152a28c(&local_68,param_2);
      if (0 < *param_3) {
        puVar20 = *(undefined8 **)(param_3 + 2);
        plVar13 = (long *)*puVar20;
        plVar12 = (long *)"";
        if (plVar13 != (long *)0x0) {
          plVar12 = plVar13;
        }
        sVar6 = _strlen((char *)plVar12);
        plVar13 = (long *)puVar20[1];
        local_88 = (long *)"";
        if (plVar13 != (long *)0x0) {
          local_88 = plVar13;
        }
        sVar7 = _strlen((char *)local_88);
        local_90 = (int)sVar6;
        local_80 = (int)sVar7;
        local_98 = plVar12;
        if ((local_90 != 0xc) || (*plVar12 != 0x6c616e7265746e49 || (int)plVar12[1] != 0x656d614e))
        {
          uVar11 = ___cxa_allocate_exception(0x30);
          FUN_101447188(local_b0,&DAT_106e0cc01,"Unknown attribute \'$1\'");
          FUN_10152a28c(&local_70,&local_98);
          FUN_1011cb734(&local_78);
          FUN_1011cb734(auStack_b8);
          FUN_1011cb734(auStack_d0);
          FUN_1011cb734(auStack_e0);
          FUN_101242ce8(uVar11,local_b0,&local_70,&local_78,auStack_b8,auStack_d0,auStack_e0);
                    /* WARNING: Subroutine does not return */
          ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
        }
        if (local_68 != (int *)0x0) {
          *local_68 = *local_68 + 1;
        }
        if ((local_c8 != (int *)0x0) && (iVar5 = *local_c8, *local_c8 = iVar5 + -1, iVar5 + -1 == 0)
           ) {
          FUN_101449efc();
        }
        local_c8 = local_68;
        FUN_10152a28c(local_b0,&local_88);
        piVar2 = local_68;
        local_68 = local_b0[0];
        local_b0[0] = piVar2;
        if ((piVar2 != (int *)0x0) && (iVar5 = *piVar2, *piVar2 = iVar5 + -1, iVar5 + -1 == 0)) {
          FUN_101449efc();
        }
        if (1 < *param_3) {
          uVar11 = ___cxa_allocate_exception(0x30);
          FUN_101447188(local_b0,&DAT_106e0cc01,"Unknown attribute \'$1\'");
          FUN_10152a28c(&local_70,&local_98);
          FUN_1011cb734(&local_78);
          FUN_1011cb734(auStack_b8);
          FUN_1011cb734(auStack_d0);
          FUN_1011cb734(auStack_e0);
          FUN_101242ce8(uVar11,local_b0,&local_70,&local_78,auStack_b8,auStack_d0,auStack_e0);
                    /* WARNING: Subroutine does not return */
          ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
        }
      }
      FUN_10120d708(&local_98);
      local_100 = local_68;
      if (local_68 != (int *)0x0) {
        *local_68 = *local_68 + 1;
      }
      FUN_10120e274(&local_98,&local_100);
      if ((local_100 != (int *)0x0) &&
         (iVar5 = *local_100, *local_100 = iVar5 + -1, iVar5 + -1 == 0)) {
        FUN_101449efc();
      }
      pvVar9 = operator_new(0x38);
      FUN_10147f72c(pvVar9,&local_98,&local_c8,0);
      lVar19 = *plVar18;
      *plVar18 = (long)pvVar9;
      if (lVar19 != 0) {
        FUN_101478454(plVar18);
      }
      piVar2 = (int *)CONCAT44(uStack_8c,local_90);
      if ((piVar2 != (int *)0x0) && (iVar5 = *piVar2, *piVar2 = iVar5 + -1, iVar5 + -1 == 0)) {
        FUN_101449efc();
      }
      if ((local_68 != (int *)0x0) && (iVar5 = *local_68, *local_68 = iVar5 + -1, iVar5 + -1 == 0))
      {
        FUN_101449efc();
      }
      if ((local_c8 != (int *)0x0) && (iVar5 = *local_c8, *local_c8 = iVar5 + -1, iVar5 + -1 == 0))
      {
        FUN_101449efc();
      }
      return;
    }
    if (0 < *param_3) {
      puVar20 = *(undefined8 **)(param_3 + 2);
      plVar12 = (long *)*puVar20;
      pcVar1 = "";
      plVar18 = (long *)pcVar1;
      if (plVar12 != (long *)0x0) {
        plVar18 = plVar12;
      }
      sVar6 = _strlen((char *)plVar18);
      if (((int)sVar6 == 5) && ((int)*plVar18 == 0x73616c43 && *(char *)((long)plVar18 + 4) == 's'))
      {
        plVar13 = (long *)puVar20[1];
        plVar12 = (long *)pcVar1;
        if (plVar13 != (long *)0x0) {
          plVar12 = plVar13;
        }
        sVar6 = _strlen((char *)plVar12);
        local_90 = 5;
        local_80 = (int)sVar6;
        local_98 = plVar18;
        local_88 = plVar12;
        FUN_10152a28c(&local_68,&local_88);
        if (1 < *param_3) {
          lVar19 = *(long *)(param_3 + 2);
          piVar14 = *(int **)(lVar19 + 0x10);
          piVar2 = (int *)pcVar1;
          if (piVar14 != (int *)0x0) {
            piVar2 = piVar14;
          }
          sVar6 = _strlen((char *)piVar2);
          pcVar15 = *(char **)(lVar19 + 0x18);
          pcVar3 = pcVar1;
          if (pcVar15 != (char *)0x0) {
            pcVar3 = pcVar15;
          }
          sVar7 = _strlen(pcVar3);
          if (((int)sVar6 == 4) && (*piVar2 == 0x65707954)) {
            uVar8 = FUN_1002fd908(pcVar3,(long)(int)sVar7);
            if (((uVar8 >> 0x20 & 1) == 0) || (4 < (int)uVar8 + 4U)) {
              uVar11 = ___cxa_allocate_exception(0x30);
              FUN_101447188(&local_98,&DAT_106e0cc01,"Illegal type");
              FUN_1011cb734(local_b0);
              FUN_1011cb734(&local_c8);
              FUN_1011cb734(&local_70);
              FUN_1011cb734(&local_78);
              FUN_1011cb734(auStack_b8);
              FUN_101242ce8(uVar11,&local_98,local_b0,&local_c8,&local_70,&local_78,auStack_b8);
                    /* WARNING: Subroutine does not return */
              ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
            }
            FUN_10120d708(&local_c8);
            if ((int)uVar8 == -3) {
              if (2 < *param_3) {
                lVar19 = *(long *)(param_3 + 2);
                plVar12 = *(long **)(lVar19 + 0x20);
                plVar18 = (long *)pcVar1;
                if (plVar12 != (long *)0x0) {
                  plVar18 = plVar12;
                }
                sVar6 = _strlen((char *)plVar18);
                plVar13 = *(long **)(lVar19 + 0x28);
                plVar12 = (long *)pcVar1;
                if (plVar13 != (long *)0x0) {
                  plVar12 = plVar13;
                }
                if (((int)sVar6 == 0xf) &&
                   (*plVar18 == 0x6172547961727241 &&
                    *(long *)((long)plVar18 + 7) == 0x726f74616c736e61)) {
                  sVar6 = _strlen((char *)plVar18);
                  sVar7 = _strlen((char *)plVar12);
                  local_90 = (int)sVar6;
                  local_80 = (int)sVar7;
                  local_98 = plVar18;
                  local_88 = plVar12;
                  FUN_10152a28c(&local_d8,&local_88);
                  FUN_10120e274(&local_c8,&local_d8);
                  if ((local_d8 != (int *)0x0) &&
                     (iVar5 = *local_d8, *local_d8 = iVar5 + -1, iVar5 + -1 == 0)) {
                    FUN_101449efc();
                  }
                  iVar5 = 3;
                  goto LAB_101530638;
                }
              }
              uVar11 = ___cxa_allocate_exception(0x30);
              FUN_101447188(&local_98,&DAT_106e0cc01,
                            "Array doesn\'t have an \'ArrayTranslator\' attribute");
              FUN_1011cb734(local_b0);
              FUN_1011cb734(&local_70);
              FUN_1011cb734(&local_78);
              FUN_1011cb734(auStack_b8);
              FUN_1011cb734(auStack_d0);
              FUN_101242ce8(uVar11,&local_98,local_b0,&local_70,&local_78,auStack_b8,auStack_d0);
                    /* WARNING: Subroutine does not return */
              ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
            }
            iVar5 = 2;
LAB_101530638:
            FUN_1011cb734(&local_70);
            FUN_10152a28c(&local_78,param_2);
            if (iVar5 < *param_3) {
              lVar19 = *(long *)(param_3 + 2);
              plVar12 = *(long **)(lVar19 + (ulong)(uint)(iVar5 << 1) * 8);
              plVar18 = (long *)pcVar1;
              if (plVar12 != (long *)0x0) {
                plVar18 = plVar12;
              }
              sVar6 = _strlen((char *)plVar18);
              plVar12 = *(long **)(lVar19 + (ulong)(iVar5 << 1 | 1) * 8);
              if (plVar12 != (long *)0x0) {
                pcVar1 = (char *)plVar12;
              }
              sVar7 = _strlen(pcVar1);
              local_90 = (int)sVar6;
              local_80 = (int)sVar7;
              local_88 = (long *)pcVar1;
              local_98 = plVar18;
              if ((local_90 != 0xc) ||
                 (*plVar18 != 0x6c616e7265746e49 || (int)plVar18[1] != 0x656d614e)) {
                uVar11 = ___cxa_allocate_exception(0x30);
                FUN_101447188(local_b0,&DAT_106e0cc01,"Unknown attribute \'$1\'");
                FUN_10152a28c(auStack_b8,&local_98);
                FUN_1011cb734(auStack_d0);
                FUN_1011cb734(auStack_e0);
                FUN_1011cb734(auStack_e8);
                FUN_1011cb734(auStack_f0);
                FUN_101242ce8(uVar11,local_b0,auStack_b8,auStack_d0,auStack_e0,auStack_e8,auStack_f0
                             );
                    /* WARNING: Subroutine does not return */
                ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
              }
              FUN_10152a28c(local_b0,param_2);
              piVar2 = local_70;
              local_70 = local_b0[0];
              local_b0[0] = piVar2;
              if ((piVar2 != (int *)0x0) && (iVar4 = *piVar2, *piVar2 = iVar4 + -1, iVar4 + -1 == 0)
                 ) {
                FUN_101449efc();
              }
              FUN_10152a28c(local_b0,&local_88);
              piVar2 = local_78;
              local_78 = local_b0[0];
              local_b0[0] = piVar2;
              if ((piVar2 != (int *)0x0) && (iVar4 = *piVar2, *piVar2 = iVar4 + -1, iVar4 + -1 == 0)
                 ) {
                FUN_101449efc();
              }
              if (iVar5 + 1 < *param_3) {
                uVar11 = ___cxa_allocate_exception(0x30);
                FUN_101447188(local_b0,&DAT_106e0cc01,"Unknown attribute \'$1\'");
                FUN_10152a28c(auStack_b8,&local_98);
                FUN_1011cb734(auStack_d0);
                FUN_1011cb734(auStack_e0);
                FUN_1011cb734(auStack_e8);
                FUN_1011cb734(auStack_f0);
                FUN_101242ce8(uVar11,local_b0,auStack_b8,auStack_d0,auStack_e0,auStack_e8,auStack_f0
                             );
                    /* WARNING: Subroutine does not return */
                ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
              }
            }
            FUN_10120d708(&local_98);
            local_f8 = local_68;
            if (local_68 != (int *)0x0) {
              *local_68 = *local_68 + 1;
            }
            FUN_10120e274(&local_98,&local_f8);
            if ((local_f8 != (int *)0x0) &&
               (iVar5 = *local_f8, *local_f8 = iVar5 + -1, iVar5 + -1 == 0)) {
              FUN_101449efc();
            }
            FUN_10152957c(local_b0,&local_78);
            piVar2 = local_78;
            local_78 = local_b0[0];
            local_b0[0] = piVar2;
            if ((piVar2 != (int *)0x0) && (iVar5 = *piVar2, *piVar2 = iVar5 + -1, iVar5 + -1 == 0))
            {
              FUN_101449efc();
            }
            pvVar9 = operator_new(0x38);
            FUN_101481054(pvVar9,&local_78,&local_70,&local_98,&local_c8,uVar8);
            lVar19 = *(long *)(param_1 + 0x40);
            *(void **)(param_1 + 0x40) = pvVar9;
            if (lVar19 != 0) {
              pvVar9 = (void *)FUN_1014784fc();
              operator_delete(pvVar9);
            }
            piVar2 = (int *)CONCAT44(uStack_8c,local_90);
            if ((piVar2 != (int *)0x0) && (iVar5 = *piVar2, *piVar2 = iVar5 + -1, iVar5 + -1 == 0))
            {
              FUN_101449efc();
            }
            if ((local_78 != (int *)0x0) &&
               (iVar5 = *local_78, *local_78 = iVar5 + -1, iVar5 + -1 == 0)) {
              FUN_101449efc();
            }
            if ((local_70 != (int *)0x0) &&
               (iVar5 = *local_70, *local_70 = iVar5 + -1, iVar5 + -1 == 0)) {
              FUN_101449efc();
            }
            if ((local_c0 != (int *)0x0) &&
               (iVar5 = *local_c0, *local_c0 = iVar5 + -1, iVar5 + -1 == 0)) {
              FUN_101449efc();
            }
            if (local_68 == (int *)0x0) {
              return;
            }
            iVar5 = *local_68;
            *local_68 = iVar5 + -1;
            if (iVar5 + -1 != 0) {
              return;
            }
            FUN_101449efc();
            return;
          }
        }
        uVar11 = ___cxa_allocate_exception(0x30);
        FUN_101447188(&local_98,&DAT_106e0cc01,"Missing \'Type\' attribute");
        FUN_1011cb734(local_b0);
        FUN_1011cb734(&local_c8);
        FUN_1011cb734(&local_70);
        FUN_1011cb734(&local_78);
        FUN_1011cb734(auStack_b8);
        FUN_101242ce8(uVar11,&local_98,local_b0,&local_c8,&local_70,&local_78,auStack_b8);
                    /* WARNING: Subroutine does not return */
        ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
      }
    }
    uVar11 = ___cxa_allocate_exception(0x30);
    FUN_101447188(&local_98,&DAT_106e0cc01,"Missing \'Class\' attribute");
    FUN_1011cb734(local_b0);
    FUN_1011cb734(&local_c8);
    FUN_1011cb734(&local_68);
    FUN_1011cb734(&local_70);
    FUN_1011cb734(&local_78);
    FUN_101242ce8(uVar11,&local_98,local_b0,&local_c8,&local_68,&local_70,&local_78);
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
  }
  if (((int)param_2[1] != 0xd) ||
     (*(long *)*param_2 != 0x536e6f74656c6241 || *(long *)(*param_2 + 5) != 0x616d656863536e6f)) {
    uVar11 = ___cxa_allocate_exception(0x30);
    FUN_101447188(&local_98,&DAT_106e0cc01,
                  "Expected \'AbletonSchema\' root node, got \'$1\' instead");
    FUN_10152a28c(local_b0,param_2);
    FUN_1011cb734(&local_c8);
    FUN_1011cb734(&local_68);
    FUN_1011cb734(&local_70);
    FUN_1011cb734(&local_78);
    FUN_101242ce8(uVar11,&local_98,local_b0,&local_c8,&local_68,&local_70,&local_78);
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
  }
  if (0 < *param_3) {
    puVar20 = *(undefined8 **)(param_3 + 2);
    piVar14 = (int *)*puVar20;
    pcVar1 = "";
    piVar2 = (int *)pcVar1;
    if (piVar14 != (int *)0x0) {
      piVar2 = piVar14;
    }
    sVar6 = _strlen((char *)piVar2);
    pcVar15 = (char *)puVar20[1];
    pcVar3 = pcVar1;
    if (pcVar15 != (char *)0x0) {
      pcVar3 = pcVar15;
    }
    sVar7 = _strlen(pcVar3);
    if (((int)sVar6 == 7) && (*piVar2 == 0x73726556 && *(int *)((long)piVar2 + 3) == 0x6e6f6973)) {
      uVar8 = FUN_1002fd908(pcVar3,(long)(int)sVar7);
      if ((uVar8 & 0x1fffffffe) != 0x100000004) {
        uVar11 = ___cxa_allocate_exception(0x30);
        FUN_101447188(&local_98,&DAT_106e0cc01,"Unsupported schema version");
        FUN_1011cb734(local_b0);
        FUN_1011cb734(&local_c8);
        FUN_1011cb734(&local_68);
        FUN_1011cb734(&local_70);
        FUN_1011cb734(&local_78);
        FUN_101242ce8(uVar11,&local_98,local_b0,&local_c8,&local_68,&local_70,&local_78);
                    /* WARNING: Subroutine does not return */
        ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
      }
      if (1 < *param_3) {
        lVar19 = *(long *)(param_3 + 2);
        plVar12 = *(long **)(lVar19 + 0x10);
        plVar18 = (long *)pcVar1;
        if (plVar12 != (long *)0x0) {
          plVar18 = plVar12;
        }
        sVar6 = _strlen((char *)plVar18);
        pcVar15 = *(char **)(lVar19 + 0x18);
        pcVar3 = pcVar1;
        if (pcVar15 != (char *)0x0) {
          pcVar3 = pcVar15;
        }
        sVar7 = _strlen(pcVar3);
        if ((int)sVar6 == 0xf) {
          lVar19 = *plVar18;
          lVar17 = *(long *)((long)plVar18 + 7);
          lVar16 = 0x746e756f43726f74;
        }
        else {
          if ((int)sVar6 != 0x10) goto LAB_101530c1c;
          lVar19 = *plVar18;
          lVar17 = plVar18[1];
          lVar16 = 0x7265626d754e726f;
        }
        if (lVar19 == 0x74616c736e617254 && lVar17 == lVar16) {
          uVar8 = FUN_1002fd908(pcVar3,(long)(int)sVar7);
          if ((uVar8 & 0x180000000) != 0x100000000) {
            uVar11 = ___cxa_allocate_exception(0x30);
            FUN_101447188(&local_98,&DAT_106e0cc01,"Invalid \'TranslatorNumber\' value");
            FUN_1011cb734(local_b0);
            FUN_1011cb734(&local_c8);
            FUN_1011cb734(&local_68);
            FUN_1011cb734(&local_70);
            FUN_1011cb734(&local_78);
            FUN_101242ce8(uVar11,&local_98,local_b0,&local_c8,&local_68,&local_70,&local_78);
                    /* WARNING: Subroutine does not return */
            ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
          }
          if (*param_3 < 3) {
            iVar5 = 0;
          }
          else {
            lVar19 = *(long *)(param_3 + 2);
            plVar12 = *(long **)(lVar19 + 0x20);
            plVar18 = (long *)pcVar1;
            if (plVar12 != (long *)0x0) {
              plVar18 = plVar12;
            }
            sVar6 = _strlen((char *)plVar18);
            plVar12 = *(long **)(lVar19 + 0x28);
            local_88 = (long *)pcVar1;
            if (plVar12 != (long *)0x0) {
              local_88 = plVar12;
            }
            sVar7 = _strlen((char *)local_88);
            local_90 = (int)sVar6;
            local_80 = (int)sVar7;
            local_98 = plVar18;
            if ((local_90 != 0xb) ||
               (*plVar18 != 0x6f4365676e616843 || *(long *)((long)plVar18 + 3) != 0x746e756f4365676e
               )) {
              uVar11 = ___cxa_allocate_exception(0x30);
              FUN_101447188(local_b0,&DAT_106e0cc01,"Unknown attribute $1");
              FUN_10152a28c(&local_c8,&local_98);
              FUN_1011cb734(&local_68);
              FUN_1011cb734(&local_70);
              FUN_1011cb734(&local_78);
              FUN_1011cb734(auStack_b8);
              FUN_101242ce8(uVar11,local_b0,&local_c8,&local_68,&local_70,&local_78,auStack_b8);
                    /* WARNING: Subroutine does not return */
              ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
            }
            uVar10 = FUN_1002fd908(local_88,(long)local_80);
            iVar5 = (int)uVar10;
            if ((uVar10 & 0x100000000) == 0) {
              iVar5 = 0;
            }
            if (((uVar10 >> 0x20 & 1) == 0) || (iVar5 < 0)) {
              uVar11 = ___cxa_allocate_exception(0x30);
              FUN_101447188(local_b0,&DAT_106e0cc01,"Invalid \'ChangeCount\' value");
              FUN_1011cb734(&local_c8);
              FUN_1011cb734(&local_68);
              FUN_1011cb734(&local_70);
              FUN_1011cb734(&local_78);
              FUN_1011cb734(auStack_b8);
              FUN_101242ce8(uVar11,local_b0,&local_c8,&local_68,&local_70,&local_78,auStack_b8);
                    /* WARNING: Subroutine does not return */
              ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
            }
          }
          pvVar9 = operator_new(0x70);
          FUN_1015146c0(pvVar9,uVar8,iVar5);
          lVar19 = *(long *)(param_1 + 0x38);
          *(void **)(param_1 + 0x38) = pvVar9;
          if (lVar19 == 0) {
            return;
          }
          pvVar9 = (void *)FUN_10148dbd4();
          operator_delete(pvVar9);
          return;
        }
      }
LAB_101530c1c:
      uVar11 = ___cxa_allocate_exception(0x30);
      FUN_101447188(&local_98,&DAT_106e0cc01,"Missing \'TranslatorNumber\' attribute");
      FUN_1011cb734(local_b0);
      FUN_1011cb734(&local_c8);
      FUN_1011cb734(&local_68);
      FUN_1011cb734(&local_70);
      FUN_1011cb734(&local_78);
      FUN_101242ce8(uVar11,&local_98,local_b0,&local_c8,&local_68,&local_70,&local_78);
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
    }
  }
  uVar11 = ___cxa_allocate_exception(0x30);
  FUN_101447188(&local_98,&DAT_106e0cc01,"Missing \'Class\' attribute");
  FUN_1011cb734(local_b0);
  FUN_1011cb734(&local_c8);
  FUN_1011cb734(&local_68);
  FUN_1011cb734(&local_70);
  FUN_1011cb734(&local_78);
  FUN_101242ce8(uVar11,&local_98,local_b0,&local_c8,&local_68,&local_70,&local_78);
                    /* WARNING: Subroutine does not return */
  ___cxa_throw(uVar11,&PTR_vtable_106661270,FUN_10124335c);
}

