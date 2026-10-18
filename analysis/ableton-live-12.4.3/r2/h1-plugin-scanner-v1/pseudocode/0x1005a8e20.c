
/* WARNING: Removing unreachable block (ram,0x0001005a8f90) */
/* WARNING: Removing unreachable block (ram,0x0001005a9280) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_1005a8e20(long *param_1,long *param_2,undefined4 param_3,undefined4 param_4,
                  undefined8 param_5)

{
  ulong uVar1;
  long lVar2;
  long lVar3;
  int iVar4;
  void *pvVar5;
  int *******pppppppiVar6;
  ulong uVar7;
  long lVar8;
  char *******pppppppcVar9;
  undefined4 local_188;
  undefined4 uStack_184;
  int *******local_180;
  ulong uStack_178;
  ulong local_170;
  int *******local_160;
  ulong uStack_158;
  ulong local_150;
  undefined4 local_144;
  void *local_140;
  undefined8 uStack_138;
  long local_130;
  undefined8 local_128;
  char *******local_120;
  ulong local_118;
  undefined8 uStack_110;
  uint local_108;
  char *******local_100;
  undefined1 local_f8 [16];
  uint local_e8;
  int *******local_e0;
  ulong uStack_d8;
  undefined8 local_d0;
  uint local_c8;
  void *local_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined1 auStack_a8 [24];
  char local_90;
  undefined4 local_88 [2];
  undefined8 local_80;
  undefined4 local_74 [5];
  
  local_74[0] = param_3;
  iVar4 = (**(code **)(*param_2 + 0x10))();
  param_1[1] = 0;
  param_1[2] = 0;
  *param_1 = 0;
  if (iVar4 != 0) {
    local_88[0] = 0;
    local_80 = std::system_category();
    lVar8 = param_2[1];
    pvVar5 = operator_new(0x120);
    uStack_b0 = _UNK_1009d2778;
    local_b8 = _DAT_1009d2770;
    local_c0 = pvVar5;
    _memcpy(pvVar5,
            "SELECT pm.module_id, pm.path, pd.relpath, pm.scanstate, pd.id, pm.fingerprint,        pm.processor   FROM plugin_modules AS pm        JOIN plugin_domains AS pd ON (pm.module_id = pd.module_id)  WHERE pm.arch = :arch    AND pd.id = :domain_id   AND pm.processor & :processor_mask <> 0"
            ,0x11b);
    *(undefined1 *)((long)pvVar5 + 0x11b) = 0;
    local_e0 = (int *******)s__arch_100a4a7dd;
    uStack_d8 = CONCAT44(uStack_d8._4_4_,param_3);
    local_c8 = 2;
    local_f8 = FUN_100437d68(param_5);
    local_100 = (char *******)0x100a4a7e3;
    local_e8 = 6;
    local_120 = (char *******)0x100a4a7b2;
    local_118 = CONCAT44(local_118._4_4_,param_4);
    local_108 = 2;
    FUN_1005a6818(auStack_a8,lVar8,&local_c0,local_88,&local_e0,&local_100,&local_120);
    if (local_108 != 0xffffffff) {
      (*(code *)(&PTR_FUN_100b6daf0)[local_108])(&local_140,&local_118);
    }
    if (local_e8 != 0xffffffff) {
      (*(code *)(&PTR_FUN_100b6daf0)[local_e8])(&local_120,local_f8);
    }
    if (local_c8 != 0xffffffff) {
      (*(code *)(&PTR_FUN_100b6daf0)[local_c8])(&local_100,&uStack_d8);
    }
    FUN_1005a4e00(local_88);
    local_128 = 0;
    local_120 = (char *******)0x0;
    local_100 = (char *******)0x0;
    local_f8._0_8_ = 0;
    local_f8._8_8_ = 0;
    local_118 = 0;
    uStack_110 = 0;
    local_c0 = (void *)0x0;
    local_b8 = 0;
    uStack_b0 = 0;
    local_140 = (void *)0x0;
    uStack_138 = 0;
    local_130 = 0;
    local_144 = 0;
    while (iVar4 = FUN_1005a9464(auStack_a8,local_88,(long)&local_128 + 4,&local_100,&local_120,
                                 &local_128,&local_c0,&local_140,&local_144), iVar4 != 0) {
      uVar7 = (ulong)local_f8[0xf];
      if ((long)uVar7 < 0) {
        if (0x7ffffffffffffff7 < (ulong)local_f8._0_8_) {
                    /* WARNING: Subroutine does not return */
          FUN_100134f2c(&local_e0);
        }
        uVar7 = local_f8._0_8_;
        pppppppcVar9 = local_100;
        if (0x16 < (ulong)local_f8._0_8_) goto LAB_1005a9040;
LAB_1005a9018:
        local_d0 = CONCAT17((char)uVar7,(undefined7)local_d0);
        pppppppiVar6 = (int *******)&local_e0;
        if (uVar7 != 0) goto LAB_1005a9064;
      }
      else {
        pppppppcVar9 = (char *******)&local_100;
        if (uVar7 < 0x17) goto LAB_1005a9018;
LAB_1005a9040:
        uVar1 = 0x19;
        if ((uVar7 | 7) != 0x17) {
          uVar1 = (uVar7 | 7) + 1;
        }
        pppppppiVar6 = operator_new(uVar1);
        local_d0 = uVar1 | 0x8000000000000000;
        local_e0 = pppppppiVar6;
        uStack_d8 = uVar7;
LAB_1005a9064:
        _memmove(pppppppiVar6,pppppppcVar9,uVar7);
      }
      *(undefined1 *)((long)pppppppiVar6 + uVar7) = 0;
      uStack_158 = uStack_d8;
      local_160 = local_e0;
      local_150 = local_d0;
      uVar7 = (ulong)uStack_110._7_1_;
      if ((long)uVar7 < 0) {
        if (0x7ffffffffffffff7 < local_118) {
                    /* WARNING: Subroutine does not return */
          FUN_100134f2c(&local_e0);
        }
        uVar7 = local_118;
        pppppppcVar9 = local_120;
        if (0x16 < local_118) goto LAB_1005a90c4;
LAB_1005a909c:
        local_d0 = CONCAT17((char)uVar7,(undefined7)local_d0);
        pppppppiVar6 = (int *******)&local_e0;
        if (uVar7 != 0) goto LAB_1005a90e8;
      }
      else {
        pppppppcVar9 = (char *******)&local_120;
        if (uVar7 < 0x17) goto LAB_1005a909c;
LAB_1005a90c4:
        uVar1 = 0x19;
        if ((uVar7 | 7) != 0x17) {
          uVar1 = (uVar7 | 7) + 1;
        }
        pppppppiVar6 = operator_new(uVar1);
        local_d0 = uVar1 | 0x8000000000000000;
        local_e0 = pppppppiVar6;
        uStack_d8 = uVar7;
LAB_1005a90e8:
        _memmove(pppppppiVar6,pppppppcVar9,uVar7);
      }
      *(undefined1 *)((long)pppppppiVar6 + uVar7) = 0;
      uStack_178 = uStack_d8;
      local_180 = local_e0;
      local_170 = local_d0;
      local_188 = (undefined4)local_128;
      uStack_184 = local_144;
      FUN_10043ce2c(&local_e0,&local_c0);
      uVar7 = param_1[1];
      if (uVar7 < (ulong)param_1[2]) {
        FUN_1005d235c(uVar7,(long)&local_128 + 4,&local_160,&local_180,local_74,&uStack_184,
                      &local_188,&local_e0,&local_140);
        lVar8 = uVar7 + 0x68;
      }
      else {
        lVar8 = FUN_1005d20e0(param_1,(long)&local_128 + 4,&local_160,&local_180,local_74,
                              &uStack_184,&local_188,&local_e0,&local_140);
      }
      param_1[1] = lVar8;
      if ((local_e0 != (int *******)0x0) &&
         (iVar4 = *(int *)local_e0, *(int *)local_e0 = iVar4 + -1, iVar4 + -1 == 0)) {
        FUN_100454b40();
      }
      if ((long)local_170 < 0) {
        operator_delete(local_180);
      }
      if ((long)local_150 < 0) {
        operator_delete(local_160);
      }
    }
    FUN_1005a4e00(local_88);
    lVar2 = *param_1;
    lVar3 = param_1[1];
    lVar8 = 0;
    if (lVar3 != lVar2) {
      lVar8 = LZCOUNT((lVar3 - lVar2 >> 3) * 0x4ec4ec4ec4ec4ec5) * -2 + 0x7e;
    }
    FUN_1005d2754(lVar2,lVar3,lVar8,1);
    if (local_130 < 0) {
      operator_delete(local_140);
    }
    if (uStack_110 < 0) {
      operator_delete(local_120);
    }
    if ((long)local_f8._8_8_ < 0) {
      operator_delete(local_100);
    }
    if (local_90 == '\x01') {
      FUN_1007879a4(auStack_a8);
    }
  }
  return;
}

