
undefined8 * FUN_1011c1c24(undefined8 *param_1,char *param_2)

{
  undefined8 *****pppppuVar1;
  undefined8 *****pppppuVar2;
  ulong uVar3;
  undefined8 *****pppppuVar4;
  int iVar5;
  undefined4 uVar6;
  size_t sVar7;
  undefined8 *puVar8;
  undefined8 *****pppppuVar9;
  string *psVar10;
  ulong uVar11;
  undefined8 ****ppppuVar12;
  undefined8 ****ppppuVar13;
  string sVar14;
  string *local_140;
  ulong uStack_138;
  undefined8 local_130;
  undefined8 ****local_f8;
  ulong local_f0;
  undefined8 local_e8;
  undefined8 ****local_e0;
  undefined8 ****ppppuStack_d8;
  undefined8 uStack_d0;
  undefined1 local_c8;
  undefined7 uStack_c7;
  undefined1 uStack_c0;
  undefined1 auStack_bf [15];
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined1 local_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  char local_88;
  undefined1 local_80;
  undefined8 local_78;
  
  sVar7 = _strlen(param_2);
  if (0x7ffffffffffffff7 < sVar7) {
                    /* WARNING: Subroutine does not return */
    FUN_100234518(param_1);
  }
  if (sVar7 < 0x17) {
    *(char *)((long)param_1 + 0x17) = (char)sVar7;
    puVar8 = param_1;
    if (sVar7 != 0) goto LAB_1011c1ca8;
  }
  else {
    uVar11 = 0x19;
    if ((sVar7 | 7) != 0x17) {
      uVar11 = (sVar7 | 7) + 1;
    }
    puVar8 = operator_new(uVar11);
    param_1[1] = sVar7;
    param_1[2] = uVar11 | 0x8000000000000000;
    *param_1 = puVar8;
LAB_1011c1ca8:
    _memmove(puVar8,param_2,sVar7);
  }
  *(undefined1 *)((long)puVar8 + sVar7) = 0;
  puVar8 = param_1 + 3;
  *puVar8 = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  param_1[7] = 0x8000000080000000;
  param_1[6] = 0x8000000080000000;
  *(undefined4 *)(param_1 + 8) = 0;
  *(undefined1 *)((long)param_1 + 0x44) = 0;
  if (((DAT_106f4de98 & 1) == 0) && (iVar5 = ___cxa_guard_acquire(&DAT_106f4de98), iVar5 != 0)) {
    FUN_10034c66c(&DAT_106f4dea8,"(\\d+)\\.(\\d+)(?:\\.(\\d+))?(?:([dab])(\\d+))?(?: (.*))?",0);
    ___cxa_atexit(FUN_10034c610,&DAT_106f4dea8,0x100000000);
    ___cxa_guard_release(&DAT_106f4de98);
  }
  local_b0 = 0;
  uStack_a8 = 0;
  local_a0 = 0;
  local_98 = 0;
  uStack_90 = 0;
  local_88 = '\0';
  local_80 = 0;
  local_78 = 0;
  ppppuStack_d8 = (undefined8 ****)0x0;
  local_e0 = (undefined8 *****)0x0;
  local_c8 = 0;
  uStack_d0 = 0;
  auStack_bf._0_8_ = 0;
  uStack_c7 = 0;
  uStack_c0 = 0;
  sVar7 = _strlen(param_2);
  iVar5 = FUN_100355794(&DAT_106f4dea8,param_2,param_2 + sVar7,&local_e0,0x1040);
  if ((iVar5 == 0) || (local_88 == '\x01')) {
    *(undefined1 *)((long)param_1 + 0x44) = 0;
    goto LAB_1011c1d48;
  }
  *(undefined1 *)((long)param_1 + 0x44) = 1;
  uVar11 = ((long)ppppuStack_d8 - (long)local_e0 >> 3) * -0x5555555555555555;
  pppppuVar2 = (undefined8 *****)local_e0;
  if (uVar11 < 2) {
    pppppuVar2 = &local_e0;
  }
  if (*(char *)(pppppuVar2 + 5) == '\x01') {
    pppppuVar2 = (undefined8 *****)local_e0;
    if (uVar11 < 2) {
      pppppuVar2 = &local_e0;
    }
    ppppuVar12 = pppppuVar2[3];
    ppppuVar13 = pppppuVar2[4];
    uVar11 = (long)ppppuVar13 - (long)ppppuVar12;
    if (0x7ffffffffffffff7 < uVar11) {
                    /* WARNING: Subroutine does not return */
      FUN_100234518(&local_140);
    }
    if (uVar11 < 0x17) {
      local_130 = CONCAT17((char)uVar11,(undefined7)local_130);
      psVar10 = (string *)&local_140;
    }
    else {
      uVar3 = 0x19;
      if ((uVar11 | 7) != 0x17) {
        uVar3 = (uVar11 | 7) + 1;
      }
      psVar10 = operator_new(uVar3);
      local_130 = uVar3 | 0x8000000000000000;
      uStack_138 = uVar11;
      local_140 = psVar10;
    }
    if (ppppuVar13 != ppppuVar12) {
      _memmove(psVar10,ppppuVar12,uVar11);
    }
    psVar10[uVar11] = (string)0x0;
  }
  else {
    local_140 = (string *)0x0;
    uStack_138 = 0;
    local_130 = 0;
  }
  uVar6 = std::stoi((string *)&local_140,(ulong *)0x0,10);
  pppppuVar2 = (undefined8 *****)(auStack_bf + 7);
  *(undefined4 *)(param_1 + 6) = uVar6;
  if ((long)local_130 < 0) {
    operator_delete(local_140);
  }
  uVar11 = ((long)ppppuStack_d8 - (long)local_e0 >> 3) * -0x5555555555555555;
  pppppuVar9 = (undefined8 *****)(local_e0 + 8);
  if (uVar11 < 3) {
    pppppuVar9 = pppppuVar2;
  }
  if (*(char *)pppppuVar9 == '\x01') {
    pppppuVar9 = (undefined8 *****)(local_e0 + 6);
    if (uVar11 < 3) {
      pppppuVar9 = (undefined8 *****)&local_c8;
    }
    ppppuVar12 = *pppppuVar9;
    pppppuVar9 = (undefined8 *****)(local_e0 + 7);
    if (uVar11 < 3) {
      pppppuVar9 = (undefined8 *****)&uStack_c0;
    }
    ppppuVar13 = *pppppuVar9;
    uVar11 = (long)ppppuVar13 - (long)ppppuVar12;
    if (0x7ffffffffffffff7 < uVar11) {
                    /* WARNING: Subroutine does not return */
      FUN_100234518(&local_140);
    }
    if (uVar11 < 0x17) {
      local_130 = CONCAT17((char)uVar11,(undefined7)local_130);
      psVar10 = (string *)&local_140;
    }
    else {
      uVar3 = 0x19;
      if ((uVar11 | 7) != 0x17) {
        uVar3 = (uVar11 | 7) + 1;
      }
      psVar10 = operator_new(uVar3);
      local_130 = uVar3 | 0x8000000000000000;
      uStack_138 = uVar11;
      local_140 = psVar10;
    }
    if (ppppuVar13 != ppppuVar12) {
      _memmove(psVar10,ppppuVar12,uVar11);
    }
    psVar10[uVar11] = (string)0x0;
  }
  else {
    local_140 = (string *)0x0;
    uStack_138 = 0;
    local_130 = 0;
  }
  uVar6 = std::stoi((string *)&local_140,(ulong *)0x0,10);
  *(undefined4 *)((long)param_1 + 0x34) = uVar6;
  if ((long)local_130 < 0) {
    operator_delete(local_140);
  }
  uVar11 = ((long)ppppuStack_d8 - (long)local_e0 >> 3) * -0x5555555555555555;
  pppppuVar9 = (undefined8 *****)(local_e0 + 0xb);
  pppppuVar4 = (undefined8 *****)(local_e0 + 9);
  if (uVar11 < 4) {
    pppppuVar9 = pppppuVar2;
    pppppuVar4 = (undefined8 *****)&local_c8;
  }
  if (*(char *)pppppuVar9 == '\x01') {
    ppppuVar12 = *pppppuVar4;
    pppppuVar1 = (undefined8 *****)(local_e0 + 10);
    if (uVar11 < 4) {
      pppppuVar1 = (undefined8 *****)&uStack_c0;
    }
    ppppuVar13 = *pppppuVar1;
    uVar11 = (long)ppppuVar13 - (long)ppppuVar12;
    if (0x7ffffffffffffff7 < uVar11) {
                    /* WARNING: Subroutine does not return */
      FUN_100234518(&local_140);
    }
    if (uVar11 < 0x17) {
      local_130 = CONCAT17((char)uVar11,(undefined7)local_130);
      psVar10 = (string *)&local_140;
    }
    else {
      uVar3 = 0x19;
      if ((uVar11 | 7) != 0x17) {
        uVar3 = (uVar11 | 7) + 1;
      }
      psVar10 = operator_new(uVar3);
      local_130 = uVar3 | 0x8000000000000000;
      uStack_138 = uVar11;
      local_140 = psVar10;
    }
    if (ppppuVar13 != ppppuVar12) {
      _memmove(psVar10,ppppuVar12,uVar11);
    }
    psVar10[uVar11] = (string)0x0;
    uVar11 = uStack_138;
    if (-1 < (long)local_130) {
      uVar11 = local_130 >> 0x38;
    }
    if (uVar11 == 0) goto LAB_1011c1fe4;
    if (*(char *)pppppuVar9 == '\x01') {
      ppppuVar12 = *pppppuVar4;
      ppppuVar13 = *pppppuVar1;
      uVar11 = (long)ppppuVar13 - (long)ppppuVar12;
      if (0x7ffffffffffffff7 < uVar11) {
                    /* WARNING: Subroutine does not return */
        FUN_100234518(&local_f8);
      }
      if (uVar11 < 0x17) {
        local_e8 = CONCAT17((char)uVar11,(undefined7)local_e8);
        pppppuVar9 = &local_f8;
      }
      else {
        uVar3 = 0x19;
        if ((uVar11 | 7) != 0x17) {
          uVar3 = (uVar11 | 7) + 1;
        }
        pppppuVar9 = operator_new(uVar3);
        local_e8 = uVar3 | 0x8000000000000000;
        local_f8 = pppppuVar9;
        local_f0 = uVar11;
      }
      if (ppppuVar13 != ppppuVar12) {
        _memmove(pppppuVar9,ppppuVar12,uVar11);
      }
      *(undefined1 *)((long)pppppuVar9 + uVar11) = 0;
    }
    else {
      local_f8 = (undefined8 *****)0x0;
      local_f0 = 0;
      local_e8 = 0;
    }
    uVar6 = std::stoi((string *)&local_f8,(ulong *)0x0,10);
    *(undefined4 *)(param_1 + 7) = uVar6;
    if ((long)local_e8 < 0) {
      operator_delete(local_f8);
    }
  }
  else {
    local_140 = (string *)0x0;
    uStack_138 = 0;
    local_130 = 0;
LAB_1011c1fe4:
    *(undefined4 *)(param_1 + 7) = 0;
  }
  if ((long)local_130 < 0) {
    operator_delete(local_140);
  }
  uVar11 = ((long)ppppuStack_d8 - (long)local_e0 >> 3) * -0x5555555555555555;
  pppppuVar9 = (undefined8 *****)(local_e0 + 0xe);
  if (uVar11 < 5) {
    pppppuVar9 = pppppuVar2;
  }
  if (*(char *)pppppuVar9 == '\x01') {
    pppppuVar9 = (undefined8 *****)(local_e0 + 0xc);
    if (uVar11 < 5) {
      pppppuVar9 = (undefined8 *****)&local_c8;
    }
    ppppuVar12 = *pppppuVar9;
    pppppuVar9 = (undefined8 *****)(local_e0 + 0xd);
    if (uVar11 < 5) {
      pppppuVar9 = (undefined8 *****)&uStack_c0;
    }
    ppppuVar13 = *pppppuVar9;
    uVar11 = (long)ppppuVar13 - (long)ppppuVar12;
    if (0x7ffffffffffffff7 < uVar11) {
                    /* WARNING: Subroutine does not return */
      FUN_100234518(&local_140);
    }
    if (uVar11 < 0x17) {
      local_130 = CONCAT17((char)uVar11,(undefined7)local_130);
      psVar10 = (string *)&local_140;
    }
    else {
      uVar3 = 0x19;
      if ((uVar11 | 7) != 0x17) {
        uVar3 = (uVar11 | 7) + 1;
      }
      psVar10 = operator_new(uVar3);
      local_130 = uVar3 | 0x8000000000000000;
      local_140 = psVar10;
    }
    if (ppppuVar13 != ppppuVar12) {
      _memmove(psVar10,ppppuVar12,uVar11);
    }
    psVar10[uVar11] = (string)0x0;
    if ((long)local_130 < 0) {
      sVar14 = *local_140;
      operator_delete(local_140);
    }
    else {
      sVar14 = local_140._0_1_;
    }
    if (sVar14 == (string)0x0) goto LAB_1011c22b8;
    uVar11 = ((long)ppppuStack_d8 - (long)local_e0 >> 3) * -0x5555555555555555;
    pppppuVar9 = (undefined8 *****)(local_e0 + 0x11);
    if (uVar11 < 6) {
      pppppuVar9 = pppppuVar2;
    }
    if (*(char *)pppppuVar9 == '\x01') {
      pppppuVar9 = (undefined8 *****)(local_e0 + 0xf);
      if (uVar11 < 6) {
        pppppuVar9 = (undefined8 *****)&local_c8;
      }
      ppppuVar12 = *pppppuVar9;
      pppppuVar9 = (undefined8 *****)(local_e0 + 0x10);
      if (uVar11 < 6) {
        pppppuVar9 = (undefined8 *****)&uStack_c0;
      }
      ppppuVar13 = *pppppuVar9;
      uVar11 = (long)ppppuVar13 - (long)ppppuVar12;
      if (0x7ffffffffffffff7 < uVar11) {
                    /* WARNING: Subroutine does not return */
        FUN_100234518(&local_140);
      }
      if (uVar11 < 0x17) {
        local_130 = CONCAT17((char)uVar11,(undefined7)local_130);
        psVar10 = (string *)&local_140;
      }
      else {
        uVar3 = 0x19;
        if ((uVar11 | 7) != 0x17) {
          uVar3 = (uVar11 | 7) + 1;
        }
        psVar10 = operator_new(uVar3);
        local_130 = uVar3 | 0x8000000000000000;
        local_140 = psVar10;
        uStack_138 = uVar11;
      }
      if (ppppuVar13 != ppppuVar12) {
        _memmove(psVar10,ppppuVar12,uVar11);
      }
      psVar10[uVar11] = (string)0x0;
    }
    else {
      local_140 = (string *)0x0;
      uStack_138 = 0;
      local_130 = 0;
    }
    uVar6 = std::stoi((string *)&local_140,(ulong *)0x0,10);
    *(undefined4 *)((long)param_1 + 0x3c) = uVar6;
    if ((long)local_130 < 0) {
      operator_delete(local_140);
    }
  }
  else {
    local_140 = (string *)0x0;
    uStack_138 = 0;
    local_130 = 0;
    sVar14 = (string)0x0;
LAB_1011c22b8:
    *(undefined4 *)((long)param_1 + 0x3c) = 0;
  }
  uVar11 = ((long)ppppuStack_d8 - (long)local_e0 >> 3) * -0x5555555555555555;
  pppppuVar9 = (undefined8 *****)(local_e0 + 0x14);
  if (uVar11 < 7) {
    pppppuVar9 = pppppuVar2;
  }
  if (*(char *)pppppuVar9 == '\x01') {
    pppppuVar2 = (undefined8 *****)(local_e0 + 0x12);
    if (uVar11 < 7) {
      pppppuVar2 = (undefined8 *****)&local_c8;
    }
    ppppuVar12 = *pppppuVar2;
    pppppuVar2 = (undefined8 *****)(local_e0 + 0x13);
    if (uVar11 < 7) {
      pppppuVar2 = (undefined8 *****)&uStack_c0;
    }
    ppppuVar13 = *pppppuVar2;
    uVar11 = (long)ppppuVar13 - (long)ppppuVar12;
    if (0x7ffffffffffffff7 < uVar11) {
                    /* WARNING: Subroutine does not return */
      FUN_100234518(&local_140);
    }
    if (uVar11 < 0x17) {
      local_130 = CONCAT17((char)uVar11,(undefined7)local_130);
      psVar10 = (string *)&local_140;
    }
    else {
      uVar3 = 0x19;
      if ((uVar11 | 7) != 0x17) {
        uVar3 = (uVar11 | 7) + 1;
      }
      psVar10 = operator_new(uVar3);
      local_130 = uVar3 | 0x8000000000000000;
      uStack_138 = uVar11;
      local_140 = psVar10;
    }
    if (ppppuVar13 != ppppuVar12) {
      _memmove(psVar10,ppppuVar12,uVar11);
    }
    psVar10[uVar11] = (string)0x0;
    if (-1 < *(char *)((long)param_1 + 0x2f)) goto LAB_1011c23dc;
LAB_1011c240c:
    operator_delete((void *)*puVar8);
    param_1[4] = uStack_138;
    *puVar8 = local_140;
    param_1[5] = local_130;
    if ((byte)sVar14 < 0x62) goto LAB_1011c23f4;
LAB_1011c242c:
    if (sVar14 == (string)0x62) {
      *(undefined4 *)(param_1 + 8) = 3;
      goto LAB_1011c1d48;
    }
    if (sVar14 == (string)0x64) {
      *(undefined4 *)(param_1 + 8) = 1;
      goto LAB_1011c1d48;
    }
  }
  else {
    local_140 = (string *)0x0;
    uStack_138 = 0;
    local_130 = 0;
    if (*(char *)((long)param_1 + 0x2f) < '\0') goto LAB_1011c240c;
LAB_1011c23dc:
    param_1[4] = uStack_138;
    *puVar8 = local_140;
    param_1[5] = local_130;
    if (0x61 < (byte)sVar14) goto LAB_1011c242c;
LAB_1011c23f4:
    if (sVar14 == (string)0x0) {
      *(undefined4 *)(param_1 + 8) = 4;
      goto LAB_1011c1d48;
    }
    if (sVar14 == (string)0x61) {
      *(undefined4 *)(param_1 + 8) = 2;
      goto LAB_1011c1d48;
    }
  }
  *(undefined4 *)(param_1 + 8) = 0;
LAB_1011c1d48:
  if ((undefined8 *****)local_e0 != (undefined8 *****)0x0) {
    ppppuStack_d8 = local_e0;
    operator_delete(local_e0);
  }
  return param_1;
}

