
/* WARNING: Removing unreachable block (ram,0x00010307a864) */
/* WARNING: Removing unreachable block (ram,0x00010307a884) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_10307a630(undefined8 *param_1)

{
  ulong uVar1;
  long lVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  int iVar5;
  char *pcVar6;
  size_t sVar7;
  char **ppcVar8;
  undefined8 uVar9;
  char **ppcVar10;
  char *local_c0;
  size_t sStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined1 local_98 [16];
  undefined1 auStack_88 [8];
  undefined4 local_80;
  undefined4 uStack_7c;
  long *local_78;
  void *local_70 [2];
  char local_59;
  undefined8 local_58;
  undefined8 uStack_50;
  undefined7 local_48;
  undefined1 uStack_41;
  
  ppcVar8 = &local_c0;
  ppcVar10 = &local_c0;
  sStack_b8 = _UNK_1058c29e0;
  local_c0 = _DAT_1058c29d8;
  uStack_a8 = _UNK_1058c29f0;
  local_b0 = _DAT_1058c29e8;
  local_98 = FUN_1011aeb80(&local_c0);
  if ((local_98._8_8_ & 1) == 0) {
    local_c0 = operator_new(0x28);
    local_c0[0x20] = 'y';
    uVar4 = s_Misc_MultiF0_Mac_libmultif0_64_d_105be1663._24_8_;
    uVar3 = s_Misc_MultiF0_Mac_libmultif0_64_d_105be1663._16_8_;
    uVar9 = s_Misc_MultiF0_Mac_libmultif0_64_d_105be1663._0_8_;
    local_c0[0x21] = 'l';
    local_c0[0x22] = 'i';
    local_c0[0x23] = 'b';
    *(undefined8 *)(local_c0 + 8) = s_Misc_MultiF0_Mac_libmultif0_64_d_105be1663._8_8_;
    *(undefined8 *)local_c0 = uVar9;
    *(undefined8 *)(local_c0 + 0x18) = uVar4;
    *(undefined8 *)(local_c0 + 0x10) = uVar3;
    local_c0[0x24] = '\0';
    local_b0 = _UNK_1055d96a8;
    sStack_b8 = _DAT_1055d96a0;
    FUN_1011db938(&local_80);
    (**(code **)(*local_78 + 0xc0))(local_70);
    FUN_100241e54(&local_58,local_70,&local_c0);
    if (local_59 < '\0') {
      operator_delete(local_70[0]);
      lVar2 = CONCAT44(uStack_7c,local_80);
    }
    else {
      lVar2 = CONCAT44(uStack_7c,local_80);
    }
    if ((lVar2 != 0) && (iVar5 = *(int *)(lVar2 + 8) + -1, *(int *)(lVar2 + 8) = iVar5, iVar5 == 0))
    {
      FUN_10128eea0();
    }
    local_80 = 0;
    local_78 = (long *)std::system_category();
    iVar5 = FUN_103e897f8(&local_58,&local_80);
    if (iVar5 == 0) {
      std::chrono::system_clock::now();
      FUN_103f40190(auStack_88);
      iVar5 = FUN_103f3c8b8(auStack_88);
      if (iVar5 != 0) {
        uVar9 = FUN_103f39a78(auStack_88,"MultiF0: No MultiF0 library found at ");
        uVar9 = FUN_100259ba4(uVar9,&local_58);
        uVar9 = FUN_103f39a78(uVar9,". (");
        std::error_code::message();
        uVar9 = FUN_103f3a958(uVar9,local_70);
        FUN_103f39a78(uVar9,")");
        if (local_59 < '\0') {
          operator_delete(local_70[0]);
        }
      }
      thunk_FUN_103f395e4(auStack_88);
      *param_1 = 0;
      param_1[1] = 0;
      param_1[2] = 0;
    }
    else {
      param_1[1] = uStack_50;
      *param_1 = local_58;
      param_1[2] = CONCAT17(uStack_41,local_48);
    }
    if (-1 < (long)local_b0) {
      return;
    }
    operator_delete(local_c0);
    return;
  }
  pcVar6 = (char *)FUN_1011abfa4(local_98);
  sVar7 = _strlen(pcVar6);
  if (0x7ffffffffffffff7 < sVar7) {
                    /* WARNING: Subroutine does not return */
    FUN_100234518(&local_c0);
  }
  if (sVar7 < 0x17) {
    local_b0 = CONCAT17((char)sVar7,(undefined7)local_b0);
    if (sVar7 == 0) goto LAB_10307a754;
  }
  else {
    uVar1 = 0x19;
    if ((sVar7 | 7) != 0x17) {
      uVar1 = (sVar7 | 7) + 1;
    }
    ppcVar8 = operator_new(uVar1);
    local_b0 = uVar1 | 0x8000000000000000;
    local_c0 = (char *)ppcVar8;
    sStack_b8 = sVar7;
  }
  _memcpy(ppcVar8,pcVar6,sVar7);
  ppcVar10 = ppcVar8;
LAB_10307a754:
  *(char *)((long)ppcVar10 + sVar7) = '\0';
  param_1[1] = sStack_b8;
  *param_1 = local_c0;
  param_1[2] = local_b0;
  return;
}

