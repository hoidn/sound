// 0x10023a970 FUN_10023a970 state=exported-with-warnings body_bytes=1296 warnings=1 chunk=chunk-00097.jsonl

undefined8 FUN_10023a970(byte *param_1)

{
  undefined4 uVar1;
  undefined8 ****ppppuVar2;
  int iVar3;
  char *pcVar4;
  size_t sVar5;
  int ****ppppiVar6;
  ulong uVar7;
  undefined8 uVar8;
  ulong extraout_x1;
  byte *pbVar9;
  int *local_98;
  int ***local_90;
  size_t sStack_88;
  undefined8 local_80;
  int ***local_70;
  size_t sStack_68;
  undefined8 local_60;
  undefined8 ***local_58;
  ulong uStack_50;
  undefined7 local_48;
  byte bStack_41;
  
  if ((*param_1 & 1) != 0) {
    return 0;
  }
  FUN_10023a630(&local_70);
  uVar1 = *(undefined4 *)(param_1 + 0x1c0);
  pcVar4 = (char *)FUN_1001c19dc(param_1 + 0x40);
  sVar5 = _strlen(pcVar4);
  if (0x7ffffffffffffff7 < sVar5) {
                    /* WARNING: Subroutine does not return */
    FUN_100147bd8(&local_90);
  }
  if (sVar5 < 0x17) {
    local_80 = CONCAT17((char)sVar5,(undefined7)local_80);
    ppppiVar6 = &local_90;
    if (sVar5 != 0) goto LAB_10023aa1c;
  }
  else {
    uVar7 = 0x19;
    if ((sVar5 | 7) != 0x17) {
      uVar7 = (sVar5 | 7) + 1;
    }
    ppppiVar6 = operator_new(uVar7);
    local_80 = uVar7 | 0x8000000000000000;
    local_90 = (int ***)ppppiVar6;
    sStack_88 = sVar5;
LAB_10023aa1c:
    _memmove(ppppiVar6,pcVar4,sVar5);
  }
  *(undefined1 *)((long)ppppiVar6 + sVar5) = 0;
  FUN_10073559c(&local_58,&local_70,uVar1,&local_90);
  if ((long)local_80 < 0) {
    operator_delete(local_90);
  }
  if ((long)local_60 < 0) {
    operator_delete(local_70);
  }
  iVar3 = FUN_100823cfc(&local_58);
  if (iVar3 != 0) {
    uVar7 = FUN_100823dac(&local_58);
    if ((uVar7 & 1) == 0) {
      uVar8 = std::chrono::system_clock::now();
      FUN_10073cdf4(&local_70,4,uVar8);
      iVar3 = FUN_1007396c0(&local_70);
      if (iVar3 != 0) {
        uVar8 = FUN_100736880(&local_70,"Database: Could not delete corrupted database indicator ");
        uVar8 = FUN_10013a004(uVar8,&local_58);
        FUN_100736880(uVar8,". Unable to initialize database.");
      }
    }
    else {
      uVar7 = FUN_100823ec4(&local_58);
      if ((uVar7 & 1) != 0) goto LAB_10023aa78;
      FUN_1008241a0(&local_58);
      uVar8 = std::chrono::system_clock::now();
      FUN_10073cdf4(&local_70,4,uVar8);
      iVar3 = FUN_1007396c0(&local_70);
      if (iVar3 != 0) {
        uVar8 = FUN_100736880(&local_70,"Database: Could not delete corrupted database file ");
        uVar8 = FUN_10013a004(uVar8,&local_58);
        FUN_100736880(uVar8,". Unable to initialize database.");
      }
    }
    thunk_FUN_1007363ec(&local_70);
    uVar8 = 0;
    goto joined_r0x00010023ac34;
  }
LAB_10023aa78:
  uVar7 = uStack_50;
  if (-1 < (char)bStack_41) {
    uVar7 = (ulong)bStack_41;
  }
  if ((uVar7 == 0) || (iVar3 = FUN_100716d38(&local_58), iVar3 != 0)) {
    FUN_10023a630(&local_70,param_1);
    FUN_1001c19dc(param_1 + 0x40);
    FUN_100446c84(&local_90);
    uVar8 = FUN_10023af84(&local_70,&local_90,*(undefined4 *)(param_1 + 0x1c0));
    if (((int ****)local_90 != (int ****)0x0) &&
       (iVar3 = *(int *)local_90, *(int *)local_90 = iVar3 + -1, iVar3 + -1 == 0)) {
      FUN_100469e84();
    }
    if ((long)local_60 < 0) {
      operator_delete(local_70);
      if (0 < (int)uVar8) goto LAB_10023aaf8;
LAB_10023abbc:
      FUN_1001a83a4(&DAT_100bab270);
      if ((extraout_x1 & 1) == 0) {
        (**(code **)(**(long **)(param_1 + 0x38) + 0x140))(&local_70);
        if ((long)local_60 < 0) {
          if (sStack_68 != 0) {
            FUN_100147c88(&local_90,local_70);
            goto LAB_10023acac;
          }
LAB_10023acf4:
          (**(code **)(**(long **)(param_1 + 0x38) + 0x148))(&local_90);
          iVar3 = FUN_100716c08(&local_90);
          if (iVar3 != 0) {
            FUN_1001c19dc(param_1 + 0x40);
            FUN_100446c84(&local_98);
            uVar8 = FUN_10023af84(&local_90,&local_98,*(undefined4 *)(param_1 + 0x1c0));
            FUN_100133ec0(&local_98);
            if (0 < (int)uVar8) {
              FUN_1001c19dc(param_1 + 0x40);
              FUN_100446c84(&local_98);
              FUN_10023b4e0(&local_58,&local_90,&local_98,uVar8);
              FUN_100133ec0(&local_98);
            }
          }
        }
        else {
          if (local_60._7_1_ == '\0') goto LAB_10023acf4;
          sStack_88 = sStack_68;
          local_90 = local_70;
          local_80 = local_60;
LAB_10023acac:
          uVar7 = FUN_100823cfc(&local_90);
          if ((uVar7 & 1) == 0) {
            thunk_FUN_100452170(&local_98,&local_70);
            FUN_10023b614(&local_70,&local_58,&local_98);
            if ((local_98 != (int *)0x0) &&
               (iVar3 = *local_98, *local_98 = iVar3 + -1, iVar3 + -1 == 0)) {
              FUN_100469e84();
            }
          }
        }
        if ((long)local_80 < 0) {
          operator_delete(local_90);
        }
      }
      else {
        local_70 = (int ***)0x0;
        sStack_68 = 0;
        local_60 = 0;
      }
    }
    else {
      if ((int)uVar8 < 1) goto LAB_10023abbc;
LAB_10023aaf8:
      FUN_10023a630(&local_70,param_1);
      FUN_1001c19dc(param_1 + 0x40);
      FUN_100446c84(&local_90);
      FUN_10023b4e0(&local_58,&local_70,&local_90,uVar8);
      if (((int ****)local_90 != (int ****)0x0) &&
         (iVar3 = *(int *)local_90, *(int *)local_90 = iVar3 + -1, iVar3 + -1 == 0)) {
        FUN_100469e84();
      }
    }
    if (-1 < (long)local_60) goto LAB_10023ad8c;
    operator_delete(local_70);
    if ((undefined8 ****)(param_1 + 0x20) != &local_58) goto LAB_10023adb8;
  }
  else {
LAB_10023ad8c:
    if ((undefined8 ****)(param_1 + 0x20) != &local_58) {
LAB_10023adb8:
      pbVar9 = param_1 + 0x20;
      if ((char)param_1[0x37] < '\0') {
        ppppuVar2 = (undefined8 ****)local_58;
        if (-1 < (char)bStack_41) {
          uStack_50 = (ulong)bStack_41;
          ppppuVar2 = &local_58;
        }
        FUN_100147dd4(pbVar9,ppppuVar2,uStack_50);
      }
      else if ((char)bStack_41 < '\0') {
        FUN_100147d14(pbVar9,local_58,uStack_50);
      }
      else {
        *(ulong *)(param_1 + 0x28) = uStack_50;
        *(undefined8 ****)pbVar9 = local_58;
        *(ulong *)(param_1 + 0x30) = CONCAT17(bStack_41,local_48);
      }
    }
  }
  *param_1 = 1;
  uVar8 = std::chrono::system_clock::now();
  FUN_10073cdf4(&local_70,2,uVar8);
  iVar3 = FUN_1007396c0(&local_70);
  if (iVar3 != 0) {
    uVar8 = FUN_100736880(&local_70,"Database: Loading database from ");
    FUN_10013a004(uVar8,param_1 + 0x20);
  }
  thunk_FUN_1007363ec(&local_70);
  uVar8 = 1;
joined_r0x00010023ac34:
  if ((char)bStack_41 < '\0') {
    operator_delete(local_58);
    return uVar8;
  }
  return uVar8;
}

