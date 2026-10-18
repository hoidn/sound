
/* WARNING: Type propagation algorithm not settling */

void FUN_10292cd70(long param_1,undefined8 param_2)

{
  int iVar1;
  undefined1 uVar2;
  undefined8 *******pppppppuVar3;
  code *pcVar4;
  int iVar5;
  undefined8 *puVar6;
  long lVar7;
  long lVar8;
  ulong uVar9;
  undefined8 ******ppppppuVar10;
  long *plVar11;
  undefined8 ******ppppppuVar12;
  undefined8 *******pppppppuVar13;
  undefined8 *******pppppppuVar14;
  long local_90;
  long local_88;
  long *local_80;
  undefined8 *******local_78;
  undefined8 *******local_70;
  long local_68;
  
  FUN_101486fa8();
  local_70 = (undefined8 *******)0x0;
  local_68 = 0;
  uVar2 = *(undefined1 *)(param_1 + 0x68);
  *(undefined1 *)(param_1 + 0x68) = 1;
  plVar11 = *(long **)(param_1 + 0x30);
  local_78 = &local_70;
  puVar6 = (undefined8 *)(**(code **)(*plVar11 + 0x60))(plVar11);
  local_90 = (**(code **)*puVar6)(puVar6,plVar11);
  local_88 = *(long *)(local_90 + 0x18);
  local_80 = plVar11;
  if (local_88 != local_90) {
    do {
      while( true ) {
        lVar8 = local_88;
        plVar11 = (long *)(**(code **)(*local_80 + 0x60))();
        lVar7 = (**(code **)(*plVar11 + 0x20))(plVar11,local_80,lVar8);
        lVar8 = local_88;
        ppppppuVar12 = *(undefined8 *******)(*(long *)(lVar7 + 8) + 0x40);
        plVar11 = (long *)(**(code **)(*local_80 + 0x60))();
        lVar8 = (**(code **)(*plVar11 + 0x20))(plVar11,local_80,lVar8);
        if (((ppppppuVar12 == (undefined8 ******)0x0) ||
            (iVar5 = *(int *)(*(long *)(lVar8 + 8) + 0x48), iVar5 - 0x81U < 0xffffff7d)) ||
           (uVar9 = FUN_1011afdac(iVar5), pppppppuVar13 = &local_70, pppppppuVar3 = local_70,
           (uVar9 & 1) == 0)) break;
joined_r0x00010292cea0:
        pppppppuVar14 = pppppppuVar13;
        if (pppppppuVar3 != (undefined8 *******)0x0) {
          do {
            pppppppuVar13 = pppppppuVar3;
            ppppppuVar10 = pppppppuVar13[4];
            if (ppppppuVar12 == ppppppuVar10) {
              iVar1 = *(int *)(pppppppuVar13 + 5);
              if (iVar5 < iVar1) goto LAB_10292cea8;
              if (iVar1 == iVar5 || iVar5 <= iVar1) goto LAB_10292ce0c;
            }
            else {
              if (ppppppuVar12 < ppppppuVar10) goto LAB_10292cea8;
              if (ppppppuVar12 <= ppppppuVar10) goto LAB_10292ce0c;
            }
            pppppppuVar3 = (undefined8 *******)pppppppuVar13[1];
            if ((undefined8 *******)pppppppuVar13[1] == (undefined8 *******)0x0) {
              pppppppuVar14 = pppppppuVar13 + 1;
              break;
            }
          } while( true );
        }
        ppppppuVar10 = operator_new(0x30);
        ppppppuVar10[4] = ppppppuVar12;
        *(int *)(ppppppuVar10 + 5) = iVar5;
        *ppppppuVar10 = (undefined8 *****)0x0;
        ppppppuVar10[1] = (undefined8 *****)0x0;
        ppppppuVar10[2] = pppppppuVar13;
        *pppppppuVar14 = ppppppuVar10;
        if ((undefined8 *******)*local_78 != (undefined8 *******)0x0) {
          ppppppuVar10 = *pppppppuVar14;
          local_78 = (undefined8 *******)*local_78;
        }
        FUN_100255d54(local_70,ppppppuVar10);
        local_68 = local_68 + 1;
LAB_10292ce0c:
        local_88 = *(long *)(local_88 + 0x18);
        if (local_88 == local_90) goto LAB_10292cf68;
      }
      plVar11 = (long *)(**(code **)(*local_80 + 0x60))();
      (**(code **)(*plVar11 + 0x18))(plVar11,local_80,&local_90);
    } while (local_88 != local_90);
  }
LAB_10292cf68:
  lVar8 = local_68;
  *(undefined1 *)(param_1 + 0x68) = uVar2;
  iVar5 = FUN_10156d4c8(*(undefined8 *)(param_1 + 0x30));
  if (lVar8 == iVar5) {
    FUN_10292d008(param_1);
    FUN_102931824(&local_78,local_70);
    return;
  }
  FUN_101488e64(param_2,
                "Multiple sets of per-note controller change events with the same note ID and CC number"
               );
                    /* WARNING: Does not return */
  pcVar4 = (code *)SoftwareBreakpoint(1,0x10292cfc8);
  (*pcVar4)();
LAB_10292cea8:
  pppppppuVar3 = (undefined8 *******)*pppppppuVar13;
  goto joined_r0x00010292cea0;
}

