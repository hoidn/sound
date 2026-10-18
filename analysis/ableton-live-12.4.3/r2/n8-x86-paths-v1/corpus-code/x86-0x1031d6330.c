// x86 0x1031d6330 FUN_1031d6330 state=exported-with-warnings chunk=chunk-02323.jsonl code_sha256=946b0440fa0ae038d117d83b3d2d9bcba1595cfaaaf0a55e9f40d719ad10c518

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 * FUN_1031d6330(undefined8 *param_1)

{
  int *piVar1;
  long lVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  char cVar6;
  char *pcVar7;
  size_t sVar8;
  void *pvVar9;
  undefined8 uVar10;
  ulong uVar11;
  undefined1 auVar12 [16];
  undefined8 local_b0;
  undefined1 local_a8;
  byte local_a0;
  undefined7 uStack_9f;
  undefined8 uStack_98;
  void *local_90;
  byte local_88 [16];
  void *local_78;
  undefined4 local_70;
  undefined4 uStack_6c;
  long *local_68;
  undefined1 local_60 [8];
  undefined8 local_58;
  undefined4 uStack_50;
  undefined1 uStack_4c;
  undefined2 uStack_4b;
  undefined1 uStack_49;
  char *local_48;
  undefined8 uStack_40;
  
  local_48 = _DAT_105e2c7a8;
  uStack_40 = _UNK_105e2c7b0;
  local_58._0_4_ = _DAT_105e2c798;
  local_58._4_4_ = _UNK_105e2c79c;
  uStack_50 = _UNK_105e2c7a0;
  uStack_4c = (undefined1)_UNK_105e2c7a4;
  uStack_4b = (undefined2)((uint)_UNK_105e2c7a4 >> 8);
  uStack_49 = (undefined1)((uint)_UNK_105e2c7a4 >> 0x18);
  auVar12 = FUN_101188890(&local_58);
  local_b0 = auVar12._0_8_;
  local_a8 = auVar12[8];
  if ((auVar12._8_8_ & 1) == 0) {
    local_48 = operator_new(0x28);
    uVar10 = s_Misc_MultiF0_Mac_libmultif0_64_d_106147513._8_8_;
    *(undefined8 *)local_48 = s_Misc_MultiF0_Mac_libmultif0_64_d_106147513._0_8_;
    *(undefined8 *)(local_48 + 8) = uVar10;
    uVar5 = s_Misc_MultiF0_Mac_libmultif0_64_d_106147513._28_4_;
    uVar4 = s_Misc_MultiF0_Mac_libmultif0_64_d_106147513._24_4_;
    uVar3 = s_Misc_MultiF0_Mac_libmultif0_64_d_106147513._20_4_;
    *(undefined4 *)(local_48 + 0x10) = s_Misc_MultiF0_Mac_libmultif0_64_d_106147513._16_4_;
    *(undefined4 *)(local_48 + 0x14) = uVar3;
    *(undefined4 *)(local_48 + 0x18) = uVar4;
    *(undefined4 *)(local_48 + 0x1c) = uVar5;
    local_48[0x20] = 'y';
    local_48[0x21] = 'l';
    local_48[0x22] = 'i';
    local_48[0x23] = 'b';
    local_48[0x24] = '\0';
    local_58._0_4_ = 0x29;
    local_58._4_4_ = 0;
    uStack_50 = 0x24;
    uStack_4c = 0;
    uStack_4b = 0;
    uStack_49 = 0;
    FUN_1011b8fa0(&local_70);
    (**(code **)(*local_68 + 0xc0))(local_88);
    FUN_1002bc250(&local_a0,local_88,&local_58);
    if ((local_88[0] & 1) != 0) {
      operator_delete(local_78);
    }
    if (CONCAT44(uStack_6c,local_70) != 0) {
      piVar1 = (int *)(CONCAT44(uStack_6c,local_70) + 8);
      *piVar1 = *piVar1 + -1;
      if (*piVar1 == 0) {
        FUN_1012716c0();
      }
    }
    local_70 = 0;
    local_68 = (long *)std::system_category();
    cVar6 = FUN_104041e50(&local_a0,&local_70);
    if (cVar6 == '\0') {
      uVar10 = std::chrono::system_clock::now();
      FUN_104110150(local_60,uVar10);
      cVar6 = FUN_10410c530(local_60);
      if (cVar6 != '\0') {
        uVar10 = FUN_104108bf0(local_60,"MultiF0: No MultiF0 library found at ");
        uVar10 = FUN_1002d3d70(uVar10,&local_a0);
        uVar10 = FUN_104108bf0(uVar10,". (");
        std::error_code::message();
        uVar10 = FUN_104109ed0(uVar10,local_88);
        FUN_104108bf0(uVar10,")");
        if ((local_88[0] & 1) != 0) {
          operator_delete(local_78);
        }
      }
      FUN_104108a10(local_60);
      *param_1 = 0;
      param_1[1] = 0;
      param_1[2] = 0;
    }
    else if ((local_a0 & 1) == 0) {
      param_1[2] = local_90;
      *param_1 = CONCAT71(uStack_9f,local_a0);
      param_1[1] = uStack_98;
    }
    else {
      FUN_1002adc90(param_1,local_90,uStack_98);
    }
    if ((local_a0 & 1) != 0) {
      operator_delete(local_90);
    }
    if (((uint)local_58 & 1) == 0) {
      return param_1;
    }
    operator_delete(local_48);
    return param_1;
  }
  pcVar7 = (char *)FUN_1011858d0(&local_b0);
  sVar8 = _strlen(pcVar7);
  if (0xfffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
    FUN_1002adc00(&local_58);
  }
  if (sVar8 < 0x17) {
    local_58._0_4_ = CONCAT31(local_58._1_3_,(char)sVar8 * '\x02');
    pvVar9 = (void *)((long)&local_58 + 1);
    lVar2 = local_58;
    if (sVar8 == 0) goto LAB_1031d64dd;
  }
  else {
    uVar11 = 0x1a;
    if ((sVar8 | 7) != 0x17) {
      uVar11 = (sVar8 | 7) + 1;
    }
    pvVar9 = operator_new(uVar11);
    local_58 = uVar11 + 1;
    uStack_50 = (undefined4)sVar8;
    uStack_4c = (undefined1)(sVar8 >> 0x20);
    uStack_4b = (undefined2)(sVar8 >> 0x28);
    uStack_49 = (undefined1)(sVar8 >> 0x38);
    local_48 = pvVar9;
  }
  _memcpy(pvVar9,pcVar7,sVar8);
  lVar2 = local_58;
LAB_1031d64dd:
  local_58._4_4_ = (undefined4)((ulong)lVar2 >> 0x20);
  *(undefined1 *)((long)pvVar9 + sVar8) = 0;
  param_1[2] = local_48;
  local_58._0_1_ = (undefined1)lVar2;
  *(undefined1 *)param_1 = (undefined1)local_58;
  local_58._1_3_ = (undefined3)((ulong)lVar2 >> 8);
  *(ulong *)((long)param_1 + 1) =
       CONCAT17((undefined1)uStack_50,CONCAT43(local_58._4_4_,local_58._1_3_));
  *(uint *)((long)param_1 + 9) = CONCAT13(uStack_4c,uStack_50._1_3_);
  *(undefined2 *)((long)param_1 + 0xd) = uStack_4b;
  *(undefined1 *)((long)param_1 + 0xf) = uStack_49;
  return param_1;
}

