
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 *
FUN_1011c2bb0(undefined1 *param_1,char *param_2,char *param_3,char *param_4,char *param_5,
             undefined4 param_6,undefined4 param_7)

{
  ulong uVar1;
  ulong uVar2;
  undefined8 uVar3;
  bool bVar4;
  size_t sVar5;
  undefined1 *puVar6;
  undefined8 ****ppppuVar7;
  undefined8 *puVar8;
  undefined8 *puVar9;
  undefined8 *puVar10;
  char *pcVar11;
  undefined8 *puVar12;
  ulong *puVar13;
  char cVar14;
  undefined1 *puVar15;
  long lVar16;
  byte bVar17;
  ulong uVar18;
  undefined8 uVar19;
  undefined8 uVar20;
  undefined2 local_98;
  undefined6 uStack_96;
  char local_81;
  undefined8 ***local_80;
  ulong uStack_78;
  undefined8 local_70;
  
  puVar15 = param_1 + 8;
  *param_1 = 0;
  sVar5 = _strlen(param_4);
  if (0x7ffffffffffffff7 < sVar5) {
                    /* WARNING: Subroutine does not return */
    FUN_100234518(puVar15);
  }
  if (sVar5 < 0x17) {
    param_1[0x1f] = (char)sVar5;
    puVar6 = puVar15;
    if (sVar5 != 0) goto LAB_1011c2c58;
  }
  else {
    uVar18 = 0x19;
    if ((sVar5 | 7) != 0x17) {
      uVar18 = (sVar5 | 7) + 1;
    }
    puVar6 = operator_new(uVar18);
    *(size_t *)(param_1 + 0x10) = sVar5;
    *(ulong *)(param_1 + 0x18) = uVar18 | 0x8000000000000000;
    *(undefined1 **)(param_1 + 8) = puVar6;
LAB_1011c2c58:
    _memmove(puVar6,param_4,sVar5);
  }
  puVar6[sVar5] = 0;
  puVar6 = param_1 + 0x20;
  sVar5 = _strlen(param_5);
  if (0x7ffffffffffffff7 < sVar5) {
                    /* WARNING: Subroutine does not return */
    FUN_100234518(puVar6);
  }
  if (sVar5 < 0x17) {
    param_1[0x37] = (char)sVar5;
    if (sVar5 != 0) goto LAB_1011c2cc4;
  }
  else {
    uVar18 = 0x19;
    if ((sVar5 | 7) != 0x17) {
      uVar18 = (sVar5 | 7) + 1;
    }
    puVar6 = operator_new(uVar18);
    *(size_t *)(param_1 + 0x28) = sVar5;
    *(ulong *)(param_1 + 0x30) = uVar18 | 0x8000000000000000;
    *(undefined1 **)(param_1 + 0x20) = puVar6;
LAB_1011c2cc4:
    _memmove(puVar6,param_5,sVar5);
  }
  puVar6[sVar5] = 0;
  puVar12 = (undefined8 *)(param_1 + 0x38);
  sVar5 = _strlen(param_3);
  if (0x7ffffffffffffff7 < sVar5) {
                    /* WARNING: Subroutine does not return */
    FUN_100234518(puVar12);
  }
  if (sVar5 < 0x17) {
    param_1[0x4f] = (char)sVar5;
    puVar8 = puVar12;
    if (sVar5 != 0) goto LAB_1011c2d34;
  }
  else {
    uVar18 = 0x19;
    if ((sVar5 | 7) != 0x17) {
      uVar18 = (sVar5 | 7) + 1;
    }
    puVar8 = operator_new(uVar18);
    *(size_t *)(param_1 + 0x40) = sVar5;
    *(ulong *)(param_1 + 0x48) = uVar18 | 0x8000000000000000;
    *(undefined8 **)(param_1 + 0x38) = puVar8;
LAB_1011c2d34:
    _memmove(puVar8,param_3,sVar5);
  }
  *(undefined1 *)((long)puVar8 + sVar5) = 0;
  bVar17 = param_1[0x4f];
  sVar5 = *(size_t *)(param_1 + 0x40);
  if (-1 < (char)bVar17) {
    sVar5 = (ulong)bVar17;
  }
  uVar18 = sVar5 + 1;
  if (0x7ffffffffffffff7 < uVar18) {
                    /* WARNING: Subroutine does not return */
    FUN_100234518(&local_80);
  }
  if (uVar18 < 0x17) {
    uStack_78 = 0;
    local_80 = (undefined8 ****)0x0;
    ppppuVar7 = &local_80;
    local_70 = uVar18 << 0x38;
    if (sVar5 != 0) goto LAB_1011c2db0;
  }
  else {
    uVar1 = 0x19;
    if ((uVar18 | 7) != 0x17) {
      uVar1 = (uVar18 | 7) + 1;
    }
    ppppuVar7 = operator_new(uVar1);
    local_70 = uVar1 | 0x8000000000000000;
    local_80 = ppppuVar7;
    uStack_78 = uVar18;
LAB_1011c2db0:
    puVar8 = (undefined8 *)*puVar12;
    if (-1 < (char)bVar17) {
      puVar8 = puVar12;
    }
    _memmove(ppppuVar7,puVar8,sVar5);
  }
  *(undefined2 *)((long)ppppuVar7 + sVar5) = 0x20;
  puVar6 = *(undefined1 **)(param_1 + 8);
  if (-1 < (char)param_1[0x1f]) {
    puVar6 = puVar15;
  }
  puVar8 = (undefined8 *)std::string::append((char *)&local_80,(ulong)puVar6);
  uVar20 = puVar8[1];
  uVar19 = *puVar8;
  *(undefined8 *)(param_1 + 0x60) = puVar8[2];
  *(undefined8 *)(param_1 + 0x58) = uVar20;
  *(undefined8 *)(param_1 + 0x50) = uVar19;
  puVar8[1] = 0;
  puVar8[2] = 0;
  *puVar8 = 0;
  if ((long)local_70 < 0) {
    operator_delete(local_80);
  }
  puVar8 = (undefined8 *)(param_1 + 0x68);
  sVar5 = _strlen(param_2);
  if (0x7ffffffffffffff7 < sVar5) {
                    /* WARNING: Subroutine does not return */
    FUN_100234518(puVar8);
  }
  if (sVar5 < 0x17) {
    param_1[0x7f] = (char)sVar5;
    puVar9 = puVar8;
    if (sVar5 != 0) goto LAB_1011c2e7c;
  }
  else {
    uVar18 = 0x19;
    if ((sVar5 | 7) != 0x17) {
      uVar18 = (sVar5 | 7) + 1;
    }
    puVar9 = operator_new(uVar18);
    *(size_t *)(param_1 + 0x70) = sVar5;
    *(ulong *)(param_1 + 0x78) = uVar18 | 0x8000000000000000;
    *(undefined8 **)(param_1 + 0x68) = puVar9;
LAB_1011c2e7c:
    _memmove(puVar9,param_2,sVar5);
  }
  *(undefined1 *)((long)puVar9 + sVar5) = 0;
  bVar17 = param_1[0x7f];
  sVar5 = *(size_t *)(param_1 + 0x70);
  if (-1 < (char)bVar17) {
    sVar5 = (ulong)bVar17;
  }
  uVar18 = sVar5 + 1;
  if (0x7ffffffffffffff7 < uVar18) {
                    /* WARNING: Subroutine does not return */
    FUN_100234518(&local_80);
  }
  if (uVar18 < 0x17) {
    uStack_78 = 0;
    local_80 = (undefined8 ****)0x0;
    ppppuVar7 = &local_80;
    local_70 = uVar18 << 0x38;
    if (sVar5 != 0) goto LAB_1011c2efc;
  }
  else {
    uVar1 = 0x19;
    if ((uVar18 | 7) != 0x17) {
      uVar1 = (uVar18 | 7) + 1;
    }
    ppppuVar7 = operator_new(uVar1);
    local_70 = uVar1 | 0x8000000000000000;
    local_80 = ppppuVar7;
    uStack_78 = uVar18;
LAB_1011c2efc:
    puVar9 = (undefined8 *)*puVar8;
    if (-1 < (char)bVar17) {
      puVar9 = puVar8;
    }
    _memmove(ppppuVar7,puVar9,sVar5);
  }
  *(undefined2 *)((long)ppppuVar7 + sVar5) = 0x20;
  puVar8 = *(undefined8 **)(param_1 + 0x38);
  if (-1 < (char)param_1[0x4f]) {
    puVar8 = puVar12;
  }
  puVar8 = (undefined8 *)std::string::append((char *)&local_80,(ulong)puVar8);
  uVar20 = puVar8[1];
  uVar19 = *puVar8;
  *(undefined8 *)(param_1 + 0x90) = puVar8[2];
  *(undefined8 *)(param_1 + 0x88) = uVar20;
  *(undefined8 *)(param_1 + 0x80) = uVar19;
  puVar8[1] = 0;
  puVar8[2] = 0;
  *puVar8 = 0;
  if ((long)local_70 < 0) {
    operator_delete(local_80);
  }
  puVar8 = (undefined8 *)(param_1 + 0x98);
  param_1[0xaf] = 0x15;
  uVar19 = s_2026_07_07_e3d8be4d07_105b6825a._0_8_;
  *(ulong *)(param_1 + 0xa0) =
       CONCAT35(s_2026_07_07_e3d8be4d07_105b6825a._13_3_,s_2026_07_07_e3d8be4d07_105b6825a._8_5_);
  *(undefined8 *)(param_1 + 0x98) = uVar19;
  *(ulong *)(param_1 + 0xa5) =
       CONCAT53(s_2026_07_07_e3d8be4d07_105b6825a._16_5_,s_2026_07_07_e3d8be4d07_105b6825a._13_3_);
  param_1[0xad] = 0;
  local_70._7_1_ = '\a';
  local_80 = (undefined8 ***)0x203a646c697542;
  puVar10 = (undefined8 *)std::string::append((char *)&local_80,(ulong)puVar8);
  puVar9 = (undefined8 *)(param_1 + 0xb0);
  uVar20 = puVar10[1];
  uVar19 = *puVar10;
  *(undefined8 *)(param_1 + 0xc0) = puVar10[2];
  *(undefined8 *)(param_1 + 0xb8) = uVar20;
  *puVar9 = uVar19;
  puVar10[1] = 0;
  puVar10[2] = 0;
  *puVar10 = 0;
  if (local_70._7_1_ < '\0') {
    operator_delete(local_80);
  }
  pcVar11 = operator_new(0x30);
  *(char **)(param_1 + 200) = pcVar11;
  uVar19 = _DAT_1055cdf20;
  *(undefined8 *)(param_1 + 0xd8) = _UNK_1055cdf28;
  *(undefined8 *)(param_1 + 0xd0) = uVar19;
  uVar3 = s_e3d8be4d07c71dbd4de9e4183bf90652_105b6b9b2._24_8_;
  uVar20 = s_e3d8be4d07c71dbd4de9e4183bf90652_105b6b9b2._16_8_;
  uVar19 = s_e3d8be4d07c71dbd4de9e4183bf90652_105b6b9b2._0_8_;
  *(undefined8 *)(pcVar11 + 8) = s_e3d8be4d07c71dbd4de9e4183bf90652_105b6b9b2._8_8_;
  *(undefined8 *)pcVar11 = uVar19;
  *(undefined8 *)(pcVar11 + 0x18) = uVar3;
  *(undefined8 *)(pcVar11 + 0x10) = uVar20;
  *(undefined8 *)(pcVar11 + 0x20) = s_e3d8be4d07c71dbd4de9e4183bf90652_105b6b9b2._32_8_;
  pcVar11[0x28] = '\0';
  *(undefined4 *)(param_1 + 0xe0) = param_7;
  *(undefined4 *)(param_1 + 0xe4) = param_6;
  param_1[0xe8] = 1;
  FUN_1011c1c24(param_1 + 0xf0,param_4);
  bVar17 = param_1[0x4f];
  sVar5 = *(size_t *)(param_1 + 0x40);
  if (-1 < (char)bVar17) {
    sVar5 = (ulong)bVar17;
  }
  uVar18 = sVar5 + 1;
  if (0x7ffffffffffffff7 < uVar18) {
                    /* WARNING: Subroutine does not return */
    FUN_100234518(&local_80);
  }
  if (uVar18 < 0x17) {
    uStack_78 = 0;
    local_80 = (undefined8 ****)0x0;
    ppppuVar7 = &local_80;
    local_70 = uVar18 << 0x38;
    if (sVar5 != 0) goto LAB_1011c30a4;
  }
  else {
    uVar1 = 0x19;
    if ((uVar18 | 7) != 0x17) {
      uVar1 = (uVar18 | 7) + 1;
    }
    ppppuVar7 = operator_new(uVar1);
    local_70 = uVar1 | 0x8000000000000000;
    local_80 = ppppuVar7;
    uStack_78 = uVar18;
LAB_1011c30a4:
    puVar10 = (undefined8 *)*puVar12;
    if (-1 < (char)bVar17) {
      puVar10 = puVar12;
    }
    _memmove(ppppuVar7,puVar10,sVar5);
  }
  *(undefined2 *)((long)ppppuVar7 + sVar5) = 0x5f;
  puVar6 = *(undefined1 **)(param_1 + 8);
  if (-1 < (char)param_1[0x1f]) {
    puVar6 = puVar15;
  }
  puVar12 = (undefined8 *)std::string::append((char *)&local_80,(ulong)puVar6);
  uVar20 = puVar12[1];
  uVar19 = *puVar12;
  *(undefined8 *)(param_1 + 0x148) = puVar12[2];
  *(undefined8 *)(param_1 + 0x140) = uVar20;
  *(undefined8 *)(param_1 + 0x138) = uVar19;
  puVar12[1] = 0;
  puVar12[2] = 0;
  *puVar12 = 0;
  if ((long)local_70 < 0) {
    operator_delete(local_80);
    bVar17 = param_1[0xaf];
    uVar18 = *(ulong *)(param_1 + 0xa0);
    if (-1 < (char)bVar17) {
      uVar18 = (ulong)bVar17;
    }
    if (uVar18 != 0) goto LAB_1011c3148;
LAB_1011c31b8:
    bVar17 = param_1[199];
    uVar18 = *(ulong *)(param_1 + 0xb8);
    if (-1 < (char)bVar17) {
      uVar18 = (ulong)bVar17;
    }
    if (uVar18 != 0) goto LAB_1011c31d0;
LAB_1011c3278:
    local_70 = local_70 & 0xffffffffffffff;
    local_80 = (undefined8 ***)((ulong)local_80 & 0xffffffffffffff00);
  }
  else {
    bVar17 = param_1[0xaf];
    uVar18 = *(ulong *)(param_1 + 0xa0);
    if (-1 < (char)bVar17) {
      uVar18 = (ulong)bVar17;
    }
    if (uVar18 == 0) goto LAB_1011c31b8;
LAB_1011c3148:
    local_81 = '\x01';
    local_98 = 0x5f;
    puVar12 = (undefined8 *)*puVar8;
    if (-1 < (char)bVar17) {
      puVar12 = puVar8;
    }
    puVar13 = (ulong *)std::string::append((char *)&local_98,(ulong)puVar12);
    uStack_78 = puVar13[1];
    local_80 = (undefined8 ***)*puVar13;
    local_70 = puVar13[2];
    puVar13[1] = 0;
    puVar13[2] = 0;
    *puVar13 = 0;
    ppppuVar7 = (undefined8 ****)local_80;
    if (-1 < (long)local_70) {
      ppppuVar7 = &local_80;
    }
    std::string::append(param_1 + 0x138,(ulong)ppppuVar7);
    if ((long)local_70 < 0) {
      operator_delete(local_80);
    }
    if (-1 < local_81) goto LAB_1011c31b8;
    operator_delete((void *)CONCAT62(uStack_96,local_98));
    bVar17 = param_1[199];
    uVar18 = *(ulong *)(param_1 + 0xb8);
    if (-1 < (char)bVar17) {
      uVar18 = (ulong)bVar17;
    }
    if (uVar18 == 0) goto LAB_1011c3278;
LAB_1011c31d0:
    uVar1 = uVar18 + 1;
    if (0x7ffffffffffffff7 < uVar1) {
                    /* WARNING: Subroutine does not return */
      FUN_100234518(&local_80);
    }
    if (uVar1 < 0x17) {
      uStack_78 = 0;
      local_80 = (undefined8 ****)0x0;
      ppppuVar7 = &local_80;
      local_70 = uVar1 << 0x38;
    }
    else {
      uVar2 = 0x19;
      if ((uVar1 | 7) != 0x17) {
        uVar2 = (uVar1 | 7) + 1;
      }
      ppppuVar7 = operator_new(uVar2);
      local_70 = uVar2 | 0x8000000000000000;
      local_80 = ppppuVar7;
      uStack_78 = uVar1;
    }
    *(undefined1 *)ppppuVar7 = 0x20;
    puVar12 = (undefined8 *)*puVar9;
    if (-1 < (char)bVar17) {
      puVar12 = puVar9;
    }
    _memmove((undefined1 *)((long)ppppuVar7 + 1),puVar12,uVar18);
    ((undefined1 *)((long)ppppuVar7 + 1))[uVar18] = 0;
  }
  puVar12 = *(undefined8 **)(param_1 + 0x50);
  if (-1 < (char)param_1[0x67]) {
    puVar12 = (undefined8 *)(param_1 + 0x50);
  }
  puVar12 = (undefined8 *)std::string::insert((ulong)&local_80,(char *)0x0,(ulong)puVar12);
  uVar20 = puVar12[1];
  uVar19 = *puVar12;
  *(undefined8 *)(param_1 + 0x160) = puVar12[2];
  *(undefined8 *)(param_1 + 0x158) = uVar20;
  *(undefined8 *)(param_1 + 0x150) = uVar19;
  puVar12[1] = 0;
  puVar12[2] = 0;
  *puVar12 = 0;
  if ((long)local_70 < 0) {
    operator_delete(local_80);
    cVar14 = param_1[0x1f];
    if (-1 < cVar14) goto LAB_1011c32d0;
LAB_1011c32e8:
    bVar4 = false;
    if (*(long *)(param_1 + 0x10) == 0) goto LAB_1011c3374;
  }
  else {
    cVar14 = param_1[0x1f];
    if (cVar14 < '\0') goto LAB_1011c32e8;
LAB_1011c32d0:
    if (cVar14 == '\0') {
      bVar4 = false;
      goto LAB_1011c3374;
    }
  }
  lVar16 = (long)(char)param_1[0x37];
  if (lVar16 < 0) {
    lVar16 = *(long *)(param_1 + 0x28);
  }
  bVar4 = false;
  if (lVar16 != 0) {
    lVar16 = (long)(char)param_1[0x4f];
    if (lVar16 < 0) {
      lVar16 = *(long *)(param_1 + 0x40);
    }
    bVar4 = false;
    if (lVar16 != 0) {
      lVar16 = (long)(char)param_1[0x67];
      if (lVar16 < 0) {
        lVar16 = *(long *)(param_1 + 0x58);
      }
      bVar4 = false;
      if (lVar16 != 0) {
        lVar16 = (long)(char)param_1[0x7f];
        if (lVar16 < 0) {
          lVar16 = *(long *)(param_1 + 0x70);
        }
        bVar4 = false;
        if (lVar16 != 0) {
          lVar16 = (long)(char)param_1[0x97];
          if (lVar16 < 0) {
            lVar16 = *(long *)(param_1 + 0x88);
          }
          bVar4 = false;
          if (lVar16 != 0) {
            if ((param_1[0x134] == '\x01') && (*(int *)(param_1 + 0xe4) - 1U < 4)) {
              bVar4 = *(int *)(param_1 + 0xe0) != -0x80000000;
            }
            else {
              bVar4 = false;
            }
          }
        }
      }
    }
  }
LAB_1011c3374:
  *param_1 = bVar4;
  return param_1;
}

