// 0x10023af84 FUN_10023af84 state=exported-with-warnings body_bytes=1080 warnings=1 chunk=chunk-00097.jsonl

int FUN_10023af84(undefined8 param_1,undefined8 *param_2,undefined8 param_3)

{
  long *plVar1;
  undefined8 *puVar2;
  int iVar3;
  int iVar4;
  ulong uVar5;
  int *piVar6;
  long *plVar7;
  undefined8 uVar8;
  long lVar9;
  long lVar10;
  long *plVar11;
  long *plVar12;
  undefined8 *puVar13;
  int *local_e0;
  int *local_d8;
  int *local_d0;
  long *local_c8;
  long *local_c0;
  int local_b0 [2];
  undefined8 local_a8;
  int *local_a0;
  int *local_98;
  int *local_90;
  undefined8 *local_80;
  undefined8 *local_78;
  char local_69;
  undefined8 **local_68;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_100d60390;
  if (((DAT_100e72530 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_100e72530), iVar4 != 0)) {
    FUN_100240ba8();
    ___cxa_atexit(FUN_100245c78,&DAT_100e72538,0x100000000);
    ___cxa_guard_release(&DAT_100e72530);
  }
  FUN_100478cec(&local_98,&DAT_100e72538,param_3);
  local_78 = (undefined8 *)PTR_format_custom<TString>_100d60960;
  local_80 = param_2;
  FUN_10045e294(&local_a0,L"{}-files-",9,0xf,&local_80);
  local_b0[0] = 0;
  local_a8 = std::system_category();
  FUN_100297e50(&local_80,0x80000000,0);
  FUN_1006f0c44(&local_c8,param_1,0x42,&local_80,local_b0);
  if (local_68 == &local_80) {
    lVar10 = 0x20;
LAB_10023b05c:
    (**(code **)((long)*local_68 + lVar10))();
  }
  else if (local_68 != (undefined8 **)0x0) {
    lVar10 = 0x28;
    goto LAB_10023b05c;
  }
  plVar7 = local_c0;
  if (local_c8 == local_c0) {
    iVar4 = 0;
    plVar1 = local_c8;
    plVar11 = local_c0;
  }
  else {
    iVar4 = 0;
    plVar12 = local_c8;
    do {
      FUN_1006fb554(plVar12);
      FUN_1002a5210(&local_d0);
      iVar3 = FUN_100448e58(&local_d0,&local_a0);
      if (iVar3 != 0) {
        FUN_1002a0e40(&local_d8,&local_d0,0x1f);
        FUN_100446c84(&local_e0,"-");
        if (local_e0 == (int *)0x0) {
          lVar10 = -1;
        }
        else {
          lVar10 = (long)(local_e0[1] / 2 + -1);
        }
        FUN_100446db4(&local_80,&local_d8,local_e0 + 4,lVar10);
        if ((local_e0 != (int *)0x0) && (iVar3 = *local_e0, *local_e0 = iVar3 + -1, iVar3 + -1 == 0)
           ) {
          FUN_100469e84();
        }
        if ((long)local_78 - (long)local_80 == 0x18) {
          lVar10 = local_80[2];
          if (lVar10 == 0) {
            lVar9 = -1;
          }
          else {
            lVar9 = (long)(*(int *)(lVar10 + 4) / 2 + -1);
          }
          uVar5 = FUN_1001b2e54(lVar10 + 0x10,lVar9);
          if (((uVar5 >> 0x20 & 1) != 0) &&
             (iVar3 = (int)uVar5, piVar6 = local_98, iVar3 < (int)param_3)) {
            for (; piVar6 != local_90; piVar6 = piVar6 + 1) {
              if (*piVar6 == iVar3) {
                if (iVar4 <= iVar3) {
                  iVar4 = iVar3;
                }
                break;
              }
            }
          }
        }
        puVar2 = local_80;
        puVar13 = local_78;
        if (local_80 != (undefined8 *)0x0) {
          while (puVar13 != puVar2) {
            puVar13 = puVar13 + -1;
            piVar6 = (int *)*puVar13;
            if ((piVar6 != (int *)0x0) && (iVar3 = *piVar6, *piVar6 = iVar3 + -1, iVar3 + -1 == 0))
            {
              FUN_100469e84();
            }
          }
          local_78 = puVar2;
          operator_delete(local_80);
        }
        if ((local_d8 != (int *)0x0) && (iVar3 = *local_d8, *local_d8 = iVar3 + -1, iVar3 + -1 == 0)
           ) {
          FUN_100469e84();
        }
      }
      if ((local_d0 != (int *)0x0) && (iVar3 = *local_d0, *local_d0 = iVar3 + -1, iVar3 + -1 == 0))
      {
        FUN_100469e84();
      }
      plVar12 = plVar12 + 1;
      plVar1 = local_c8;
      plVar11 = local_c0;
    } while (plVar12 != plVar7);
  }
  if (plVar1 != (long *)0x0) {
    local_c8 = plVar1;
    if (plVar11 == plVar1) {
      operator_delete(plVar1);
    }
    else {
      do {
        plVar11 = plVar11 + -1;
        plVar7 = (long *)*plVar11;
        *plVar11 = 0;
        if (plVar7 != (long *)0x0) {
          (**(code **)(*plVar7 + 8))();
        }
      } while (plVar11 != plVar1);
      operator_delete(local_c8);
    }
  }
  if (local_b0[0] != 0) {
    uVar8 = std::chrono::system_clock::now();
    FUN_10073cdf4(&local_c8,4,uVar8);
    iVar3 = FUN_1007396c0(&local_c8);
    if (iVar3 != 0) {
      uVar8 = FUN_100736880(&local_c8,"Database: failed to scan for previous database version: ");
      std::error_code::message();
      FUN_100737760(uVar8,&local_80);
      if (local_69 < '\0') {
        operator_delete(local_80);
        thunk_FUN_1007363ec(&local_c8);
        goto joined_r0x00010023b374;
      }
    }
    thunk_FUN_1007363ec(&local_c8);
  }
joined_r0x00010023b374:
  if ((local_a0 != (int *)0x0) && (iVar3 = *local_a0, *local_a0 = iVar3 + -1, iVar3 + -1 == 0)) {
    FUN_100469e84();
  }
  if (local_98 != (int *)0x0) {
    local_90 = local_98;
    operator_delete(local_98);
  }
  if (*(long *)PTR____stack_chk_guard_100d60390 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return iVar4;
}

