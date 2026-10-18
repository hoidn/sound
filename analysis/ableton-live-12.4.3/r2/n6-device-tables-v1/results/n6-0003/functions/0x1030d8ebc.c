
/* WARNING: Removing unreachable block (ram,0x0001030d9384) */
/* WARNING: Removing unreachable block (ram,0x0001030d93a4) */

void FUN_1030d8ebc(long param_1,long param_2)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_58;
  double dStack_50;
  undefined1 local_48;
  long local_40;
  int local_38;
  char local_34;
  
  puVar1 = *(undefined8 **)(param_2 + 8);
  if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
    *puVar1 = *(undefined8 *)(param_1 + 0x60);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d906c;
LAB_1030d8f24:
    puVar1 = (undefined8 *)FUN_1030ed054(param_2,param_1 + 0x70);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d90ac;
LAB_1030d8f40:
    puVar1 = (undefined8 *)FUN_1030ed054(param_2,param_1 + 0x88);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d90ec;
LAB_1030d8f5c:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xa0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d912c;
LAB_1030d8f78:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xd0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d916c;
LAB_1030d8f94:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0xe8);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d91ac;
LAB_1030d8fb0:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x100);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d91ec;
LAB_1030d8fcc:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x118);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d922c;
LAB_1030d8fe8:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x130);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d926c;
LAB_1030d9004:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x148);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d92ac;
LAB_1030d9020:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x160);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d92ec;
LAB_1030d903c:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x178);
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed1cc(param_2,param_1 + 0x58);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d8f24;
LAB_1030d906c:
    *puVar1 = *(undefined8 *)(param_1 + 0x78);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d8f40;
LAB_1030d90ac:
    *puVar1 = *(undefined8 *)(param_1 + 0x90);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d8f5c;
LAB_1030d90ec:
    *puVar1 = *(undefined8 *)(param_1 + 0xa8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d8f78;
LAB_1030d912c:
    *puVar1 = *(undefined8 *)(param_1 + 0xd8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d8f94;
LAB_1030d916c:
    *puVar1 = *(undefined8 *)(param_1 + 0xf0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d8fb0;
LAB_1030d91ac:
    *puVar1 = *(undefined8 *)(param_1 + 0x108);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d8fcc;
LAB_1030d91ec:
    *puVar1 = *(undefined8 *)(param_1 + 0x120);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d8fe8;
LAB_1030d922c:
    *puVar1 = *(undefined8 *)(param_1 + 0x138);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d9004;
LAB_1030d926c:
    *puVar1 = *(undefined8 *)(param_1 + 0x150);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d9020;
LAB_1030d92ac:
    *puVar1 = *(undefined8 *)(param_1 + 0x168);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d903c;
LAB_1030d92ec:
    *puVar1 = *(undefined8 *)(param_1 + 0x180);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
  }
  *(undefined8 **)(param_2 + 8) = puVar1;
  local_58 = DAT_1055d1ec0;
  local_68 = *(undefined8 *)(param_1 + 0x198);
  uStack_60 = 0;
  dStack_50 = (double)NEON_fmov(0xbf800000,4);
  dStack_50 = -dStack_50;
  local_48 = 0;
  local_40 = 0;
  local_38 = 0;
  local_34 = '\0';
  if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[1] = 0;
    *puVar1 = local_68;
    puVar1[3] = dStack_50;
    puVar1[2] = local_58;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    local_34 = '\0';
    local_38 = 0;
    local_40 = 0;
    local_48 = 0;
    uStack_60 = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030ed7f0(param_2,&local_68);
  }
  *(undefined8 **)(param_2 + 8) = puVar1;
  if ((local_40 != 0) && (local_34 == '\x01')) {
    FUN_101a24778(local_40,(long)local_38 << 2);
    puVar1 = *(undefined8 **)(param_2 + 8);
  }
  if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
    *puVar1 = *(undefined8 *)(param_1 + 0x1b0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9684;
LAB_1030d944c:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x1c0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d96c4;
LAB_1030d9468:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x1d8);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9704;
LAB_1030d9484:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x1f0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9744;
LAB_1030d94a0:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x208);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9784;
LAB_1030d94bc:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x220);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d97c4;
LAB_1030d94d8:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x2c8);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9804;
LAB_1030d94f4:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x238);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9844;
LAB_1030d9510:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x250);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9884;
LAB_1030d952c:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x268);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d98c4;
LAB_1030d9548:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x280);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9904;
LAB_1030d9564:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x298);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9944;
LAB_1030d9580:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x2b0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9984;
LAB_1030d959c:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x2e0);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d99c4;
LAB_1030d95b8:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x2f8);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9a04;
LAB_1030d95d4:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x310);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9a44;
LAB_1030d95f0:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x328);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9a84;
LAB_1030d960c:
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x340);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9ac4;
  }
  else {
    puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x1a8);
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d944c;
LAB_1030d9684:
    *puVar1 = *(undefined8 *)(param_1 + 0x1c8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d9468;
LAB_1030d96c4:
    *puVar1 = *(undefined8 *)(param_1 + 0x1e0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d9484;
LAB_1030d9704:
    *puVar1 = *(undefined8 *)(param_1 + 0x1f8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d94a0;
LAB_1030d9744:
    *puVar1 = *(undefined8 *)(param_1 + 0x210);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d94bc;
LAB_1030d9784:
    *puVar1 = *(undefined8 *)(param_1 + 0x228);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d94d8;
LAB_1030d97c4:
    *puVar1 = *(undefined8 *)(param_1 + 0x2d0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d94f4;
LAB_1030d9804:
    *puVar1 = *(undefined8 *)(param_1 + 0x240);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d9510;
LAB_1030d9844:
    *puVar1 = *(undefined8 *)(param_1 + 600);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d952c;
LAB_1030d9884:
    *puVar1 = *(undefined8 *)(param_1 + 0x270);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d9548;
LAB_1030d98c4:
    *puVar1 = *(undefined8 *)(param_1 + 0x288);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d9564;
LAB_1030d9904:
    *puVar1 = *(undefined8 *)(param_1 + 0x2a0);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d9580;
LAB_1030d9944:
    *puVar1 = *(undefined8 *)(param_1 + 0x2b8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d959c;
LAB_1030d9984:
    *puVar1 = *(undefined8 *)(param_1 + 0x2e8);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d95b8;
LAB_1030d99c4:
    *puVar1 = *(undefined8 *)(param_1 + 0x300);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d95d4;
LAB_1030d9a04:
    *puVar1 = *(undefined8 *)(param_1 + 0x318);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d95f0;
LAB_1030d9a44:
    *puVar1 = *(undefined8 *)(param_1 + 0x330);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (*(undefined8 **)(param_2 + 0x10) <= puVar1) goto LAB_1030d960c;
LAB_1030d9a84:
    *puVar1 = *(undefined8 *)(param_1 + 0x348);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    puVar1 = puVar1 + 7;
    *(undefined8 **)(param_2 + 8) = puVar1;
    if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
LAB_1030d9ac4:
      *puVar1 = *(undefined8 *)(param_1 + 0x360);
      puVar1[1] = 0;
      puVar1[2] = 0x8000000000000000;
      puVar1[3] = 0x7f7fffff7f7fffff;
      *(undefined1 *)(puVar1 + 4) = 0;
      puVar1[5] = 0;
      *(undefined4 *)(puVar1 + 6) = 0;
      *(undefined1 *)((long)puVar1 + 0x34) = 0;
      puVar1 = puVar1 + 7;
      *(undefined8 **)(param_2 + 8) = puVar1;
      if (puVar1 < *(undefined8 **)(param_2 + 0x10)) goto LAB_1030d9b04;
      goto LAB_1030d9644;
    }
  }
  puVar1 = (undefined8 *)FUN_1030c50c0(param_2,param_1 + 0x358);
  *(undefined8 **)(param_2 + 8) = puVar1;
  if (puVar1 < *(undefined8 **)(param_2 + 0x10)) {
LAB_1030d9b04:
    *puVar1 = *(undefined8 *)(param_1 + 0x378);
    puVar1[1] = 0;
    puVar1[2] = 0x8000000000000000;
    puVar1[3] = 0x7f7fffff7f7fffff;
    *(undefined1 *)(puVar1 + 4) = 0;
    puVar1[5] = 0;
    *(undefined4 *)(puVar1 + 6) = 0;
    *(undefined1 *)((long)puVar1 + 0x34) = 0;
    *(undefined8 **)(param_2 + 8) = puVar1 + 7;
    return;
  }
LAB_1030d9644:
  uVar2 = FUN_1030c50c0(param_2,param_1 + 0x370);
  *(undefined8 *)(param_2 + 8) = uVar2;
  return;
}

