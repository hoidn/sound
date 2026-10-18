// 0x1001b015c FUN_1001b015c state=exported-with-warnings role=update channel names
// source chunk chunk-00077.jsonl; code_sha256=8d09b13b7ce192bd005bcc118fc2487f363a6848e01e823d1c11b12f15b21a62

/* WARNING: Removing unreachable block (ram,0x0001001b05c0) */

undefined8 * FUN_1001b015c(undefined8 *param_1,undefined8 param_2)

{
  undefined8 *****pppppuVar1;
  bool bVar2;
  long lVar3;
  int iVar4;
  undefined8 *puVar5;
  ulong uVar6;
  long *plVar7;
  long *plVar8;
  undefined8 uVar9;
  long *plVar10;
  undefined8 uVar11;
  void *local_520 [2];
  char local_509;
  char local_508;
  undefined8 ****local_500;
  ulong uStack_4f8;
  byte local_4e9;
  char local_4e8;
  void *local_4e0;
  long lStack_4d8;
  undefined8 local_4d0;
  undefined1 auStack_4c8 [208];
  long *local_3f8;
  void *local_3f0 [2];
  char local_3d9;
  char local_3d8;
  undefined1 local_3d0;
  undefined7 uStack_3cf;
  char local_3b9;
  char local_3b8;
  void *local_3b0 [2];
  char local_399;
  char local_398;
  undefined8 ****local_390;
  ulong uStack_388;
  byte local_379;
  char local_378;
  void *local_370;
  long lStack_368;
  undefined8 local_360;
  undefined1 auStack_358 [208];
  undefined1 auStack_288 [208];
  undefined1 auStack_1b8 [48];
  long *local_188 [6];
  undefined1 auStack_158 [48];
  undefined1 auStack_128 [48];
  undefined1 auStack_f8 [48];
  undefined1 local_c8 [48];
  long *local_98 [6];
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_101b8c408;
  puVar5 = operator_new(0x68);
  FUN_10140288c(puVar5,1);
  *puVar5 = &PTR_FUN_101bd17e8;
  *param_1 = puVar5;
  thunk_FUN_10034d8ac(auStack_358,param_2);
  FUN_1001ce984(&local_390);
  if (local_378 == '\x01') {
    if (((DAT_101debbb8 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_101debbb8), iVar4 != 0)) {
      FUN_1001b128c(auStack_1b8,"11(.*)-beta","push3-dev");
      FUN_1001b13d4(local_188,"11(.*)-release","push3-release");
      FUN_1001b151c(auStack_158,"12(.*)-public-beta","push3-12-public-beta");
      FUN_1001b1664(auStack_128,"12(.*)-private-beta","push3-12-private-beta");
      FUN_1001b17ac(auStack_f8,"12(.*)-release","push3-12-release");
      FUN_1001b18f4(&DAT_101debbe0,auStack_1b8,5,local_c8);
      FUN_1001b11b0(auStack_f8);
      FUN_1001b11b0(auStack_128);
      FUN_1001b11b0(auStack_158);
      FUN_1001b11b0(local_188);
      FUN_1001b11b0(auStack_1b8);
      ___cxa_atexit(FUN_1001b1208,&DAT_101debbe0,0x100000000);
      ___cxa_guard_release(&DAT_101debbb8);
    }
    if (DAT_101debbe0 != (long *)0x101debbe8) {
      plVar8 = DAT_101debbe0;
      do {
        FUN_1001b5868(auStack_1b8,plVar8 + 4,0);
        uVar6 = uStack_388;
        pppppuVar1 = (undefined8 *****)local_390;
        if (-1 < (char)local_379) {
          uVar6 = (ulong)local_379;
          pppppuVar1 = &local_390;
        }
        iVar4 = FUN_1001b1ed8(pppppuVar1,(long)pppppuVar1 + uVar6,auStack_1b8,0);
        if (local_188[0] != (long *)0x0) {
          LOAcquire();
          lVar3 = local_188[0][1];
          local_188[0][1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*local_188[0] + 0x10))(local_188[0]);
            std::__shared_weak_count::__release_weak();
          }
        }
        std::locale::~locale(auStack_1b8);
        if (iVar4 != 0) {
          if (*(char *)((long)plVar8 + 0x4f) < '\0') {
            FUN_10018127c(&local_370,plVar8[7],plVar8[8]);
          }
          else {
            lStack_368 = plVar8[8];
            local_370 = (void *)plVar8[7];
            local_360 = plVar8[9];
          }
          goto LAB_1001b02e8;
        }
        plVar7 = (long *)plVar8[1];
        plVar10 = plVar8;
        if ((long *)plVar8[1] == (long *)0x0) {
          do {
            plVar8 = (long *)plVar10[2];
            bVar2 = (long *)*plVar8 != plVar10;
            plVar10 = plVar8;
          } while (bVar2);
        }
        else {
          do {
            plVar8 = plVar7;
            plVar7 = (long *)*plVar8;
          } while ((long *)*plVar8 != (long *)0x0);
        }
      } while (plVar8 != (long *)0x101debbe8);
    }
  }
  local_360 = CONCAT17(9,(undefined7)local_360);
  lStack_368 = CONCAT62(lStack_368._2_6_,0x76);
  local_370 = (void *)s_push3_dev_10183861b._0_8_;
LAB_1001b02e8:
  FUN_1001b0bb8(auStack_288,auStack_358,&local_370);
  FUN_1001ce978(local_3b0);
  local_3d0 = 0;
  local_3b8 = '\0';
  FUN_10028643c(local_3f0);
  thunk_FUN_1002cb2e8(param_1 + 1,auStack_288,local_3b0,&local_3d0,local_3f0);
  if ((local_3d8 == '\x01') && (local_3d9 < '\0')) {
    operator_delete(local_3f0[0]);
  }
  if ((local_3b8 == '\x01') && (local_3b9 < '\0')) {
    operator_delete((void *)CONCAT71(uStack_3cf,local_3d0));
  }
  if ((local_398 == '\x01') && (local_399 < '\0')) {
    operator_delete(local_3b0[0]);
  }
  FUN_10034e100(auStack_288);
  if (local_360 < 0) {
    operator_delete(local_370);
  }
  if ((local_378 == '\x01') && ((char)local_379 < '\0')) {
    operator_delete(local_390);
  }
  FUN_10034e100(auStack_358);
  thunk_FUN_1002c7818(param_1 + 0x29,*param_1,param_1 + 1,1);
  param_1[0x3b] = 0;
  param_1[0x38] = 0;
  param_1[0x37] = 0;
  param_1[0x3a] = 0;
  param_1[0x39] = 0;
  iVar4 = FUN_1001ce990();
  if ((iVar4 != 0) && (uVar6 = FUN_1001ce998(), (uVar6 & 1) == 0)) {
    thunk_FUN_10034d8ac(auStack_4c8,param_2);
    FUN_1001ce984(&local_500);
    if (local_4e8 == '\x01') {
      if (((DAT_101debbc0 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_101debbc0), iVar4 != 0))
      {
        FUN_1001bd948(local_c8,"11(.*)-beta","push3-12-public-beta");
        FUN_1001b17ac(local_98,"11(.*)-release","push3-12-release");
        FUN_1001b18f4(&DAT_101debbf8,local_c8,2,local_520);
        FUN_1001b11b0(local_98);
        FUN_1001b11b0(local_c8);
        ___cxa_atexit(FUN_1001b1208,&DAT_101debbf8,0x100000000);
        ___cxa_guard_release(&DAT_101debbc0);
      }
      if (DAT_101debbf8 != (long *)0x101debc00) {
        plVar8 = DAT_101debbf8;
        do {
          FUN_1001b5868(local_c8,plVar8 + 4,0);
          uVar6 = uStack_4f8;
          pppppuVar1 = (undefined8 *****)local_500;
          if (-1 < (char)local_4e9) {
            uVar6 = (ulong)local_4e9;
            pppppuVar1 = &local_500;
          }
          iVar4 = FUN_1001b1ed8(pppppuVar1,(long)pppppuVar1 + uVar6,local_c8,0);
          if (local_98[0] != (long *)0x0) {
            LOAcquire();
            lVar3 = local_98[0][1];
            local_98[0][1] = lVar3 + -1;
            LORelease();
            if (lVar3 == 0) {
              (**(code **)(*local_98[0] + 0x10))(local_98[0]);
              std::__shared_weak_count::__release_weak();
            }
          }
          std::locale::~locale(local_c8);
          if (iVar4 != 0) {
            if (*(char *)((long)plVar8 + 0x4f) < '\0') {
              FUN_10018127c(&local_4e0,plVar8[7],plVar8[8]);
            }
            else {
              lStack_4d8 = plVar8[8];
              local_4e0 = (void *)plVar8[7];
              local_4d0 = plVar8[9];
            }
            goto LAB_1001b051c;
          }
          plVar7 = (long *)plVar8[1];
          plVar10 = plVar8;
          if ((long *)plVar8[1] == (long *)0x0) {
            do {
              plVar8 = (long *)plVar10[2];
              bVar2 = (long *)*plVar8 != plVar10;
              plVar10 = plVar8;
            } while (bVar2);
          }
          else {
            do {
              plVar8 = plVar7;
              plVar7 = (long *)*plVar8;
            } while ((long *)*plVar8 != (long *)0x0);
          }
        } while (plVar8 != (long *)0x101debc00);
      }
    }
    local_4d0 = CONCAT17(0x14,(undefined7)local_4d0);
    lStack_4d8._0_1_ = s_push3_12_public_beta_101838655[8];
    lStack_4d8._1_1_ = s_push3_12_public_beta_101838655[9];
    lStack_4d8._2_1_ = s_push3_12_public_beta_101838655[10];
    lStack_4d8._3_1_ = s_push3_12_public_beta_101838655[0xb];
    lStack_4d8._4_1_ = s_push3_12_public_beta_101838655[0xc];
    lStack_4d8._5_1_ = s_push3_12_public_beta_101838655[0xd];
    lStack_4d8._6_1_ = s_push3_12_public_beta_101838655[0xe];
    lStack_4d8._7_1_ = s_push3_12_public_beta_101838655[0xf];
    local_4e0 = (void *)s_push3_12_public_beta_101838655._0_8_;
    local_4d0 = CONCAT35(local_4d0._5_3_,0x61746562);
LAB_1001b051c:
    FUN_1001b0bb8(auStack_1b8,auStack_4c8,&local_4e0);
    FUN_1001ce978(local_c8);
    FUN_10028643c(local_520);
    FUN_1001b0ce0(&local_3f8,auStack_1b8,local_c8,PTR_nullopt_101b95c20,local_520);
    plVar8 = local_3f8;
    local_3f8 = (long *)0x0;
    plVar7 = (long *)param_1[0x3a];
    param_1[0x3a] = plVar8;
    if (plVar7 != (long *)0x0) {
      (**(code **)(*plVar7 + 8))();
      plVar8 = local_3f8;
      local_3f8 = (long *)0x0;
      if (plVar8 != (long *)0x0) {
        (**(code **)(*plVar8 + 8))();
      }
    }
    if ((local_508 == '\x01') && (local_509 < '\0')) {
      operator_delete(local_520[0]);
    }
    FUN_10034e100(auStack_1b8);
    if (local_4d0 < 0) {
      operator_delete(local_4e0);
    }
    if ((local_4e8 == '\x01') && ((char)local_4e9 < '\0')) {
      operator_delete(local_500);
    }
    FUN_10034e100(auStack_4c8);
    uVar9 = *param_1;
    uVar11 = param_1[0x3a];
    plVar8 = operator_new(0x70);
    thunk_FUN_1002c7818(plVar8,uVar9,uVar11,1);
    plVar7 = (long *)param_1[0x3b];
    param_1[0x3b] = plVar8;
    if (plVar7 != (long *)0x0) {
      (**(code **)(*plVar7 + 8))();
      plVar8 = (long *)param_1[0x3b];
    }
    (**(code **)(*plVar8 + 0x28))(plVar8);
  }
  if (*(long *)PTR____stack_chk_guard_101b8c408 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return param_1;
}

