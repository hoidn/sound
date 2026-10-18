
/* WARNING: Removing unreachable block (ram,0x000100005428) */
/* WARNING: Type propagation algorithm not settling */

void FUN_100005058(long *param_1,char param_2,undefined4 param_3,undefined8 param_4)

{
  char cVar1;
  undefined8 *****pppppuVar2;
  long *plVar3;
  undefined8 ******ppppppuVar4;
  undefined8 ****ppppuVar5;
  int iVar6;
  long lVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  undefined4 local_118;
  undefined4 uStack_114;
  void *local_110;
  long lStack_108;
  long local_100;
  undefined8 ******local_f8;
  long *local_f0;
  undefined8 ****local_e8;
  undefined8 uStack_e0;
  undefined7 local_d8;
  char cStack_d1;
  undefined4 local_d0;
  char local_c9;
  undefined8 ******local_c8;
  undefined8 *****local_c0;
  undefined8 *****local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 *******local_a0;
  long *plStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  long local_80;
  int local_70;
  undefined4 uStack_6c;
  undefined8 local_68;
  undefined8 *******local_60;
  int *piStack_58;
  long local_50;
  
  local_d0 = param_3;
  local_c9 = param_2;
  lVar7 = FUN_100101084();
  if (lVar7 != 0) {
    FUN_10000576c(&local_a0,param_1);
    FUN_100026a54(&local_a0);
    if ((long)local_90 < 0) {
      operator_delete(local_a0);
      cVar1 = *(char *)((long)param_1 + 0x17);
      goto joined_r0x0001000050a8;
    }
  }
  cVar1 = *(char *)((long)param_1 + 0x17);
joined_r0x0001000050a8:
  if (cVar1 < '\0') {
    FUN_100005a5c(&local_110,*param_1,param_1[1]);
  }
  else {
    lStack_108 = param_1[1];
    local_110 = (void *)*param_1;
    local_100 = param_1[2];
  }
  thunk_FUN_100019bd4(&local_f8,&local_110);
  plVar3 = local_f0;
  local_c8 = local_f8;
  local_c0 = (undefined8 *****)local_f0;
  if (local_f0 != (long *)0x0) {
    local_f0[1] = local_f0[1] + 1;
  }
  if (cStack_d1 < '\0') {
    FUN_100005a5c(&local_b8,local_e8,uStack_e0);
    pppppuVar2 = local_c0;
    ppppppuVar4 = local_c8;
    local_70 = 0;
    local_68 = std::system_category();
    local_a0 = (undefined8 *******)ppppppuVar4;
    plStack_98 = (long *)pppppuVar2;
  }
  else {
    uStack_b0 = uStack_e0;
    local_b8 = (undefined8 *****)local_e8;
    local_a8 = CONCAT17(cStack_d1,local_d8);
    local_70 = 0;
    local_68 = std::system_category();
    local_a0 = (undefined8 *******)local_f8;
    plStack_98 = plVar3;
  }
  if (plStack_98 != (long *)0x0) {
    plStack_98[1] = plStack_98[1] + 1;
  }
  ppppuVar5 = local_b8;
  uVar8 = uStack_b0;
  lVar7 = local_a8;
  if (local_a8 < 0) {
    FUN_100005a5c(&local_90,local_b8,uStack_b0);
    ppppuVar5 = local_90;
    uVar8 = uStack_88;
    lVar7 = local_80;
  }
  local_80 = lVar7;
  uStack_88 = uVar8;
  local_90 = ppppuVar5;
  local_60 = &local_a0;
  piStack_58 = &local_70;
  local_50 = CONCAT71(local_50._1_7_,1);
  lVar7 = FUN_100019fac(&local_a0,0x34,&local_70);
  if (local_70 == 0) {
    FUN_100004d44(lVar7 + 0x10,param_4);
  }
  iVar6 = FUN_10001a0b4(&local_a0);
  if (iVar6 != 0) {
    FUN_10001a0dc(&local_a0,&local_70);
  }
  if (local_80 < 0) {
    operator_delete(local_90);
  }
  if (plStack_98 != (long *)0x0) {
    LOAcquire();
    lVar7 = plStack_98[1];
    plStack_98[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*plStack_98 + 0x10))(plStack_98);
      std::__shared_weak_count::__release_weak();
    }
  }
  if (local_70 != 0) {
    uVar8 = ___cxa_allocate_exception(0x50);
    FUN_100004fb0(&local_60,"Failed opening/closing file");
    uVar9 = FUN_100019f94(&local_c8);
    FUN_100005b94(uVar8,&local_60,uVar9,CONCAT44(uStack_6c,local_70),local_68);
                    /* WARNING: Subroutine does not return */
    ___cxa_throw(uVar8,&PTR_vtable_10029db70,FUN_100005ae8);
  }
  if (local_a8._7_1_ < '\0') {
    operator_delete(local_b8);
  }
  if (local_c0 != (undefined8 *****)0x0) {
    LOAcquire();
    lVar7 = (long)local_c0[1];
    local_c0[1] = (undefined8 ****)(lVar7 + -1);
    LORelease();
    if (lVar7 == 0) {
      (**(code **)((long)*local_c0 + 0x10))(local_c0);
      std::__shared_weak_count::__release_weak();
    }
  }
  if (cStack_d1 < '\0') {
    operator_delete(local_e8);
  }
  if (local_f0 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_f0[1];
    local_f0[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_f0 + 0x10))(local_f0);
      std::__shared_weak_count::__release_weak();
    }
  }
  if (local_100 < 0) {
    operator_delete(local_110);
  }
  if (local_c9 == '\x01') {
    FUN_100004d44(PTR_clog_10029c1e8,param_4);
  }
  if (*(char *)((long)param_1 + 0x17) < '\0') {
    FUN_100005a5c(&local_60,*param_1,param_1[1]);
  }
  else {
    piStack_58 = (int *)param_1[1];
    local_60 = (undefined8 *******)*param_1;
    local_50 = param_1[2];
  }
  local_70 = 1;
  local_118 = 7;
  uStack_114 = 4;
  local_c0 = (undefined8 *****)0x0;
  local_b8 = (undefined8 *****)0x0;
  local_c8 = (undefined8 ******)0x0;
  local_c8 = operator_new(0xa0);
  local_b8 = local_c8 + 0x14;
  plStack_98 = (long *)piStack_58;
  local_a0 = local_60;
  local_90 = (undefined8 ****)local_50;
  local_60 = (undefined8 *******)0x0;
  piStack_58 = (int *)0x0;
  local_50 = 0;
  local_c0 = local_c8;
  FUN_1000062b0(&local_c8,0,&local_a0,&local_70,&local_c9,&uStack_114,&local_d0,&local_118,
                &DAT_1002ccaa0);
  if ((long)local_90 < 0) {
    operator_delete(local_a0);
  }
  FUN_100044298(&local_c8);
  ppppppuVar4 = local_c8;
  pppppuVar2 = local_c0;
  if (local_c8 != (undefined8 ******)0x0) {
    for (; (undefined8 ******)pppppuVar2 != ppppppuVar4; pppppuVar2 = pppppuVar2 + -5) {
      if (*(uint *)(pppppuVar2 + -1) != 0xffffffff) {
        (*(code *)(&PTR_FUN_10029dbb0)[*(uint *)(pppppuVar2 + -1)])(&local_a0,pppppuVar2 + -4);
      }
      *(undefined4 *)(pppppuVar2 + -1) = 0xffffffff;
    }
    local_c0 = ppppppuVar4;
    operator_delete(local_c8);
  }
  local_90 = (undefined8 ****)CONCAT17(2,(undefined7)local_90);
  local_a0 = (undefined8 *******)CONCAT53(local_a0._3_5_,0x7471);
  local_60 = (undefined8 *******)CONCAT44(local_60._4_4_,7);
  local_c0 = (undefined8 *****)0x0;
  local_b8 = (undefined8 *****)0x0;
  local_c8 = (undefined8 ******)0x0;
  local_c8 = operator_new(0x78);
  local_b8 = local_c8 + 0xf;
  *(undefined4 *)local_c8 = 1;
  *(char *)(local_c8 + 1) = local_c9;
  *(undefined4 *)(local_c8 + 4) = 0;
  local_c0 = local_c8 + 5;
  FUN_100006694(&local_c8,4,local_d0,&local_60,&DAT_1002ccaa0);
  FUN_100044afc(&local_a0,&local_c8);
  ppppppuVar4 = local_c8;
  pppppuVar2 = local_c0;
  if (local_c8 != (undefined8 ******)0x0) {
    for (; (undefined8 ******)pppppuVar2 != ppppppuVar4; pppppuVar2 = pppppuVar2 + -5) {
      if (*(uint *)(pppppuVar2 + -1) != 0xffffffff) {
        (*(code *)(&PTR_FUN_10029dbb0)[*(uint *)(pppppuVar2 + -1)])(&local_70,pppppuVar2 + -4);
      }
      *(undefined4 *)(pppppuVar2 + -1) = 0xffffffff;
    }
    local_c0 = ppppppuVar4;
    operator_delete(local_c8);
  }
  if ((long)local_90 < 0) {
    operator_delete(local_a0);
  }
  FUN_100014160();
  return;
}

