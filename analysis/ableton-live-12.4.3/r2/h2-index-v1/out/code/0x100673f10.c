// 0x100673f10 FUN_100673f10 state=exported-with-warnings body_bytes=792 warnings=1 chunk=chunk-00268.jsonl

uint FUN_100673f10(long *param_1,undefined8 param_2)

{
  int iVar1;
  uint uVar2;
  undefined8 *puVar3;
  void *pvVar4;
  undefined8 *puVar5;
  undefined8 uVar6;
  uint uVar7;
  long *local_d8;
  long lStack_d0;
  long local_c8;
  int *piStack_c0;
  int *local_b8;
  int *local_b0;
  int *local_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 *puStack_88;
  undefined8 *puStack_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 local_50;
  undefined4 local_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_100d60390;
  FUN_100295758(&local_a8,param_2);
  uStack_68 = 0;
  local_70 = 0;
  uStack_58 = 0;
  uStack_60 = 0;
  puStack_88 = (undefined8 *)0x0;
  local_90 = 0;
  uStack_78 = 0;
  puStack_80 = (undefined8 *)0x0;
  uStack_98 = 0;
  local_a0 = 0;
  local_50 = 0x400;
  local_48 = 0;
  local_40 = 0;
  puVar3 = operator_new(0x18);
  *puVar3 = 0x10000;
  pvVar4 = operator_new(1);
  puVar5 = _malloc(0x38);
  puVar3[1] = pvVar4;
  puVar3[2] = puVar5;
  puVar5[4] = 0;
  *puVar5 = puVar5 + 4;
  puVar5[1] = pvVar4;
  puVar5[5] = 0;
  puVar5[6] = 0;
  *(undefined1 *)(puVar5 + 3) = 1;
  puVar5[2] = 1;
  puStack_88 = puVar3;
  puStack_80 = puVar3;
  uVar2 = FUN_1002b143c(&local_a8,&local_a0);
  if (uVar2 != 0) {
    FUN_1001d4d4c(&local_b0);
    FUN_1001d4d4c(&local_b8);
    FUN_1001d4d4c(&piStack_c0);
    lStack_d0 = 0;
    local_c8 = 0;
    local_d8 = &lStack_d0;
    uVar6 = FUN_1001f60e0(&local_d8,"db-path",&local_b0);
    uVar6 = FUN_1001f60e0(uVar6,"ipc-channel",param_1 + 6);
    uVar6 = FUN_1001f60e0(uVar6,"usage-data_file",&local_b8);
    uVar6 = FUN_1001f60e0(uVar6,"fileref-map-path",&piStack_c0);
    uVar6 = FUN_1001f60e0(uVar6,"parent-pid",param_1 + 10);
    uVar6 = FUN_1001f60e0(uVar6,"log-traces",param_1 + 0xb);
    uVar6 = FUN_10024f3b4(uVar6,"profile-log",param_1 + 0xc);
    uVar6 = FUN_1001f60e0(uVar6,"os-events-flags",param_1 + 0xd);
    uVar6 = FUN_1001f5f9c(uVar6,"db-stats-trigger",param_1 + 0xe);
    uVar6 = FUN_1001f5f9c(uVar6,"db-stale-factor",(long)param_1 + 0x74);
    uVar6 = FUN_10024f3b4(uVar6,"sound-analyzer",param_1 + 0xf);
    uVar6 = FUN_10024f3b4(uVar6,"auto-keywords",(long)param_1 + 0x79);
    uVar6 = FUN_1002500b0(uVar6,"features",param_1 + 0x10);
    puVar3 = (undefined8 *)FUN_1002b1668(&local_a0,uVar6);
    FUN_100154078(&local_d8,lStack_d0);
    FUN_10049ebcc(&local_d8,&local_b0);
    if (*(char *)((long)param_1 + 0x17) < '\0') {
      operator_delete((void *)*param_1);
    }
    param_1[1] = lStack_d0;
    *param_1 = (long)local_d8;
    param_1[2] = local_c8;
    FUN_10049ebcc(&local_d8,&local_b8);
    if (*(char *)((long)param_1 + 0x4f) < '\0') {
      operator_delete((void *)param_1[7]);
    }
    param_1[8] = lStack_d0;
    param_1[7] = (long)local_d8;
    param_1[9] = local_c8;
    FUN_10049ebcc(&local_d8,&piStack_c0);
    if (*(char *)((long)param_1 + 0x2f) < '\0') {
      operator_delete((void *)param_1[3]);
      param_1[4] = lStack_d0;
      param_1[3] = (long)local_d8;
      param_1[5] = local_c8;
    }
    else {
      param_1[4] = lStack_d0;
      param_1[3] = (long)local_d8;
      param_1[5] = local_c8;
    }
    if ((piStack_c0 != (int *)0x0) &&
       (iVar1 = *piStack_c0, *piStack_c0 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_100469e84();
    }
    if ((local_b8 != (int *)0x0) && (iVar1 = *local_b8, *local_b8 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_100469e84();
    }
    if ((local_b0 != (int *)0x0) && (iVar1 = *local_b0, *local_b0 = iVar1 + -1, iVar1 + -1 == 0)) {
      FUN_100469e84();
    }
  }
  uVar7 = (uint)puVar3;
  FUN_10014d918(&local_a0);
  if ((local_a8 != (int *)0x0) && (iVar1 = *local_a8, *local_a8 = iVar1 + -1, iVar1 + -1 == 0)) {
    FUN_100469e84();
  }
  if ((uVar2 & 1) == 0) {
    uVar7 = 0;
  }
  if (*(long *)PTR____stack_chk_guard_100d60390 == local_38) {
    return uVar7 & 1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}

