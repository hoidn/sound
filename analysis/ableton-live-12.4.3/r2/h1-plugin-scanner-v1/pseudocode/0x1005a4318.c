
/* WARNING: Removing unreachable block (ram,0x0001005a4848) */
/* WARNING: Removing unreachable block (ram,0x0001005a49b0) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1  [16]
FUN_1005a4318(long *param_1,undefined8 param_2,undefined4 param_3,undefined8 param_4,long *param_5,
             undefined8 param_6,undefined8 param_7)

{
  undefined8 uVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  bool bVar4;
  byte bVar5;
  int iVar6;
  char *******pppppppcVar7;
  long lVar8;
  ulong uVar9;
  ulong uVar10;
  long lVar11;
  ulong uVar12;
  uint uVar13;
  long lVar14;
  undefined8 *******pppppppuVar15;
  char *******pppppppcVar16;
  uint uVar17;
  uint uVar18;
  undefined1 auVar19 [16];
  char *******local_1a0;
  uint local_190;
  uint uStack_18c;
  char *******pppppppcStack_188;
  undefined8 *******local_180;
  char local_178;
  undefined2 uStack_177;
  undefined4 uStack_175;
  char local_171;
  uint local_170;
  undefined4 uStack_168;
  undefined3 uStack_164;
  int local_160 [2];
  undefined8 local_158;
  undefined8 *******local_150;
  char *******pppppppcStack_148;
  undefined8 *******local_140;
  undefined8 *******local_130;
  char *******pppppppcStack_128;
  undefined8 *******local_120;
  char *local_110;
  undefined8 *******local_108;
  char *******pppppppcStack_100;
  uint local_f8;
  char *local_f0;
  uint local_e8 [4];
  uint local_d8;
  char *******local_d0;
  undefined1 local_c8 [16];
  uint local_b8;
  char *local_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  char *******local_98;
  undefined8 *******local_90;
  undefined8 local_88;
  uint local_80;
  undefined1 auStack_71 [17];
  
  iVar6 = (**(code **)(*param_1 + 0x10))();
  if (iVar6 == 0) {
    uVar10 = 0;
    uVar12 = 0;
    goto LAB_1005a4a28;
  }
  FUN_10067ac78(&local_190,param_2);
  if ((long)local_180 < 0) {
    FUN_100135b64(&local_130,CONCAT44(uStack_18c,local_190),pppppppcStack_188);
    if ((long)local_180 < 0) {
      operator_delete((void *)CONCAT44(uStack_18c,local_190));
    }
  }
  else {
    local_130 = (undefined8 *******)CONCAT44(uStack_18c,local_190);
    pppppppcStack_128 = pppppppcStack_188;
    local_120 = local_180;
  }
  FUN_10067ac78(&local_190,param_7);
  if ((long)local_180 < 0) {
    FUN_100135b64(&local_150,CONCAT44(uStack_18c,local_190),pppppppcStack_188);
    if ((long)local_180 < 0) {
      operator_delete((void *)CONCAT44(uStack_18c,local_190));
    }
  }
  else {
    local_150 = (undefined8 *******)CONCAT44(uStack_18c,local_190);
    pppppppcStack_148 = pppppppcStack_188;
    local_140 = local_180;
  }
  local_160[0] = 0;
  local_158 = std::system_category();
  lVar14 = param_1[1];
  auVar19 = FUN_100437d68(param_5);
  local_110 = operator_new(0x100);
  uVar3 = s_SELECT_pm_module_id__pd_id____do_100a48a41._216_8_;
  uVar2 = s_SELECT_pm_module_id__pd_id____do_100a48a41._208_8_;
  uVar1 = s_SELECT_pm_module_id__pd_id____do_100a48a41._192_8_;
  pppppppcStack_100 = _UNK_1009d26d8;
  local_108 = _DAT_1009d26d0;
  *(undefined8 *)(local_110 + 200) = s_SELECT_pm_module_id__pd_id____do_100a48a41._200_8_;
  *(undefined8 *)(local_110 + 0xc0) = uVar1;
  *(undefined8 *)(local_110 + 0xd8) = uVar3;
  *(undefined8 *)(local_110 + 0xd0) = uVar2;
  uVar1 = s_SELECT_pm_module_id__pd_id____do_100a48a41._224_8_;
  *(ulong *)(local_110 + 0xe8) =
       CONCAT53(s_SELECT_pm_module_id__pd_id____do_100a48a41._235_5_,
                s_SELECT_pm_module_id__pd_id____do_100a48a41._232_3_);
  *(undefined8 *)(local_110 + 0xe0) = uVar1;
  uVar1 = CONCAT35(s_SELECT_pm_module_id__pd_id____do_100a48a41._240_3_,
                   s_SELECT_pm_module_id__pd_id____do_100a48a41._235_5_);
  *(undefined8 *)(local_110 + 0xf3) = s_SELECT_pm_module_id__pd_id____do_100a48a41._243_8_;
  *(undefined8 *)(local_110 + 0xeb) = uVar1;
  uVar3 = s_SELECT_pm_module_id__pd_id____do_100a48a41._152_8_;
  uVar2 = s_SELECT_pm_module_id__pd_id____do_100a48a41._144_8_;
  uVar1 = s_SELECT_pm_module_id__pd_id____do_100a48a41._128_8_;
  *(undefined8 *)(local_110 + 0x88) = s_SELECT_pm_module_id__pd_id____do_100a48a41._136_8_;
  *(undefined8 *)(local_110 + 0x80) = uVar1;
  *(undefined8 *)(local_110 + 0x98) = uVar3;
  *(undefined8 *)(local_110 + 0x90) = uVar2;
  uVar3 = s_SELECT_pm_module_id__pd_id____do_100a48a41._184_8_;
  uVar2 = s_SELECT_pm_module_id__pd_id____do_100a48a41._176_8_;
  uVar1 = s_SELECT_pm_module_id__pd_id____do_100a48a41._160_8_;
  *(undefined8 *)(local_110 + 0xa8) = s_SELECT_pm_module_id__pd_id____do_100a48a41._168_8_;
  *(undefined8 *)(local_110 + 0xa0) = uVar1;
  *(undefined8 *)(local_110 + 0xb8) = uVar3;
  *(undefined8 *)(local_110 + 0xb0) = uVar2;
  uVar3 = s_SELECT_pm_module_id__pd_id____do_100a48a41._88_8_;
  uVar2 = s_SELECT_pm_module_id__pd_id____do_100a48a41._80_8_;
  uVar1 = s_SELECT_pm_module_id__pd_id____do_100a48a41._64_8_;
  *(undefined8 *)(local_110 + 0x48) = s_SELECT_pm_module_id__pd_id____do_100a48a41._72_8_;
  *(undefined8 *)(local_110 + 0x40) = uVar1;
  *(undefined8 *)(local_110 + 0x58) = uVar3;
  *(undefined8 *)(local_110 + 0x50) = uVar2;
  uVar3 = s_SELECT_pm_module_id__pd_id____do_100a48a41._120_8_;
  uVar2 = s_SELECT_pm_module_id__pd_id____do_100a48a41._112_8_;
  uVar1 = s_SELECT_pm_module_id__pd_id____do_100a48a41._96_8_;
  *(undefined8 *)(local_110 + 0x68) = s_SELECT_pm_module_id__pd_id____do_100a48a41._104_8_;
  *(undefined8 *)(local_110 + 0x60) = uVar1;
  *(undefined8 *)(local_110 + 0x78) = uVar3;
  *(undefined8 *)(local_110 + 0x70) = uVar2;
  uVar3 = s_SELECT_pm_module_id__pd_id____do_100a48a41._24_8_;
  uVar2 = s_SELECT_pm_module_id__pd_id____do_100a48a41._16_8_;
  uVar1 = s_SELECT_pm_module_id__pd_id____do_100a48a41._0_8_;
  *(undefined8 *)(local_110 + 8) = s_SELECT_pm_module_id__pd_id____do_100a48a41._8_8_;
  *(undefined8 *)local_110 = uVar1;
  *(undefined8 *)(local_110 + 0x18) = uVar3;
  *(undefined8 *)(local_110 + 0x10) = uVar2;
  uVar3 = s_SELECT_pm_module_id__pd_id____do_100a48a41._56_8_;
  uVar2 = s_SELECT_pm_module_id__pd_id____do_100a48a41._48_8_;
  uVar1 = s_SELECT_pm_module_id__pd_id____do_100a48a41._32_8_;
  *(undefined8 *)(local_110 + 0x28) = s_SELECT_pm_module_id__pd_id____do_100a48a41._40_8_;
  *(undefined8 *)(local_110 + 0x20) = uVar1;
  *(undefined8 *)(local_110 + 0x38) = uVar3;
  *(undefined8 *)(local_110 + 0x30) = uVar2;
  local_110[0xfb] = '\0';
  local_88 = pppppppcStack_128;
  local_90 = local_130;
  if (-1 < (long)local_120) {
    local_88 = (char *******)((ulong)local_120 >> 0x38);
    local_90 = &local_130;
  }
  local_98 = (char *******)0x100a4a7f7;
  local_80 = 5;
  local_d0 = (char *******)0x100a4a7e3;
  local_b8 = 6;
  local_f0 = ":processor_mask";
  local_e8[0] = (uint)param_4;
  local_d8 = 2;
  local_c8 = auVar19;
  FUN_1005a6818(&local_190,lVar14,&local_110,local_160,&local_98,&local_d0,&local_f0);
  if (local_d8 != 0xffffffff) {
    (*(code *)(&PTR_FUN_100b6daf0)[local_d8])(&local_b0,local_e8);
  }
  if (local_b8 != 0xffffffff) {
    (*(code *)(&PTR_FUN_100b6daf0)[local_b8])(&local_f0,local_c8);
  }
  if (local_80 != 0xffffffff) {
    (*(code *)(&PTR_FUN_100b6daf0)[local_80])(&local_d0,&local_90);
  }
  if ((long)pppppppcStack_100 < 0) {
    operator_delete(local_110);
    if (local_160[0] == 0) goto LAB_1005a45ac;
LAB_1005a458c:
    bVar5 = 0;
LAB_1005a4644:
    uVar17 = 0;
    local_1a0 = (char *******)0x0;
    bVar4 = false;
    uStack_164 = 0;
    uStack_168 = 0;
    pppppppuVar15 = (undefined8 *******)0x0;
    uVar13 = 0;
    uVar18 = 0;
  }
  else {
    if (local_160[0] != 0) goto LAB_1005a458c;
LAB_1005a45ac:
    local_d0 = (char *******)0x0;
    local_c8._0_8_ = (undefined8 *******)0x0;
    local_c8._8_8_ = 0;
    bVar5 = FUN_1007879e8(&local_190,local_160);
    bVar5 = local_160[0] == 0 & bVar5;
    if (bVar5 != 1) goto LAB_1005a4644;
    FUN_100787e94(&local_190,&local_f0);
    FUN_100787e94(&local_190,&local_110);
    FUN_1007881cc(&local_190,&local_d0);
    FUN_100787e94(&local_190,&local_b0);
    bVar4 = (int)local_110 != 0;
    pppppppuVar15 = (undefined8 *******)(long)local_c8[0xf];
    if ((long)pppppppuVar15 < 0) {
      if ((undefined8 *******)0x7ffffffffffffff7 < (ulong)local_c8._0_8_) {
                    /* WARNING: Subroutine does not return */
        FUN_100134f2c(&local_98);
      }
      pppppppuVar15 = (undefined8 *******)local_c8._0_8_;
      pppppppcVar16 = local_d0;
      if ((undefined8 *******)0x16 < (ulong)local_c8._0_8_) goto LAB_1005a47dc;
LAB_1005a462c:
      local_88 = (char *******)CONCAT17((char)pppppppuVar15,(undefined7)local_88);
      pppppppcVar7 = (char *******)&local_98;
      if (pppppppuVar15 != (undefined8 *******)0x0) goto LAB_1005a4804;
    }
    else {
      pppppppcVar16 = (char *******)&local_d0;
      if (pppppppuVar15 < (undefined8 *******)0x17) goto LAB_1005a462c;
LAB_1005a47dc:
      uVar10 = 0x19;
      if (((ulong)pppppppuVar15 | 7) != 0x17) {
        uVar10 = ((ulong)pppppppuVar15 | 7) + 1;
      }
      pppppppcVar7 = operator_new(uVar10);
      local_88 = (char *******)(uVar10 | 0x8000000000000000);
      local_98 = pppppppcVar7;
      local_90 = pppppppuVar15;
LAB_1005a4804:
      _memmove(pppppppcVar7,pppppppcVar16,(size_t)pppppppuVar15);
    }
    *(undefined1 *)((long)pppppppcVar7 + (long)pppppppuVar15) = 0;
    local_1a0 = local_98;
    uStack_164 = (undefined3)((ulong)local_88 >> 0x20);
    uVar17 = (uint)local_88._7_1_;
    pppppppuVar15 = local_90;
    uVar13 = (uint)local_f0;
    uVar18 = (uint)local_b0;
    uStack_168 = (undefined4)local_88;
  }
  if (local_178 == '\x01') {
    FUN_1007879a4(&local_190);
  }
  if (bVar5 == 0) {
    FUN_100783784(&local_190,param_1[1],1,local_160);
    FUN_1005a4e00(local_160);
    uVar9 = FUN_1005a4f68(param_1,0,&local_130,&local_150,param_3,param_4,param_5,param_6,0);
    FUN_1007839d4(&local_190,local_160);
    FUN_1005a4e00(local_160);
    thunk_FUN_100785fdc(&local_190);
    uVar10 = 0;
    uVar12 = 0;
  }
  else {
    uStack_18c = CONCAT31(uStack_18c._1_3_,bVar4);
    local_190 = uVar13;
    local_170 = uVar18;
    if (uVar17 >> 7 == 0) {
      pppppppcStack_188 = local_1a0;
      local_178 = (char)uStack_168;
      uStack_177 = (undefined2)((uint)uStack_168 >> 8);
      uStack_175 = CONCAT31(uStack_164,uStack_168._3_1_);
      local_171 = (char)uVar17;
      local_180 = pppppppuVar15;
      if (bVar4) goto LAB_1005a46ac;
LAB_1005a4774:
      lVar14 = *param_5;
      if (lVar14 == 0) {
        local_90 = (undefined8 *******)0xffffffffffffffff;
      }
      else {
        local_90 = (undefined8 *******)(long)(*(int *)(lVar14 + 4) / 2 + -1);
      }
      local_98 = (char *******)(lVar14 + 0x10);
      FUN_1005a4be8(param_1[1],local_190,&local_98,&local_150,local_160);
    }
    else {
      FUN_100135b64(&pppppppcStack_188,local_1a0,pppppppuVar15);
      if ((uStack_18c & 1) == 0) goto LAB_1005a4774;
LAB_1005a46ac:
      iVar6 = FUN_100679138(param_7,&pppppppcStack_188);
      uVar13 = local_190;
      if (iVar6 != 0) {
        lVar14 = *param_5;
        if (lVar14 == 0) {
          lVar11 = -1;
        }
        else {
          lVar11 = (long)(*(int *)(lVar14 + 4) / 2 + -1);
        }
        lVar8 = param_1[1];
        local_b0 = operator_new(0x60);
        uVar3 = s_UPDATE_plugin_domains_SET_relpat_100a49d6c._56_8_;
        uVar2 = s_UPDATE_plugin_domains_SET_relpat_100a49d6c._48_8_;
        uVar1 = s_UPDATE_plugin_domains_SET_relpat_100a49d6c._32_8_;
        local_c8._0_8_ = lVar14 + 0x10;
        uStack_a0 = _UNK_1009d27d8;
        local_a8 = _DAT_1009d27d0;
        *(undefined8 *)(local_b0 + 0x28) = s_UPDATE_plugin_domains_SET_relpat_100a49d6c._40_8_;
        *(undefined8 *)(local_b0 + 0x20) = uVar1;
        *(undefined8 *)(local_b0 + 0x38) = uVar3;
        *(undefined8 *)(local_b0 + 0x30) = uVar2;
        uVar1 = s_UPDATE_plugin_domains_SET_relpat_100a49d6c._64_8_;
        *(ulong *)(local_b0 + 0x48) =
             CONCAT35(s_UPDATE_plugin_domains_SET_relpat_100a49d6c._77_3_,
                      s_UPDATE_plugin_domains_SET_relpat_100a49d6c._72_5_);
        *(undefined8 *)(local_b0 + 0x40) = uVar1;
        uVar1 = CONCAT53(s_UPDATE_plugin_domains_SET_relpat_100a49d6c._80_5_,
                         s_UPDATE_plugin_domains_SET_relpat_100a49d6c._77_3_);
        *(undefined8 *)(local_b0 + 0x55) = s_UPDATE_plugin_domains_SET_relpat_100a49d6c._85_8_;
        *(undefined8 *)(local_b0 + 0x4d) = uVar1;
        uVar3 = s_UPDATE_plugin_domains_SET_relpat_100a49d6c._24_8_;
        uVar2 = s_UPDATE_plugin_domains_SET_relpat_100a49d6c._16_8_;
        uVar1 = s_UPDATE_plugin_domains_SET_relpat_100a49d6c._0_8_;
        *(undefined8 *)(local_b0 + 8) = s_UPDATE_plugin_domains_SET_relpat_100a49d6c._8_8_;
        *(undefined8 *)local_b0 = uVar1;
        *(undefined8 *)(local_b0 + 0x18) = uVar3;
        *(undefined8 *)(local_b0 + 0x10) = uVar2;
        local_b0[0x5d] = '\0';
        local_d0 = (char *******)0x100a4aaee;
        local_b8 = 6;
        local_f0 = ":module_id";
        local_e8[0] = uVar13;
        local_d8 = 2;
        pppppppcStack_100 = pppppppcStack_148;
        local_108 = local_150;
        if (-1 < (long)local_140) {
          pppppppcStack_100 = (char *******)((ulong)local_140 >> 0x38);
          local_108 = &local_150;
        }
        local_110 = ":relpath";
        local_f8 = 5;
        local_c8._8_8_ = lVar11;
        FUN_1005a6818(&local_98,lVar8,&local_b0,local_160,&local_d0,&local_f0,&local_110);
        if (local_f8 != 0xffffffff) {
          (*(code *)(&PTR_FUN_100b6daf0)[local_f8])(auStack_71,&local_108);
        }
        if (local_d8 != 0xffffffff) {
          (*(code *)(&PTR_FUN_100b6daf0)[local_d8])(&local_110,local_e8);
        }
        if (local_b8 != 0xffffffff) {
          (*(code *)(&PTR_FUN_100b6daf0)[local_b8])(&local_f0,local_c8);
        }
        if (local_160[0] == 0) {
          FUN_100787c3c(&local_98,local_160);
        }
        if ((char)local_80 == '\x01') {
          FUN_1007879a4(&local_98);
        }
      }
    }
    FUN_1005a4e00(local_160);
    uVar9 = (ulong)local_190;
    uVar10 = (ulong)local_170;
    if (local_171 < '\0') {
      operator_delete(pppppppcStack_188);
    }
    if (uVar17 >> 7 == 0) {
      uVar12 = 0x100000000;
    }
    else {
      operator_delete(local_1a0);
      uVar12 = 0x100000000;
    }
  }
  if ((long)local_140 < 0) {
    operator_delete(local_150);
  }
  if ((long)local_120 < 0) {
    operator_delete(local_130);
  }
  uVar12 = uVar12 | uVar9 & 0xffffffff;
LAB_1005a4a28:
  auVar19._8_8_ = uVar10;
  auVar19._0_8_ = uVar12;
  return auVar19;
}

