
void FUN_10319cb10(long param_1,long *param_2)

{
  ulong uVar1;
  undefined8 *puVar2;
  code *pcVar3;
  int iVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  void *pvVar7;
  undefined8 uVar8;
  long *plVar9;
  undefined4 uVar10;
  uint uVar11;
  uint uVar12;
  ulong uVar13;
  ulong uVar14;
  undefined8 *puVar15;
  long *plVar16;
  char *pcVar17;
  long lVar18;
  void *pvVar19;
  int iVar20;
  long lVar21;
  long *plVar22;
  long lVar23;
  char *local_b8;
  undefined1 local_b0;
  long local_a8;
  char *local_a0;
  long local_98;
  long local_90;
  long *local_88;
  long *local_80;
  char *local_70;
  undefined1 local_68;
  
  local_88 = (long *)0x105be692e;
  local_80 = (long *)((ulong)local_80 & 0xffffffffffffff00);
  FUN_102348ce8(param_1,&local_88,0,1);
  (**(code **)(*param_2 + 0x5a0))(&local_88,param_2);
  if (local_88 != local_80) {
    iVar20 = 0;
    plVar22 = local_88;
    do {
      if (*plVar22 == 0) {
        puVar2 = *(undefined8 **)(param_1 + 0x90);
        if (puVar2 < *(undefined8 **)(param_1 + 0x98)) {
          *puVar2 = 0;
          puVar2[1] = 0;
          puVar15 = puVar2 + 2;
        }
        else {
          pvVar19 = *(void **)(param_1 + 0x88);
          lVar21 = (long)puVar2 - (long)pvVar19 >> 4;
          uVar1 = lVar21 + 1;
          if (uVar1 >> 0x3c != 0) {
            FUN_1031c267c(param_1 + 0x88);
            goto LAB_10319d53c;
          }
          uVar13 = (long)*(undefined8 **)(param_1 + 0x98) - (long)pvVar19;
          uVar14 = (long)uVar13 >> 3;
          if (uVar14 <= uVar1) {
            uVar14 = uVar1;
          }
          if (0x7fffffffffffffef < uVar13) {
            uVar14 = 0xfffffffffffffff;
          }
          if (uVar14 == 0) {
            pvVar7 = (void *)0x0;
          }
          else {
            if (uVar14 >> 0x3c != 0) {
                    /* WARNING: Subroutine does not return */
              FUN_10024a858();
            }
            pvVar7 = operator_new(uVar14 << 4);
          }
          puVar15 = (undefined8 *)((long)pvVar7 + lVar21 * 0x10);
          *puVar15 = 0;
          puVar15[1] = 0;
          puVar15 = puVar15 + 2;
          _memcpy(pvVar7,pvVar19,(long)puVar2 - (long)pvVar19);
          *(void **)(param_1 + 0x88) = pvVar7;
          *(undefined8 **)(param_1 + 0x90) = puVar15;
          *(void **)(param_1 + 0x98) = (void *)((long)pvVar7 + uVar14 * 0x10);
          if (pvVar19 != (void *)0x0) {
            operator_delete(pvVar19);
          }
        }
        *(undefined8 **)(param_1 + 0x90) = puVar15;
      }
      else {
        uVar5 = FUN_10319c4dc(&local_90);
        FUN_10319c95c(&local_98,uVar5,*plVar22);
        FUN_1023490d0(param_1,local_90);
        if (local_98 != 0) {
          FUN_1023490d0(param_1);
        }
        iVar4 = (int)plVar22[2];
        if (iVar4 < 5) {
          if (iVar4 < 3) {
            if (iVar4 == 1) {
              FUN_10294c50c(&local_b8);
              local_70 = "Indexer";
              local_68 = 0;
              FUN_10294c65c(local_b8,&local_70);
              FUN_10294c6bc(local_b8,iVar20,(char)plVar22[4]);
              pcVar17 = local_b8;
              local_a0 = local_b8;
              if ((local_b8 != (char *)0x0) && (*(int *)(local_b8 + 8) == 0)) {
                FUN_10128eea0(local_b8);
              }
            }
            else if (iVar4 == 2) {
              FUN_10294c9bc(&local_b8);
              local_70 = "Indexer";
              local_68 = 0;
              FUN_10294cb00(local_b8,&local_70);
              FUN_10294cb60(local_b8,iVar20);
              pcVar17 = local_b8;
              local_a0 = local_b8;
              if ((local_b8 != (char *)0x0) && (*(int *)(local_b8 + 8) == 0)) {
                FUN_10128eea0(local_b8);
              }
            }
            else {
LAB_10319cfa0:
              FUN_10295bb44(&local_b8);
              local_70 = "Indexer";
              local_68 = 0;
              FUN_10295bc88(local_b8,&local_70);
              FUN_10295bce8(local_b8,iVar20);
              pcVar17 = local_b8;
              local_a0 = local_b8;
              if ((local_b8 != (char *)0x0) && (*(int *)(local_b8 + 8) == 0)) {
                FUN_10128eea0(local_b8);
              }
            }
          }
          else if (iVar4 == 3) {
            FUN_10294d2f4(&local_b8);
            local_70 = "Indexer";
            local_68 = 0;
            FUN_10294d438(local_b8,&local_70);
            FUN_10294d498(local_b8,iVar20);
            pcVar17 = local_b8;
            local_a0 = local_b8;
            if ((local_b8 != (char *)0x0) && (*(int *)(local_b8 + 8) == 0)) {
              FUN_10128eea0(local_b8);
            }
          }
          else {
            if (iVar4 != 4) goto LAB_10319cfa0;
            FUN_10294d788(&local_b8);
            local_70 = "Indexer";
            local_68 = 0;
            FUN_10294d8cc(local_b8,&local_70);
            FUN_10294d92c(local_b8,iVar20);
            pcVar17 = local_b8;
            local_a0 = local_b8;
            if ((local_b8 != (char *)0x0) && (*(int *)(local_b8 + 8) == 0)) {
              FUN_10128eea0(local_b8);
            }
          }
        }
        else if (iVar4 < 7) {
          if (iVar4 == 5) {
            FUN_10294ce50(&local_b8);
            local_70 = "Indexer";
            local_68 = 0;
            FUN_10294cf94(local_b8,&local_70);
            FUN_10294cff4(local_b8,iVar20,*(undefined4 *)((long)plVar22 + 0x14));
            pcVar17 = local_b8;
            local_a0 = local_b8;
            if ((local_b8 != (char *)0x0) && (*(int *)(local_b8 + 8) == 0)) {
              FUN_10128eea0(local_b8);
            }
          }
          else {
            if (iVar4 != 6) goto LAB_10319cfa0;
            FUN_10294dc3c(&local_b8);
            local_70 = "Indexer";
            local_68 = 0;
            FUN_10294ddb0(local_b8,&local_70);
            FUN_10294de10((int)plVar22[3],*(undefined4 *)((long)plVar22 + 0x1c),local_b8,iVar20);
            pcVar17 = local_b8;
            local_a0 = local_b8;
            if ((local_b8 != (char *)0x0) && (*(int *)(local_b8 + 8) == 0)) {
              FUN_10128eea0(local_b8);
            }
          }
        }
        else if (iVar4 == 7) {
          FUN_10294e4ec(&local_b8);
          local_70 = "MappedIndexer";
          local_68 = 0;
          FUN_10294e6bc(local_b8,&local_70);
          FUN_10294e71c(local_b8,plVar22 + 5);
          FUN_10294e7c4(local_b8,iVar20);
          pcVar17 = local_b8;
          local_a0 = local_b8;
          if ((local_b8 != (char *)0x0) && (*(int *)(local_b8 + 8) == 0)) {
            FUN_10128eea0(local_b8);
          }
        }
        else {
          if (iVar4 != 8) goto LAB_10319cfa0;
          FUN_10294e120(&local_b8);
          local_70 = "CollisionScaledMode";
          local_68 = 0;
          FUN_10294e264(local_b8,&local_70);
          FUN_10294e2c4(local_b8,iVar20);
          pcVar17 = local_b8;
          uVar5 = *(undefined8 *)(*(long *)(param_1 + 0x90) + -0x10);
          local_70 = "InMode";
          local_68 = 0;
          if ((long *)*plVar22 == (long *)0x0) {
            uVar10 = 0;
          }
          else {
            uVar6 = (**(code **)(*(long *)*plVar22 + 0x170))();
            uVar8 = FUN_1026e8318();
            iVar4 = FUN_10147fd68(uVar6,uVar8);
            uVar10 = 4;
            if (iVar4 == 0) {
              uVar10 = 0;
            }
          }
          FUN_102321e6c(uVar5,pcVar17,&local_70,uVar10);
          pcVar17 = local_b8;
          local_a0 = local_b8;
          if ((local_b8 != (char *)0x0) && (*(int *)(local_b8 + 8) == 0)) {
            FUN_10128eea0(local_b8);
          }
        }
        uVar5 = FUN_1023490d0(param_1,pcVar17);
        if ((int)plVar22[2] == 2) {
          FUN_10319c4dc(&local_a8,uVar5,plVar22[1]);
          lVar21 = local_a8;
          FUN_1023490d0(param_1,local_a8);
          lVar18 = local_90;
          local_70 = "Out";
          local_68 = 0;
          local_b8 = "In";
          local_b0 = 0;
          if ((long *)*plVar22 == (long *)0x0) {
            uVar10 = 0;
          }
          else {
            uVar5 = (**(code **)(*(long *)*plVar22 + 0x170))();
            uVar6 = FUN_1026e8318();
            iVar4 = FUN_10147fd68(uVar5,uVar6);
            uVar10 = 4;
            if (iVar4 == 0) {
              uVar10 = 0;
            }
          }
          FUN_102321c3c(lVar18,&local_70,pcVar17,&local_b8,uVar10);
          local_70 = "Toggle";
          local_68 = 0;
          if ((long *)plVar22[1] == (long *)0x0) {
            uVar10 = 0;
          }
          else {
            uVar5 = (**(code **)(*(long *)plVar22[1] + 0x170))();
            uVar6 = FUN_1026e8318();
            iVar4 = FUN_10147fd68(uVar5,uVar6);
            uVar10 = 4;
            if (iVar4 == 0) {
              uVar10 = 0;
            }
          }
          FUN_102321e6c(lVar21,pcVar17,&local_70,uVar10);
          plVar9 = *(long **)(param_1 + 0x90);
          if (plVar9 < *(long **)(param_1 + 0x98)) {
            *plVar9 = lVar18;
            plVar9[1] = lVar21;
            *(long **)(param_1 + 0x90) = plVar9 + 2;
          }
          else {
            pvVar19 = *(void **)(param_1 + 0x88);
            lVar23 = (long)plVar9 - (long)pvVar19 >> 4;
            uVar1 = lVar23 + 1;
            if (uVar1 >> 0x3c != 0) {
              FUN_1031c267c(param_1 + 0x88);
              goto LAB_10319d53c;
            }
            uVar13 = (long)*(long **)(param_1 + 0x98) - (long)pvVar19;
            uVar14 = (long)uVar13 >> 3;
            if (uVar14 <= uVar1) {
              uVar14 = uVar1;
            }
            if (0x7fffffffffffffef < uVar13) {
              uVar14 = 0xfffffffffffffff;
            }
            if (uVar14 == 0) {
              pvVar7 = (void *)0x0;
            }
            else {
              if (uVar14 >> 0x3c != 0) {
                    /* WARNING: Subroutine does not return */
                FUN_10024a858();
              }
              pvVar7 = operator_new(uVar14 << 4);
            }
            plVar16 = (long *)((long)pvVar7 + lVar23 * 0x10);
            *plVar16 = lVar18;
            plVar16[1] = lVar21;
            _memcpy(pvVar7,pvVar19,(long)plVar9 - (long)pvVar19);
            *(void **)(param_1 + 0x88) = pvVar7;
            *(long **)(param_1 + 0x90) = plVar16 + 2;
            *(void **)(param_1 + 0x98) = (void *)((long)pvVar7 + uVar14 * 0x10);
            if (pvVar19 != (void *)0x0) {
              operator_delete(pvVar19);
            }
            *(long **)(param_1 + 0x90) = plVar16 + 2;
          }
          if ((lVar21 != 0) &&
             (iVar4 = *(int *)(lVar21 + 8) + -1, *(int *)(lVar21 + 8) = iVar4, iVar4 == 0)) {
            FUN_10128eea0(lVar21);
          }
        }
        else {
          if ((long *)*plVar22 == (long *)0x0) {
            uVar10 = 0;
            if (local_98 != 0) goto LAB_10319d104;
LAB_10319d15c:
            lVar18 = local_90;
            local_70 = "Out";
            local_68 = 0;
            local_b8 = "In";
            local_b0 = 0;
            FUN_102321c3c(local_90,&local_70,pcVar17,&local_b8,uVar10);
          }
          else {
            uVar5 = (**(code **)(*(long *)*plVar22 + 0x170))();
            uVar6 = FUN_1026e8318();
            iVar4 = FUN_10147fd68(uVar5,uVar6);
            uVar10 = 4;
            if (iVar4 == 0) {
              uVar10 = 0;
            }
            if (local_98 == 0) goto LAB_10319d15c;
LAB_10319d104:
            lVar18 = local_90;
            lVar21 = local_98;
            local_70 = "Out";
            local_68 = 0;
            FUN_102321d9c(local_90,&local_70,local_98,uVar10);
            local_70 = "In";
            local_68 = 0;
            FUN_102321e6c(lVar21,pcVar17,&local_70,uVar10);
          }
          plVar9 = *(long **)(param_1 + 0x90);
          if (plVar9 < *(long **)(param_1 + 0x98)) {
            *plVar9 = lVar18;
            plVar9[1] = 0;
            plVar16 = plVar9 + 2;
          }
          else {
            pvVar19 = *(void **)(param_1 + 0x88);
            lVar21 = (long)plVar9 - (long)pvVar19 >> 4;
            uVar1 = lVar21 + 1;
            if (uVar1 >> 0x3c != 0) {
              FUN_1031c267c(param_1 + 0x88);
LAB_10319d53c:
                    /* WARNING: Does not return */
              pcVar3 = (code *)SoftwareBreakpoint(1,0x10319d540);
              (*pcVar3)();
            }
            uVar13 = (long)*(long **)(param_1 + 0x98) - (long)pvVar19;
            uVar14 = (long)uVar13 >> 3;
            if (uVar14 <= uVar1) {
              uVar14 = uVar1;
            }
            if (0x7fffffffffffffef < uVar13) {
              uVar14 = 0xfffffffffffffff;
            }
            if (uVar14 == 0) {
              pvVar7 = (void *)0x0;
            }
            else {
              if (uVar14 >> 0x3c != 0) {
                    /* WARNING: Subroutine does not return */
                FUN_10024a858();
              }
              pvVar7 = operator_new(uVar14 << 4);
            }
            plVar16 = (long *)((long)pvVar7 + lVar21 * 0x10);
            *plVar16 = lVar18;
            plVar16[1] = 0;
            plVar16 = plVar16 + 2;
            _memcpy(pvVar7,pvVar19,(long)plVar9 - (long)pvVar19);
            *(void **)(param_1 + 0x88) = pvVar7;
            *(long **)(param_1 + 0x90) = plVar16;
            *(void **)(param_1 + 0x98) = (void *)((long)pvVar7 + uVar14 * 0x10);
            if (pvVar19 != (void *)0x0) {
              operator_delete(pvVar19);
            }
          }
          *(long **)(param_1 + 0x90) = plVar16;
        }
        uVar5 = *(undefined8 *)(param_1 + 0x80);
        if ((long *)*plVar22 == (long *)0x0) {
          uVar11 = 0;
          plVar9 = (long *)plVar22[1];
          if (plVar9 != (long *)0x0) goto LAB_10319d3d8;
LAB_10319d414:
          uVar12 = 0;
        }
        else {
          uVar6 = (**(code **)(*(long *)*plVar22 + 0x170))();
          uVar8 = FUN_1026e8318();
          iVar4 = FUN_10147fd68(uVar6,uVar8);
          uVar11 = 4;
          if (iVar4 == 0) {
            uVar11 = 0;
          }
          plVar9 = (long *)plVar22[1];
          if (plVar9 == (long *)0x0) goto LAB_10319d414;
LAB_10319d3d8:
          uVar6 = (**(code **)(*plVar9 + 0x170))();
          uVar8 = FUN_1026e8318();
          iVar4 = FUN_10147fd68(uVar6,uVar8);
          uVar12 = 4;
          if (iVar4 == 0) {
            uVar12 = 0;
          }
        }
        FUN_102322110(pcVar17,uVar5,uVar12 | uVar11);
        if ((pcVar17 != (char *)0x0) &&
           (iVar4 = *(int *)(pcVar17 + 8), *(int *)(pcVar17 + 8) = iVar4 + -1, iVar4 + -1 == 0)) {
          FUN_10128eea0(pcVar17);
        }
        if ((local_98 != 0) &&
           (iVar4 = *(int *)(local_98 + 8) + -1, *(int *)(local_98 + 8) = iVar4, iVar4 == 0)) {
          FUN_10128eea0();
        }
        if ((lVar18 != 0) &&
           (iVar4 = *(int *)(lVar18 + 8) + -1, *(int *)(lVar18 + 8) = iVar4, iVar4 == 0)) {
          FUN_10128eea0(lVar18);
        }
      }
      plVar22 = plVar22 + 7;
      iVar20 = iVar20 + 1;
    } while (plVar22 != local_80);
  }
  plVar9 = local_88;
  plVar22 = local_80;
  if (local_88 != (long *)0x0) {
    for (; plVar22 != plVar9; plVar22 = plVar22 + -7) {
      if (plVar22[-2] != 0) {
        if (*(char *)((long)plVar22 + -4) == '\x01') {
          FUN_101a24778(plVar22[-2],(long)(int)plVar22[-1] << 2);
        }
        plVar22[-2] = 0;
        *(undefined4 *)(plVar22 + -1) = 0;
      }
    }
    local_80 = plVar9;
    operator_delete(local_88);
  }
  return;
}

