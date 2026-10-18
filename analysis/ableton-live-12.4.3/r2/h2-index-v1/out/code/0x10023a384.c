// 0x10023a384 FUN_10023a384 state=exported-with-warnings body_bytes=580 warnings=1 chunk=chunk-00097.jsonl

uint FUN_10023a384(byte *param_1)

{
  ulong uVar1;
  undefined4 uVar2;
  undefined8 ******ppppppuVar3;
  uint uVar4;
  int iVar5;
  char *pcVar6;
  size_t sVar7;
  undefined8 ******ppppppuVar8;
  undefined8 uVar9;
  undefined8 *****local_88;
  size_t local_80;
  undefined8 uStack_78;
  void *local_70 [2];
  char local_59;
  undefined8 *****local_58;
  ulong uStack_50;
  undefined7 local_48;
  byte bStack_41;
  
  if ((*param_1 & 1) != 0) {
    return 0;
  }
  FUN_10023a630(local_70);
  uVar2 = *(undefined4 *)(param_1 + 0x1c0);
  pcVar6 = (char *)FUN_1001c19dc(param_1 + 0x40);
  sVar7 = _strlen(pcVar6);
  if (0x7ffffffffffffff7 < sVar7) {
                    /* WARNING: Subroutine does not return */
    FUN_100147bd8(&local_88);
  }
  if (sVar7 < 0x17) {
    uStack_78 = CONCAT17((char)sVar7,(undefined7)uStack_78);
    ppppppuVar8 = &local_88;
    if (sVar7 == 0) goto LAB_10023a440;
  }
  else {
    uVar1 = 0x19;
    if ((sVar7 | 7) != 0x17) {
      uVar1 = (sVar7 | 7) + 1;
    }
    ppppppuVar8 = operator_new(uVar1);
    uStack_78 = uVar1 | 0x8000000000000000;
    local_88 = ppppppuVar8;
    local_80 = sVar7;
  }
  _memmove(ppppppuVar8,pcVar6,sVar7);
LAB_10023a440:
  *(undefined1 *)((long)ppppppuVar8 + sVar7) = 0;
  FUN_10073559c(&local_58,local_70,uVar2,&local_88);
  if ((long)uStack_78 < 0) {
    operator_delete(local_88);
  }
  if (local_59 < '\0') {
    operator_delete(local_70[0]);
  }
  uVar4 = FUN_100823cfc(&local_58);
  if (uVar4 == 0) {
    ppppppuVar8 = (undefined8 ******)(param_1 + 0x20);
    if (ppppppuVar8 != &local_58) {
      if ((char)param_1[0x37] < '\0') {
        ppppppuVar3 = (undefined8 ******)local_58;
        if (-1 < (char)bStack_41) {
          uStack_50 = (ulong)bStack_41;
          ppppppuVar3 = &local_58;
        }
        FUN_100147dd4(ppppppuVar8,ppppppuVar3,uStack_50);
      }
      else if ((char)bStack_41 < '\0') {
        FUN_100147d14(ppppppuVar8,local_58,uStack_50);
      }
      else {
        *(ulong *)(param_1 + 0x28) = uStack_50;
        *ppppppuVar8 = local_58;
        *(ulong *)(param_1 + 0x30) = CONCAT17(bStack_41,local_48);
      }
    }
    *param_1 = 1;
    uVar9 = std::chrono::system_clock::now();
    FUN_10073cdf4(local_70,2,uVar9);
    iVar5 = FUN_1007396c0(local_70);
    if (iVar5 != 0) {
      uVar9 = FUN_100736880(local_70,"Database: Loading database from ");
      FUN_10013a004(uVar9,ppppppuVar8);
    }
  }
  else {
    uVar9 = std::chrono::system_clock::now();
    FUN_10073cdf4(local_70,4,uVar9);
    iVar5 = FUN_1007396c0(local_70);
    if (iVar5 != 0) {
      uVar9 = FUN_100736880(local_70,
                            "Database: Could not repair corrupted database in secondary instance ");
      uVar9 = FUN_10013a004(uVar9,&local_58);
      FUN_100736880(uVar9,". Unable to initialize database.");
    }
  }
  thunk_FUN_1007363ec(local_70);
  if (-1 < (char)bStack_41) {
    return uVar4 ^ 1;
  }
  operator_delete(local_58);
  return uVar4 ^ 1;
}

